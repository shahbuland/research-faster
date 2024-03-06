from base_chat_harness import BaseChatHarness
from pdf_reader import PDFReader
import re

class PDFHarness(BaseChatHarness):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.reader = PDFReader()

    def run_commands(self, user_input):
        matches = re.findall(r'\[arxiv (.*?)\]', user_input)
        for match in matches:
            url = f"https://arxiv.org/abs/{match}"
            pdf_content = self.reader(url)
            user_input = user_input.replace(f'[arxiv {match}]', pdf_content)
        return user_input
