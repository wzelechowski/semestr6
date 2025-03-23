import tkinter as tk
from tkinter import filedialog, messagebox
import json
import converter as conv


def save_settings():
    settings = {
        "space": float(entry_spacing.get()),
        "align": alignment_var.get(),
        "header_b": headers_b_val.get(),
        "header_i": headers_i_val.get(),
        "value_b": value_b_val.get(),
        "value_i": value_i_val.get(),
        "page_num": page_num_val.get(),
        "format": format_val.get(),
    }
    with open("settings.txt", "w") as file:
        json.dump(settings, file)
    messagebox.showinfo("Info", "Ustawienia zostały zapisane")


def load_settings():
    try:
        with open("settings.txt", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None


def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    entry_file.delete(0, tk.END)
    entry_file.insert(0, file_path)


def docx_loc():
    docx_output = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word Files", "*.docx")])
    entry_docx_out.delete(0, tk.END)
    entry_docx_out.insert(0, docx_output)


def pdf_loc():
    pdf_output = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    entry_pdf_out.delete(0, tk.END)
    entry_pdf_out.insert(0, pdf_output)


def convert():
    file_path = entry_file.get()
    docx_out = entry_docx_out.get()
    pdf_out = entry_pdf_out.get()
    title = entry_title.get()
    space = float(entry_spacing.get())
    align = alignment_var.get()
    header_b = headers_b_val.get()
    header_i = headers_i_val.get()
    value_b = value_b_val.get()
    value_i = value_i_val.get()
    page_num = page_num_val.get()
    format = format_val.get()

    if not file_path or not docx_out or not pdf_out or not title:
        messagebox.showwarning("Info", "Wybierz plik, podaj tytuł oraz lokalizacje zapisu DOCX i PDF!")
        return

    conv.convert_excel(file_path, docx_out, pdf_out, title, space, align, header_b, header_i,
                 value_b, value_i, page_num, format)
    messagebox.showinfo("Info", "Konwersja zakończona!")


canva = tk.Tk()
canva.title("Excel Converter")

settings = load_settings()

tk.Label(canva, text="Plik do konwersji:").pack()
entry_file = tk.Entry(canva, width=50)
entry_file.pack()
tk.Button(canva, text="Wybierz", command=select_file).pack()

tk.Label(canva, text="Tytuł dokumentu:").pack()
entry_title = tk.Entry(canva, width=50)
entry_title.pack()

tk.Label(canva, text="Odstępy:").pack()
entry_spacing = tk.Entry(canva, width=10)
entry_spacing.pack()
entry_spacing.insert(0, str(settings["space"]) if settings else "10")

tk.Label(canva, text="Rozmieszczenie tekstu:").pack()
alignment_var = tk.StringVar(value=settings["align"] if settings else "Wyrównaj do lewej")
tk.OptionMenu(canva, alignment_var, "Wyrównaj do lewej", "Wyśrodkowany", "Wyrównaj do prawej").pack()

headers_b_val = tk.BooleanVar(value=settings["header_b"] if settings else True)
headers_i_val = tk.BooleanVar(value=settings["header_i"] if settings else False)
value_b_val = tk.BooleanVar(value=settings["value_b"] if settings else False)
value_i_val = tk.BooleanVar(value=settings["value_i"] if settings else False)
page_num_val = tk.BooleanVar(value=settings["page_num"] if settings else True)

tk.Checkbutton(canva, text="Pogrubienie nagłówków", variable=headers_b_val).pack()
tk.Checkbutton(canva, text="Kursywa nagłówków", variable=headers_i_val).pack()
tk.Checkbutton(canva, text="Pogrubienie zawartości komórek", variable=value_b_val).pack()
tk.Checkbutton(canva, text="Kursywa zawartości komórek", variable=value_i_val).pack()
tk.Checkbutton(canva, text="Numeracja stron", variable=page_num_val).pack()

format_val = tk.StringVar(value=settings["format"] if settings else "lines")
tk.Label(canva, text="Format wyjściowy:").pack()
tk.Radiobutton(canva, text="nagłówkek: treść", variable=format_val, value="lines").pack()
tk.Radiobutton(canva, text="Tabela", variable=format_val, value="table").pack()

tk.Label(canva, text="Lokalizacja pliku DOCX:").pack()
entry_docx_out = tk.Entry(canva, width=50)
entry_docx_out.pack()
tk.Button(canva, text="Wybierz", command=docx_loc).pack()

tk.Label(canva, text="Lokalizacja pliku PDF:").pack()
entry_pdf_out = tk.Entry(canva, width=50)
entry_pdf_out.pack()
tk.Button(canva, text="Wybierz", command=pdf_loc).pack()

tk.Button(canva, text="Zapisz ustawienia", command=save_settings).pack()

tk.Button(canva, text="Konwertuj", command=convert).pack()

canva.mainloop()