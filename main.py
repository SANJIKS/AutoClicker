import pyautogui
import time
import os
import shutil
import schedule

from clicker import click_on_blank

def find_and_click(images, attempts=2, interval=2, confidence=0.70, all_matches=False, escape_image='images/cancel.PNG'):
    for attempt in range(attempts):
        for image in images:
            try:
                found = False
                if all_matches:
                    locations = list(pyautogui.locateAllOnScreen(image, confidence=confidence))
                    print(locations.count())
                    if locations:
                        for location in locations:
                            pyautogui.click(pyautogui.center(location))
                            print('Найдено ' + image)
                            found = True
                else:
                    location = pyautogui.locateCenterOnScreen(image, confidence=confidence)
                    if location:
                        pyautogui.click(location)
                        print('Найдено ' + image)
                        found = True

                if found:
                    return True
            except:
                print(f"Изображение {image} не найдено, попытка {attempt+1} из {attempts}")
                time.sleep(interval)
        time.sleep(interval)
    return False

def click_escape(escape_image):
    try:
        location = pyautogui.locateCenterOnScreen(escape_image, confidence=0.70)
        if location:
            pyautogui.click(location)
            print(f"Нажатие на {escape_image} для отмены.")
    except:
        print(f"Изображение {escape_image} для отмены не найдено.")


def delete_runs():
    detect_dir = "C:\\Users\\User\\Desktop\\pixelclicker\\runs\\detect"
    screenshots_dir = "C:\\Users\\User\\Desktop\\pixelclicker\\screenshots"
    
    for folder_name in os.listdir(detect_dir):
        folder_path = os.path.join(detect_dir, folder_name)
        if os.path.isdir(folder_path) and folder_name.startswith("train"):
            shutil.rmtree(folder_path)
    print("Deleted all 'train' folders in runs/detect directory.")
    
    for screenshot in os.listdir(screenshots_dir):
        screenshot_path = os.path.join(screenshots_dir, screenshot)
        if os.path.isfile(screenshot_path):
            os.remove(screenshot_path)
    print("Deleted all screenshots in screenshots directory.")

schedule.every(10).minutes.do(delete_runs)


def main():
    while True:
        carrot_is_ready = ('images/Carrot.png', 'images/ready.png', 'images/ready-test.png')
        harvest = ('images/Harvest.PNG',)
        # blank = ('blank.PNG', 'blank1.PNG', 'blank2.PNG', 'blank3.PNG', 'blank4.PNG', 'blank5.PNG', 'blank6.PNG')
        # blank = ['new_blank.PNG']
        plant = ('images/plant.PNG',)
        carrot_to_plant = ('images/carrot_to_plant.PNG',)

        if find_and_click(carrot_is_ready):
            time.sleep(2)
            if find_and_click(harvest, attempts=1, interval=0):
                print("Урожай собран.")
        

        if click_on_blank():
            time.sleep(2) 
            if find_and_click(plant, attempts=1, interval=0):
                time.sleep(2)
                if find_and_click(carrot_to_plant, attempts=2, interval=0):
                    print("Морковь посажена.")
                else:
                    print("Не удалось найти иконку моркови для посадки.")
                    click_escape('images/cancel.PNG')
            else:
                click_escape('images/cancel.PNG')

        time.sleep(3)

        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()