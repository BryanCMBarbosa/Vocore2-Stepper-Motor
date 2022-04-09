'''
library is public domain. Enjoy!
Made by Bryan Barbosa (Github: BryanCMBarbosa) from Federal University of Juiz de Fora and CREA Lab - UC Berkeley
'''

from vocoreGPIO import *

class stepper:
    def __init__(self, direction_pin, direction, step_pin, steps_per_revolution, enable_pin = -1, enable_on=False, pulse_width=5, driver="drv8825", micro_stepping=1, micro_stepping_pins=()):
        self.direction_pin = direction_pin
        self.direction = direction
        self.step_pin = step_pin
        self.steps_per_revolution = steps_per_revolution
        self.enable_pin = enable_pin
        self.enable_on = enable_on
        self.pulse_width = pulse_width
        self.driver = driver
        self.micro_stepping = micro_stepping
        self.micro_stepping_pins = micro_stepping_pins
        self.micro_stepping_on = False

        self.setup_pins()

    def setup_pins(self): #Initial pin setup for mode and state for direction, step and enable
        pinMode(self.direction_pin, True)
        pinMode(self.step_pin, True)

        if self.micro_stepping != 1 and len(self.micro_stepping_pins) != 0:
            for i in self.micro_stepping_pins: #Sets each of the micro stepping pins as OUTPUT
                pinMode(i, True)

        digitalWrite(self.direction_pin, self.direction)
        digitalWrite(self.step_pin, False)

        if self.enable_pin != -1:
            pinMode(self.enable_pin, True)
            digitalWrite(self.enable_pin, self.enable_on)

    def turn_off_microstepping(self): #Turns off the pins attached to microstepping ports on driver
        if self.micro_stepping_on:
            for pin in self.micro_stepping_pins:#Sets each of the micro stepping pins signal as LOW
                digitalWrite(pin, False)
        
            self.micro_stepping_on = False

    def setup_micro_stepping(self): #Sets up the microstepping configuration according to the microstepping fraction and the driver model setted
        if self.driver.lower() == "drv8825" or self.driver.lower() == "drv8824":
            self.setup_drv8825_drv8824()
        elif self.driver.lower() == "a4988":
            self.setup_a4988()
        elif self.driver.lower() == "tmc2208":
            self.setup_tmc2208()
        
        self.micro_stepping_on = True

    def setup_drv8825_drv8824(self): #Microstepping configuration for DRV8825 and DRV8824
        if self.micro_stepping == 2:
            digitalWrite(self.micro_stepping_pins[0], True)
            digitalWrite(self.micro_stepping_pins[1], False)
            digitalWrite(self.micro_stepping_pins[2], False)
        elif self.micro_stepping == 4:
            digitalWrite(self.micro_stepping_pins[0], False)
            digitalWrite(self.micro_stepping_pins[1], True)
            digitalWrite(self.micro_stepping_pins[2], False)
        elif self.micro_stepping == 8:
            digitalWrite(self.micro_stepping_pins[0], True)
            digitalWrite(self.micro_stepping_pins[1], True)
            digitalWrite(self.micro_stepping_pins[2], False)
        elif self.micro_stepping == 16:
            digitalWrite(self.micro_stepping_pins[0], False)
            digitalWrite(self.micro_stepping_pins[1], False)
            digitalWrite(self.micro_stepping_pins[2], True)
        elif self.micro_stepping == 32:
            digitalWrite(self.micro_stepping_pins[0], True)
            digitalWrite(self.micro_stepping_pins[1], False)
            digitalWrite(self.micro_stepping_pins[2], True)
        else:
            digitalWrite(self.micro_stepping_pins[0], False)
            digitalWrite(self.micro_stepping_pins[1], False)
            digitalWrite(self.micro_stepping_pins[2], False)

    def setup_a4988(self): #Microstepping configuration for A4988
        if self.micro_stepping == 2:
            digitalWrite(self.micro_stepping_pins[0], True)
            digitalWrite(self.micro_stepping_pins[1], False)
            digitalWrite(self.micro_stepping_pins[2], False)
        elif self.micro_stepping == 4:
            digitalWrite(self.micro_stepping_pins[0], False)
            digitalWrite(self.micro_stepping_pins[1], True)
            digitalWrite(self.micro_stepping_pins[2], False)
        elif self.micro_stepping == 8:
            digitalWrite(self.micro_stepping_pins[0], True)
            digitalWrite(self.micro_stepping_pins[1], True)
            digitalWrite(self.micro_stepping_pins[2], False)
        elif self.micro_stepping == 16:
            digitalWrite(self.micro_stepping_pins[0], True)
            digitalWrite(self.micro_stepping_pins[1], True)
            digitalWrite(self.micro_stepping_pins[2], True)
        else:
            digitalWrite(self.micro_stepping_pins[0], False)
            digitalWrite(self.micro_stepping_pins[1], False)
            digitalWrite(self.micro_stepping_pins[2], False)

    def setup_tmc2208(self): #Microstepping configuration for TMC2208
        if self.micro_stepping == 2:
            digitalWrite(self.micro_stepping_pins[0], True)
            digitalWrite(self.micro_stepping_pins[1], False)
        elif self.micro_stepping == 4:
            digitalWrite(self.micro_stepping_pins[0], False)
            digitalWrite(self.micro_stepping_pins[1], True)
        elif self.micro_stepping == 16:
            digitalWrite(self.micro_stepping_pins[0], True)
            digitalWrite(self.micro_stepping_pins[1], True)
        else:  #The default for TMC2208 is microstepping at 1/8
            digitalWrite(self.micro_stepping_pins[0], False)
            digitalWrite(self.micro_stepping_pins[1], False)
            self.micro_stepping = 8

    def step(self, number_of_steps=1): #Sends a command to the motor to rotate a number of steps passed through parameter (pre-setted as 1)
        if self.enable_on:
            print("Turn off enable before sending step commands.")
        else:
            digitalWrite(self.direction_pin, self.direction)
            if self.micro_stepping != 1 and self.micro_stepping_on:
                self.setup_micro_stepping()

            for i in range(number_of_steps):
                digitalWrite(self.step_pin, True)
                delay(self.pulse_width)
                digitalWrite(self.step_pin, False)
                delay(self.pulse_width)
        
            self.turn_off_microstepping()

    def turn_xdegrees(self, degrees=360): #Sends a command to the motor to rotate an specific angle
        steps = ((self.steps_per_revolution * self.micro_stepping) * degrees) / 360
        self.step(steps)

    def toggle_direction(self): #Toggle the direction setted for rotation
        digitalWrite(self.direction_pin, not digitalRead(self.direction_pin))

    def toggle_enable(self): #Toggle the enable pin state
        if self.enable_pin != -1:
            digitalWrite(self.enable_pin, not digitalWrite(self.enable_pin))

            if digitalRead(self.enable_pin) == "1":
                self.enable_on = True
            else:
                self.enable_on = False
        else:
            print("Enable pin not defined.")