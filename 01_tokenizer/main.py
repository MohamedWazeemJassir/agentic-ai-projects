import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

print("This is a tokenizer program for GPT-4o model ")

text = input("Enter text: ")

tokens = enc.encode(text)

print("Tokens", tokens)
print("Decoded", enc.decode(tokens))