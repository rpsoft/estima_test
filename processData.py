# %%
import os
import pdfplumber

from dotenv import load_dotenv

# Load variables from .env into environment
load_dotenv()

persist_dir = os.getenv("PERSIST_DIR", "./chroma_db")

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings

# Initialize embeddings model
embeddings = OllamaEmbeddings(
	model= os.getenv("EMBEDDINGS_MODEL", "oscardp96/medcpt-article" ),
	base_url=os.getenv("OLLAMA_URL", "localhost:11434")
)

# Read pdf files in the docs folder
docs_folder = "aws_raw"
document_files = [f for f in os.listdir(docs_folder) if f.endswith('.txt')]
print(f"Found {len(document_files)} PDF files in {docs_folder} folder")

if os.path.exists(persist_dir):
	# Reload existing Chroma DB
	vectorstore = Chroma(
		persist_directory=persist_dir,
		embedding_function=embeddings
	)

	print("Loaded existing Chroma DB from", persist_dir)
else:
	print("Creating new Chroma DB")
	document_dict = {}

	for txt_file in document_files:
		with open(os.path.join(docs_folder, txt_file), "r", encoding="utf-8") as f:
			document_dict[txt_file] = f.read()



	# %%

	# Initialize the text splitter
	text_splitter = RecursiveCharacterTextSplitter(
		chunk_size=1000,
		chunk_overlap=200,
		separators=["\n\n", "\n", " ", ""]  # prefer splitting at paragraphs/sentences
	)

	# Chunk the texts in document_dict
	documents = []
	for filename, text in document_dict.items():
		chunks = text_splitter.split_text(text)

		for j, chunk in enumerate(chunks):
			documents.append(
				Document(
					page_content=chunk,
					metadata={"filename": filename, "chunk_id": j}
				)
			)

	# Prepare embeddings and ChromaDB
	vectorstore = Chroma.from_documents(
		documents,
		embedding=embeddings,
		persist_directory=persist_dir
	)
