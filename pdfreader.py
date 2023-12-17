import os
import fitz
from flask import Flask, render_template, request, send_file
import pyttsx3


app = Flask(__name__)

class PDFReader:
    def __init__(self):
        self.uploaded_file_path = None
        self.tts_engine = pyttsx3.init()

    def read_aloud(self, content):
        if content.strip():
            self.tts_engine.say(content)
            self.tts_engine.runAndWait()
            return "Reading aloud..."
        else:
            return "No content to read aloud."

pdf_reader = PDFReader()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.endswith(".pdf"):
            file_path = os.path.join("uploads", file.filename)
            file.save(file_path)
            pdf_reader.uploaded_file_path = file_path
            return render_template("index.html", content="PDF uploaded successfully.")

    return render_template("index.html")

@app.route("/open_pdf")
def open_pdf():
    if pdf_reader.uploaded_file_path:
        pdf_document = fitz.open(pdf_reader.uploaded_file_path)
        num_pages = pdf_document.page_count

        content = ""
        for page_number in range(num_pages):
            page = pdf_document.load_page(page_number)
            content += page.get_text()

        return render_template("index.html", content=content)
    else:
        return render_template("index.html", content="Please upload a PDF file first.")

@app.route("/read_aloud")
def read_aloud():
    if pdf_reader.uploaded_file_path:
        pdf_document = fitz.open(pdf_reader.uploaded_file_path)
        content = ""
        for page_number in range(pdf_document.page_count):
            page = pdf_document.load_page(page_number)
            content += page.get_text()

        result = pdf_reader.read_aloud(content)
        return render_template("index.html", content=result)
    else:
        return render_template("index.html", content="Please upload a PDF file first.")

@app.route("/download")
def download():
    if pdf_reader.uploaded_file_path:
        return send_file(pdf_reader.uploaded_file_path, as_attachment=True)
    else:
        return render_template("index.html", content="Please upload a PDF file first.")

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
