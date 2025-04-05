import tkinter as tk
from tkinter import scrolledtext
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# --- API Client ---
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

def chat_with_gpt(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error] {str(e)}"

def send_message():
    user_msg = entry.get()
    if user_msg.strip() == "":
        return
    chat_window.insert(tk.END, f"You: {user_msg}\n", "user")
    entry.delete(0, tk.END)
    
    response = chat_with_gpt(user_msg)
    chat_window.insert(tk.END, f"Chatbot: {response}\n\n", "bot")
    chat_window.see(tk.END)

# --- GUI Setup ---
root = tk.Tk()
root.title("chatbot AI")

# Colors
bg_color = "#0D0D0D"         # deep black
input_bg = "#1A1A1A"         # dark grayish black
text_color = "#FFFFFF"       # white
highlight_blue = "#00BFFF"   # deep sky blue

# Configure overall background
root.configure(bg=bg_color)

chat_window = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, width=80, height=25, font=("Consolas", 12),
    bg=bg_color, fg=text_color, insertbackground=text_color, borderwidth=0
)
chat_window.pack(padx=10, pady=10)
chat_window.tag_config("user", foreground=highlight_blue)
chat_window.tag_config("bot", foreground=text_color)
chat_window.insert(tk.END, "Chatbot: Hello! Ask me anything.\n\n", "bot")

entry_frame = tk.Frame(root, bg=bg_color)
entry_frame.pack(padx=10, pady=(0, 10))

entry = tk.Entry(entry_frame, width=70, font=("Consolas", 12), bg=input_bg, fg=text_color, insertbackground=text_color, borderwidth=0)
entry.pack(side=tk.LEFT, padx=(0, 10))
entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(entry_frame, text="Send", command=send_message, bg=highlight_blue, fg="black", font=("Consolas", 11, "bold"))
send_button.pack(side=tk.RIGHT)

entry.focus()
root.mainloop()
