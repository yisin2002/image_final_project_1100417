import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# HSV顏色範圍
penColorHSV = [[62, 173, 0, 115, 255, 255]]

# 紀錄軌跡點
drawPoints = []

def detectPenHaar(frame):
    """
    模擬Haar分類器的筆頭偵測器
    輸入：彩色影像
    輸出：list of 矩形框 (x, y, w, h) 偵測到的筆頭區域
    """
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    pen_regions = []

    for colorRange in penColorHSV:
        lower = np.array(colorRange[:3])
        upper = np.array(colorRange[3:])
        mask = cv2.inRange(hsv, lower, upper)

        # 找輪廓
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 500:
                x, y, w, h = cv2.boundingRect(cnt)
                pen_regions.append((x, y, w, h))

    return pen_regions

def drawTrackingPoints(img, points):
    for i in range(1, len(points)):
        cv2.line(img, (points[i-1][0], points[i-1][1]), (points[i][0], points[i][1]), (255, 0, 0), 5)
    for p in points:
        cv2.circle(img, (p[0], p[1]), 5, (0, 0, 255), cv2.FILLED)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    imgDraw = frame.copy()

    # 用模擬Haar檢測器偵測筆頭區域
    detected_pens = detectPenHaar(frame)

    for (x, y, w, h) in detected_pens:
        # 畫出偵測框（模擬Haar偵測結果）
        cv2.rectangle(imgDraw, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # 筆頭中心點
        cx, cy = x + w // 2, y + h // 2
        cv2.circle(imgDraw, (cx, cy), 8, (255, 0, 0), cv2.FILLED)

        # 記錄軌跡點
        drawPoints.append((cx, cy))

    # 畫出軌跡線
    if len(drawPoints) > 1:
        drawTrackingPoints(imgDraw, drawPoints)

    cv2.imshow("Pen Detection (Haar-like)", imgDraw)
    cv2.imshow("Original", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
