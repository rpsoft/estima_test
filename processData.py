# %%
import os
import pdfplumber

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.vectorstores import Chroma

# Import our configuration and embeddings factory
from config import config
from embeddings_factory import create_embeddings, get_embeddings_info

# Initialize embeddings model based on configuration
embeddings = create_embeddings()

# Print embeddings configuration
embeddings_info = get_embeddings_info()
print(f"Using embeddings: {embeddings_info['provider']} - {embeddings_info['model']}")

# Read pdf files in the docs folder
docs_folder = "aws_raw"
document_files = [f for f in os.listdir(docs_folder) if f.endswith('.txt')]
print(f"Found {len(document_files)} PDF files in {docs_folder} folder")

if os.path.exists(config.persist_dir):
	# Reload existing Chroma DB
	vectorstore = Chroma(
		persist_directory=config.persist_dir,
		embedding_function=embeddings
	)

	print("Loaded existing Chroma DB from", config.persist_dir)
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
		persist_directory=config.persist_dir
	)
