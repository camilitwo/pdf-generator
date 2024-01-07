import pdfkit
import locale
from datetime import datetime, timedelta

def formatear_pesos_chilenos(valor):
    locale.setlocale(locale.LC_ALL, '')
    return locale.format('%.0f', valor, grouping=True, monetary=True)

def generar_pdf(nombre_cliente, modelo_aire_precio):
    logo_url = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
    logo_on_right = True
    nombreE = "Empresa Nombre"

    bruto = sum(precio for _, precio in modelo_aire_precio)
    bruto_formateado = '$' + formatear_pesos_chilenos(bruto)
    total_con_iva = bruto * 1.19
    total_con_iva_formateado = '$' + formatear_pesos_chilenos(total_con_iva)

    # Obtener la fecha actual y calcular la fecha de vencimiento (30 días)
    sysdate = datetime.now().strftime('%d/%m/%Y')
    fecha_vencimiento = (datetime.now() + timedelta(days=30)).strftime('%d/%m/%Y')

    # Crear el contenido HTML
    contenido_html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                background-color: #f5f5f5;
                color: #333;
                margin: 20px;
            }}

            h1 {{
                color: #3498db;
            }}

            table {{
                border-collapse: collapse;
                width: 100%;
                margin-top: 20px;
            }}

            th, td {{
                border: 1px solid #ddd;
                padding: 10px;
                text-align: left;
            }}

            th {{
                background-color: #3498db;
                color: white;
            }}

            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}

            tr:hover {{
                background-color: #ddd;
            }}
                .logo-container {{
                display: flex;
                align-items: center;  
            }}

            .subtotal-table {{
                border-collapse: collapse;
                width: 30%;
                margin-top: 20px;
            }}

            .subtotal-table th, .subtotal-table td {{
                border: 1px solid #ddd;
                padding: 10px;
            }}

            .suma-total {{
                font-weight: bold;
                text-align: left;
            }}
            table.logo-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        table.logo-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
            border: none;  /* Elimina el borde de la tabla */
        }}

        table.logo-table td {{
            text-align: {"right" if logo_on_right else "left"};
            border: none;  /* Elimina el borde de las celdas */
        }}

        .logo {{
            max-width: 100px;
            max-height: 100px;
             float: right; 
        }}

        h2 {{
            margin: 0;  /* Elimina el margen del encabezado h2 */
        }}
        .nombre-empresa {{
            text-align: left;
            float: left;
        }}

        /* Estilo para el footer */
        .footer {{
            margin-top: 300px;
            text-align: center;
            font-size: 12px;
        }}
        </style>
    </head>
    <body>
       <table class="logo-table">
        <tr>
            <td class="nombre-empresa!important"><h2>{nombreE}</h2></td>
            <td><img src="{logo_url}" alt="Logo de la empresa" class="logo"></td>
        </tr>
    </table>
        <h3>Factura para {nombre_cliente}</h3>
        <p>Fecha: {sysdate}</p>
        <br><br><br>
        <p>Estimado(a) {nombre_cliente}, adjuntamos la cotización solicitada.</p>
        <p>Atentamente,</p>
        <p>{nombreE}</p>
        <br><br><br>
        <!-- Contenedor de las tablas -->
        <div>
            <!-- Tabla de detalles de cotización -->
            <table>
                <tr>
                    <th>Detalle Cotización</th>
                    <th>Precio</th>
                </tr>
                {''.join(f"<tr><td>{modelo}</td><td>${formatear_pesos_chilenos(precio)}</td></tr>" for modelo, precio in modelo_aire_precio)}
            </table>
            
            <!-- Tabla de totales -->
            <table class="subtotal-table" style="float: right; margin-top: 20px;">
                <tr class="suma-total">
                    <td colspan="2">Bruto:</td>
                    <td style="text-align: right;">{bruto_formateado}</td>
                </tr>
                <tr class="suma-total">
                    <td colspan="2">Total con IVA (19%):</td>
                    <td style="text-align: right;">{total_con_iva_formateado}</td>
                </tr>
            </table>
        </div>
        
        <!-- Footer con la fecha de vencimiento -->
        <div class="footer">
            Esta factura tendrá vigencia hasta el {fecha_vencimiento}
        </div>
    </body>
    </html>
    """

    # Guardar el contenido HTML en un archivo
    archivo_html = f"{nombre_cliente}_factura.html"
    with open(archivo_html, "w", encoding="utf-8") as file:
        file.write(contenido_html)

    # Generar el PDF desde el contenido HTML
    pdf_output = f"{nombre_cliente}_factura.pdf"
    pdfkit.from_file(archivo_html, pdf_output)

    print(f"PDF generado exitosamente: {pdf_output}")

    send_email(archivo_html, pdf_output)

# Ejemplo de uso:
#cliente = "Juan Pérez"
#modelos_precio = [("Modelo1", 500), ("Modelo2", 470000), ("Modelo3", 900600)]

#generar_pdf(cliente, modelos_precio)

def send_email(archivo_html, pdf_output):
    import resend
    import html2text
    import base64

    with open(archivo_html, 'r', encoding='utf-8') as file:
        contenido_html = file.read()

    contenido_texto = html2text.html2text(contenido_html)

    with open(pdf_output, 'rb') as pdf_file:
        pdf_content = pdf_file.read()

    pdf_base64 = base64.b64encode(pdf_content).decode("utf-8")

    print('Enviando email')
    resend.api_key = "re_SNBRPBR6_J5CPjRzadLJXa3AVPuu1836D"

    r = resend.Emails.send({
    "from": "onboarding@resend.dev",
    "to": "camilo.igv@gmail.com",
    "subject": "Cotización Aire Acondicionado",
    "html": contenido_html,
    "attachments": [
        {
            "filename": "Cotización.pdf",  # Nombre del archivo adjunto
            "content": pdf_base64,          # Contenido del archivo adjunto
        }
    ]
    })

    print(r.status_code)

