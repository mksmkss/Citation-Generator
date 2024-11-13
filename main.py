import customtkinter as ctk
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import datetime
import re
import pyperclip
from tkinter import messagebox


class CitationGenerator(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Version
        self.version = "1.0.0"  # バージョン変数を追加

        # Window configuration
        self.title("Citation Format Generator")
        self.geometry("1000x1000")

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(7, weight=1)

        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.create_widgets()

    def create_widgets(self):
        # Title
        self.title_label = ctk.CTkLabel(
            self, text="Citation Format Generator", font=("Helvetica", 24, "bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Input Fields Frame
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.input_frame.grid_columnconfigure(1, weight=1)

        # URL Input
        self.url_label = ctk.CTkLabel(
            self.input_frame, text="URL:", font=("Helvetica", 14)
        )
        self.url_label.grid(row=0, column=0, padx=10, pady=5)

        self.url_entry = ctk.CTkEntry(
            self.input_frame, placeholder_text="Enter URL here...", width=400
        )
        self.url_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.url_entry.bind("<KeyRelease>", lambda e: self.generate_citations())

        # Fetch URL Button
        self.fetch_button = ctk.CTkButton(
            self.input_frame, text="Fetch Metadata", command=self.fetch_metadata
        )
        self.fetch_button.grid(row=0, column=2, padx=10, pady=5)

        # Manual Input Fields
        input_fields = [
            ("Title:", "title_entry", "Enter title..."),
            ("Author:", "author_entry", "Enter author..."),
            ("Year:", "year_entry", str(datetime.datetime.now().year)),
            (
                "URL Date:",
                "urldate_entry",
                datetime.datetime.now().strftime("%Y/%m/%d"),
            ),
            ("Note:", "note_entry", "Online;"),
        ]

        for i, (label_text, attr_name, placeholder) in enumerate(input_fields):
            label = ctk.CTkLabel(
                self.input_frame, text=label_text, font=("Helvetica", 14)
            )
            label.grid(row=i + 1, column=0, padx=10, pady=5)

            entry = ctk.CTkEntry(
                self.input_frame, placeholder_text=placeholder, width=400
            )
            entry.grid(row=i + 1, column=1, padx=10, pady=5, sticky="ew")
            entry.bind("<KeyRelease>", lambda e: self.generate_citations())
            setattr(self, attr_name, entry)

        # BibTeX Output
        self.bibtex_text = ctk.CTkTextbox(
            self, width=900, height=200, font=("Courier New", 12)
        )
        self.bibtex_text.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="nsew")

        # Copy BibTeX Button
        self.copy_bibtex_button = ctk.CTkButton(
            self,
            text="Copy BibTeX",
            command=lambda: self.copy_to_clipboard(self.bibtex_text),
        )
        self.copy_bibtex_button.grid(
            row=4, column=0, padx=(0, 30), pady=(0, 10), sticky="se"
        )

        # Text Citation Output
        self.text_citation = ctk.CTkTextbox(
            self, width=900, height=150, font=("Helvetica", 12)
        )
        self.text_citation.grid(row=6, column=0, padx=20, pady=(0, 10), sticky="nsew")

        # Copy Text Button
        self.copy_text_button = ctk.CTkButton(
            self,
            text="Copy Text",
            command=lambda: self.copy_to_clipboard(self.text_citation),
        )
        self.copy_text_button.grid(
            row=6, column=0, padx=(0, 30), pady=(0, 10), sticky="se"
        )

        # Status Bar
        self.status_label = ctk.CTkLabel(self, text="Ready", font=("Helvetica", 12))
        self.status_label.grid(row=7, column=0, padx=20, pady=5)

        # Clear All Button
        self.clear_button = ctk.CTkButton(
            self, text="Clear All", command=self.clear_fields
        )
        self.clear_button.grid(row=8, column=0, padx=20, pady=10, sticky="s")

        # Version and Author info
        info_text = f"Version {self.version} | Created by 鈴木柾孝"
        self.info_label = ctk.CTkLabel(
            self, text=info_text, font=("Helvetica", 10), text_color="gray"
        )
        self.info_label.grid(row=9, column=0, padx=20, pady=(0, 10), sticky="se")

    def clean_text(self, text):
        """Clean text for BibTeX entry"""
        if not text:
            return ""
        text = re.sub(r"[^\w\s-]", "", text)
        text = " ".join(text.split())
        return text

    def generate_key(self, title, year):
        """Generate a BibTeX citation key"""
        if not title:
            return f"web{year}"
        first_word = self.clean_text(title).split()[0].lower()
        return f"{first_word}{year}"

    def fetch_metadata(self):
        """Fetch metadata from URL"""
        url = self.url_entry.get().strip()

        if not url:
            messagebox.showwarning("Warning", "Please enter a URL")
            return

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        try:
            self.status_label.configure(text="Fetching webpage...")

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Update title
            if soup.title:
                self.title_entry.delete(0, ctk.END)
                self.title_entry.insert(0, self.clean_text(soup.title.string))

            # Update author if available
            author = ""
            author_meta = soup.find("meta", {"name": ["author", "Author", "AUTHOR"]})
            if author_meta:
                author = self.clean_text(author_meta.get("content", ""))
            else:
                # Try other common author meta tags
                author_meta = soup.find(
                    "meta", {"property": ["article:author", "og:author"]}
                )
                if author_meta:
                    author = self.clean_text(author_meta.get("content", ""))

            if author:
                self.author_entry.delete(0, ctk.END)
                self.author_entry.insert(0, author)

            # 日付を探す - 複数のパターンをチェック
            date_meta = soup.find(
                lambda tag: (
                    (
                        tag.name == "meta"
                        and tag.get("name")
                        in ["date", "Date", "published_time", "publication_date"]
                    )
                    or (
                        tag.name == "p"
                        and any(
                            cls in tag.get("class", [])
                            for cls in ["date", "published_time", "publication_date"]
                        )
                    )
                )
            )

            year = datetime.datetime.now().year
            if date_meta:
                if date_meta.name == "meta":
                    date_str = date_meta.get("content", "")
                else:
                    date_str = date_meta.text.strip()
                try:
                    # 様々な日付フォーマットに対応
                    for fmt in [
                        "%Y-%m-%d",
                        "%Y/%m/%d",
                        "%Y年%m月%d日",
                        "%Y",
                        "%Y.%m.%d",
                    ]:
                        try:
                            year = datetime.datetime.strptime(date_str, fmt).year
                            break
                        except ValueError:
                            continue
                except:
                    pass

            self.year_entry.delete(0, ctk.END)
            self.year_entry.insert(0, str(year))

            # Update URL
            self.url_entry.delete(0, ctk.END)
            self.url_entry.insert(0, url)

            # Update URL date with current date
            current_date = datetime.datetime.now().strftime("%Y/%m/%d")
            self.urldate_entry.delete(0, ctk.END)
            self.urldate_entry.insert(0, current_date)

            # Update note
            self.note_entry.delete(0, ctk.END)
            self.note_entry.insert(0, "Online;")

            # メタデータ取得後に引用を生成
            self.generate_citations()

            self.status_label.configure(text="Metadata fetched successfully!")

        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}")
            messagebox.showerror("Error", f"Error fetching metadata: {str(e)}")

    def generate_citations(self):
        """Generate both BibTeX and text citations"""
        try:
            title = self.title_entry.get().strip()
            author = self.author_entry.get().strip()
            year = self.year_entry.get().strip()
            url = self.url_entry.get().strip()
            urldate = self.urldate_entry.get().strip()
            note = self.note_entry.get().strip()

            # 必須フィールドが空の場合は生成をスキップ
            if not (title or author or year):
                return

            key = self.generate_key(title, year)

            # Generate BibTeX
            bibtex = f"""@misc{{{key},
            title = {{{title}}},
            author = {{{author if author else "Unknown"}}},
            year = {{{year}}},
            url = {{{url}}},
            urldate = {{{urldate}}},
            note = {{{note} accessed {urldate}}}
            }}"""

            # Generate text citation (Japanese format)
            text_citation = f"""{author}『{title}』,{year} ,{url} , {urldate}閲覧."""

            self.bibtex_text.delete("1.0", ctk.END)
            self.bibtex_text.insert("1.0", bibtex)

            self.text_citation.delete("1.0", ctk.END)
            self.text_citation.insert("1.0", text_citation)

            self.status_label.configure(text="Citations updated")

        except Exception as e:
            # エラーメッセージを控えめに
            self.status_label.configure(text="Waiting for input...")

    def copy_to_clipboard(self, text_widget):
        """Copy content from specified text widget to clipboard"""
        content = text_widget.get("1.0", ctk.END).strip()
        if content:
            pyperclip.copy(content)
            self.status_label.configure(text="Copied to clipboard!")
        else:
            messagebox.showinfo("Info", "Nothing to copy!")

    def clear_fields(self):
        """Clear all fields"""
        self.url_entry.delete(0, ctk.END)
        self.title_entry.delete(0, ctk.END)
        self.author_entry.delete(0, ctk.END)
        self.year_entry.delete(0, ctk.END)
        self.urldate_entry.delete(0, ctk.END)
        self.note_entry.delete(0, ctk.END)
        self.bibtex_text.delete("1.0", ctk.END)
        self.text_citation.delete("1.0", ctk.END)
        self.status_label.configure(text="Ready")


def main():
    app = CitationGenerator()
    app.mainloop()


if __name__ == "__main__":
    main()
