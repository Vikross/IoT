import tkinter as tk
import random
import time
import threading

class SmartLampApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Умная Лампочка")

        self.light_level = 100
        self.is_lamp_on = False
        self.auto_mode = False
        self.light_threshold = 50
        self.update_interval = 10

        self.light_level_label = tk.Label(root, text=f"Уровень освещенности: {self.light_level}%", font=("Arial", 14))
        self.light_level_label.pack()

        self.lamp_status_label = tk.Label(root, text="Лампочка выключена", font=("Arial", 14))
        self.lamp_status_label.pack()

        self.toggle_button = tk.Button(root, text="Включить/Выключить вручную", command=self.toggle_lamp, font=("Arial", 12))
        self.toggle_button.pack()

        self.auto_button = tk.Button(root, text="Переключить в автоматический режим", command=self.toggle_auto_mode, font=("Arial", 12))
        self.auto_button.pack()

        self.update_data()

    def toggle_lamp(self):
        if not self.auto_mode:
            self.is_lamp_on = not self.is_lamp_on
            self.update_lamp_status()

    def toggle_auto_mode(self):
        self.auto_mode = not self.auto_mode
        if self.auto_mode:
            self.auto_button.config(text="Автоматический режим включен")
        else:
            self.auto_button.config(text="Переключить в автоматический режим")

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
            elif self.light_level >= self.light_threshold and self.is_lamp_on:
                self.is_lamp_on = False
                self.update_lamp_status()

        self.light_level = random.randint(0, 100)
        self.light_level_label.config(text=f"Уровень освещенности: {self.light_level}%")

        self.root.after(self.update_interval * 1000, self.update_data)

def run_app():
    root = tk.Tk()
    app = SmartLampApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_app()
