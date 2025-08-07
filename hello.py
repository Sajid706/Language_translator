import tkinter as tk
from tkinter import ttk, messagebox
from transformers import MarianMTModel, MarianTokenizer
import torch

# --- Supported Language Models ---
LANGUAGE_MODELS = {
    "Hindi": "Helsinki-NLP/opus-mt-en-hi",
    "Bengali": "Helsinki-NLP/opus-mt-en-bn",
    "Tamil": "Helsinki-NLP/opus-mt-en-ta",
    "Malayalam": "Helsinki-NLP/opus-mt-en-ml",
    "Telugu": "Helsinki-NLP/opus-mt-en-te"
}

# --- Model Cache for Faster Switching ---
model_cache = {}

def load_model(lang):
    if lang in model_cache:
        return model_cache[lang]
    model_name = LANGUAGE_MODELS[lang]
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    model_cache[lang] = (tokenizer, model)
    return tokenizer, model

def translate_text():
    english_text = input_text.get("1.0", tk.END).strip()
    selected_lang = lang_combo.get()

    if not english_text:
        messagebox.showwarning("Input Needed", "Please enter an English sentence.")
        return
    if selected_lang not in LANGUAGE_MODELS:
        messagebox.showwarning("Language Needed", "Please select a target language.")
        return

    try:
        tokenizer, model = load_model(selected_lang)
        batch = tokenizer.prepare_seq2seq_batch([english_text], return_tensors='pt', padding=True)
        with torch.no_grad():
            translated = model.generate(**batch)
        translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)

        output_text.config(state='normal')
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated_text)
        output_text.config(state='disabled')

    except Exception as e:
        messagebox.showerror("Translation Error", str(e))

# --- Hover effect ---
def on_enter(e):
    translate_btn.config(bg="#1e90ff", fg="white")

def on_leave(e):
    translate_btn.config(bg="#f0f0f0", fg="#000")

# --- GUI Setup ---
root = tk.Tk()
root.title("🌍 English to Indian Language Translator")
root.geometry("700x530")
root.configure(bg="white")
root.resizable(False, False)

# --- Fonts ---
HEADER_FONT = ("Segoe UI", 20, "bold")
LABEL_FONT = ("Segoe UI", 12)
TEXT_FONT = ("Segoe UI", 11)

# --- Header ---
tk.Label(root, text="🌐 English → Indian Language Translator", font=HEADER_FONT,
         bg="white", fg="#1e90ff").pack(pady=20)

# --- Language Dropdown ---
tk.Label(root, text="Choose Target Language:", font=LABEL_FONT,
         bg="white", fg="black").pack()
lang_combo = ttk.Combobox(root, values=list(LANGUAGE_MODELS.keys()), state="readonly",
                          font=LABEL_FONT, width=25)
lang_combo.set("Hindi")
lang_combo.pack(pady=10)

# --- Input Area ---
tk.Label(root, text="Enter English Sentence:", font=LABEL_FONT,
         bg="white", fg="black").pack()
input_text = tk.Text(root, height=5, width=70, font=TEXT_FONT,
                     bg="#f8f8f8", fg="#000", insertbackground='black',
                     bd=1, relief='solid')
input_text.pack(pady=10)

# --- Translate Button ---
translate_btn = tk.Button(root, text="🔁 Translate", command=translate_text,
                          font=LABEL_FONT, bg="#f0f0f0", fg="#000",
                          activebackground="#1e90ff", activeforeground="white",
                          padx=20, pady=6, relief="flat", bd=1, cursor="hand2")
translate_btn.pack(pady=15)
translate_btn.bind("<Enter>", on_enter)
translate_btn.bind("<Leave>", on_leave)

# --- Output Area ---
tk.Label(root, text="Translation Output:", font=LABEL_FONT,
         bg="white", fg="black").pack()
output_text = tk.Text(root, height=5, width=70, font=TEXT_FONT,
                      bg="#f8f8f8", fg="green", bd=1, relief='solid', state='disabled')
output_text.pack(pady=10)

# --- Footer ---
tk.Label(root, text="✨ Powered by Hugging Face | Built with ❤️", font=("Arial", 9),
         bg="white", fg="#999").pack(pady=5)

# --- Start GUI ---
root.mainloop()
