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
docs_folder = "docs"
pdf_files = [f for f in os.listdir(docs_folder) if f.endswith('.pdf')]
print(f"Found {len(pdf_files)} PDF files in {docs_folder} folder")

if os.path.exists(persist_dir):
	# Reload existing Chroma DB
	vectorstore = Chroma(
		persist_directory=persist_dir,
		embedding_function=embeddings
	)

	print("Loaded existing Chroma DB from", persist_dir)
else:

	pdf_dict = {}

	for pdf_file in pdf_files:
		with pdfplumber.open(docs_folder + "/" + pdf_file) as pdf:
			full_text = ""
			for page in pdf.pages:
				words = page.extract_words()
				line = ""
				last_top = None
				for word in words:
					# Start a new line if y-position changes significantly
					if last_top is not None and abs(word['top'] - last_top) > 3:
						full_text += line.strip() + "\n"
						line = ""
					line += word['text'] + " "
					last_top = word['top']
				full_text += line.strip() + "\n"  # flush last line of the page
			pdf_dict[pdf_file] = full_text


	# %%

	# Initialize the text splitter
	text_splitter = RecursiveCharacterTextSplitter(
		chunk_size=1000,
		chunk_overlap=200,
		# separators=["\n\n", "\n", " ", ""]
	)

	# Chunk the texts in pdf_dict
	documents = []
	for filename, text in pdf_dict.items():
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
