import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab

def find_all_images(target_image_path, threshold=0.5):
    screenshot = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    target_image = cv2.imread(target_image_path, cv2.IMREAD_COLOR)

    result = cv2.matchTemplate(screen, target_image, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)

    points = []
    for pt in zip(*locations[::-1]):
        points.append(pt)
        pyautogui.click(pt[0] + target_image.shape[1]//2, pt[1] + target_image.shape[0]//2)

    return points

if __name__ == "__main__":
    found_points = find_all_images("blank4.PNG", threshold=0.8)
    print(f"Найдено точек: {len(found_points)}")
