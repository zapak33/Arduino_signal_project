import serial
import tkinter as tk

# Replace with your correct COM port (e.g., 'COM4', '/dev/ttyUSB0')
arduino = serial.Serial('COM5', 9600)  # <-- Update this if needed

# GUI setup
root = tk.Tk()
root.title("Ultrasonic Distance Indicator")
root.geometry("300x500")
root.resizable(False, False)

# Title
title_label = tk.Label(root, text="Ultrasonic Sensor Distance", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Distance display label (large)
distance_label = tk.Label(root, text="Distance: -- cm", font=("Arial", 20), fg="blue")
distance_label.pack(pady=10)

# Canvas for traffic light circles
canvas = tk.Canvas(root, width=200, height=330, bg="black")
canvas.pack()

# Circles: Top (orange), Middle (white), Bottom (green)
circle_top = canvas.create_oval(50, 10, 150, 110, fill="gray")
circle_middle = canvas.create_oval(50, 120, 150, 220, fill="gray")
circle_bottom = canvas.create_oval(50, 230, 150, 330, fill="gray")

def update_display(distance):
    """Update which circle is lit based on distance."""
    if distance < 5:
        canvas.itemconfig(circle_top, fill="orange")
        canvas.itemconfig(circle_middle, fill="gray")
        canvas.itemconfig(circle_bottom, fill="gray")
    elif distance <= 20:
        canvas.itemconfig(circle_top, fill="gray")
        canvas.itemconfig(circle_middle, fill="white")
        canvas.itemconfig(circle_bottom, fill="gray")
    else:
        canvas.itemconfig(circle_top, fill="gray")
        canvas.itemconfig(circle_middle, fill="gray")
        canvas.itemconfig(circle_bottom, fill="green")

def read_serial():
    try:
        data = arduino.readline().decode('utf-8').strip()
        if data.isdigit():
            distance = int(data)
            distance_label.config(text=f"Distance: {distance} cm")
            update_display(distance)
    except:
        pass
    root.after(100, read_serial)

read_serial()
root.mainloop()
