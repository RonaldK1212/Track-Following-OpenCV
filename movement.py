import RPi.GPIO as GPIO
import time



def setup_motors(motorLP, motorLN, motorRP, motorRN, pwmFreq):
    GPIO.setmode(GPIO.BCM)
    motorPins = [motorLP, motorLN, motorRP, motorRN]
    for motor in motorPins:
        GPIO.setup(motor, GPIO.OUT)
        
    return motorPins

def setup_pwm():
    motorL_pwm = GPIO.PWM(motorLP, pwmFreq)
    motorR_pwm = GPIO.PWM(motorRP, pwmFreq)
    
    return motorL_pwm, motorR_pwm

def set_motor_speed(speed, motor):
    if speed < 0:
        speed = 100+speed
        if motor == 'L':
            GPIO.output(motorLN, 1)
            motorL_pwm.start(speed)
        elif motor == 'R':
            GPIO.output(motorRN, 1)
            motorR_pwm.start(speed)
    else:
        # Forward direction
        if motor == 'L':
            GPIO.output(motorLN, 0)
            motorL_pwm.start(speed)
        elif motor == 'R':
            GPIO.output(motorRN, 0)
            motorR_pwm.start(speed)


def move_servo(angle):
    # Calculate the duty cycle based on the angle
    dutyCycle = angle / 18.0 + 2.5

    # Start the PWM signal
    servoPwm.start(dutyCycle)

def forward(speed):
    set_motor_speed(speed, 'L')
    set_motor_speed(speed, 'R')
def backward(speed):
    set_motor_speed(-speed, 'L')
    set_motor_speed(-speed, 'R')
def steer_left():
    move_servo(0)
def steer_right():
    move_servo(180)

def steer_forward():
    move_servo(95)

def stop_moving():
    set_motor_speed(0, 'L')
    set_motor_speed(0, 'R')
    move_servo(95)



pwmFreq = 50

servoPin = 4
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# Set the pin as an output
GPIO.setup(servoPin, GPIO.OUT)

# Create a PWM object for the servo
servoPwm = GPIO.PWM(servoPin, pwmFreq)


motorLP, motorLN, motorRP, motorRN = setup_motors(27, 17, 23, 24, pwmFreq)

motorL_pwm, motorR_pwm = setup_pwm()
    
    
    
if __name__ == "__main__":
    try:        
        # creating display
        
        
        speed = 35
        steer_left()
        forward(speed)
        time.sleep(1)
        stop_moving()
        
    finally:
        GPIO.cleanup()
