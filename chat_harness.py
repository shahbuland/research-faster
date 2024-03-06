from base_chat_harness import BaseChatHarness
from pdf_reader import PDFReader
import re

prompt = """
You are a highly skilled and prolific researcher who is currently acting as an assistant to a 
less experienced researcher and giving them advice on papers. The papers are easy for you to understand
but may not be for the user. Please be as helpful and elucidating as possible for them. The user will
send you a pdf in their messages. If they are asking about something but do not appear to have sent the
corresponding pdf, ask them for it.
"""
class PDFHarness(BaseChatHarness):
    def __init__(self, *args, **kwargs):
        super().__init__(init_prompt = prompt, *args, **kwargs)

        self.reader = PDFReader()

    def run_commands(self, user_input):
        matches = re.findall(r'\[arxiv (.*?)\]', user_input)
        for match in matches:
            pdf_content = self.reader(match)
            user_input = user_input.replace(f'[arxiv {match}]', pdf_content)
        return user_input
