import cv2
import os

# 비디오 파일 경로를 지정합니다.
video_file = "video.mp4"

# 저장할 이미지 파일의 디렉토리를 지정합니다.
save_dir = "frames"

# 디렉토리가 존재하지 않는 경우, 디렉토리를 생성합니다.
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 비디오를 엽니다.
cap = cv2.VideoCapture(video_file)

# 시작 시간과 종료 시간을 초 단위로 설정합니다.
start_time = 192 # 15 seconds
end_time = 197 # 1 minute 20 seconds

# FPS (Frames Per Second)를 얻습니다.
fps = cap.get(cv2.CAP_PROP_FPS)

# 시작 프레임과 종료 프레임을 계산합니다.
start_frame = round(start_time * fps)
end_frame = round(end_time * fps)

# 시작 프레임으로 이동합니다.
cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

frame_num = start_frame
while cap.isOpened() and frame_num <= end_frame:
    ret, frame = cap.read()
    if not ret:
        break

    # 프레임을 이미지 파일로 저장합니다.
    save_path = os.path.join(save_dir, f"frame_{frame_num}.jpg")
    cv2.imwrite(save_path, frame)
    
    frame_num += 1

cap.release()
