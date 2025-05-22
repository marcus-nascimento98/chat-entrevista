from django.core.management.base import BaseCommand
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'file_name',
            type=str,
            help='Nome do arquivo para o rag'
        )

    def handle(self, *args, **options):
        file_name = options['file_name']
        pdf_path = f'ai/rag/docs_rag/{file_name}'
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap=200,
        )
        chunks = text_splitter.split_documents(
            documents=docs
        )

        persist_directory = 'ai/rag/rag_db'

        embedding = HuggingFaceEmbeddings()

        Chroma.from_documents(
            documents=chunks,
            embedding = embedding,
            persist_directory=persist_directory,
            collection_name='curriculo_marcus',
        )
