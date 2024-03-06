import os
import requests
from marker.convert import convert_single_pdf
from marker.models import load_all_models
from tinygrad.helpers import Timing

# PDF -> Markdown
class PDFReader:
    def __init__(self, cache_folder = "./paper_cache", parallel_factor = 1):
        self.cache_folder = cache_folder
        self.parallel_factor = parallel_factor

        os.makedirs(self.cache_folder, exist_ok=True)

    def __call__(self, url):
        def download_pdf(url):
            # Extract the file name from the URL
            file_name = url.split('/')[-1].replace('.', '-')
            file_path = os.path.join(self.cache_folder, file_name)

            if file_path.endswith("-pdf"):
                file_path = file_path[:-4] + ".pdf"

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
            url = "https://arxiv.org/pdf/" + url
        pdf_path = download_pdf(url)
        model_lst = load_all_models()
        full_text, _ = convert_single_pdf(pdf_path, model_lst, max_pages = 20, parallel_factor = self.parallel_factor)
        return full_text

if __name__ == "__main__":
    # Test with the transformers paper
    url = "1706.03762"
    reader = PDFReader()
    with Timing():
        output = reader(url)
