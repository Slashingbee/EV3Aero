import pyxinput

controller = pyxinput.vController()
controller.set_value('AxisRx', 0.5)  # Move rudder axis
controller.set_value('TriggerL', 1)  # Press throttle
controller.set_value('BtnB', 1)  # Press fire button
