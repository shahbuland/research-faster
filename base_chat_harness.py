from typing import List
from abc import abstractclassmethod

from copy import deepcopy
from secret import API_KEY
import openai

class BaseChatHarness:
    """
    Base class for all chat bots that make use of tools

    :param verbosity: 0 = no prints, 1 = print all model generated text, 2 = print all model generated text and tool calls
    """
    def __init__(self, init_prompt, debug_mode = False, init_messages : List[str] = [], engine = "gpt-4-0125-preview", verbosity = 0):
        self.model = engine

        self.messages = [
            {"role":"system", "content":init_prompt}
        ]

        for i in range(0, len(init_messages), 2):
            self.messages.append({"role":"user", "content":init_messages[i]})
            if i+1 < len(init_messages):
                self.messages.append({"role":"assistant", "content":init_messages[i+1]})

        self.message_base = deepcopy(self.messages)
        self.debug_mode = debug_mode
        self.verbosity = verbosity

        self.client = openai.OpenAI(api_key = API_KEY)

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
            if not self.debug_mode:
                response = self.client.chat.completions.create(
                    model = self.model,
                    messages = self.messages,
                    temperature = 0
                )
                reply =  response.choices[0].message.content
            else:
                reply = input("Assistant:")
        except Exception as e:
            del self.messages[-1]
            return f"API Error : {e}"

        self.messages.append({"role":"assistant", "content":reply})
        if self.verbosity >= 1:
            print("[DEBUG] Full Response:", reply)
        
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
        pass

if __name__ == "__main__":
    chat = BaseChatHarness("You are a helpful assistant")
    while True:
        print(chat(input()))
