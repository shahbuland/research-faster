from base_chat_harness import BaseChatHarness
from claude_harness import ClaudeChatHarness
from pdf_reader import PDFReader
import re

prompt = """
You are a highly skilled and prolific researcher who is currently acting as an assistant to a 
less experienced researcher and giving them advice on papers. The papers are easy for you to understand
but may not be for the user. Please be as helpful and elucidating as possible for them. The user will
send you a pdf in their messages. If they are asking about something but do not appear to have sent the
corresponding pdf, ask them for it. The papers they send you may be scanned incorrectly. Particularly,
the latex in them may not be formatted correctly. If you are responding to the user, make sure that
you always use correct latex formatting with dollar signs ($), even if the paper doesn't.
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

class ClaudePDF(ClaudeChatHarness):
    def __init__(self, *args, **kwargs):
        super().__init__(init_prompt = prompt, *args, **kwargs)

        self.reader = PDFReader()

    def run_commands(self, user_input):
        matches = re.findall(r'\[arxiv (.*?)\]', user_input)
        for match in matches:
            pdf_content = self.reader(match)
            user_input = user_input.replace(f'[arxiv {match}]', pdf_content)
        return user_input

def get_chat(version : str = "openai"):
    if version == "openai":
        return PDFHarness()
    elif version == "anthropic":
        return ClaudePDF()
