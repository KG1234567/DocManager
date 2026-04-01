# upload document
# --> uploaded_file, tags, document, date
# --> Process uploaded_file --> test.pdf (again)
# --> uploaded_file --> test.pdf --> thumbnail
# --> uploaded_file --> folder with the same name as pdf file --> test --> extract all images --> 0.jpeg, 1.jpeg etc
# --> uploaded_file --> total pages
# upload_date --> time, datetime

from datetime import datetime

from db.repository import DocumentRepository
from core.file_manager import FileManager
from core.thumbnail import ThumbnailGenerator
from core.reader import PDFReader
from core.models import Document

class DocumentService:
    def __init__(self):
        self.repo = DocumentRepository()
        self.file_manager = FileManager()
        self.thumbnail_generator = ThumbnailGenerator()
        self.reader = PDFReader()

    def upload_document(self, uploaded_file, tags, description, lecture_date=None):

        # Save file
        file_path = self.file_manager.save_file(uploaded_file)

        # Generate thumbnail
        thumbnail_path = self.thumbnail_generator.generate_thumbnail(file_path)

        # Get total pages
        total_pages = self.thumbnail_generator.get_total_pages(file_path)

        # Convert to images
        self.reader.convert_pdf_to_images(file_path)
        
        # Create required variables : upload date
        upload_date = datetime.now().strftime("%Y-%m-%d")
        doc = Document(
            id=None,
            name=uploaded_file.name,
            path=file_path,
            thumbnail_path=thumbnail_path,
            tags=tags,
            description=description,
            upload_date=datetime.now().strftime("%Y-%m-%d"),
            lecture_date=lecture_date,
            total_pages=total_pages
        )

        # Save to database
        self.repo.add_document(doc)

    def search_document(self, tag=None, date=None):
        return self.repo.search_documents(tag, date)

    def get_all_documents(self):
        return self.repo.get_all_documents()

    
