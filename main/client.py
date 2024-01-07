import pandas as pd
import requests

def cargar_datos_desde_excel(ruta_excel):
    df = pd.read_excel(ruta_excel)

    # Visualiza el DataFrame
    print(df)

    # Procesa los datos para construir la estructura de cliente y modelos_precio
    clientes = []
    modelos_precio = []

    cliente_actual = None

    for index, row in df.iterrows():
        if pd.notna(row['Cliente']):
            # Nuevo cliente
            cliente_actual = {'nombre_cliente': row['Cliente'], 'modelos_precio': []}
            clientes.append(cliente_actual)

        if pd.notna(row['Detalle']):
            # Detalle de un modelo y su precio
            modelo_precio = (row['Detalle'], row['Valor'])
            cliente_actual['modelos_precio'].append(modelo_precio)

    return clientes

# URL de la API para generar el PDF
url_api_generar_pdf = "http://127.0.0.1:5000/generar_pdf"

# Ruta del archivo Excel
ruta_excel = 'prueba.xlsx'

# Cargar datos desde el Excel
clientes = cargar_datos_desde_excel(ruta_excel)

# Iterar sobre los clientes y enviar los datos a la API para generar el PDF
for cliente in clientes:
    # Enviar datos a la API
    response = requests.post(url_api_generar_pdf, json=cliente)

    # Verificar el estado de la respuesta
    if response.status_code == 200:
        print(f"PDF generado exitosamente para {cliente['nombre_cliente']}")
    else:
        print(f"Error al generar el PDF para {cliente['nombre_cliente']}. Estado: {response.status_code}")
        print(response.text)
