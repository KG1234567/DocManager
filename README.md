<img width="1352" height="601" alt="pdf_m6" src="https://github.com/user-attachments/assets/4926e281-afdb-4b2f-847d-986500e7bd80" />
<img width="1355" height="630" alt="pdf_m5" src="https://github.com/user-attachments/assets/7ec78ffa-eb62-41c7-84e3-e1053160b112" />
<img width="1354" height="662" alt="pdf_m4" src="https://github.com/user-attachments/assets/2637a0da-7ce6-4881-b827-f3fa759eae4c" />
<img width="1356" height="672" alt="pdf_m3" src="https://github.com/user-attachments/assets/f65571af-2407-474e-a4b6-cd77f528b591" />
<img width="1344" height="683" alt="pdf_m2" src="https://github.com/user-attachments/assets/ea22d0b6-f9b0-4db0-8a3a-4f36c70b316c" />
<img width="1333" height="670" alt="pdf_m1" src="https://github.com/user-attachments/assets/67252dde-bc28-42b2-91fa-8fec6429473e" />

# DocManager - Document Intelligence Application

A Python-web based document management and analytics system that helps to organize scattered PDFs, enables fast search, and provides insights into user behavior through clickstream analytics.


## Problem Statement

Managing multiple PDFs (notes, books, documents) across a system becomes inefficient when: 

- Files are scattered in different folders
- Manual search takes significant time 
- No tracking of what content is actually used

This project solves that by creating a centralized seachable document system with built-in analytics.

## Solution

The Document Intelligence System allows users to:

- Upload & organize documents in one place.
- Add metadata (tags, description, date).
- Search documents instantly using filters.
- View PDFs with smooth navigation.
- Track user activity and analyze behavior.
- Admin control to clean up the storage (file, thumbnail, images).
## Features

1. Document Upload & Storage

- Upload PDF files via UI
- Store files locally
- Save metadata in database: \
         1. File name  \
         2. Tags  
         3. Description \
         4. Date (Optional)

2. Smart Search
- Search documents using: \
       1. Tags  \
       2. Date
- Eliminates manual file browsing

3. PDF Viewer
- Convert PDF -> Images using PyMuPDF
- Enables faster rendering in UI

4. Clickstream Analytics
- Tracks user actions like:  
      1. Upload   
      2. Search   
      3. Open Document  
      4. Previous    
      5. Next   
      6. Close

5. Clean storage using Admin Control

- To delete all thumbnails, pdf and images stored in the local storage to clean up the space.
## Tech Stack

**Frontend:** Streamlit

**Backend:** Python (OOP-based design)

**Database:** SQLite

**PDF Processing:** PyMuPDF



## Installation

1. Clone Repository

```bash
  git clone https://github.com/KG1234567/DocManager.git
  cd DocManager
```

2. Create Virtual Environment

```bash
  python -m venv venv
  source venv/bin/activate      
  # Windows: venv\Scripts\activate
```

3. Install Dependencies

```bash
  pip install -r requirements.txt
```

4. Run Application

```bash
  streamlit run app\main.py
```

 
   
## Key Learnings

- Designing end-to-end data flow (UI -> Backend -> DB -> Analytics).
- Applying Object-Oriented Programming in real projects.
- Implementing basic product analytics (clickstream).
- Thinking beyond features -> building system.
## Limitations

- High storage usage due to PDF -> image conversion.
- No compression/optimization implemented (by design scope).
## Future Improvements

- PDF compression & Optimization
- Cloud Storage integration
- Advanced search (full-text search)
- User authentication system
- Dashboard for analytics visualization.
