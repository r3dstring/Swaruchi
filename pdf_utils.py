from pypdf import PdfReader

def extract_pdf(path):

    reader = PdfReader(path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text


def chunk_text(text, size=2000):

    chunks = []

    for i in range(0, len(text), size):

        chunks.append(text[i:i+size])

    return chunks