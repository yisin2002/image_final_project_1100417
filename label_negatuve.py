import cv2
import os

# ========== 設定 ==========
image_folder = './negatives'  # 圖片資料夾
output_file = 'negatives.txt'  # 輸出標註檔案
resize_width = 800  # 縮放寬度 (超過才縮)

# ========== 縮放函式 ==========
def resize_image(img, width=800):
    h, w = img.shape[:2]
    if w > width:
        ratio = width / w
        new_dim = (width, int(h * ratio))
        img = cv2.resize(img, new_dim)
    return img

# ========== 初始化 ==========
images = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.png'))]
current_image_index = 0
drawing = False
ix, iy = -1, -1
boxes = []
img = None
img_display = None

# ========== 滑鼠事件 ==========
def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, img_display, boxes

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_display = img.copy()
            cv2.rectangle(img_display, (ix, iy), (x, y), (0, 255, 0), 2)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        x1, y1 = min(ix, x), min(iy, y)
        x2, y2 = max(ix, x), max(iy, y)
        boxes.append((x1, y1, x2 - x1, y2 - y1))
        cv2.rectangle(img_display, (x1, y1), (x2, y2), (255, 0, 0), 2)

# ========== 主程式 ==========
if not images:
    print("找不到任何圖片。請確認 ./negatives/ 資料夾內有圖")
    exit()

with open(output_file, 'w') as f_out:
    while current_image_index < len(images):
        boxes = []
        img_path = os.path.join(image_folder, images[current_image_index])
        img = cv2.imread(img_path)
        img = resize_image(img, width=resize_width)
        img_display = img.copy()
        clone = img.copy()

        cv2.namedWindow('image')
        cv2.setMouseCallback('image', draw_rectangle)

        print(f"\n[{current_image_index+1}/{len(images)}] 標註: {images[current_image_index]}")
        print("滑鼠拖曳畫框，按 s 儲存並進下一張，r 重標，n 跳過，q 或關閉視窗離開。")

        while True:
            cv2.imshow('image', img_display)
            key = cv2.waitKey(20) & 0xFF

            # 判斷視窗是否被關閉
            if cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) < 1:
                print("視窗已關閉，結束程式")
                exit()

            if key == ord('r'):
                img_display = clone.copy()
                boxes = []
                print("🔁 重新標註")

            elif key == ord('s'):
                for box in boxes:
                    line = f"{img_path} 1 {box[0]} {box[1]} {box[2]} {box[3]}\n"
                    f_out.write(line)
                print("💾 已儲存標註")
                break

            elif key == ord('n'):
                print("⏭️ 跳過圖片")
                break

            elif key == ord('q'):
                print("👋 離開")
                exit()

        current_image_index += 1

    print("✅ 所有圖片標註完成")
    cv2.destroyAllWindows()
