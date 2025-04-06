import fitz
import tkinter as tk
from tkinter import filedialog
import subprocess
import threading
import re

class PDFReader:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Reader")

        self.text_widget = tk.Text(root, wrap="word", width=80, height=20)
        self.text_widget.grid(row=0, column=0, columnspan=3, padx=10, pady=(10,5), sticky="nsew")
        self.text_widget.config(font=("Helvetica", 12))  

        self.open_button = tk.Button(root, text="Open PDF", command=self.open_pdf, width=10)
        self.open_button.grid(row=1, column=0, padx=5, pady=(0,10), sticky="w")

        self.play_button = tk.Button(root, text="Play", command=self.play_reading, width=10)
        self.play_button.grid(row=1, column=1, padx=5, pady=(0,10))

        self.pause_button = tk.Button(root, text="Pause", command=self.pause_reading, width=10)
        self.pause_button.grid(row=1, column=2, padx=5, pady=(0,10), sticky="e")
        self.pause_button.config(state=tk.DISABLED)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_reading, width=10)
        self.stop_button.grid(row=2, column=1, padx=5, pady=(0,10))
        self.stop_button.config(state=tk.DISABLED)

        self.status_bar = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=3, column=0, columnspan=3, sticky="ew")

        self.is_paused = False
        self.speaker_process = None

    def open_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            try:
                pdf_document = fitz.open(file_path)
                num_pages = pdf_document.page_count

                self.status_bar.config(text=f"Loading {num_pages} pages...")
                self.root.update_idletasks()

                content = "\n".join([pdf_document.load_page(i).get_text() for i in range(num_pages)])

                # Limpiar el texto (eliminar puntos para fluidez)
                content = re.sub(r"\.", "", content)

                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.END, content)
                self.status_bar.config(text="PDF loaded successfully.")
                self.enable_controls()
            except Exception as e:
                self.status_bar.config(text=f"Error: {str(e)}")

    def play_reading(self):
        content = self.text_widget.get(1.0, tk.END).strip()
        if content:
            self.is_paused = False
            self.status_bar.config(text="Reading aloud...")
            self.disable_controls()
            self.pause_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            
            self.speaker_process = threading.Thread(target=self._speak, args=(content,))
            self.speaker_process.start()

    def _speak(self, text):
        try:
            # Reproduce el texto ignorando los puntos
            subprocess.run(f'espeak-ng -v es "{text}" --stdout | paplay', shell=True)
            self.status_bar.config(text="Reading completed.")
            self.enable_controls()
        except Exception as e:
            self.status_bar.config(text=f"Error: {str(e)}")

    def pause_reading(self):
        if self.speaker_process and self.speaker_process.is_alive():
            self.is_paused = not self.is_paused
            if self.is_paused:
                subprocess.run("pkill -STOP espeak-ng", shell=True)
                self.status_bar.config(text="Paused.")
                self.pause_button.config(text="Resume")
            else:
                subprocess.run("pkill -CONT espeak-ng", shell=True)
                self.status_bar.config(text="Reading resumed.")
                self.pause_button.config(text="Pause")

    def stop_reading(self):
        if self.speaker_process and self.speaker_process.is_alive():
            subprocess.run("pkill espeak-ng", shell=True)
            self.status_bar.config(text="Reading stopped.")
            self.enable_controls()

    def disable_controls(self):
        self.open_button.config(state=tk.DISABLED)
        self.play_button.config(state=tk.DISABLED)

    def enable_controls(self):
        self.open_button.config(state=tk.NORMAL)
        self.play_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")  
    pdf_reader = PDFReader(root)
    root.mainloop()
