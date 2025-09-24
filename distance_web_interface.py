from flask import Flask, jsonify, render_template_string
import serial
import threading

app = Flask(__name__)
distance_data = 0

# Connect to Arduino (Update COM port as needed)
arduino = serial.Serial('COM5', 9600)  # Change 'COM4' to your port

def read_serial():
    global distance_data
    
    while True:
        try:
            line = arduino.readline().decode('utf-8').strip()
            if line.isdigit():
                distance_data = int(line)
        except:
            continue

@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Distance Monitor</title>
            <style>
                body {
                    text-align: center;
                    font-family: Arial;
                    padding-top: 50px;
                }
                #box {
                    width: 200px;
                    height: 200px;
                    margin: auto;
                    background-color: grey;
                    border: 2px solid black;
                }
                h2 {
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <h1>Ultrasonic Distance Display</h1>
            <div id="box"></div>
            <h2 id="distance">Distance: -- cm</h2>

            <script>
                function updateDistance() {
                    fetch('/distance')
                        .then(response => response.json())
                        .then(data => {
                            let dist = data.distance;
                            document.getElementById('distance').innerText = "Distance: " + dist + " cm";
                            let color = "grey";
                            if(dist < 10) color = "red";
                            else if(dist < 20) color = "orange";
                            else if(dist < 40) color = "yellow";
                            else color = "green";
                            document.getElementById('box').style.backgroundColor = color;
                        });
                }
                setInterval(updateDistance, 1000);
            </script>
        </body>
        </html>
    ''')

@app.route('/distance')
def get_distance():
    return jsonify({'distance': distance_data})

if __name__ == '__main__':
    thread = threading.Thread(target=read_serial)
    thread.daemon = True
    thread.start()
    app.run(debug=True)
