import cv2
import time
import numpy as np
import requests
import json
import pywhatkit
from pymongo import MongoClient

# DB Connection
def insert_document(response, age):
    # Cadena de conexión obtenida desde MongoDB Atlas
    # Reemplaza <username>, <password> y <dbname> con tus propios valores
    # También puedes necesitar cambiar el host y el puerto dependiendo de tu configuración
    uri = "mongodb+srv://efrenalvarez:T.6gqWaF!Kv!MJq@cluster0.5jyeskn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    # Crea una instancia del cliente MongoClient
    client = MongoClient(uri)

    # Accede a la base de datos
    db = client.get_database('VidaVerde')

    # Accede a la colección donde deseas insertar el documento
    collection = db['datos']

    # Crea el documento a insertar
    document = {
        'response': response,
        'age': age
    }

    # Inserta el documento en la colección
    collection.insert_one(document)

    # Cierra la conexión
    client.close()


# End DB Connection


client_id = 'hkRmyxdbrq4y84fjmUOFR0UD'
client_secret = '40UggdZZNOa8E2pKvLEuEETQoXDZkjOMw0iFtwZ3Ii2a3sDs'

net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel")

cap = cv2.VideoCapture(0) 

def age_detection(img):
    
    params = {'url': 'https://labs.everypixel.com/static/i/estest_sample3.jpg'}
    response = requests.get('https://api.everypixel.com/v1/faces', params=params, auth=(client_id, client_secret)).json()
    
    print(response)
    if response['status'] == 'ok':
        for face in response['faces']:
            age = face['age']
            print(f"Estimated age: {age}")
            insert_document(response, age)
            # wa_messege()

    else:
        print("No faces detected.")

frame_count = 0

def wa_messege():
    try:
    
        # sending message to receiver
        # using pywhatkit
        pywhatkit.sendwhatmsg("+5213326176382", 
                                "alerta de incendio", 
                                1, 1)
        print("Successfully Sent!")
        
    except:
    
        # handling exception 
        # and printing error message
        print("An Unexpected Error!")

while True:
    ret, frame = cap.read()


    resized_frame = cv2.resize(frame, (300, 300))

    blob = cv2.dnn.blobFromImage(resized_frame, 1.0, (300, 300), (104.0, 177.0, 123.0))

    net.setInput(blob)

    detections = net.forward()

    person_detected = False
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5: 
            person_detected = True
            break

    if person_detected:
        print("Person detected in the image!")
        frame_count += 1
        filename = f"captured_image_{frame_count}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Image saved as {filename}")
        age_detection(resized_frame)
        # wa_messege()
    else:
        print("No person detected in the image.")

        

    time.sleep(5)


