# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS 
from pdf_generator import generar_pdf

app = Flask(__name__)
CORS(app)
@app.route('/generar_pdf', methods=['POST'])
def generar_pdf_api():
    try:
        # Obtener datos del cuerpo de la solicitud POST en formato JSON
        data = request.get_json()

        # Extraer información del cliente y los modelos y precios
        nombre_cliente = data.get('nombre_cliente')
        modelos_precio = data.get('modelos_precio')

        # Generar el PDF
        generar_pdf(nombre_cliente, modelos_precio)

        return jsonify({'mensaje': 'PDF generado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
