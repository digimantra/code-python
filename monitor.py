from flask import Flask, request
from flask_socketio import SocketIO, emit
from mylib.centroidtracker import CentroidTracker
from mylib.trackableobject import TrackableObject
from imutils.video import FPS
import time
import numpy as np
import  imutils
import time, dlib, cv2
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

t0 = time.time()




def send_monitoring_info(totalUp, totalDown):
    info = {
        "exit": totalUp,
        "enter": totalDown
    }
    # print(info)
    socketio.emit('monitoring_info', info)
	

def run():
    global totalUp, totalDown, x
    # Initialize variables and objects
    net = cv2.dnn.readNetFromCaffe("mobilenet_ssd/MobileNetSSD_deploy.prototxt", "mobilenet_ssd/MobileNetSSD_deploy.caffemodel")
    input = "videos/example_01.mp4"
    vs = cv2.VideoCapture(input)
    threshold_confidence = 0.4

    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
		"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
		"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
		"sofa", "train", "tvmonitor"]

    x = []
    totalUp = 0
    totalDown = 0
    W = None
    H = None
    ct = CentroidTracker(maxDisappeared=40, maxDistance=50)
    trackers = []
    trackableObjects = {}
    totalFrames = 0
    empty = []
    empty1 = []
    fps = FPS().start()

    while True:
        frame = vs.read()
        frame = frame[1] if input else frame
        
        if input is not None and frame is None:
            break
        
        frame = imutils.resize(frame, width = 500)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


        if W is None or H is None:
            (H, W) = frame.shape[:2]

        status = "Waiting"
        rects = []

        if totalFrames % 30 == 0:
            status = "Detecting"
            trackers = []

            blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
            net.setInput(blob)
            detections = net.forward()


            for i in np.arange(0, detections.shape[2]):

                confidence = detections[0, 0, i, 2]

                if confidence > threshold_confidence:

                    idx = int(detections[0, 0, i, 1])

                    if CLASSES[idx] != "person":
                        continue

                    box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                    (startX, startY, endX, endY) = box.astype("int")

                    tracker = dlib.correlation_tracker()
                    rect = dlib.rectangle(startX, startY, endX, endY)
                    tracker.start_track(rgb, rect)
                    trackers.append(tracker)

        else:

            for tracker in trackers:

                status = "Tracking"
                tracker.update(rgb)
                pos = tracker.get_position()

                startX = int(pos.left())
                startY = int(pos.top())
                endX = int(pos.right())
                endY = int(pos.bottom())

                rects.append((startX, startY, endX, endY))


        cv2.line(frame, (0, H // 2), (W, H // 2), (0, 0, 0), 3)
        cv2.putText(frame, "-Prediction border - Entrance-", (10, H - ((i * 20) + 200)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)


        objects = ct.update(rects)


        for (objectID, centroid) in objects.items():

            to = trackableObjects.get(objectID, None)

            if to is None:
                to = TrackableObject(objectID, centroid)

            else:

                y = [c[1] for c in to.centroids]
                direction = centroid[1] - np.mean(y)
                to.centroids.append(centroid)


                if not to.counted:

                    if direction < 0 and centroid[1] < H // 2:
                        totalUp += 1
                        
                        empty.append(totalUp)
                        to.counted = True
                        send_monitoring_info(totalUp=1,totalDown=0)



                    elif direction > 0 and centroid[1] > H // 2:
                        totalDown += 1
                        empty1.append(totalDown)
                        x = []
                        x.append(len(empty1)-len(empty))
                        to.counted = True
                        send_monitoring_info(totalUp=0,totalDown=1)

            trackableObjects[objectID] = to

            text = "ID {}".format(objectID)
            cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.circle(frame, (centroid[0], centroid[1]), 4, (255, 255, 255), -1)

        info = [
        ("Exit", totalUp),
        ("Enter", totalDown),
        ("Status", status),
        ]

        info2 = [
        ("Total people inside", x),
        ]


        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, H - ((i * 20) + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        for (i, (k, v)) in enumerate(info2):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (265, H - ((i * 20) + 60)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)


        cv2.imshow("Real-Time Monitoring/Analysis Window", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        totalFrames += 1
        fps.update()

    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    cv2.destroyAllWindows()


# Route to trigger the run method
@app.route('/trigger-model', methods=['POST'])
def trigger_webhook():
    threading.Thread(target=run).start()
    return 'Webhook triggered successfully'



# # SocketIO event handler for client connection
@socketio.on('connect')
def handle_connect():
    print('Client connected')

# # SocketIO event handler for client disconnection
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    # Start the Flask app with SocketIO support
    socketio.run(app)