import tkinter as tk
from tkinter import ttk, messagebox
import requests

def llamar_api_generar_pdf():
    # Obtener datos de la interfaz gráfica
    nombre_cliente = entry_cliente.get()

    # Verificar que se haya ingresado el nombre del cliente
    if not nombre_cliente:
        messagebox.showerror("Error", "Por favor, ingrese el nombre del cliente.")
        return

    # Construir la estructura de datos para enviar a la API
    cliente = {
        "nombre_cliente": nombre_cliente,
        "modelos_precio": []
    }

    # Recorrer los elementos en el Treeview y agregarlos a la estructura de datos
    for item in treeview.get_children():
        detalle = treeview.item(item, "values")[0]
        valor = treeview.item(item, "values")[1]
        cliente["modelos_precio"].append((detalle, int(valor)))

    # URL de la API para generar el PDF
    url_api_generar_pdf = "http://127.0.0.1:5000/generar_pdf"

    # Enviar datos a la API
    try:
        response = requests.post(url_api_generar_pdf, json=cliente)
        response.raise_for_status()

        messagebox.showinfo("Éxito", f"PDF generado exitosamente para {nombre_cliente}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error al llamar a la API: {e}")

def agregar_item():
    # Obtener detalle y valor ingresados
    detalle = entry_detalle.get()
    valor = entry_valor.get()

    # Verificar que se hayan ingresado ambos campos
    if not detalle or not valor:
        messagebox.showerror("Error", "Por favor, ingrese tanto el detalle como el valor.")
        return

    # Agregar elemento al Treeview
    treeview.insert("", "end", values=(detalle, valor))

    # Limpiar campos de entrada después de agregar el elemento
    entry_detalle.delete(0, "end")
    entry_valor.delete(0, "end")

# Crear la interfaz gráfica
app = tk.Tk()
app.title("Generador de PDF")

# Componentes de la interfaz gráfica
label_cliente = tk.Label(app, text="Nombre del Cliente:")
entry_cliente = tk.Entry(app)

# Botones y campos de entrada para agregar elementos a la grilla
label_detalle = tk.Label(app, text="Detalle:")
entry_detalle = tk.Entry(app)

label_valor = tk.Label(app, text="Valor:")
entry_valor = tk.Entry(app)

button_agregar = tk.Button(app, text="Agregar", command=agregar_item)
button_generar_pdf = tk.Button(app, text="Generar PDF", command=llamar_api_generar_pdf)

# Treeview para mostrar la grilla de cotización
treeview = ttk.Treeview(app, columns=("Detalle", "Valor"), show="headings", height=5)
treeview.heading("Detalle", text="Detalle")
treeview.heading("Valor", text="Valor")

# Posicionamiento de los componentes en la interfaz gráfica
label_cliente.grid(row=0, column=0, sticky="e")
entry_cliente.grid(row=0, column=1)

label_detalle.grid(row=1, column=0, sticky="e")
entry_detalle.grid(row=1, column=1)

label_valor.grid(row=2, column=0, sticky="e")
entry_valor.grid(row=2, column=1)

button_agregar.grid(row=3, column=0, pady=10)
button_generar_pdf.grid(row=3, column=1, pady=10)

treeview.grid(row=4, column=0, columnspan=2, pady=10)

# Iniciar la aplicación
app.mainloop()
