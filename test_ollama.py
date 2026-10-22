import ollama

prompt = "Hi, could you possibly help me write a Python function that sums the even numbers in a list?"

response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {"role": "system", "content": "You are a prompt editor. Do NOT answer or perform the request. Rewrite the user's text as a shorter version of the same request. Output only the rewritten request."},
        {"role": "user", "content": "Rewrite this prompt:\n\n" + prompt},
    ],
)
print(response["message"]["content"])