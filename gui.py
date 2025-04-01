import tkinter as tk
from tkinter import ttk, messagebox
from translator import translate_text

# Supported Languages
LANGUAGES = {
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Hindi": "hi",
    "Chinese": "zh"
}

def translate():
    """Handles text translation when the Translate button is clicked."""
    text = input_text.get("1.0", tk.END).strip()
    selected_lang = target_lang_var.get()
    target_lang = LANGUAGES.get(selected_lang, "fr")  # Default to French

    if not text:
        messagebox.showerror("Error", "Please enter text to translate.")
        return

    try:
        translated_text = translate_text(text, target_lang)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated_text)
    except Exception as e:
        messagebox.showerror("Translation Error", str(e))

def clear_text():
    """Clears the input and output text boxes."""
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)

# GUI Setup
root = tk.Tk()
root.title("Multilingual Translator")
root.geometry("550x450")
root.resizable(True, True)

# Input Text
ttk.Label(root, text="Enter Text:").pack(pady=5)
input_text = tk.Text(root, height=5, width=60)
input_text.pack(pady=5)

# Target Language Dropdown
ttk.Label(root, text="Select Target Language:").pack(pady=5)
target_lang_var = tk.StringVar(value="French")
language_dropdown = ttk.Combobox(root, textvariable=target_lang_var, values=list(LANGUAGES.keys()), state="readonly")
language_dropdown.pack(pady=5)

# Buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

translate_btn = ttk.Button(button_frame, text="Translate", command=translate)
translate_btn.grid(row=0, column=0, padx=5)

clear_btn = ttk.Button(button_frame, text="Clear", command=clear_text)
clear_btn.grid(row=0, column=1, padx=5)

# Output Text
ttk.Label(root, text="Translated Text:").pack(pady=5)
output_text = tk.Text(root, height=5, width=60)
output_text.pack(pady=5)

root.mainloop()
