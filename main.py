from chat_harness import PDFHarness

if __name__ == "__main__":
    chat = PDFHarness()

    while True:
        print(chat(input()))