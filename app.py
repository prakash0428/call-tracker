import os
import fitz  # PyMuPDF
from flask import Flask, request, render_template

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.endswith(".pdf"):
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            call_data = extract_call_data(filepath)

            if call_data:
                return render_template("index.html", call_data=call_data)
            else:
                return render_template("index.html", message="No call data found. Please upload again.")
        else:
            return render_template("index.html", message="Only PDF files are allowed.")
    return render_template("index.html")


def extract_call_data(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()

    lines = text.split("\n")
    keywords = ["incoming", "outgoing", "missed", "duration"]
    call_lines = [line for line in lines if any(keyword in line.lower() for keyword in keywords)]

    if call_lines:
        return call_lines
    return None


if __name__ == "__main__":
    app.run(debug=True)
