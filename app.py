import gradio as gr
from openai import OpenAI
from retrieval import retrieve

OLLAMA_BASE_URL = "http://localhost:11434/v1"
client = OpenAI(base_url=OLLAMA_BASE_URL,api_key="ollama")
MODEL = "gpt-oss:20b"
system_message = "You are a helpful assistant that answers questions based on the provided context. If the answer is not in the context, say answer is not provided to me. Keep your answers concise and relevant to the user's notes on Transformers."


def rewrite_question(question, history):
    rewrite_question__system_prompt = """
You are a query-rewriting assistant.

Your task is ONLY to rewrite the user's latest question using the chat history
so that it becomes a clear, standalone, context-complete question.

Rules:
- DO NOT answer the question.
- DO NOT add explanations.
- DO NOT include any extra text.
- Preserve the original intent.
- If the question is already clear, return it unchanged.
- Output must contain exactly one rewritten question.
"""


    messages = [{"role": "system", "content": rewrite_question__system_prompt}] + history + [{"role": "user", "content": question}]

    response = client.chat.completions.create(model=MODEL, messages=messages)

    return response.choices[0].message.content


def chat(message, history):
        # 1. format history explicitly for safety/consistency
        history = [{"role": h["role"], "content": h["content"]} for h in history]
        
        if history != []:
            message = rewrite_question(message, history)


        rag_context = retrieve(message)
        print("rag_context is ",rag_context)
        # 2. Construct the message payload
        # Note: We will define system_message in the next section
        # Combine message and RAG context as a single string

        user_content = message
        if rag_context:
            user_content = f"Context:\n{rag_context}\n\nQuestion: {message}"
            

        messages = [{"role": "system", "content": system_message}] + history + [
            {"role": "user", "content": user_content}
        ]

        # # Call Ollama API with stream=True
        # stream = client.chat.completions.create(model=MODEL, messages=messages, stream=True)

        # # 4. Accumulate and Yield
        # response = ""
        # for chunk in stream:
        #     response += chunk.choices[0].delta.content or ''
        #     yield response # Updates the UI incrementally

        response = client.chat.completions.create(model=MODEL, messages=messages)
            
        return response.choices[0].message.content

gr.ChatInterface(fn=chat).launch()



