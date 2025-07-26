import fitz

def extract_call_data(pdf_path):
    lines = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text = page.get_text()
            for l in text.splitlines():
                if 'incoming' in l.lower() or 'outgoing' in l.lower():
                    lines.append(l)
    return lines
