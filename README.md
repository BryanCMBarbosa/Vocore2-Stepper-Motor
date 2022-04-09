# Vocore 2 Stepper Motor Python Library

Made by Bryan Barbosa from [Federal University of Juiz de Fora](https://ufjf.br/) and [CREA - University of California, Berkeley](https://crea.berkeley.edu/).

## Importing
The library can be used by simply importing the Python file to your project.

```python
import vocoreStepperMotor
```
For an easier control, we recommend to import as:
```python
from vocoreStepperMotor import *
```

## Usage
The usage of the library is simple. For a basic use, we only have to set direction (1, for one side, or 0, for another), the attached pins for step and direction, and the number of steps per revolution. The pulse width of the steps is setted as 5 milliseconds, by default. See this example for a DRV2588 driver without microstepping:

```python
from vocoreStepperMotor import *

#Define the pins attached to the driver:
direction_pin = 40
step_pin = 41

#Define the direction
direction = 1

#Define the number of steps for revolution according to the Stepper Motor specs
steps_per_revolution = 200

#Create an object Stepper Motor
sm = stepper(direction_pin, direction, step_pin, steps_per_revolution)

#Now, our Stepper Motor is ready:
delay(2000) #Wait for 2 seconds
sm.turn_xdegrees(90) #Sends a command to the Stepper Motor to turn 90 degrees
delay(2000) #Wait for 2 seconds
sm.toggle_direction() #Invert the motor revolution direction
sm.turn_xdegrees(90) #Sends a command to the Stepper Motor to turn 90 degrees, now, to the other side
delay(2000) #Wait for 2 seconds
sm.turn_xdegrees(360) #Sends a command to the Stepper Motor to turn a full revolution
```

It's not complex either if you want to use other features such as microstepping, the enable pin and change the driver model:

```python
from vocoreStepperMotor import *

#Define the pins attached to the driver:
direction_pin = 40
step_pin = 41
enable_pin = 39

#Define the direction
direction = 0 

#Define the number of steps for revolution according to the Stepper Motor specs
steps_per_revolution = 200

#Define if you want to start the enable pin turned on, True turns off the driver, False keep it turned on. It can be changed by using the method ".toggle_enable()"
enable_on = False

#Define the pulse width
pulse_width = 10

#Define the driver model, by default we are using "DRV8825", which the configuration also works for "DRV8824".Currently we have also available the driver models A4988 and TMC2208
driver = "TMC2208"

#Define the microstepping fraction by setting the denominator, e.g., micro_stepping = 16 means 1/16 micro_stepping config.
micro_stepping = 16

#Define the microstepping pins. ATTENTION: TMC2208 has TWO microstepping pins on legacy mode. DRV8825, DRV8824 and A4988 have THREE microstepping pins. Since this example is setting up microstepping for TMC2208, we set a tuple of only TWO elements, which are the pins attached to the microstepping ports on the driver.
micro_stepping_pins = (12, 13)

#Create an object Stepper Motor
sm = stepper(step_pin, direction_pin, direction, enable_pin, enable_on, pulse_width, driver, micro_stepping, micro_stepping_pins)

#Now, our Stepper Motor is ready:
delay(2000) #Wait for 2 seconds
sm.turn_xdegrees(90) #Sends a command to the Stepper Motor to turn 90 degrees
delay(2000) #Wait for 2 seconds
sm.toggle_direction() #Invert the motor revolution direction
sm.turn_xdegrees(90) #Sends a command to the Stepper Motor to turn 90 degrees, now, to the other side
delay(2000) #Wait for 2 seconds
sm.turn_xdegrees(360) #Sends a command to the Stepper Motor to turn a full revolution
```

### More about the driver models and microstepping
The stepper motor driver models available are:
- DRV8825
- DRV8824
- A4988
- TMC2208 (legacy mode)

When setting microstepping, pay attention to the number of pins used for microstepping in each driver model. TMC2208 only uses two pins on legacy mode. DRV8825, DRV8824 and A4988 use three pins.
The order of pins declaration inside the tuple matters, so attach and declare following the schema:
#### DRV8825 and DRV8824
```python
micro_stepping = (12, 13, 14)
```
micro_stepping[0] ----- MODE0 (M0)

micro_stepping[1] ----- MODE1 (M1)

micro_stepping[2] ----- MODE2 (M2)

#### A4988
```python
micro_stepping = (12, 13, 14)
```
micro_stepping[0] ----- MS1

micro_stepping[1] ----- MS2

micro_stepping[2] ----- MS3

#### TMC2208
```python
micro_stepping = (12, 13)
```
micro_stepping[0] ----- MS1

micro_stepping[1] ----- MS2

You can add support to other stepper motor drivers by making a pull request!
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
