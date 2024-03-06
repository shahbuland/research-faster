from chat_harness import PDFHarness

if __name__ == "__main__":
    chat = PDFHarness()

    print("Usage: Use command [arxiv ...] in your message to load an entire arxiv paper into the context. The ... here can be a full url to a PDF file, or the code at the end (i.e. 2403.03206)")
    print("=======================")
    while True:
        print("=======================")
        user_msg = input()
        print("=======================")
        print(chat(user_msg))
