import cv2
import os

# 이미지 디렉토리를 지정합니다.
img_dir = "ca"

# 상하로 잘라낼 비율을 설정합니다. (여기서는 10%로 설정)
crop_ratio_vertical = 0.15

# 좌우로 잘라낼 비율을 설정합니다. (여기서는 20%로 설정)
crop_ratio_horizontal = 0.14

for filename in os.listdir(img_dir):
    if filename.endswith(".jpg"):
        # 이미지 파일을 읽어옵니다.
        img_path = os.path.join(img_dir, filename)
        img = cv2.imread(img_path)

        # 이미지의 높이와 너비를 가져옵니다.
        h, w = img.shape[:2]

        # 자를 픽셀 수를 계산합니다.
        crop_h = round(h * crop_ratio_vertical)
        crop_w = round(w * crop_ratio_horizontal)

        # 이미지를 자릅니다.
        cropped_img = img[crop_h:-crop_h, crop_w:-crop_w]

        # 자른 이미지를 다시 저장합니다.
        cv2.imwrite(img_path, cropped_img)
        print(filename)