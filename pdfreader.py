import fitz  
import tkinter as tk
from tkinter import filedialog
import pyttsx3

class PDFReader:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Reader")

        self.text_widget = tk.Text(root, wrap="word", width=80, height=25)
        self.text_widget.pack(pady=10)

        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open PDF", command=self.open_pdf)
        file_menu.add_command(label="Read Aloud", command=self.read_aloud)
        file_menu.add_command(label="Exit", command=root.destroy)

        self.tts_engine = pyttsx3.init()

    def open_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            pdf_document = fitz.open(file_path)
            num_pages = pdf_document.page_count

            content = ""
            for page_number in range(num_pages):
                page = pdf_document.load_page(page_number)
                content += page.get_text()

            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.END, content)

    def read_aloud(self):
        content = self.text_widget.get(1.0, tk.END)
        if content.strip():
            self.tts_engine.say(content)
            self.tts_engine.runAndWait()

if __name__ == "__main__":
    root = tk.Tk()
    pdf_reader = PDFReader(root)
    root.mainloop()
