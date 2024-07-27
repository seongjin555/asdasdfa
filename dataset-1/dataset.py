import cv2
import numpy as np

# 이미지 불러오기
for i in range(900, 1000):
    print(i)
    img = cv2.imread('images/frame_' + str(i) + '.jpg')
    height, width, _ = img.shape

    # 이미지를 BGR에서 HSV로 변환
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 파란색 당구대를 위한 HSV 범위 설정
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # HSV 이미지에서 파란색만 추출하기 위한 마스크 생성
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # 마스크를 반전시켜 파란색이 아닌 부분을 검출
    mask = cv2.bitwise_not(mask)

    # 노이즈 제거를 위한 모폴로지 연산 수행
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # 바운딩 박스 그리기
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    j = [0, 1, 2]
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # 물체의 색상 판별
        object_bgr = img[y:y+h, x:x+w, :]
        average_color = cv2.mean(object_bgr, mask=mask[y:y+h, x:x+w])
        b, g, r = average_color[:3]

        if r > 150 and g < 120 and b < 120:  # R 값이 높고 나머지는 낮으면 빨강
            label = 1
        elif r > 150 and g > 120 and b < 120:  # 두개가 높고 B 값이 낮으면 노랑
            label = 2
        elif r > 150 and g > 120 and b > 120:  # 셋다 높으면 하얀색
            label = 0
        else:
            continue  # 다른 색상의 물체는 무시

        # 직사각형의 비율 확인
        ratio = max(w, h) / min(w, h)
        if ratio > 2:
            continue  # 직사각형의 가로세로 비율이 2 이상이면 무시

        # 물체 주변의 색상 확인
        border_bgr = img[max(0, y-1):min(height, y+h+1), max(0, x-1):min(width, x+w+1), :]
        border_mask = cv2.inRange(border_bgr, lower_blue, upper_blue)
        border_ratio = np.count_nonzero(border_mask) / border_mask.size
        if border_ratio < 0.5:
            continue  # 물체 주변의 색상이 50% 이상 파란색이 아니면 무시

        print(int(r), int(g), int(b), label, x, y, w, h)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        j.remove(label)

    if len(j) == 0:
        print("ok")
    else:
        print(i, "error")
        break

