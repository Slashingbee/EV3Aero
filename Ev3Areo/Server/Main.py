import socket
import pygame
import sys
import time
import vgamepad as vg  # Import vgamepad

def get_motor_positions(ip_address, port, retries=60, delay=0.5):
    """Attempts to receive motor positions from the specified IP and port."""
    for attempt in range(retries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip_address, port))
                data = s.recv(1024)
                received_str = data.decode()
                # Parse the motor positions and touch state
                pos_a_degrees = received_str.split(",")[0].split(":")[1].strip().split()[0]
                pos_b_degrees = received_str.split(",")[1].split(":")[1].strip().split()[0]
                pos_c_degrees = received_str.split(",")[2].split(":")[1].strip().split()[0]
                touch_state = received_str.split(",")[3].split(":")[1].strip()
                return pos_a_degrees, pos_b_degrees, pos_c_degrees, touch_state
        except (IndexError, ValueError, socket.error) as e:
            print(f"Error receiving motor positions (attempt {attempt + 1}/{retries}): {e}")
            time.sleep(delay)
    return "N/A", "N/A", "N/A", "N/A"

def main():
    ip_address = 'EV3-IP'  #  [LOCAL] IP of the device sending motor data (replaced random local ip with placeholder). (if using custom connection might not be needed)
    port = 12345  # Port to connect to (default port).

    # Set limits for motor positions
    limit_a = 40  
    limit_b = 45  
    limit_c = 50  

    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption('Motor Positions')
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    # Initialize vGamepad (Xbox 360 Controller)
    gamepad = vg.VX360Gamepad()
    print("vGamepad initialized!")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pos_a_degrees, pos_b_degrees, pos_c_degrees, touch_state = get_motor_positions(ip_address, port)

        if pos_a_degrees != "N/A":
            pos_a_degrees = max(min(float(pos_a_degrees), limit_a), -limit_a)
        if pos_b_degrees != "N/A":
            pos_b_degrees = max(min(float(pos_b_degrees), limit_b), -limit_b)
        if pos_c_degrees != "N/A":
            pos_c_degrees = max(min(float(pos_c_degrees), limit_c), -limit_c)

        # Scale motor positions to joystick axis range (-32768 to 32767)
        scaled_pos_a = int((float(pos_a_degrees) / limit_a) * 32767)
        scaled_pos_b = int((float(pos_b_degrees) / limit_b) * 32767)

        # Scale motor C to right joystick Y-axis (-32768 to 32767)
        if pos_c_degrees == "N/A":
            scaled_pos_c = 0  # Default to center if data is invalid
        else:
            scaled_pos_c = int((float(pos_c_degrees) / limit_c) * 32767)

        # Send values to virtual gamepad
        gamepad.left_joystick(x_value=scaled_pos_a, y_value=scaled_pos_b)  # Left joystick
        gamepad.right_joystick(x_value=0, y_value=scaled_pos_c)  # Right joystick Y-axis

        # Set button state
        if touch_state == "1":
            gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        else:
            gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)

        gamepad.update()  # Apply changes to virtual controller

        # Display motor positions on screen
        screen.fill((255, 255, 255))
        text_a = font.render(f"Motor A Position: {pos_a_degrees} degrees", True, (0, 0, 0))
        text_b = font.render(f"Motor B Position: {pos_b_degrees} degrees", True, (0, 0, 0))
        text_c = font.render(f"Motor C Position: {pos_c_degrees} degrees", True, (0, 0, 0))
        text_touch = font.render(f"Button State: {touch_state}", True, (0, 0, 0))
        screen.blit(text_a, (20, 50))
        screen.blit(text_b, (20, 100))
        screen.blit(text_c, (20, 150))
        screen.blit(text_touch, (20, 200))

        pygame.display.flip()
        clock.tick(1000)  # Update every 1 millisecond

if __name__ == "__main__":
    main()
