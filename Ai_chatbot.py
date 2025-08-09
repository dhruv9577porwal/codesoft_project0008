import tkinter as tk
from tkinter import scrolledtext
import datetime

# --------------------- BOT LOGIC ---------------------
def get_bot_response(user_input):
    user_input = user_input.lower()

    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I assist you today?"
    elif "how are you" in user_input:
        return "I'm doing fantastic! Thanks for asking 😊"
    elif "name" in user_input:
        return "I'm RAAS – your friendly Python chatbot 🤖"
    elif "bye" in user_input or "exit" in user_input:
        return "Goodbye! Take care! 👋"
    elif "help" in user_input:
        return "Ask me about the weather, time, jokes, or just say hi!"
    elif "creator" in user_input or "who made you" in user_input:
        return "I was crafted by Anurag Porwal, a passionate coder ❤️ using Python and Tkinter!"
    elif "time" in user_input:
        return "The current time is " + datetime.datetime.now().strftime("%I:%M %p")
    elif "date" in user_input:
        return "Today is " + datetime.datetime.now().strftime("%A, %d %B %Y")     
    elif "joke" in user_input:
        return "Why do programmers prefer dark mode? Because light attracts bugs! 😄"
    elif "weather" in user_input:
        return "I'm not connected to live data, but I hope it's pleasant where you are! ☀️"
    else:
        return "Sorry, I didn't get that. Could you rephrase?"

# --------------------- FUNCTIONS ---------------------
def send_message():
    user_input = entry.get().strip()
    if not user_input:
        return
    current_time = datetime.datetime.now().strftime("%H:%M")

    chat_area.insert(tk.END, f"You [{current_time}]: {user_input}\n", 'user')
    response = get_bot_response(user_input)
    chat_area.insert(tk.END, f"RAAS [{current_time}]: {response}\n\n", 'bot')
    chat_area.see(tk.END)
    entry.delete(0, tk.END)

def clear_chat():
    chat_area.delete(1.0, tk.END)

# --------------------- GUI ---------------------
root = tk.Tk()
root.title("💬 RAAS - Rule-Based Chatbot")
root.geometry("650x650")
root.configure(bg="#1a1a2e")

# Chat area
chat_area = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, font=("Segoe UI", 12),
    bg="#e8eaf6", fg="#1a1a2e", padx=12, pady=12, bd=2, relief="sunken"
)
chat_area.tag_config('user', foreground='#1565c0', font=('Segoe UI Semibold', 12, 'bold'))
chat_area.tag_config('bot', foreground='#2e7d32', font=('Segoe UI', 12))
chat_area.pack(padx=12, pady=12, fill=tk.BOTH, expand=True)

# Entry frame
entry_frame = tk.Frame(root, bg="#1a1a2e")
entry_frame.pack(pady=8, fill=tk.X)

entry = tk.Entry(entry_frame, font=("Segoe UI", 13), width=40,
                 bg="#ffffff", fg="#1a1a2e", bd=3, relief="groove")
entry.pack(side=tk.LEFT, padx=10, pady=5)

send_button = tk.Button(entry_frame, text="➤ Send", command=send_message,
                        bg="#3949ab", fg="white", font=("Segoe UI Semibold", 11),
                        width=10, bd=3, relief="raised")
send_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(root, text="🧹 Clear Chat", command=clear_chat,
                         bg="#d32f2f", fg="white", font=("Segoe UI", 10),
                         width=12, bd=3, relief="ridge")
clear_button.pack(pady=8)

# Bind Enter key
entry.bind("<Return>", lambda event: send_message())

root.mainloop()
