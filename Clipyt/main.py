import os
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.ttk import Progressbar, Style, Button, Label, Entry
import threading
from slide_extractor import SlideExtractor
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pytesseract
from dark_theme import apply_dark_theme

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class SlideExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Slide Extractor")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        app_width = 800
        app_height = 600
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)
        self.root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        self.style = apply_dark_theme(root)

        self.bg_canvas = tk.Canvas(root, bg="#2b2b2b", highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)

        self.content_frame = tk.Frame(self.bg_canvas, bg="#2b2b2b", bd=5, relief='raised', highlightbackground="#3a3a3a", highlightthickness=2)
        self.content_frame_id = self.bg_canvas.create_window(0, 0, window=self.content_frame, anchor="center")

        self.bg_canvas.bind('<Configure>', self.on_canvas_resize)

        self.create_widgets(self.content_frame)

    def on_canvas_resize(self, event):
        self.draw_background_pattern(event.width, event.height)
        self.bg_canvas.coords(self.content_frame_id, event.width / 2, event.height / 2)

    def draw_background_pattern(self, width, height):
        self.bg_canvas.delete("pattern_line")
        
        grid_spacing = 30
        line_color = "#3c3c3c"

        for i in range(0, width, grid_spacing):
            self.bg_canvas.create_line(i, 0, i, height, fill=line_color, dash=(2, 2), tags="pattern_line")
        for i in range(0, height, grid_spacing):
            self.bg_canvas.create_line(0, i, width, i, fill=line_color, dash=(2, 2), tags="pattern_line")

    def create_widgets(self, parent_frame):

        Label(parent_frame, text="Enter YouTube URL:", style="Header.TLabel").grid(row=0, column=0, pady=20, padx=20, sticky="w")
        self.url_entry = Entry(parent_frame, width=50, font=("Helvetica", 14))
        self.url_entry.grid(row=0, column=1, pady=10, padx=20)

        Label(parent_frame, text="Frame Interval (Seconds):").grid(row=1, column=0, pady=20, padx=20, sticky="w")
        self.interval_entry = Entry(parent_frame, width=10, font=("Helvetica", 14))
        self.interval_entry.insert(0, "5")
        self.interval_entry.grid(row=1, column=1, pady=10, padx=20)

        Label(parent_frame, text="Similarity Threshold (0.0 to 1.0):").grid(row=2, column=0, pady=20, padx=20, sticky="w")
        self.threshold_entry = Entry(parent_frame, width=10, font=("Helvetica", 14))
        self.threshold_entry.insert(0, "0.9")
        self.threshold_entry.grid(row=2, column=1, pady=10, padx=20)

        Label(parent_frame, text="Output Directory: slides/").grid(row=3, column=0, pady=20, padx=20, sticky="w")

        self.progress_label = Label(parent_frame, text="Status: Ready", style="Status.TLabel")
        self.progress_label.grid(row=4, column=0, pady=20, padx=20, sticky="w")

        self.progress_bar = Progressbar(parent_frame, orient="horizontal", length=500, mode="indeterminate")
        self.progress_bar.grid(row=4, column=1, pady=20, padx=20)

        self.extract_button = Button(parent_frame, text="Extract Slides", style="Accent.TButton", command=self.extract_slides)
        self.extract_button.grid(row=5, column=0, columnspan=2, pady=30)

        self.pdf_button = Button(parent_frame, text="Generate PDF", style="Accent.TButton", command=self.generate_pdf)
        self.pdf_button.grid(row=6, column=0, columnspan=2, pady=20)

    def extract_slides(self):
        url = self.url_entry.get()
        interval = int(self.interval_entry.get())
        threshold = float(self.threshold_entry.get())

        self.toggle_inputs(state="disabled")
        self.progress_label.config(text="Status: Downloading video...")
        self.progress_bar.start()

        threading.Thread(target=self.start_slide_extraction, args=(url, interval, threshold), daemon=True).start()

    def start_slide_extraction(self, url, interval, threshold):
        try:
            extractor = SlideExtractor(video_url=url, interval=interval, similarity_threshold=threshold)
            success = extractor.extract_slides()
            status = "Extraction Complete!" if success else "Extraction Failed!"
            self.progress_label.config(text=f"Status: {status}")
        except Exception as e:
            self.progress_label.config(text=f"Error: {str(e)}")
        finally:
            self.progress_bar.stop()
            self.toggle_inputs(state="normal")

    def toggle_inputs(self, state):
        self.url_entry.config(state=state)
        self.interval_entry.config(state=state)
        self.threshold_entry.config(state=state)
        self.extract_button.config(state=state)

    def generate_pdf(self):
        slide_folder = "slides"
        pdf_filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        if not pdf_filename:
            return

        try:
            c = canvas.Canvas(pdf_filename, pagesize=letter)
            c.setFont("Helvetica", 16)

            slide_images = sorted(f for f in os.listdir(slide_folder) if f.endswith(".png"))

            y = 750
            for slide in slide_images:
                slide_path = os.path.join(slide_folder, slide)
                img = Image.open(slide_path)
                img_width, img_height = img.size
                aspect_ratio = (img_height * 500) / img_width
                c.drawImage(slide_path, 50, y, width=500, height=aspect_ratio)

                y -= 550
                if y < 100:
                    c.showPage()
                    y = 750

            c.save()
            messagebox.showinfo("Success", f"PDF generated successfully at:\n{pdf_filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Error generating PDF: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SlideExtractorApp(root)
    root.mainloop()
