import os
import sys
import pyautogui
import time
import threading
import win32gui
import pygetwindow as gw
import keyboard
import tkinter as tk

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
    global isActive
    if isActive:
        stop_event.set()
        isActive = False
        stop_event.clear()
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
            pyautogui.moveTo(start_x + 20, start_y, duration=0.2)
            pyautogui.moveTo(start_x - 20, start_y, duration=0.2)
            time.sleep(0.2)

            if win32gui.IsIconic(active_window):
                win32gui.ShowWindow(active_window, 9)

            try:
                win32gui.SetForegroundWindow(active_window)
            except Exception as e:
                pyautogui.keyDown('alt')
                pyautogui.press('tab')
                pyautogui.keyUp('alt')


            if stop_event.wait(120):
                break



def start():
    global isActive
    if not isActive:
        isActive = True
        listener_thread = threading.Thread(target=main_loop, daemon=True)
        listener_thread.start()
        status.config(text="Started")
        status.config(fg="green")

def interface():
    global status
    root = tk.Tk()
    root.title("Mover")
    root.iconbitmap(resource_path("images/icon.ico"))
    root.geometry("300x300")
    label1 = tk.Label(root, text="Status: ", font=("Arial", 12))
    status = tk.Label(root, text="Not started", font=("Arial", 12), fg="red")
    btn1 = tk.Button(root, text="Start (Ctrl + Z)", command=start, font=("Arial", 12))
    btn2 = tk.Button(root, text="Stop (Ctrl + Q)", command=handle_exit, font=("Arial", 12))
    btn3 = tk.Button(root, text="Exit", command=root.destroy, font=("Arial", 12))
    label1.pack(padx=10, pady=10)
    status.pack(padx=10, pady=10)
    btn1.pack(padx=10, pady=10)
    btn2.pack(padx=10, pady=10)
    btn3.pack(padx=10, pady=10)
    root.mainloop()

if __name__ == "__main__":
    hotkey_id1 = keyboard.add_hotkey('ctrl+q', handle_exit)
    hotkey_id2 = keyboard.add_hotkey('ctrl+z', start)
    interface()
    keyboard.remove_hotkey(hotkey_id1)
    keyboard.remove_hotkey(hotkey_id2)

