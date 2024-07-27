import cv2
import numpy as np
from ultralytics import YOLO

# Load the trained model
model = YOLO('best.pt')

def detect_objects(video_source=0):
    cap = cv2.VideoCapture(video_source)

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        # Predict
        results = model.predict(frame)

        # Iterate over the detection results
        for result in results:
            # Get the class counts
            uniq, cnt = np.unique(result.boxes.cls.cpu().numpy(), return_counts=True)
            uniq_cnt_dict = dict(zip(uniq, cnt))

            # Print the class counts
            # print('\n{class num:counts} =', uniq_cnt_dict, '\n')

            # Draw the bounding boxes and labels
            for c, box in zip(result.boxes.cls, result.boxes.xyxy):
                x1, y1, x2, y2 = box
                class_id = int(c)
                class_name = model.names[class_id]

                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
                cv2.putText(frame, f'{class_name}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

        # Show the frame
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run the function
detect_objects('test.mp4')
