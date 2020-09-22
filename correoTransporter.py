# -*- coding: utf-8 -*-
#Importación de las librerías
import smtplib, ssl
#
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEImage import MIMEImage

#estos son datos inventados para poder trabajar el archivo
predio = 'predio1'

#estos correos deberían venir en el arreglo de sys.array, se han hasta 5 correos
#rellenar el arreglo con correos para hacer la prueba
correos = ['e.navagoro@gmail.com','corellanajara@hotmail.com','alexisespinosa@reset.cl']

#este arreglo es momentaneo para probar que llegan todo tipo de archivos, están referenciados en el mismo directorio al que llega el archivo

reportes = ["document.pdf","reporte.txt","archivo.xlsx","archivo.csv"]

#Este es el arreglo con el que se trabaja que luego debería ser reemplazado por el sys.array que trae los contenidos del arreglo
#'archivo',predio,correos y reportes

arreglo = ['file',predio,correos,reportes]


asunto = "📃 Reportes - Sofía Gestión Agrícola 🍃"


body = """\
<html>
  <body>
    <div style="width:30%;margin-left:35%">
    <img src="cid:image1"/>
    </div>
    <h2 style="color:black;text-aling:center;font-size:24px">Hola,<br>
        Han llegado tu reporte automático desde Sofía Gestión Agrícola desde el Predio : """+arreglo[1]+"""
        <br>
        <a href="www.sofiagestionagricola.cl">www.sofiasgestionagricola.cl</a>
    </h2>
  </body>
</htm>
"""

#credenciales

mail_usuario = 'sofiainforma@reset.cl' #credencial de usuario
mail_destino = arreglo[2]
clave = 's0f1adoslomejorx' #credencial de contraseña

#datos del mail

mensaje = MIMEMultipart()
mensaje["Subject"] = asunto
mensaje["From"] = mail_usuario
mensaje["To"] = ", ".join(mail_destino)

#inserta el body tipo html

mensaje.attach(MIMEText(body, "html"))

#busca la imagen y la lee
fp = open('correo.png', 'rb')
mensajeImagen = MIMEImage(fp.read())
fp.close()

# Define el id de la imagen
mensajeImagen.add_header('Content-ID', '<image1>')
#inserta la imagen
mensaje.attach(mensajeImagen)

nombreArchivos = arreglo[3] # estos archivos están en el mismo directorio de el archivo

#recorre los archivos, los lee y los adjunta al correo

for archivo in nombreArchivos:
    print(archivo)
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(archivo, 'rb').read())
    encoders.encode_base64(part)
    mensaje.attach(part)
    part.add_header('Content-Disposition', 'attachment', filename=archivo)

#este recibe el contenenido del mensaje como cadena

text = mensaje.as_string()

#se logea y manda

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(mail_usuario, clave)
    server.sendmail(
        mail_usuario, mail_destino, text
    )
    server.close()

    print 'Correo Enviado'
except:
    print 'Ha ocurrido un error al enviar el correo...'
