#!/usr/bin/env python3

import socket
import time
import math
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C  # type: ignore
from ev3dev2.sensor.lego import TouchSensor  # type: ignore
from ev3dev2.sensor import INPUT_1  # type: ignore
from ev3dev2.button import Button  # type: ignore

# Adjustable parameters
REFRESH_RATE = 0.001  # Refresh rate in seconds (1 milliseconds)
DEADZONE = 5  # Slightly increased deadzone to avoid unnecessary micro-movements
MAX_ANGLE_A = 40  # Maximum angle to scale the curve for motor A
MAX_ANGLE_B = 60  # Maximum angle to scale the curve for motor B
MAX_ANGLE_C = 90   # Limit for motor C movement
MAX_DUTY_CYCLE_A = 35  # Reduced maximum motor duty cycle to reduce power
MAX_DUTY_CYCLE_B = 20  # Increased power for motor B
SMOOTHING_FACTOR = 0.3  # Increased smoothing factor to reduce overshoot
STALL_THRESHOLD = 0.999  # Improved stall detection threshold
MOTION_TIMEOUT = 0.1  # Time in seconds before locking activation
RESET_POSITION_VALUE = 0  # Value to set when button OK is pressed

# PID parameters (adjusted to reduce overshoot)
KP_A, KI_A, KD_A = 0.5, 0.00002, 0.001  # For motor A
KP_B, KI_B, KD_B = 0.5, 0.00002, 0.001  # For motor B

# Initialize motors
motor_a = LargeMotor(OUTPUT_A)
motor_b = LargeMotor(OUTPUT_B)
motor_c = MediumMotor(OUTPUT_C)

# Initialize touch sensor
touch_sensor = TouchSensor(INPUT_1)
button = Button()

# State tracking variables
smoothed_duty_a = 0
smoothed_duty_b = 0
smoothed_duty_c = 0  # Inertia for motor C
lock_state_a = 0  # 0 = unlocked, 1 = locked
lock_state_b = 0  # 0 = unlocked, 1 = locked
last_movement_time_a = time.time()
last_movement_time_b = time.time()

prev_error_a, integral_a = 0, 0
prev_error_b, integral_b = 0, 0

# Inertia simulation smoothing factor for motor C
INERTIA_SMOOTHING_FACTOR = 0.5  # Adjust this factor for the desired inertia effect

def get_motor_positions():
    return motor_a.position, motor_b.position, motor_c.position

def get_motor_speeds():
    return motor_a.speed, motor_b.speed

# PID control function
def pid_control(error, prev_error, integral, kp, ki, kd, max_duty):
    integral += error * REFRESH_RATE
    derivative = (error - prev_error) / REFRESH_RATE
    output = kp * error + ki * integral + kd * derivative
    return max(min(output, max_duty), -max_duty), integral, error

# Function to push motor to zero degrees using PID control with inertia for motor C
def push_to_zero_pid():
    global smoothed_duty_a, smoothed_duty_b, smoothed_duty_c, lock_state_a, lock_state_b
    global last_movement_time_a, last_movement_time_b, prev_error_a, integral_a, prev_error_b, integral_b
    
    pos_a, pos_b, pos_c = get_motor_positions()
    speed_a, speed_b = get_motor_speeds()
    current_time = time.time()
    
    # Detect motion state and apply full force when out of range for motor A
    if abs(pos_a) > MAX_ANGLE_A:
        motor_a.duty_cycle_sp = MAX_DUTY_CYCLE_A * (-1 if pos_a > 0 else 1)
        motor_a.run_direct()
    elif abs(pos_a) <= DEADZONE:
        lock_state_a = 0
        motor_a.stop_action = "coast"
        motor_a.stop()
    elif abs(speed_a) > STALL_THRESHOLD:
        last_movement_time_a = current_time
    elif lock_state_a == 0 and (current_time - last_movement_time_a) > MOTION_TIMEOUT:
        lock_state_a = 1
    
    # Detect motion state and apply full force when out of range for motor B
    if abs(pos_b) > MAX_ANGLE_B:
        motor_b.duty_cycle_sp = MAX_DUTY_CYCLE_B * (-1 if pos_b > 0 else 1)
        motor_b.run_direct()
    elif abs(pos_b) <= DEADZONE:
        lock_state_b = 0
        motor_b.stop_action = "coast"
        motor_b.stop()
    elif abs(speed_b) > STALL_THRESHOLD:
        last_movement_time_b = current_time
    elif lock_state_b == 0 and (current_time - last_movement_time_b) > MOTION_TIMEOUT:
        lock_state_b = 1
    
    # Apply PID control based on lock state for motor A
    if lock_state_a:
        output_a, integral_a, prev_error_a = pid_control(-pos_a, prev_error_a, integral_a, KP_A, KI_A, KD_A, MAX_DUTY_CYCLE_A)
        smoothed_duty_a = smoothed_duty_a * SMOOTHING_FACTOR + output_a * (1 - SMOOTHING_FACTOR)
        motor_a.duty_cycle_sp = smoothed_duty_a
        motor_a.run_direct()
    
    # Apply PID control based on lock state for motor B
    if lock_state_b:
        output_b, integral_b, prev_error_b = pid_control(-pos_b, prev_error_b, integral_b, KP_B, KI_B, KD_B, MAX_DUTY_CYCLE_B)
        smoothed_duty_b = smoothed_duty_b * SMOOTHING_FACTOR + output_b * (1 - SMOOTHING_FACTOR)
        motor_b.duty_cycle_sp = smoothed_duty_b
        motor_b.run_direct()
    
    # Inertia simulation for motor C
    if abs(pos_c) > MAX_ANGLE_C:
        # Direct control when motor C exceeds the max angle (no inertia in this case)
        motor_c.duty_cycle_sp = 0
        motor_c.stop()
    else:
        # Apply inertia smoothing for motor C
        target_duty_c = 0  # Target is always zero for centering or your specific target value
        smoothed_duty_c = smoothed_duty_c * (1 - INERTIA_SMOOTHING_FACTOR) + target_duty_c * INERTIA_SMOOTHING_FACTOR
        motor_c.duty_cycle_sp = smoothed_duty_c
        motor_c.run_direct()

def check_button_press():
    if button.enter:
        motor_a.position = RESET_POSITION_VALUE
        motor_b.position = RESET_POSITION_VALUE
        motor_c.position = RESET_POSITION_VALUE

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))
server_socket.listen(5)

try:
    while True:
        client_socket, _ = server_socket.accept()
        
        while True:
            pos_a, pos_b, pos_c = get_motor_positions()
            touch_state = 1 if touch_sensor.is_pressed else 0
            
            # Invert the motor C position for sending over TCP
            inverted_pos_c = -pos_c
            
            # Send motor data with inverted motor C value
            data = "Motor A: {} degrees, Motor B: {} degrees, Motor C: {} degrees, Button: {}".format(pos_a, pos_b, inverted_pos_c, touch_state)
            try:
                client_socket.sendall(data.encode('utf-8'))
            except BrokenPipeError:
                break
            
            # Apply PID push to zero for motors A and B
            push_to_zero_pid()
            check_button_press()
            
            time.sleep(REFRESH_RATE)
except KeyboardInterrupt:
    pass
finally:
    server_socket.close()
