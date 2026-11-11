import os

from langchain_community.document_loaders import PyPDFLoader

def load_pdf_PyPDFLoader(file_path):
    loader = PyPDFLoader(file_path, mode="page")
    documents = loader.load()
    return documents


def save_docs_to_file(docs, out_path="./docs/loaded/loaded_docs.txt"):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        for i, doc in enumerate(docs):
            f.write("=" * 80 + "\n")
            source = doc.metadata.get("source")
            page = doc.metadata.get("page")
            f.write(f"[DOC {i}] source={source} | page={page} | chars={len(doc.page_content)}\n")
            f.write("=" * 80 + "\n")
            f.write(doc.page_content)
            f.write("\n\n")
    print(f"Saved {len(docs)} documents to {out_path}")


PDF_PATHS = (
    "./docs/Pedoman_Nasional_Pelayanan_Kedokteran_(PNPK)_Tata_Laksana_Diabetes_Melitus_Tipe_2_Dewasa.pdf",
    "./docs/Pedoman_Nasional_Pelayanan_Klinis_(PNPK)_Tatalaksana_Diabetes_Melitus_Tipe_2_Dewasa.pdf",
    "./docs/Pedoman-Pengelolaan-dan-Pencegahan-DMT2-Ebook.pdf",
)


def load_all_docs():
    print("Loading PDF documents...")
    docs = []
    for path in PDF_PATHS:
        docs.extend(load_pdf_PyPDFLoader(path))
    print(f"Loaded {len(docs)} documents from PDF files.")
    save_docs_to_file(docs)
    return docs
