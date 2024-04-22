import cv2
import time
import requests
from pymongo import MongoClient
import serial
from datetime import datetime

ser = serial.Serial('COM11', 9600)  # Replace 'COM3' with the appropriate port name

# DB Connection
def insert_document(response, age, timestamp):
    uri = "mongodb+srv://efrenalvarez:T.6gqWaF!Kv!MJq@cluster0.5jyeskn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri)
    db = client.get_database('VidaVerde')
    collection = db['datos']
    document = {
        'response': response,
        'age': age,
        'timestamp': timestamp
    }
    print(document)
    collection.insert_one(document)
    client.close()

# End DB Connection
client_id = 'hkRmyxdbrq4y84fjmUOFR0UD'
client_secret = '40UggdZZNOa8E2pKvLEuEETQoXDZkjOMw0iFtwZ3Ii2a3sDs'
net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel")
cap = cv2.VideoCapture(0)
frame_count = 0

def age_detection(filename):
    with open(filename, 'rb') as file:
        data = {'data': file}
        response = requests.post('https://api.everypixel.com/v1/faces', files=data, auth=(client_id, client_secret)).json()

    if response['status'] == 'ok':
        for face in response['faces']:
            age = face['age']
            print(f"Estimated age: {age}")
            if age < 30:
                print("underage")
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                message = f'hay una persona en su cocina que parece que tiene {age} años'
                send_discord_message(message, filename)
                insert_document(response, age, timestamp)
    else:
        print("No faces detected.")

def send_discord_message(log, filename):
    webhook_url = 'https://discord.com/api/webhooks/1200638486273855539/Jx7HvbY_NM0hNymd_lxzOGcSGF2-Ro2EkGx2kJid2624PEuY7DqTtOS_8Z8FdZDNzv61'

    print('here')
    message = f"""
    {log}
    @here
    """
    if filename:
        with open(filename, 'rb') as file:
            files = {'file': file}
            payload = {'content': message}
            requests.post(webhook_url, data=payload, files=files)
    else:
        requests.post(webhook_url, json={'content': message})

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
        age_detection(filename)
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        if line == '¡Humo o gas detectado!':
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            send_discord_message(f"¡Humo o gas detectado! - {timestamp}", None)
            insert_document('fire incident', None, timestamp)
    time.sleep(2)
