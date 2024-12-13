import tkinter as tk
import random
import time
import paho.mqtt.client as mqtt
import threading
import json

class SmartLampApp:
    def __init__(self, root, broker="test.mosquitto.org"):
        self.root = root
        self.root.title("Умная Лампочка")

        self.light_level = 100
        self.is_lamp_on = False
        self.auto_mode = False
        self.light_threshold = 50
        self.update_interval = 10

        self.broker = broker
        self.port = 1883
        self.client = mqtt.Client()

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()

        self.client.subscribe("smartlamp/commands")
        self.client.subscribe("smartlamp/sensors")

        self.light_level_label = tk.Label(root, text=f"Уровень освещенности: {self.light_level}%", font=("Arial", 14))
        self.light_level_label.pack()

        self.lamp_status_label = tk.Label(root, text="Лампочка выключена", font=("Arial", 14))
        self.lamp_status_label.pack()

        self.toggle_button = tk.Button(root, text="Включить/Выключить вручную", command=self.toggle_lamp, font=("Arial", 12))
        self.toggle_button.pack()

        self.auto_button = tk.Button(root, text="Переключить в автоматический режим", command=self.toggle_auto_mode, font=("Arial", 12))
        self.auto_button.pack()

        self.update_data()

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        topic = msg.topic

        if topic == "smartlamp/commands":
            self.process_commands(message)
        elif topic == "smartlamp/sensors":
            self.process_sensors(message)

    def process_commands(self, message):
        if message == "manual":
            self.auto_mode = False
            self.auto_button.config(text="Автоматический режим выключен")
        elif message == "auto":
            self.auto_mode = True
            self.auto_button.config(text="Автоматический режим включен")
        elif message == "lamp_on":
            self.is_lamp_on = True
            self.update_lamp_status()
        elif message == "lamp_off":
            self.is_lamp_on = False
            self.update_lamp_status()

    def process_sensors(self, message):
        try:
            sensor_data = json.loads(message)
            self.light_level = sensor_data.get('light_level', self.light_level)
            self.light_level_label.config(text=f"Уровень освещенности: {self.light_level}%")
        except Exception as e:
            print(f"Ошибка обработки данных сенсора: {e}")

    def toggle_lamp(self):
        if not self.auto_mode:
            self.is_lamp_on = not self.is_lamp_on
            self.update_lamp_status()
            self.client.publish("smartlamp/commands", "lamp_on" if self.is_lamp_on else "lamp_off")

    def toggle_auto_mode(self):
        if self.auto_mode:
            self.auto_mode = False
            self.client.publish("smartlamp/commands", "manual")
        else:
            self.auto_mode = True
            self.client.publish("smartlamp/commands", "auto")

    def update_lamp_status(self):
        if self.is_lamp_on:
            self.lamp_status_label.config(text="Лампочка включена")
        else:
            self.lamp_status_label.config(text="Лампочка выключена")

    def update_data(self):
        if self.auto_mode:
            if self.light_level < self.light_threshold and not self.is_lamp_on:
                self.is_lamp_on = True
                self.update_lamp_status()
                self.client.publish("smartlamp/commands", "lamp_on")
            elif self.light_level >= self.light_threshold and self.is_lamp_on:
                self.is_lamp_on = False
                self.update_lamp_status()
                self.client.publish("smartlamp/commands", "lamp_off")

        self.light_level = random.randint(0, 100)
        self.client.publish("smartlamp/sensors", json.dumps({"light_level": self.light_level}))

        self.root.after(self.update_interval * 1000, self.update_data)

def run_app():
    root = tk.Tk()
    app = SmartLampApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_app()