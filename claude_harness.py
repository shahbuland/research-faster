from abc import abstractclassmethod
from copy import deepcopy
from typing import List

import anthropic
from secret import CLAUDE_API_KEY

class ClaudeChatHarness:
    """
    Base class for some chat bot made off of openai api
    """
    def __init__(self, init_prompt = "You are a helpful assistant.", engine = "claude-3-opus-20240229"):
        self.model = engine
        self.system = init_prompt
        self.client = anthropic.Anthropic(api_key = CLAUDE_API_KEY)
        self.messages = []

    def reset(self):
        self.messages = deepcopy(self.message_base)
        
    def converse(self, user_input, mode = "user"):
        # Any outputs that are from a tool will get "TOOL RESULT:" added to start
        # This is to differentiate from actual user input

        if type(user_input) is not str:
            user_input = str(user_input)
        
        user_input = self.run_commands(user_input)

        self.messages.append({"role":"user", "content":user_input})

        # If not in debug try and generate response from API
        # Otherwise get user input as a debug value
        try:
            message = self.client.messages.create(
                model = self.model,
                max_tokens = 1000,
                temperature = 0.0,
                system = self.system,
                messages = self.messages
            )
            reply =  message.content[0].text
        except Exception as e:
            del self.messages[-1]
            return f"API Error : {e}"

        self.messages.append({"role":"assistant", "content":reply})
        
        return self.sanitize_response(reply)

    def __call__(self, *args, **kwargs):
        return self.converse(*args, **kwargs)

    def sanitize_response(self, message : str):
        """
        Sanitize the final response to the user, i.e. to extract external dialogue or just generally to post proecess messages
        """
        return message

    @abstractclassmethod
    def run_commands(self, user_input : str) -> str:
        """
        Run any commands contained in the users input and replace them with the output of the commands
        """
        return user_input

if __name__ == "__main__":
    chat = ClaudeChatHarness()
    while True:
        print(chat(input()))
