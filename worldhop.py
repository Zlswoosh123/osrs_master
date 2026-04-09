import time
import threading
import yaml
import win32gui
import pyautogui
import keyboard

import core
import functions2 as f2


# ----------------------------
# Global pause / stop controls
# ----------------------------
pause_event = threading.Event()
stop_event = threading.Event()

# Start unpaused
pause_event.set()


def toggle_pause():
    if pause_event.is_set():
        pause_event.clear()
        print("[PAUSED] Press F8 to resume.")
    else:
        pause_event.set()
        print("[RESUMED]")


def stop_script():
    stop_event.set()
    pause_event.set()  # unpause so anything waiting can exit
    print("[STOPPING] Script will exit safely.")


# ----------------------------
# Window helpers
# ----------------------------
def focus_game_window(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    if not hwnd:
        raise RuntimeError(f"Unable to find window: {window_title}")

    win32gui.SetActiveWindow(hwnd)
    win32gui.MoveWindow(hwnd, 0, 0, 865, 830, True)
    return hwnd


def load_config(config_path="pybot-config.yaml"):
    with open(config_path, "r", encoding="utf-8") as yamlfile:
        config = yaml.safe_load(yamlfile)

    try:
        return config[0]["Config"]["client_title"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("Invalid config format in pybot-config.yaml") from exc


# ----------------------------
# Utility helpers
# ----------------------------
def wait_if_paused():
    while not pause_event.is_set():
        if stop_event.is_set():
            return
        time.sleep(0.1)


def interruptible_sleep(seconds, check_interval=0.1):
    end_time = time.time() + seconds
    while time.time() < end_time:
        if stop_event.is_set():
            return
        wait_if_paused()
        time.sleep(check_interval)


def type_and_send(message, interval=0.03):
    wait_if_paused()
    if stop_event.is_set():
        return
    pyautogui.typewrite(message, interval)
    pyautogui.press("enter")


def send_messages(messages, delay_between=3):
    for msg in messages:
        if stop_event.is_set():
            return
        type_and_send(msg)
        interruptible_sleep(delay_between)


def hop_world(world_number):
    hop_message = f"::hop {world_number}"
    type_and_send(hop_message)
    interruptible_sleep(15)


def random_wait_interruptible(min_seconds, max_seconds):
    # If you want to preserve your existing random_wait logic exactly,
    # you could instead generate the random duration inside functions2
    # and pass it here.
    import random
    duration = random.uniform(min_seconds, max_seconds)
    interruptible_sleep(duration)


# ----------------------------
# Main script
# ----------------------------
def main():
    try:
        client_title = load_config()
    except Exception as exc:
        print(f"Config error: {exc}")
        return

    try:
        focus_game_window(client_title)
        x_win, y_win, w_win, h_win = core.getWindow(client_title)
        print(f"Window found: {client_title} ({x_win}, {y_win}, {w_win}, {h_win})")
    except Exception as exc:
        print(f"Unable to find window: {client_title}")
        core.printWindows()
        print(exc)
        return

    worlds = f2.worlds_us
    message_mode = "main"

    main_messages = [
        "Yoyo bankstanding people, I bring new music to grind to for the interested",
        "I produce the music myself and its actually solid if you like the genre",
        "For EDM Fans here, checkout 'Fire in the Sound - Songs of Siren' (all platforms)",
        "Much love for any subs if you enjoy the music. Ty for the time and gl grinding",
    ]

    side_messages = [
        "I've been enjoying listening to solid lofi while I grind",
        "",
    ]

    keyboard.add_hotkey("F8", toggle_pause)
    keyboard.add_hotkey("F9", stop_script)

    print("Script started.")
    print("F8 = pause/resume | F9 = stop")

    try:
        for index, world_number in enumerate(worlds):
            if stop_event.is_set():
                break

            wait_if_paused()
            if stop_event.is_set():
                break

            print(f"[WORLD {index + 1}/{len(worlds)}] Hopping to {world_number}")
            hop_world(world_number)

            if stop_event.is_set():
                break

            if message_mode == "main":
                send_messages(main_messages, delay_between=3)
                random_wait_interruptible(16, 24)

            elif message_mode == "side":
                send_messages(side_messages, delay_between=5)
                random_wait_interruptible(6, 10)

            print(f"Finished world {world_number}")

    finally:
        keyboard.unhook_all_hotkeys()
        print("Script exited.")


if __name__ == "__main__":
    main()