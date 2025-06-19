import cv2
import os

# === 設定 ===
annotation_file = "annotations.txt"
output_folder = "positives"
output_info_file = "positives.txt"
target_size = (24, 24)  # Haar 預設訓練尺寸

# === 建立資料夾 ===
os.makedirs(output_folder, exist_ok=True)

# === 讀取並產生裁切圖 ===
count = 0
with open(annotation_file, "r") as f_in, open(output_info_file, "w") as f_out:
    for line in f_in:
        parts = line.strip().split()
        if len(parts) != 6:
            continue
        img_path, num, x, y, w, h = parts
        x, y, w, h = map(int, [x, y, w, h])

        img = cv2.imread(img_path)
        if img is None:
            print(f"⚠️ 讀不到圖片：{img_path}")
            continue

        roi = img[y:y+h, x:x+w]
        if roi.shape[0] == 0 or roi.shape[1] == 0:
            print(f"⚠️ 空框跳過：{img_path}")
            continue

        resized = cv2.resize(roi, target_size)
        output_img_path = os.path.join(output_folder, f"pos_{count}.jpg")
        cv2.imwrite(output_img_path, resized)

        # 在 positives.txt 寫入格式：相對路徑 1 0 0 w h
        f_out.write(f"{output_img_path} 1 0 0 {target_size[0]} {target_size[1]}\n")
        count += 1

print(f"✅ 成功產出 {count} 張正樣本，並儲存在 {output_folder}/positives.txt")
