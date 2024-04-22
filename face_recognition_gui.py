import cv2
import time
import requests
from pymongo import MongoClient
import serial
import tkinter as tk
from tkinter import filedialog

def main():
    def insert_document(response, age):
        uri = "mongodb+srv://efrenalvarez:T.6gqWaF!Kv!MJq@cluster0.5jyeskn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = MongoClient(uri)
        db = client.get_database('VidaVerde')
        collection = db['datos']
        document = {'response': response, 'age': age}
        collection.insert_one(document)
        client.close()

    def age_detection(filename):
        with open(filename, 'rb') as file:
            data = {'data': file}
            response = requests.post('https://api.everypixel.com/v1/faces', files=data, auth=(client_id, client_secret)).json()

        if response['status'] == 'ok':
            for face in response['faces']:
                age = face['age']
                print(f"Estimated age: {age}")
                if age < 30:
                    print("Underage ")
                    message = f'Hay una persona en su cocina que parece que tiene {age} años'
                    send_discord_message(message, filename)
                    insert_document(response, age)
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
            requests.post(webhook_url, data={'content': message})

    def detect_person():
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
            global frame_count
            frame_count += 1
            filename = f"captured_image_{frame_count}.jpg"
            cv2.imwrite(filename, frame)
            age_detection(filename)
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            if line == '¡Humo o gas detectado!':
                send_discord_message("¡Humo o gas detectado!", None)
        root.after(2000, detect_person)

    def run_program():
        global ser
        ser = serial.Serial('COM11', 9600)  # Replace 'COM3' with the appropriate port name
        detect_person()

    # Create GUI
    root = tk.Tk()
    root.title("Person Detection")
    root.geometry("400x100")

    run_button = tk.Button(root, text="Empezar la protección de mi cocina", command=run_program)
    run_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
