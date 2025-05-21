import socket
import pygame
import sys
import time
import vgamepad as vg

def get_motor_positions(ip_address, port, retries=3, delay=2):
    for attempt in range(retries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip_address, port))
                data = s.recv(1024)
                received_str = data.decode()
                pos_a_degrees = received_str.split(",")[0].split(":")[1].strip().split()[0]
                pos_b_degrees = received_str.split(",")[1].split(":")[1].strip().split()[0]
                touch_state = received_str.split(",")[2].split(":")[1].strip()
                return pos_a_degrees, pos_b_degrees, touch_state
        except (IndexError, ValueError, socket.error) as e:
            print(f"Error receiving motor positions (attempt {attempt + 1}/{retries}): {e}")
            time.sleep(delay)
    return "N/A", "N/A", "N/A"

def main():
    ip_address = 'Brick-IP'  # Replace with the actual IP address of the device
    port = 12345  # Replace with the appropriate port number

    # Set limits for motor positions
    limit_a = 180  # Set the limit for motor A degrees
    limit_b = 180  # Set the limit for motor B degrees

    # Set centering force
    centering_force = 0.01  # Adjust this value to change the centering force

    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption('Motor Positions')
    font = pygame.font.Font(None, 36)

    clock = pygame.time.Clock()

    # Initialize VGamepad device
    gamepad = vg.VX360Gamepad()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pos_a_degrees, pos_b_degrees, touch_state = get_motor_positions(ip_address, port)

        # Apply limits to motor positions
        if pos_a_degrees != "N/A":
            pos_a_degrees = max(min(float(pos_a_degrees), limit_a), -limit_a)
            # Apply centering force
            if pos_a_degrees > 0:
                pos_a_degrees -= centering_force
            elif pos_a_degrees < 0:
                pos_a_degrees += centering_force

        if pos_b_degrees != "N/A":
            pos_b_degrees = max(min(float(pos_b_degrees), limit_b), -limit_b)
            # Apply centering force
            if pos_b_degrees > 0:
                pos_b_degrees -= centering_force
            elif pos_b_degrees < 0:
                pos_b_degrees += centering_force

        # Scale motor positions to the range -32768 to 32767
        scaled_pos_a = int((float(pos_a_degrees) / limit_a) * 32767)
        scaled_pos_b = int((float(pos_b_degrees) / limit_b) * 32767)

        # Set VGamepad device axes
        gamepad.left_joystick(x_value=scaled_pos_a, y_value=scaled_pos_b)

        # Set VGamepad button state
        if touch_state == "1":
            gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        else:
            gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)

        gamepad.update()
        
        screen.fill((255, 255, 255))
        text_a = font.render(f"Motor A Position: {pos_a_degrees} degrees", True, (0, 0, 0))
        text_b = font.render(f"Motor B Position: {pos_b_degrees} degrees", True, (0, 0, 0))
        text_touch = font.render(f"Button State: {touch_state}", True, (0, 0, 0))
        screen.blit(text_a, (20, 100))
        screen.blit(text_b, (20, 150))
        screen.blit(text_touch, (20, 200))

        pygame.display.flip()
        clock.tick(100)  # Update the display every 10 milliseconds

if __name__ == "__main__":
    main()