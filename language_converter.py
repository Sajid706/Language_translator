import tkinter as tk
from tkinter import ttk, messagebox
from googletrans import Translator
from gtts import gTTS
import os
import speech_recognition as sr


# Initialize Google Translate
translator = Translator()

# Mapping: Native Display → Googletrans Language Code
LANGUAGE_MAP = {
    "English": "en", "Assamese": "as", "Bengali": "bn", "Bodo": "en",
    "Dogri": "en", "Gujarati": "gu", "Hindi": "hi", "Kannada": "kn",
    "Kashmiri": "en", "Konkani": "en", "Maithili": "en",
    "Malayalam": "ml", "Manipuri": "en", "Marathi": "mr",
    "Nepali": "ne", "Odia": "or", "Punjabi": "pa", "Sanskrit": "sa",
    "Santali": "en", "Sindhi": "sd", "Tamil": "ta", "Telugu": "te",
    "Urdu": "ur"
}


# gTTS language codes (fallback to English if unsupported)
TTS_LANG_CODES = {
    "en": "en", "as": "as", "bn": "bn", "gu": "gu", "hi": "hi", "kn": "kn", "ml": "ml", "mr": "mr",
    "ne": "ne", "or": "or", "pa": "pa", "sd": "sd", "ta": "ta", "te": "te", "ur": "ur", "sa": "sa"
}


# GUI setup
root = tk.Tk()
root.title("Multilingual Translator with Voice (22 Indian Languages)")
root.geometry("800x600")
root.configure(bg="white")

tk.Label(root, text="🌐 English ⇄ 22 Indian Languages Translator", font=("Segoe UI", 20, "bold"),
         fg="#1e90ff", bg="white").pack(pady=20)

LANGUAGE_LIST = list(LANGUAGE_MAP.keys())

# Language selectors
frame = tk.Frame(root, bg="white")
frame.pack()

tk.Label(frame, text="From:", font=("Segoe UI", 12), bg="white").grid(row=0, column=0, padx=10)
source_combo = ttk.Combobox(frame, values=LANGUAGE_LIST, width=30, state="readonly")
source_combo.set("हिन्दी (Hindi)")
source_combo.grid(row=0, column=1, padx=10)

tk.Label(frame, text="To:", font=("Segoe UI", 12), bg="white").grid(row=0, column=2, padx=10)
target_combo = ttk.Combobox(frame, values=LANGUAGE_LIST, width=30, state="readonly")
target_combo.set("தமிழ் (Tamil)")
target_combo.grid(row=0, column=3, padx=10)

# Input
tk.Label(root, text="📝 Enter or Speak Text:", font=("Segoe UI", 12), bg="white").pack(pady=10)
input_text = tk.Text(root, height=5, width=85, font=("Segoe UI", 11), bg="#f5f5f5", relief="solid", bd=1)
input_text.pack()

# Translate
def translate_text():
    text = input_text.get("1.0", tk.END).strip()
    src = LANGUAGE_MAP.get(source_combo.get())
    tgt = LANGUAGE_MAP.get(target_combo.get())

    if not text:
        messagebox.showwarning("Input Required", "Please enter text to translate.")
        return
    if src == tgt:
        messagebox.showinfo("Same Language", "Please choose different source and target languages.")
        return

    try:
        result = translator.translate(text, src=src, dest=tgt)
        output_text.config(state='normal')
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result.text)
        output_text.config(state='disabled')
    except Exception as e:
        messagebox.showerror("Translation Failed", str(e))

# Voice input
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            messagebox.showinfo("Voice Input", "Speak now...")
            audio = recognizer.listen(source, timeout=5)
            result = recognizer.recognize_google(audio)
            input_text.delete("1.0", tk.END)
            input_text.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("Voice Input Error", str(e))

# TTS
def speak_output():
    text = output_text.get("1.0", tk.END).strip()
    tgt_code = LANGUAGE_MAP.get(target_combo.get())
    tts_lang = TTS_LANG_CODES.get(tgt_code, "en")

    if not text:
        messagebox.showinfo("No Output", "No translated text found.")
        return
    try:
        tts = gTTS(text=text, lang=tts_lang)
        tts.save("translated.mp3")
        os.system("start translated.mp3")  # For Windows; use "afplay" on macOS or "xdg-open" on Linux
    except Exception as e:
        messagebox.showerror("TTS Error", str(e))

# Buttons
btn_frame = tk.Frame(root, bg="white")
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="🎙️ Voice Input", command=voice_input, bg="#0A6ED9", fg="white",
          font=("Segoe UI", 11), padx=10).pack(side="left", padx=10)
tk.Button(btn_frame, text="🔁 Translate", command=translate_text, bg="#0cbc35", fg="white",
          font=("Segoe UI", 11), padx=10).pack(side="left", padx=10)
tk.Button(btn_frame, text="🔊 Speak Output", command=speak_output, bg="#C93909", fg="white",
          font=("Segoe UI", 11), padx=10).pack(side="left", padx=10)

# Output
tk.Label(root, text="🌐 Translated Output:", font=("Segoe UI", 12), bg="white").pack()
output_text = tk.Text(root, height=5, width=85, font=("Segoe UI", 11),
                      bg="#f0f0f0", relief="solid", bd=1, state='disabled')
output_text.pack(pady=10)

tk.Label(root, text="✨ Powered by Sajid, Murali, Laiba",
         font=("Arial", 9), fg="#999", bg="white").pack(pady=5)

root.mainloop()
