from flask import Flask, request, jsonify
from flask_cors import CORS
from math import dist
from statistics import median

QUEUE_SIZE = 61
PEOPLE_ID = 0
MONITOR_ID = 62

app = Flask(__name__)
cors = CORS(app)
history = {}

def get_mid_point(p):
    x = (p[0] + p[2]) / 2
    y = (p[1] + p[3]) / 2
    return x, y

def count_busy(people, monitors):
    count = 0
    for m in monitors:
        for p in people:
            mid_m = get_mid_point(m)
            mid_p = get_mid_point(p)
            if dist(mid_m, mid_p) < 200:
                count += 1
                break
    return count

def get_of_type(objects, type):
    return list(map(lambda x: x[0], filter(lambda x: x[1] == type, objects)))

def calculate(objects):
    people = get_of_type(objects, PEOPLE_ID)
    monitor = get_of_type(objects, MONITOR_ID)

    n_people = len(people)
    n_monitor = len(monitor)

    n_busy_monitors = count_busy(people, monitor)
    n_free_monitors = n_monitor - n_busy_monitors

    return n_people, n_monitor, n_free_monitors

def add_to_queue(cam_id, locations, types):
    if cam_id not in history.keys():
        history[cam_id] = []
    if len(history[cam_id]) == 61:
        history[cam_id].pop(0)
    history[cam_id].append(calculate(list(zip(locations, types))))

def process(data):
    elements = ['cam_id', 'locations', 'types']
    if all([e in data.keys() for e in elements]):
        add_to_queue(data['cam_id'], data['locations'], data['types'])
        return "ok"
    else:
        return "wrong json format"

@app.route('/update', methods=['POST'])
def update():
    return process(request.json)

@app.route('/status', methods=['GET'])
def status():
    response = []
    for h in history.items():
        print(h[0])
        print(h[1])
        
        people = []
        monitors = []

        free_monitors = []

        for x,y,z in h[1]:
            people.append(x)
            monitors.append(y)
            free_monitors.append(z)

        response.append({
            'cam_id': h[0],
            'people': median(people),
            'monitors': median(monitors),
            'free_monitors': median(free_monitors),
        })
        
    return jsonify(response)

def run():
    app.run(host = '0.0.0.0', port = 8080)

def main():
    run()

if __name__ == '__main__':
    main()