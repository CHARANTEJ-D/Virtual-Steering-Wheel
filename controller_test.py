import vgamepad as vg
import time

gamepad = vg.VX360Gamepad()

print("Moving virtual stick to the RIGHT...")

gamepad.left_joystick_float(
    x_value_float=1.0,
    y_value_float=0.0
)

gamepad.update()

time.sleep(3)

print("Returning stick to CENTER...")

gamepad.left_joystick_float(
    x_value_float=0.0,
    y_value_float=0.0
)

gamepad.update()

print("Test complete.")