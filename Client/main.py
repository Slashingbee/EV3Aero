#!/usr/bin/env python3

import socket
import time
import math
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B # type: ignore
from ev3dev2.sensor.lego import TouchSensor # type: ignore
from ev3dev2.sensor import INPUT_1 # type: ignore
from ev3dev2.button import Button # type: ignore

# Adjustable parameters
REFRESH_RATE = 0.01  # Refresh rate in seconds (10 milliseconds)
DEADZONE = 1  # Slightly increased deadzone to avoid unnecessary micro-movements
MAX_ANGLE = 180  # Maximum angle to scale the curve
MAX_POWER = 100  # Maximum motor power
LINEARITY = 1.5  # Linearity factor for exponential curve (higher = steeper response)
POWER_MULTIPLIER = 1.0  # Power multiplier to apply force proportionally
SMOOTHING_FACTOR = 0.3  # Smoothing factor
STALL_THRESHOLD = 0.5  # Threshold below which motor is considered stalled
MOTION_TIMEOUT = 0.05  # Time in seconds before locking activation
RESET_POSITION_VALUE = 0  # Value to set when button OK is pressed

# Initialize motors
motor_a = LargeMotor(OUTPUT_A)
motor_b = LargeMotor(OUTPUT_B)

# Initialize touch sensor
touch_sensor = TouchSensor(INPUT_1)

button = Button()

# State tracking variables
smoothed_speed_a = 0
smoothed_speed_b = 0
lock_state_a = 0  # 0 = unlocked, 1 = locked
lock_state_b = 0  # 0 = unlocked, 1 = locked
last_movement_time_a = time.time()
last_movement_time_b = time.time()

def get_motor_positions():
    return motor_a.position, motor_b.position

def get_motor_speeds():
    return motor_a.speed, motor_b.speed

# Exponential control function
def exponential_control(error):
    sign = -1 if error >= 0 else 1  # Reverse direction
    normalized_error = min(abs(error) / MAX_ANGLE, 1)  # Normalize error within range
    power = MAX_POWER * (normalized_error ** LINEARITY) * sign  # Exponential scaling
    return power * POWER_MULTIPLIER

# Function to push motor to zero degrees using exponential curve
def push_to_zero_exponential():
    global smoothed_speed_a, smoothed_speed_b, lock_state_a, lock_state_b, last_movement_time_a, last_movement_time_b
    
    pos_a, pos_b = get_motor_positions()
    speed_a, speed_b = get_motor_speeds()
    current_time = time.time()
    
    # Detect motion state
    if abs(pos_a) <= DEADZONE:
        lock_state_a = 0
    elif abs(speed_a) > STALL_THRESHOLD:
        last_movement_time_a = current_time
    elif lock_state_a == 0 and (current_time - last_movement_time_a) > MOTION_TIMEOUT:
        lock_state_a = 1
    
    if abs(pos_b) <= DEADZONE:
        lock_state_b = 0
    elif abs(speed_b) > STALL_THRESHOLD:
        last_movement_time_b = current_time
    elif lock_state_b == 0 and (current_time - last_movement_time_b) > MOTION_TIMEOUT:
        lock_state_b = 1
    
    # Apply control based on lock state
    if lock_state_a:
        output_a = exponential_control(pos_a)
        smoothed_speed_a = smoothed_speed_a * SMOOTHING_FACTOR + output_a * (1 - SMOOTHING_FACTOR)
        motor_a.on(speed=smoothed_speed_a, brake=False)
    else:
        motor_a.off(brake=False)  # Coast when unlocked
    
    if lock_state_b:
        output_b = exponential_control(pos_b)
        smoothed_speed_b = smoothed_speed_b * SMOOTHING_FACTOR + output_b * (1 - SMOOTHING_FACTOR)
        motor_b.on(speed=smoothed_speed_b, brake=False)
    else:
        motor_b.off(brake=False)  # Coast when unlocked

def check_button_press():
    if button.enter:
        motor_a.position = RESET_POSITION_VALUE
        motor_b.position = RESET_POSITION_VALUE

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))
server_socket.listen(5)

try:
    while True:
        client_socket, _ = server_socket.accept()
        
        while True:
            pos_a, pos_b = get_motor_positions()
            touch_state = 1 if touch_sensor.is_pressed else 0
            
            data = "Motor A: {} degrees, Motor B: {} degrees, Button: {}".format(pos_a, pos_b, touch_state)
            try:
                client_socket.sendall(data.encode('utf-8'))
            except BrokenPipeError:
                break
            
            # Apply exponential push to zero
            push_to_zero_exponential()
            check_button_press()
            
            time.sleep(REFRESH_RATE)
except KeyboardInterrupt:
    pass
finally:
    server_socket.close()
