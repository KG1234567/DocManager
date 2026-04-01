import streamlit as st
import os
import sys
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

sys.path.append(BASE_DIR)

load_dotenv (os.path.join(BASE_DIR, ".env"))
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

from db.database import init_db
from core.services import DocumentService
from core.analytics import AnalyticsService

if "selected_doc" not in st.session_state:
    st.session_state.selected_doc = None

if "current_page" not in st.session_state:
    st.session_state.current_page = 0

if "search_results" not in st.session_state:
    st.session_state.search_results = []

if "reader_mode" not in st.session_state:
    st.session_state.reader_mode = False

if "show_reset" not in st.session_state:
    st.session_state.show_reset = False

init_db()
service = DocumentService()
analytics = AnalyticsService()

st.set_page_config(page_title="PDF_Manager", layout="wide")

st.title("Smart PDF Document Manager")

st.divider()

st.subheader("Admin Controls")
if st.button("Clean Database"):
    st.session_state.show_reset = True
    

if st.session_state.show_reset:
    # mask password text input
    password_input = st.text_input("Enter Admin Password", type="password")
    if st.button("Confirm Reset"):
        if password_input == ADMIN_PASSWORD:
            import shutil
            # delete db
            if os.path.exists("data/documents.db"):
                os.remove("data/documents.db")

            # delete storage
            pdf_dir = os.path.join("storage", "pdfs")
            thumbnail_dir = os.path.join("storage", "thumbnails")
            shutil.rmtree(pdf_dir, ignore_errors=True)
            shutil.rmtree(thumbnail_dir, ignore_errors=True)

            os.makedirs(pdf_dir, exist_ok=True)
            os.makedirs(thumbnail_dir, exist_ok=True)

            st.success("System Reset Successfully. Restart App.")
        
        else:
            st.error("Incorrect Password.")

tabs = st.tabs(["Upload", "Search & View", "Analytics"])

with tabs[0]:
    st.header("Upload PDF")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])       # object of streamlit
    tags = st.text_input("Tags (comma separated)")
    description = st.text_area("Description")
    lecture_date = st.date_input("Lecture Date (optional)", value=None)          # optional

    if st.button("Upload"):
        analytics.record_app_visits("upload_click")
        if uploaded_file and tags and description:
            service.upload_document(uploaded_file, tags, description, lecture_date)
            st.write("File Uploaded Successfully")
        else:
            st.error("Please upload a file")

with tabs[1]:
    # logic for Search & View
    st.header("Search & View")
    col1, col2 = st.columns(2)
    with col1:
        search_tag = st.text_input("Search by Tag")

    with col2:
        search_date = st.date_input("Search by Date", value=None)
    
    if st.button("Search"):
        analytics.record_app_visits("search_click")
        st.session_state.search_results = service.search_document(tag=search_tag if search_tag else None,
                                date=str(search_date) if search_date else None
        )

    results = st.session_state.search_results

    if results and not st.session_state.reader_mode:
        st.subheader(f"Results: {len(results)} documents")
        container = st.container(height=500)
        with container:
            for doc in results:
                col1, col2 = st.columns([1,3])
                with col1:
                    if doc.thumbnail_path:
                        st.image(doc.thumbnail_path, width=120)
                        
                with col2:
                    st.write(f"**{doc.name}**")
                    st.write(f"Tags: {doc.tags}")
                    st.write(f"Description: {doc.description}")
                    st.write(f"Lecture Date: {doc.lecture_date}")

                    if st.button("Open", key=f"open_{doc.id}"):
                        analytics.record_app_visits("open_document")
                        st.session_state.selected_doc = doc
                        st.session_state.current_page = 0
                        st.session_state.reader_mode = True
                        st.rerun()

    if st.session_state.reader_mode and st.session_state.selected_doc:
        st.write("Reader Mode Active")

        doc = st.session_state.selected_doc

        st.subheader(f" Reading: {doc.name}")

        folder_name = os.path.basename(doc.path).replace(".pdf", "")
        image_dir = f"storage/pdfs/{folder_name}"

        st.write("image dir:", image_dir)
        st.write("Files:",os.listdir(image_dir) if os.path.exists(image_dir) else "NOT FOUND")

        if not os.path.exists(image_dir):
            st.error("Image not found. PDF conversion failed.")
        else:
            images = sorted(os.listdir(image_dir))
            total_pages = doc.total_pages
            current_page = st.session_state.current_page

            col1, col2, col3 = st.columns([1,2,1])

            with col1:
                if st.button("Previous") and current_page > 0:
                    analytics.record_app_visits("prev_page")
                    st.session_state.current_page -= 1
                    st.rerun()

            with col3:
                if st.button("Next") and current_page < total_pages - 1:
                    analytics.record_app_visits("next_page")
                    st.session_state.current_page += 1
                    st.rerun()

            img_path = os.path.join(image_dir, images[st.session_state.current_page])
            st.image(img_path, width="stretch")


            analytics.record_page_visits(doc.id, st.session_state.current_page)
            unique_pages = analytics.get_unique_pages_viewed(doc.id)
            progress = (unique_pages/doc.total_pages)*100 if doc.total_pages else 0

            st.progress(progress / 100)

            st.write(f"Progress: {progress: .2f}% ({unique_pages}/{doc.total_pages})")
        
        if st.button("Close Reader"):
            analytics.record_app_visits("close_document")
            st.session_state.reader_mode = False
            st.rerun()
            

with tabs[2]:
    # logic for Analytics
    st.header("Analytics")

    # app_vists, page_visits

    if st.button("Reset Analytics"):
        analytics.reset_analytics()
        st.success("analytics reset successfully.")

    st.subheader("App Usage")
    app_data = analytics.get_app_visits()

    import pandas as pd

    df = pd.DataFrame(app_data, columns=["Event", "Count"])

    if df.empty:
        st.info("No analytics data yet. Perform some actions to see insights.")
    else:
        st.bar_chart(df.set_index("Event"))

    st.subheader("Document Progress")

    docs = service.get_all_documents()

    data = []
    for doc in docs:
        unique_pages = analytics.get_unique_pages_viewed(doc.id)
        progress = (unique_pages /  doc.total_pages)*100 if doc.total_pages else 0

        data.append({
            "Document": doc.name,
            "Pages Read": unique_pages,
            "Total Pages": doc.total_pages,
            "Progress (%)": round(progress, 2)
        })

    df_docs = pd.DataFrame(data)
    st.dataframe(df_docs)


