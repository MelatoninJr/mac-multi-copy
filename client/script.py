import time
import pyperclip
from pynput import keyboard
import subprocess

clipboard_history = []
previous_clipboard = pyperclip.paste()
current_modifiers = set()
current_index = 0
previous_index = 0

def notify(title, text):
    if not isinstance(title, str) or not isinstance(text, str):
        raise TypeError('Title and text must be strings.')

    cmd = 'display notification "{}" with title "{}"'.format(text, title)
    subprocess.call(['osascript', '-e', cmd])
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
            notify('Clipboard Updated', f'Current Copied Value: {previous_value}')
            # Show the popup preview
            #show_popup_preview(previous_value)

    if key == keyboard.KeyCode.from_char('r') and all(modifier in current_modifiers for modifier in [keyboard.Key.ctrl, keyboard.Key.shift]):
        if len(clipboard_history) > 0:
            # Go up one index in clipboard history
            previous_index = current_index
            current_index = min(len(clipboard_history) - 1, current_index + 1)
            previous_value = clipboard_history[current_index]
            pyperclip.copy(previous_value)
            print("Clipboard updated with previous index value:", previous_value)
            notify('Clipboard Updated', f'Current Copied Value: {previous_value}')

    if key == keyboard.KeyCode.from_char('t') and all(modifier in current_modifiers for modifier in [keyboard.Key.ctrl, keyboard.Key.shift]):
        # Reset clipboard history and index variables
        clipboard_history = []
        current_index = 0
        previous_index = 0
        notify('Clipboard History Reset', 'Clipboard history and index reset')

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
        #show_popup_preview(current_clipboard)

        previous_clipboard = current_clipboard

    time.sleep(1)