#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk

def show_popup():
    # Crear ventana emergente
    popup = tk.Toplevel()
    popup.title("Saludo")
    popup.geometry("200x80")
    popup.resizable(False, False)

    # Etiqueta
    label = ttk.Label(popup, text="Hi World", font=("Helvetica", 16))
    label.pack(expand=True)

    # Botón para cerrar
    ttk.Button(popup, text="OK", command=popup.destroy).pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()          # ocultar ventana principal
    show_popup()
    root.mainloop()