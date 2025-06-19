import os
import cv2

# === 設定 ===
input_annotation = "annotations.txt"
clean_annotation = "annotations_clean.txt"
output_info = "positives.txt"
output_dir = "positives"
target_size = (24, 24)

# === 建資料夾 ===
os.makedirs(output_dir, exist_ok=True)

# === 清理 annotations.txt，去除 w=0/h=0、路徑格式統一 ===
clean_lines = []
with open(input_annotation, "r") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) != 6:
            continue
        path, num, x, y, w, h = parts
        x, y, w, h = map(int, [x, y, w, h])
        if w > 0 and h > 0:
            path = path.replace("\\", "/")  # 換成跨平台路徑
            clean_lines.append(f"{path} {num} {x} {y} {w} {h}")

# 儲存清理後檔案
with open(clean_annotation, "w") as f:
    f.write("\n".join(clean_lines))
print(f"✅ 清理完成，共 {len(clean_lines)} 筆有效標註。")

# === 開始裁圖並產生 positives.txt ===
count = 0
with open(clean_annotation, "r") as f_in, open(output_info, "w") as f_out:
    for line in f_in:
        img_path, _, x, y, w, h = line.strip().split()
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
        out_path = os.path.join(output_dir, f"pos_{count}.jpg")
        cv2.imwrite(out_path, resized)

        # 在 positives.txt 寫入格式：路徑 1 0 0 w h
        f_out.write(f"{out_path} 1 0 0 {target_size[0]} {target_size[1]}\n")
        count += 1

print(f"✅ 已儲存 {count} 張正樣本圖至 `{output_dir}/`，並生成 `{output_info}`")
