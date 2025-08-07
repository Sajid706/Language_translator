import tkinter as tk
from tkinter import ttk, messagebox
from transformers import MarianMTModel, MarianTokenizer
from gtts import gTTS
import os
import speech_recognition as sr
import torch

# Language pairs supported by Hugging Face models
LANGUAGE_MODELS = {
    ("English", "Hindi"): "Helsinki-NLP/opus-mt-en-hi",
    ("Hindi", "English"): "Helsinki-NLP/opus-mt-hi-en",
    ("English", "Bengali"): "Helsinki-NLP/opus-mt-en-bn",
    ("Bengali", "English"): "Helsinki-NLP/opus-mt-bn-en",
    ("English", "Tamil"): "Helsinki-NLP/opus-mt-en-ta",
    ("Tamil", "English"): "Helsinki-NLP/opus-mt-ta-en",
    ("English", "Telugu"): "Helsinki-NLP/opus-mt-en-te",
    ("Telugu", "English"): "Helsinki-NLP/opus-mt-te-en",
    ("English", "Malayalam"): "Helsinki-NLP/opus-mt-en-ml",
    ("Malayalam", "English"): "Helsinki-NLP/opus-mt-ml-en",
    ("English", "Gujarati"): "Helsinki-NLP/opus-mt-en-gu",
    ("Gujarati", "English"): "Helsinki-NLP/opus-mt-gu-en",
    ("English", "Marathi"): "Helsinki-NLP/opus-mt-en-mr",
    ("Marathi", "English"): "Helsinki-NLP/opus-mt-mr-en",
    ("English", "Kannada"): "Helsinki-NLP/opus-mt-en-kn",
    ("Kannada", "English"): "Helsinki-NLP/opus-mt-kn-en",
    ("English", "Punjabi"): "Helsinki-NLP/opus-mt-en-pa",
    ("Punjabi", "English"): "Helsinki-NLP/opus-mt-pa-en",
    ("English", "Oriya"): "Helsinki-NLP/opus-mt-en-or",
    ("Oriya", "English"): "Helsinki-NLP/opus-mt-or-en",
    ("English", "Urdu"): "Helsinki-NLP/opus-mt-en-ur",
    ("Urdu", "English"): "Helsinki-NLP/opus-mt-ur-en",
    ("English", "Assamese"): "Helsinki-NLP/opus-mt-en-as",
    ("Assamese", "English"): "Helsinki-NLP/opus-mt-as-en",
}

model_cache = {}

def load_model(src, tgt):
    key = (src, tgt)
    if key in model_cache:
        return model_cache[key]
    model_name = LANGUAGE_MODELS.get(key)
    if not model_name:
        raise ValueError(f"Translation model not available for {src} to {tgt}")
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    model_cache[key] = (tokenizer, model)
    return tokenizer, model

def translate_text():
    text = input_text.get("1.0", tk.END).strip()
    src = source_combo.get()
    tgt = target_combo.get()

    if not text:
        messagebox.showwarning("Input Required", "Please enter text to translate.")
        return
    if src == tgt:
        messagebox.showinfo("Same Language", "Please choose different source and target languages.")
        return

    try:
        tokenizer, model = load_model(src, tgt)
        batch = tokenizer.prepare_seq2seq_batch([text], return_tensors="pt", padding=True)
        with torch.no_grad():
            translated = model.generate(**batch)
        output = tokenizer.decode(translated[0], skip_special_tokens=True)
        output_text.config(state='normal')
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, output)
        output_text.config(state='disabled')
    except Exception as e:
        messagebox.showerror("Translation Failed", str(e))

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

def speak_output():
    text = output_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showinfo("No Output", "No translated text found.")
        return
    try:
        tts = gTTS(text=text, lang='en')
        tts.save("translated.mp3")
        os.system("start translated.mp3")
    except Exception as e:
        messagebox.showerror("TTS Error", str(e))

# GUI setup
root = tk.Tk()
root.title("Multilingual Translator with Voice")
root.geometry("800x600")
root.configure(bg="white")

tk.Label(root, text="🌐 English ⇄ Indian Languages Translator", font=("Segoe UI", 20, "bold"),
         fg="#1e90ff", bg="white").pack(pady=20)

# Language selectors
frame = tk.Frame(root, bg="white")
frame.pack()

tk.Label(frame, text="From:", font=("Segoe UI", 12), bg="white").grid(row=0, column=0, padx=10)
source_combo = ttk.Combobox(frame, values=sorted(set([a for a, _ in LANGUAGE_MODELS.keys()])), width=20, state="readonly")
source_combo.set("English")
source_combo.grid(row=0, column=1, padx=10)

tk.Label(frame, text="To:", font=("Segoe UI", 12), bg="white").grid(row=0, column=2, padx=10)
target_combo = ttk.Combobox(frame, values=sorted(set([b for _, b in LANGUAGE_MODELS.keys()])), width=20, state="readonly")
target_combo.set("Hindi")
target_combo.grid(row=0, column=3, padx=10)

# Input
tk.Label(root, text="📝 Enter or Speak Text:", font=("Segoe UI", 12), bg="white").pack(pady=10)
input_text = tk.Text(root, height=5, width=85, font=("Segoe UI", 11), bg="#f5f5f5", relief="solid", bd=1)
input_text.pack()

# Buttons
btn_frame = tk.Frame(root, bg="white")
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="🎙️ Voice Input", command=voice_input, bg="#007bff", fg="white",
          font=("Segoe UI", 11), padx=10).pack(side="left", padx=10)
tk.Button(btn_frame, text="🔁 Translate", command=translate_text, bg="#28a745", fg="white",
          font=("Segoe UI", 11), padx=10).pack(side="left", padx=10)
tk.Button(btn_frame, text="🔊 Speak Output", command=speak_output, bg="#ff5722", fg="white",
          font=("Segoe UI", 11), padx=10).pack(side="left", padx=10)

# Output
tk.Label(root, text="🌐 Translated Output:", font=("Segoe UI", 12), bg="white").pack()
output_text = tk.Text(root, height=5, width=85, font=("Segoe UI", 11), bg="#f0f0f0", relief="solid", bd=1, state="disabled")
output_text.pack(pady=10)

tk.Label(root, text="✨ Powered by Hugging Face & Google", font=("Arial", 9), fg="#999", bg="white").pack(pady=5)

root.mainloop()
