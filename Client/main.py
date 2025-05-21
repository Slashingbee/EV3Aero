#!/usr/bin/env python3

import socket
import time
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor import INPUT_1

# Adjustable parameters
REFRESH_RATE = 0.01  # Refresh rate in seconds (10 milliseconds)
DEADZONE = 2  # Slightly increased deadzone to avoid unnecessary micro-movements
MAX_POWER = 100  # Maximum motor power
MIN_SPEED = 5  # Lower minimum speed to avoid friction
KP = 0.1 # Proportional gain
KI = 0.0001  # Integral gain
KD = 0.9  # Derivative gain
SMOOTHING_FACTOR = 0.6  # Increased smoothing for lower friction
POWER_MULTIPLIER = 0.1  # Power multiplier to limit force

# Initialize motors
motor_a = LargeMotor(OUTPUT_A)
motor_b = LargeMotor(OUTPUT_B)

# Initialize touch sensor
touch_sensor = TouchSensor(INPUT_1)

# PID variables
last_error_a = 0
integral_a = 0
last_error_b = 0
integral_b = 0

# Smoothed speed variables
smoothed_speed_a = 0
smoothed_speed_b = 0

def get_motor_positions():
    return motor_a.position, motor_b.position

# Function to apply PID control with improved smoothing
def move_to_zero_with_pid():
    global last_error_a, integral_a, last_error_b, integral_b, smoothed_speed_a, smoothed_speed_b
    
    pos_a, pos_b = get_motor_positions()

    # PID for Motor A
    error_a = -pos_a
    integral_a += error_a * REFRESH_RATE
    derivative_a = (error_a - last_error_a) / REFRESH_RATE
    output_a = KP * error_a + KI * integral_a + KD * derivative_a
    last_error_a = error_a
    
    # PID for Motor B
    error_b = -pos_b
    integral_b += error_b * REFRESH_RATE
    derivative_b = (error_b - last_error_b) / REFRESH_RATE
    output_b = KP * error_b + KI * integral_b + KD * derivative_b
    last_error_b = error_b

    # Apply power multiplier and limit power
    output_a = max(min(output_a * POWER_MULTIPLIER, MAX_POWER), -MAX_POWER)* POWER_MULTIPLIER
    output_b = max(min(output_b * POWER_MULTIPLIER, MAX_POWER), -MAX_POWER) *POWER_MULTIPLIER
    
    # Apply smoothing
    smoothed_speed_a = smoothed_speed_a * SMOOTHING_FACTOR + output_a * (1 - SMOOTHING_FACTOR) * POWER_MULTIPLIER
    smoothed_speed_b = smoothed_speed_b * SMOOTHING_FACTOR + output_b * (1 - SMOOTHING_FACTOR) * POWER_MULTIPLIER
    
    # Apply smoothed speed to motors without braking
    if abs(pos_a) > DEADZONE:
        motor_a.on(speed=smoothed_speed_a, brake=False)
    else:
        motor_a.on(speed=0, brake=False)

    if abs(pos_b) > DEADZONE:
        motor_b.on(speed=smoothed_speed_b, brake=False)
    else:
        motor_b.on(speed=0, brake=False)

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))
server_socket.listen(5)
print("Server is listening for incoming connections...")

try:
    while True:
        client_socket, addr = server_socket.accept()
        print("Connection from {} has been established.".format(addr))
        
        while True:
            pos_a, pos_b = get_motor_positions()
            touch_state = 1 if touch_sensor.is_pressed else 0
            
            data = "Motor A: {} degrees, Motor B: {} degrees, Button: {}".format(pos_a, pos_b, touch_state)
            try:
                client_socket.sendall(data.encode('utf-8'))
            except BrokenPipeError:
                print("Client disconnected.")
                break
            
            # Apply PID control
            move_to_zero_with_pid()
            
            time.sleep(REFRESH_RATE)
except KeyboardInterrupt:
    print("Server is shutting down...")
finally:
    server_socket.close()
