import cv2
from ultralytics import YOLO
import numpy as np
from test2 import find_nearest_point_squared, find_intersections, find_cushion

# Load the YOLOv8 model
model = YOLO('best.pt')

# Open the video file
video_path = "test.mp4"
cap = cv2.VideoCapture(video_path)
prev_tar_loc = None
cushion =  [118, 100, 1160, 620]

def tracking(tar_loc, tar_dir, ball1_loc, ball2_loc):
    intersect = []
    intersect += find_cushion(tar_loc, tar_dir, cushion)
    if ball1_loc != None:
        intersect += find_intersections(tar_loc, tar_dir, ball1_loc, ball_num="ball1") #ball1과의 교점
    if ball2_loc != None:    
        intersect += find_intersections(tar_loc, tar_dir, ball2_loc, ball_num="ball2") #ball2와의 교점
            
    predict_loc = find_nearest_point_squared(tar_loc, intersect)
    return predict_loc

# Get the original video's FPS
fps = cap.get(cv2.CAP_PROP_FPS)

# Set the start and end times in seconds
start_time = 0
end_time = 18

# Convert the start and end times to milliseconds
start_time_ms = start_time * 1000
end_time_ms = end_time * 1000

# Set the current position of the video file to the start time
cap.set(cv2.CAP_PROP_POS_MSEC, start_time_ms)

# Set the bounding box (x, y, width, height)
bbox = (0, 0, 1280, 720)

move = False
prev_list = [None]
hit_list = []
magnitude_list = []

# Loop through the video frames
while cap.isOpened():
    # Get the current position in the video
    current_time_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
    # Break the loop if the end time is reached
    if current_time_ms > end_time_ms:
        break

    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Crop the frame to the region of interest
        frame = frame[bbox[1]:bbox[1]+bbox[3], bbox[0]:bbox[0]+bbox[2]]
        # Run YOLOv8 inference on the frame
        results = model(frame)
        cv2.rectangle(frame, (cushion[0], cushion[1]), (cushion[2], cushion[3]), (255, 0, 0), 2)

        white_ball = red_ball = yellow_ball = None

        # Print the coordinates of each detected object
        for box in results[0].boxes:
            x1, y1, x2, y2, conf, class_id = box.data[0]
            if int(class_id) == 0:
                white_ball = [(x1+x2)/2 , (y1+y2)/2]
            elif int(class_id) == 1:
                red_ball = [(x1+x2)/2 , (y1+y2)/2]
            elif int(class_id) == 2:
                yellow_ball = [(x1+x2)/2 , (y1+y2)/2]

        tar_loc = white_ball
        ball1 = red_ball
        ball2 = yellow_ball
        if prev_tar_loc is not None:
            tar_dir = [tar_loc[0] - prev_tar_loc[0], tar_loc[1] - prev_tar_loc[1]]  
            magnitude = np.linalg.norm(tar_dir)

            if len(magnitude_list) < 5:
                magnitude_list.append(magnitude)
            else:
                del magnitude_list[0]
                magnitude_list.append(magnitude)

            avg = sum(magnitude_list)/5

            if magnitude > 1: #타겟 볼이 움직이는 상태
                move = True
                predict_loc = tracking(tar_loc, tar_dir, ball1, ball2)
                if predict_loc != None:
                    w1 = int(white_ball[0])
                    w2 = int(white_ball[1])
                    p1 = int(predict_loc[1][0])
                    p2 = int(predict_loc[1][1])
                    cv2.line(frame, (w1,w2), (p1,p2), (255, 0, 255), 2)
                    cv2.circle(frame, (p1,p2), 13, (255, 0, 255), 3)
                    if np.linalg.norm([w1-p1, w2-p2]) < 50: #쿠션인 경우에는 거리말고 x와 y좌표 값이 쿠션에 가까운 기준으로 변경
                        prev_list = [predict_loc[0], tar_dir, ball1, ball2]
                    if prev_list[0] == 'cushion': #이전에 부딧힐 거라고 예상한 객체가 쿠션인 경우
                        if (prev_list[1][0] * tar_dir[0]) < 0 or (prev_list[1][1] * tar_dir[1]) < 0 :# 벡터 값이 변한경우(x나 y의 부호변화)
                            hit_list.append(prev_list[0])
                            prev_list = [None]
                    elif prev_list[0] == 'ball1': #이전에 부딧힐 거라고 예상한 객체가 공1인 경우
                        d = [ball1[0] - prev_list[2][0], ball1[1] - prev_list[2][1]]  
                        if np.linalg.norm(d) > 1:
                            hit_list.append(prev_list[0])
                            prev_list = [None]
                    elif prev_list[0] == 'ball2': #이전에 부딧힐 거라고 예상한 객체가 공2인 경우
                        d = [ball2[0] - prev_list[3][0], ball2[1] - prev_list[3][1]]  
                        if np.linalg.norm(d) > 1:
                            hit_list.append(prev_list[0])
                            prev_list = [None]
                        
            elif move and avg < 1: # 이전까지 움직이는 상태에서 정지 상태로 바뀐 경우
                ball1_found = False
                ball2_found = False
                no_ball = True
                cushion_count = 0
                for item in hit_list:
                    if item == "cushion":
                        cushion_count += 1
                    elif item == "ball1":
                        ball1_found = True
                    elif item == "ball2":
                        ball2_found = True
                    if ball1_found and ball2_found:
                        no_ball = False
                        if cushion_count < 3:
                            print("점수 획득 실패")
                        else:
                            print("점수 획득")
                        break
                if no_ball:
                    print("점수 획득 실패")
                move = False

        prev_tar_loc = tar_loc
            
                
        # Visualize the results on the frame
        annotated_frame = results[0].plot(conf = False, labels = False)
        
        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(int((1 / fps) * 1000)) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break
print(hit_list)

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()