import cv2
import numpy as np

i = 11730
while True:
    img = cv2.imread('ca/frame_'+ str(i) +'.jpg')
    height, width, _ = img.shape

    # ROI 설정
    roi_x, roi_y, roi_w, roi_h = 20, 30, 1320, 670
    roi = img[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]

    # ROI를 BGR에서 HSV로 변환
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    # 파란색 당구대를 위한 HSV 범위 설정
    lower_blue = np.array([90, 50, 100])
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

    print(i)
    with open("frame_" + str(i) +'.txt', 'w') as f:
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            # 바운딩 박스의 크기 확인
            w_rel, h_rel = w / width, h / height
            if min(w_rel, h_rel) < 0.015 or max(w_rel, h_rel) > 0.1:
                continue  # 직사각형의 크기가 너무 작거나 크면 무시

            # 직사각형의 비율 확인
            ratio = max(w, h) / min(w, h)
            if ratio > 2:
                continue  # 직사각형의 가로세로 비율이 2 이상이면 무시

            # 물체의 색상 판별
            object_bgr = roi[y:y+h, x:x+w, :]
            average_color = cv2.mean(object_bgr, mask=mask[y:y+h, x:x+w])
            b, g, r = average_color[:3]

            if r > 150 and g < 130 and b < 200:  # R 값이 높고 나머지는 낮으면 빨강
                label = 1
            elif r > 150 and g > 130 and b < 150:  # 두개가 높고 B 값이 낮으면 노랑
                label = 2
            elif r > 150 and g > 140 and b > 150:  # 셋다 높으면 하얀색
                label = 0
            else:
                continue  # 다른 색상의 물체는 무시

            # 상대적인 좌표와 길이 계산
            x += roi_x
            y += roi_y
            x_rel, y_rel, w_rel, h_rel = (x+(w/2)) / width, (y+(h/2)) / height, w / width, h / height

            # txt 파일에 정보 저장
            f.write(f"{label} {x_rel} {y_rel} {w_rel} {h_rel}\n")
            if label == 0:
                print("흰", end= " ")
            elif label == 1:
                print("빨", end= " ")
            elif label == 2:
                print("노", end= " ")
            # print(int(r),int(g),int(b), "\n")

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    print()
    # ROI 사각형 그리기
    cv2.rectangle(img, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (255, 0, 0), 2)

    # 이미지 표시
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Image', 1200, 750)
    cv2.imshow('Image', img)
    cv2.waitKey(10000)  # 2초간 대기
    cv2.destroyAllWindows()

    i += 10  # 인덱스 증가