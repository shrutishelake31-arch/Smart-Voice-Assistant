import tkinter as tk
import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import random
import threading
import requests
import os

# ---------- STATES ----------
mode = None
riddle_answer = None
quiz_answer = None

riddles = [
    ("I speak without a mouth and hear without ears. What am I?", "echo"),
    ("The more you take, the more you leave behind. What am I?", "footsteps"),
    ("I have cities but no houses, rivers but no water. What am I?", "map"),
    ("What has to be broken before you can use it?", "egg"),
    ("I’m tall when I’m young and short when I’m old. What am I?", "candle")
]

# ---------- SPEAK ----------
def speak(text):
    chat.insert(tk.END, "Assistant: " + text + "\n")

    def run():
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()

    threading.Thread(target=run).start()

# ---------- SMART ANSWERS ----------
def smart_answer(user):
    answers = {
        "who is virat kohli": "Virat Kohli is an Indian cricketer and former captain of India.",
        "what is ai": "Artificial Intelligence is the simulation of human intelligence in machines.",
        "what is machine learning": "Machine learning is a part of AI where systems learn from data.",
        "capital of india": "The capital of India is New Delhi.",
        "prime minister": "The Prime Minister of India is Narendra Modi."
    }

    for key in answers:
        if key in user:
            return answers[key]

    return None

# ---------- PROCESS ----------
def process(user):
    global mode, riddle_answer, quiz_answer
    user = user.lower()

    # ===== GAME STATES =====
    if mode == "riddle":
        if riddle_answer in user:
            mode = None
            return "Correct! Very smart 😎"
        else:
            return "Wrong answer, try again"

    elif mode == "quiz":
        if user.isdigit():
            if int(user) == quiz_answer:
                mode = None
                return "Correct answer 🎉"
            else:
                return "Wrong answer"

    # ===== BASIC =====
    elif "hello" in user:
        return "Hello Shruti! I am your smart assistant."

    elif "how are you" in user:
        return "I am working perfectly and ready to help you."

    elif "sad" in user:
        return "Don't worry, everything will be okay."

    elif "happy" in user:
        return "That's great! Keep smiling."

    elif "motivation" in user:
        return "Believe in yourself. You can achieve anything."

    elif "time" in user:
        return datetime.datetime.now().strftime("Time is %H:%M:%S")

    elif "date" in user:
        return datetime.datetime.now().strftime("Today is %d %B %Y")

    # ===== WEATHER =====
    elif "weather" in user:
        try:
            res = requests.get("https://wttr.in/Satara?format=3")
            return res.text
        except:
            return "Unable to fetch weather"

    # ===== SEARCH =====
    elif "search" in user:
        query = user.replace("search", "")
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return "Searching Google"

    # ===== NEWS =====
    elif "news" in user:
        webbrowser.open("https://news.google.com")
        return "Opening latest news"

    # ===== PYTHON =====
    elif "python" in user:
        return "Python is a high level programming language used in AI, web development and automation."

    elif "data type" in user:
        return "Python data types include int, float, string, list, tuple and dictionary."

    elif "loop" in user:
        return "Loops repeat tasks using for and while loops."

    elif "function" in user:
        return "Function is a reusable block of code."

    elif "oops" in user:
        return "OOPS includes class, object, inheritance and polymorphism."

    elif "list" in user:
        return "List is ordered and changeable collection."

    elif "dictionary" in user:
        return "Dictionary stores data in key value pairs."

    # ===== INTERVIEW =====
    elif "interview" in user:
        return "Practice coding, revise basics and improve communication."

    elif "placement" in user:
        return "Focus on DSA, projects and aptitude."

    elif "tell me about yourself" in user:
        return "I am a computer science student with interest in programming and problem solving."

    # ===== STUDY =====
    elif "study plan" in user:
        return "Study 2 hours daily, revise and practice problems."

    elif "exam" in user:
        return "Revise topics and solve previous papers."

    # ===== CALCULATOR =====
    elif any(op in user for op in "+-*/"):
        try:
            return "Answer is " + str(eval(user))
        except:
            return "Invalid calculation"

    # ===== MUSIC =====
    elif "play song" in user:
        webbrowser.open("https://youtube.com")
        return "Playing music"

    # ===== SYSTEM =====
    elif "open notepad" in user:
        os.system("notepad")
        return "Opening Notepad"

    elif "open calculator" in user:
        os.system("calc")
        return "Opening Calculator"

    # ===== JOKE =====
    elif "joke" in user:
        return random.choice([
            "Why do programmers hate bugs? Because they are annoying!",
            "Why do coders love dark mode? Because light attracts bugs!"
        ])

    # ===== RIDDLE =====
    elif "riddle" in user:
        r = random.choice(riddles)
        riddle_answer = r[1]
        mode = "riddle"
        return r[0]

    # ===== QUIZ =====
    elif "quiz" in user:
        a = random.randint(1,10)
        b = random.randint(1,10)
        quiz_answer = a + b
        mode = "quiz"
        return f"What is {a} plus {b}?"

    # ===== EXIT =====
    elif "exit" in user:
        window.quit()

    # ===== SMART ANSWER =====
    ans = smart_answer(user)
    if ans:
        return ans

    return "I am still learning, ask something else"

# ---------- SEND ----------
def send():
    user = entry.get()
    chat.insert(tk.END, "You: " + user + "\n")

    response = process(user)
    speak(response)

    entry.delete(0, tk.END)

# ---------- VOICE ----------
def listen():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            chat.insert(tk.END, "Listening...\n")
            audio = r.listen(source)

        command = r.recognize_google(audio)
        chat.insert(tk.END, "You: " + command + "\n")

        response = process(command)
        speak(response)

    except:
        speak("Sorry, I did not understand")

# ---------- GUI ----------
window = tk.Tk()
window.title("Shruti Smart Assistant")
window.geometry("500x600")
window.configure(bg="#1e1e2f")

chat = tk.Text(window, height=25, width=60,
               bg="#1e1e1e", fg="white")
chat.pack(pady=10)

entry = tk.Entry(window, width=35,
                 bg="#2c2c2c", fg="white")
entry.pack(pady=10)

frame = tk.Frame(window, bg="#1e1e2f")
frame.pack()

tk.Button(frame, text="Send",
          command=send,
          bg="#007acc", fg="white").grid(row=0, column=0, padx=5)

tk.Button(frame, text="🎤 Speak",
          command=listen,
          bg="#0e639c", fg="white").grid(row=0, column=1, padx=5)

speak("Hello Shruti, I am your smart assistant")

window.mainloop()