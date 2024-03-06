import os
import requests
from marker.convert import convert_single_pdf
from marker.models import load_all_models

# Assumes marker is setup under "marker"

# PDF -> Markdown
class PDFReader:
    def __init__(self, cache_folder = "./paper_cache", parallel_factor = 1):
        self.cache_folder = cache_folder
        self.parallel_factor = parallel_factor

    def __call__(self, url):
        def download_pdf(self, url):
            # Extract the file name from the URL
            file_name = url.split('/')[-1].replace('.', '-')
            file_path = os.path.join(self.cache_folder, file_name)

            # Check if the file already exists in the cache
            if not os.path.exists(file_path):
                # Download the file
                response = requests.get(url)
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            return file_path

        if not url.endswith(".pdf"):
            url += ".pdf"
        if not "arxiv" in url:
            url = "https://arxiv.org/abs/" + url
        pdf_path = download_pdf(url)
        full_text, _ = convert_single_pdf(pdf_path, model_lst(), max_pages = 20, parallel_factor = self.parallel_factor)
        return full_text

if __name__ == "__main__":
    # Test with the transformers paper
    url = "https://arxiv.org/abs/1706.03762"
    reader = PDFReader()
    print(reader(url)[:100])