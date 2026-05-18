# mac_keys.py (Mac replacement for directkeys)

from pynput.keyboard import Key, Controller
import time

keyboard = Controller()

# Fake hex codes (just identifiers)
up_pressed = 0x48
down_pressed = 0x50
left_pressed = 0x4B
right_pressed = 0x4D

# Map to actual arrow keys
mac_key_map = {
    up_pressed: Key.up,
    down_pressed: Key.down,
    left_pressed: Key.left,
    right_pressed: Key.right
}

def PressKey(hexKeyCode):
    """Press a Mac keyboard key."""
    key = mac_key_map.get(hexKeyCode)
    if key:
        keyboard.press(key)
        print(f"[KEY DOWN] {key}")
    else:
        print(f"[UNKNOWN KEY] {hexKeyCode}")

def ReleaseKey(hexKeyCode):
    """Release a Mac keyboard key."""
    key = mac_key_map.get(hexKeyCode)
    if key:
        keyboard.release(key)
        print(f"[KEY UP] {key}")
    else:
        print(f"[UNKNOWN KEY] {hexKeyCode}")
