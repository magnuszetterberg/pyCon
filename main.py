
import pygame
import time
from evdev import UInput, ecodes, AbsInfo
import math

# Initialize Pygame
pygame.init()

# Initialize the joystick
pygame.joystick.init()

# Check if a joystick is connected
if pygame.joystick.get_count() == 0:
    print("No joystick connected.")
    exit()

# Create a joystick object
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Define the capabilities of the virtual joystick
capabilities = {
    ecodes.EV_ABS: [
        (ecodes.ABS_X, AbsInfo(value=0, min=0, max=32767, fuzz=0, flat=0, resolution=0)),  # Left stick X-axis
        (ecodes.ABS_Y, AbsInfo(value=0, min=0, max=32767, fuzz=0, flat=0, resolution=0)),  # Left stick Y-axis
        (ecodes.ABS_RX, AbsInfo(value=0, min=0, max=32767, fuzz=0, flat=0, resolution=0)), # Right stick X-axis
        (ecodes.ABS_RY, AbsInfo(value=0, min=0, max=32767, fuzz=0, flat=0, resolution=0)), # Right stick Y-axis
    ],
    ecodes.EV_KEY: [
        ecodes.BTN_A,
        ecodes.BTN_B,
        ecodes.BTN_X,
        ecodes.BTN_Y,
        ecodes.BTN_TL,
        ecodes.BTN_TR,
        ecodes.BTN_SELECT,
        ecodes.BTN_START,
        ecodes.BTN_THUMBL,
        ecodes.BTN_THUMBR,
    ]
}

# Create a virtual joystick device
ui = UInput(events=capabilities, name="Virtual Gamepad", version=0x3)

# Function to map joystick input to virtual joystick input
def map_to_virtual_joystick(lx_value, ly_value, rx_value, ry_value):
    # Convert joystick input range (-1 to 1) to virtual joystick input range (0 to 32767)
    lx_virtual = int((lx_value + 1) * 16383.5)
    ly_virtual = int((ly_value + 1) * 16383.5)
    rx_virtual = int((rx_value + 1) * 16383.5)
    ry_virtual = int((ry_value + 1) * 16383.5)
    
    # Send the axis events to the virtual joystick
    ui.write(ecodes.EV_ABS, ecodes.ABS_X, lx_virtual)
    ui.write(ecodes.EV_ABS, ecodes.ABS_Y, ly_virtual)
    ui.write(ecodes.EV_ABS, ecodes.ABS_RX, rx_virtual)
    ui.write(ecodes.EV_ABS, ecodes.ABS_RY, ry_virtual)
    ui.syn()

# Function to generate rotation values for the analog sticks
def generate_rotation_values(angle):
    # Calculate the x and y values for a given angle
    lx_value = math.cos(angle)
    ly_value = math.sin(angle)
    rx_value = math.cos(angle + math.pi/2)  # 90 degrees offset for right stick
    ry_value = math.sin(angle + math.pi/2)
    return lx_value, ly_value, rx_value, ry_value

# Function to press a button
def press_button(button):
    ui.write(ecodes.EV_KEY, button, 1)  # Press the button
    ui.syn()

# Function to release a button
def release_button(button):
    ui.write(ecodes.EV_KEY, button, 0)  # Release the button
    ui.syn()

# Function to simulate reset event
def simulate_reset():
    press_button(ecodes.BTN_SELECT)
    time.sleep(0.1)
    release_button(ecodes.BTN_SELECT)

# Function to simulate restart event
def simulate_restart():
    press_button(ecodes.BTN_START)
    time.sleep(0.1)
    release_button(ecodes.BTN_START)

# Main loop to simulate joystick control and events
angle = 0
while True:
    lx_value, ly_value, rx_value, ry_value = generate_rotation_values(angle)
    
    # Map joystick input to virtual joystick input
    map_to_virtual_joystick(lx_value, ly_value, rx_value, ry_value)
    
    print(f'Joystick: L({lx_value:.2f}, {ly_value:.2f}), R({rx_value:.2f}, {ry_value:.2f})')
    
    # Simulate reset and restart events periodically
    if angle % (2 * math.pi) < 0.1:  # Simulate reset once per full rotation
        print("Simulating reset event")
        simulate_reset()

    if angle % (4 * math.pi) < 0.1:  # Simulate restart every two full rotations
        print("Simulating restart event")
        simulate_restart()
    
    time.sleep(0.1)  # Delay to simulate time passing
    angle += 0.1  # Increment angle to simulate rotation
