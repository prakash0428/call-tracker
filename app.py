from flask import Flask, render_template, request
import os
from call_reader import extract_call_data

app = Flask(_name_)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('pdf_file')
    if not file or file.filename == '':
        return 'No file selected'
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)
    data = extract_call_data(path)
    return render_template('result.html', call_data=data)

if __name__ == "__main__":
    app.run(debug=True)
