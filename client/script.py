import time
import pyperclip
import pyautogui
from pynput import keyboard
from pync import Notifier
Notifier.notify('Test notification', title='Notification Test', timeout=2)
clipboard_history = []
previous_clipboard = pyperclip.paste()
current_modifiers = set()
current_index = 0
previous_index = 0

def show_popup_preview(value):
    # Show a macOS notification with the clipboard value
    Notifier.notify(value, title='Clipboard Preview', timeout=2)

def on_press(key):
    global clipboard_history, current_index, previous_index

    if key == keyboard.Key.shift or key == keyboard.Key.ctrl:
        current_modifiers.add(key)

    if key == keyboard.KeyCode.from_char('e') and all(modifier in current_modifiers for modifier in [keyboard.Key.ctrl, keyboard.Key.shift]):
        if len(clipboard_history) > 1:
            # Update clipboard with the previous value
            previous_index = current_index
            current_index = max(0, current_index - 1)
            previous_value = clipboard_history[current_index]
            pyperclip.copy(previous_value)
            print("Clipboard updated with previous value:", previous_value)

            # Show the popup preview
            show_popup_preview(previous_value)

    if key == keyboard.KeyCode.from_char('r') and all(modifier in current_modifiers for modifier in [keyboard.Key.ctrl, keyboard.Key.shift]):
        if len(clipboard_history) > 0:
            # Go up one index in clipboard history
            previous_index = current_index
            current_index = min(len(clipboard_history) - 1, current_index + 1)
            previous_value = clipboard_history[current_index]
            pyperclip.copy(previous_value)
            print("Clipboard updated with previous index value:", previous_value)

def on_release(key):
    global current_modifiers

    if key == keyboard.Key.shift or key == keyboard.Key.ctrl:
        current_modifiers.remove(key)

keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
keyboard_listener.start()

while True:
    current_clipboard = pyperclip.paste()

    if current_clipboard != previous_clipboard:
        print("Clipboard changed!")
        print("Copied:", current_clipboard)

        clipboard_history.append(current_clipboard)  # Store current clipboard value

        # Show the popup preview
        show_popup_preview(current_clipboard)

        previous_clipboard = current_clipboard

    time.sleep(1)