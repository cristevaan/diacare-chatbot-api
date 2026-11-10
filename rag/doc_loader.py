from langchain_community.document_loaders import PyPDFLoader, UnstructuredPDFLoader

def load_pdf_PyPDFLoader(file_path):
    loader = PyPDFLoader(file_path, mode="page")
    documents = loader.load()
    return documents

def load_pdf_UnstructuredPDFLoader(file_path):
    loader = UnstructuredPDFLoader(file_path, language="indonesian")
    documents = loader.load()
    return documents

docs1 = load_pdf_PyPDFLoader("./docs/Pedoman_Nasional_Pelayanan_Kedokteran_(PNPK)_Tata_Laksana_Diabetes_Melitus_Tipe_2_Dewasa.pdf")
docs2 = load_pdf_PyPDFLoader("./docs/Pedoman_Nasional_Pelayanan_Klinis_(PNPK)_Tatalaksana_Diabetes_Melitus_Tipe_2_Dewasa.pdf")
docs3 = load_pdf_UnstructuredPDFLoader("./docs/Pedoman-Pengelolaan-dan-Pencegahan-DMT2-Ebook.pdf")

docs = docs1 + docs2 + docs3

print(f"Loaded {len(docs)} documents from PDF files.")