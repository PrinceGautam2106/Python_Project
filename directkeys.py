from pynput.keyboard import Key, Controller

keyboard = Controller()

# Replace right_pressed and left_pressed with your own hex-style IDs
right_pressed = 0x4D
left_pressed  = 0x4B

mac_key_map = {
    right_pressed: Key.right,
    left_pressed: Key.left
}

def PressKey(hexKeyCode):
    key = mac_key_map.get(hexKeyCode)
    if key:
        keyboard.press(key)
        print(f"Pressed: {key}")
    else:
        print(f"Unknown key: {hexKeyCode}")

def ReleaseKey(hexKeyCode):
    key = mac_key_map.get(hexKeyCode)
    if key:
        keyboard.release(key)
        print(f"Released: {key}")
    else:
        print(f"Unknown key: {hexKeyCode}")
