import os
import sys
import pyautogui
import time
import threading
import win32gui
import pygetwindow as gw
import keyboard
import tkinter as tk
from ctypes import *
import random

root = None
status = None
isActive = False
stop_event = threading.Event()

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def handle_exit():
    global isActive, lock_input_event, status
    if isActive:
        isActive = False
        stop_event.set()
        status.config(text="Not started")
        status.config(fg="red")


def main_loop():
    windows = gw.getWindowsWithTitle('Minecraft')
    if windows:
        window = windows[0]
        while True:
            active_window = win32gui.GetForegroundWindow()
            beenActivated = False
            if window._hWnd != active_window:
                windll.user32.BlockInput(True)
                if win32gui.IsIconic(window._hWnd):
                    win32gui.ShowWindow(window._hWnd, 9)

                try:
                    win32gui.SetForegroundWindow(window._hWnd)
                except Exception as e:
                    pyautogui.keyDown('alt')
                    pyautogui.press('tab')
                    pyautogui.keyUp('alt')
                beenActivated = True
            if beenActivated:
                pyautogui.press('esc')

            time.sleep(1)
            start_x, start_y = pyautogui.position()
            random_number = random.randint(5, 100)
            random_vec = random.randint(0, 7)
            if random_vec == 0:
                pyautogui.moveTo(start_x + random_number, start_y, duration=0.5)
                pyautogui.moveTo(start_x - random_number, start_y, duration=0.5)
            elif random_vec == 1:
                pyautogui.moveTo(start_x - random_number, start_y, duration=0.5)
                pyautogui.moveTo(start_x + random_number, start_y, duration=0.5)
            elif random_vec == 2:
                pyautogui.moveTo(start_x, start_y + random_number, duration=0.5)
                pyautogui.moveTo(start_x, start_y - random_number, duration=0.5)
            elif random_vec == 3:
                pyautogui.moveTo(start_x, start_y - random_number, duration=0.5)
                pyautogui.moveTo(start_x, start_y + random_number, duration=0.5)
            elif random_vec == 4:
                pyautogui.moveTo(start_x + random_number, start_y + random_number, duration=0.5)
                pyautogui.moveTo(start_x - random_number, start_y - random_number, duration=0.5)
            elif random_vec == 5:
                pyautogui.moveTo(start_x - random_number, start_y - random_number, duration=0.5)
                pyautogui.moveTo(start_x + random_number, start_y + random_number, duration=0.5)
            elif random_vec == 6:
                pyautogui.moveTo(start_x + random_number, start_y - random_number, duration=0.5)
                pyautogui.moveTo(start_x - random_number, start_y + random_number, duration=0.5)
            elif random_vec == 7:
                pyautogui.moveTo(start_x - random_number, start_y + random_number, duration=0.5)
                pyautogui.moveTo(start_x + random_number, start_y - random_number, duration=0.5)

            time.sleep(0.4)

            windll.user32.BlockInput(False)

            if win32gui.IsIconic(active_window):
                win32gui.ShowWindow(active_window, 9)

            try:
                win32gui.SetForegroundWindow(active_window)
            except Exception as e:
                pyautogui.keyDown('alt')
                pyautogui.press('tab')
                pyautogui.keyUp('alt')

            random_number = random.randint(0, 90)
            if stop_event.wait(120 + random_number):
                break

        stop_event.clear()



def start():
    global isActive
    if not isActive:
        isActive = True
        listener_thread = threading.Thread(target=main_loop, daemon=True)
        listener_thread.start()

        status.config(text="Started")
        status.config(fg="green")

def on_closing():
    windll.user32.BlockInput(False)  # Убедиться, что ввод разблокирован
    handle_exit()  # Остановить активные процессы
    root.destroy()

def interface():
    global status, root
    root = tk.Tk()
    root.title("Mover")
    root.iconbitmap(resource_path("images/icon.ico"))
    root.geometry("300x300")
    label1 = tk.Label(root, text="Status: ", font=("Arial", 12))
    status = tk.Label(root, text="Not started", font=("Arial", 12), fg="red")
    btn1 = tk.Button(root, text="Start (Ctrl + Z)", command=start, font=("Arial", 12))
    btn2 = tk.Button(root, text="Stop (Ctrl + Q)", command=handle_exit, font=("Arial", 12))
    btn3 = tk.Button(root, text="Exit", command=on_closing, font=("Arial", 12))
    label1.pack(padx=10, pady=10)
    status.pack(padx=10, pady=10)
    btn1.pack(padx=10, pady=10)
    btn2.pack(padx=10, pady=10)
    btn3.pack(padx=10, pady=10)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    hotkey_id1 = keyboard.add_hotkey('ctrl+q', handle_exit, suppress=True)
    hotkey_id2 = keyboard.add_hotkey('ctrl+z', start, suppress=True)
    interface()
    keyboard.remove_hotkey(hotkey_id1)
    keyboard.remove_hotkey(hotkey_id2)

