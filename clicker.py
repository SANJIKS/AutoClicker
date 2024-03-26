import os
from pathlib import Path
import pyautogui
from omegaconf import OmegaConf
from predictWithOCR import DetectionPredictor
from ultralytics.yolo.utils import DEFAULT_CONFIG, ROOT
from ultralytics.yolo.utils.checks import check_imgsz
import time

current_dir = Path(__file__).resolve().parent
config_file = current_dir / "config.yaml"

from datetime import datetime

def get_screenshot_and_save():
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.join(screenshots_dir, f"screenshot_{timestamp}.png")
    screen = f'screenshot_{timestamp}.png'
    
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    
    return screen


def detect_objects_on_screenshot():
    cfg = OmegaConf.load(config_file)
    screen = get_screenshot_and_save()
    
    cfg.data = screen
    cfg.source = './screenshots/' + screen
    cfg.model = cfg.model or "yolov8n.pt"
    cfg.imgsz = check_imgsz(cfg.imgsz, min_dim=2)  # check image size
    cfg.source = cfg.source if cfg.source is not None else ROOT / "assets"
    predictor = DetectionPredictor(cfg)
    # print(cfg)

    predictor()
    object_coordinates = predictor.get_object_coordinates()
    return object_coordinates



def click_on_blank():
    object_coordinates = detect_objects_on_screenshot()
    if object_coordinates is not None:
        center_x = (object_coordinates[0] + object_coordinates[2]) // 2
        center_y = (object_coordinates[1] + object_coordinates[3]) // 2

        pyautogui.click(center_x, center_y)
        return True
    
    else:
        return False



if __name__ == "__main__":
    screenshot = get_screenshot_and_save()
    object_coordinates = detect_objects_on_screenshot()
    print(object_coordinates)

    center_x = (object_coordinates[0] + object_coordinates[2]) // 2
    center_y = (object_coordinates[1] + object_coordinates[3]) // 2

    pyautogui.click(center_x, center_y)