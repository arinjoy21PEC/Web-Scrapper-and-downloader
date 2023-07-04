import tkinter as tk
from tkinter import ttk, filedialog
import requests
from bs4 import BeautifulSoup

class Downloader:
    def __init__(self):
        self.saveto = ""
        self.window = tk.Tk()
        self.window.title("Python GUI Downloader")
        self.url_label = tk.Label(text="Enter URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry()
        self.url_entry.pack()
        self.browse_button = tk.Button(text='Browse', command=self.browse_file)
        self.browse_button.pack()
        self.download_button = tk.Button(text='Download', command=self.download)
        self.download_button.pack()
        self.modify_button = tk.Button(text='Modify', command=self.modify)
        self.modify_button.pack()
        self.window.geometry("844x344")
        self.progress_bar = ttk.Progressbar(self.window, orient='horizontal', maximum=100, length=300, mode='determinate')
        self.progress_bar.pack()
        self.window.mainloop()

    def browse_file(self):
        saveto = filedialog.asksaveasfilename(initialfile=self.url_entry.get().split("/")[-1]).split("?")[0]
        if not saveto.endswith(".html"):
            saveto += ".html"
        self.saveto = saveto

    def download(self):
        url = self.url_entry.get()
        response = requests.get(url, stream=True)
        total_size_in_bytes = 10000
        if response.headers.get("content-length"):
            total_size_in_bytes = int(response.headers.get('Content-Length', 0))
        block_size = 10000
        self.progress_bar['value'] = 0
        filename = self.url_entry.get().split("/")[-1].split("?")[0]
        if not filename.endswith(".html"):
            filename += ".html"
        if self.saveto == "":
            self.saveto = filename
        with open(self.saveto, 'wb') as f:
            for data in response.iter_content(block_size):
                self.progress_bar['value'] += (100 * block_size) / total_size_in_bytes
                self.window.update()
                f.write(data)

        print(f"File downloaded to {self.saveto}")

    def modify(self):
        if self.saveto.endswith(".html") or self.saveto.endswith(".htm"):
            with open(self.saveto, "r", encoding="utf-8") as html_file:
                soup = BeautifulSoup(html_file, "html.parser")
                text_content = soup.get_text()
                text_filename = self.saveto.rsplit(".", 1)[0] + ".txt"
                with open(text_filename, "w", encoding="utf-8") as text_file:
                    text_file.write(text_content)
                print(f"Text content downloaded to {text_filename}")
        else:
            print("The file is not an HTML file.")

Downloader()
