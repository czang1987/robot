#!/usr/bin/env python3
# File name   : move.py
# Description : Control Motor
# Product     : RaspTank  
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2019/02/23
import time
import RPi.GPIO as GPIO
import threading

# motor_EN_A: Pin7  |  motor_EN_B: Pin11
# motor_A:  Pin8,Pin10    |  motor_B: Pin13,Pin12

Motor_A_EN    = 4
Motor_B_EN    = 17

Motor_A_Pin1  = 26
Motor_A_Pin2  = 21
Motor_B_Pin1  = 27
Motor_B_Pin2  = 18

Dir_forward   = 0
Dir_backward  = 1

left_forward  = 1
left_backward = 0

right_forward = 0
right_backward= 1

pwn_A = 0
pwm_B = 0

class Motor(threading.Thread):
    def __init__(self,speed=50,radius=0.1):
        self.speed=speed
        self.pwm_A=None
        self.pwm_B=None
        self.setup()
        self.status='stop'
        super(Motor,self).__init__()
        self.__flag=threading.Event()
        self.__flag.clear()
        self.radius=radius
        
    
    def run(self):
        while 1:
            self.__flag.wait()
            if(self.status=='exit'): break
            self.process()
            pass


    def set_spread(self,speed):
        self.speed=speed

    def set_radius(self,radius):
        self.radius=radius

    def motorStop(self):#Motor stops
        GPIO.output(Motor_A_Pin1, GPIO.LOW)
        GPIO.output(Motor_A_Pin2, GPIO.LOW)
        GPIO.output(Motor_B_Pin1, GPIO.LOW)
        GPIO.output(Motor_B_Pin2, GPIO.LOW)
        GPIO.output(Motor_A_EN, GPIO.LOW)
        GPIO.output(Motor_B_EN, GPIO.LOW)


    def setup(self):#Motor initialization
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Motor_A_EN, GPIO.OUT)
        GPIO.setup(Motor_B_EN, GPIO.OUT)
        GPIO.setup(Motor_A_Pin1, GPIO.OUT)
        GPIO.setup(Motor_A_Pin2, GPIO.OUT)
        GPIO.setup(Motor_B_Pin1, GPIO.OUT)
        GPIO.setup(Motor_B_Pin2, GPIO.OUT)

        self.motorStop()
        try:
            self.pwm_A = GPIO.PWM(Motor_A_EN, 1000)
            self.pwm_B = GPIO.PWM(Motor_B_EN, 1000)
        except:
            pass


    def motor_left(self, status,direction,speed=None):#Motor 2 positive and negative rotation
        if(speed is None):  speed=self.speed

        if status == 0: # stop
            GPIO.output(Motor_B_Pin1, GPIO.LOW)
            GPIO.output(Motor_B_Pin2, GPIO.LOW)
            GPIO.output(Motor_B_EN, GPIO.LOW)
        else:
            if direction == Dir_backward:
                GPIO.output(Motor_B_Pin1, GPIO.HIGH)
                GPIO.output(Motor_B_Pin2, GPIO.LOW)
                self.pwm_B.start(100)
                self.pwm_B.ChangeDutyCycle(speed)
            elif direction == Dir_forward:
                GPIO.output(Motor_B_Pin1, GPIO.LOW)
                GPIO.output(Motor_B_Pin2, GPIO.HIGH)
                self.pwm_B.start(0)
                self.pwm_B.ChangeDutyCycle(speed)
        return direction


    def motor_right(self, status,direction ,speed=None):#Motor 1 positive and negative rotation
        if status == 0: # stop
            GPIO.output(Motor_A_Pin1, GPIO.LOW)
            GPIO.output(Motor_A_Pin2, GPIO.LOW)
            GPIO.output(Motor_A_EN, GPIO.LOW)
        else:
            if(speed is None):  speed=self.speed
            if direction == Dir_forward:#
                GPIO.output(Motor_A_Pin1, GPIO.HIGH)
                GPIO.output(Motor_A_Pin2, GPIO.LOW)
                self.pwm_A.start(100)
                self.pwm_A.ChangeDutyCycle(speed)
            elif direction == Dir_backward:
                GPIO.output(Motor_A_Pin1, GPIO.LOW)
                GPIO.output(Motor_A_Pin2, GPIO.HIGH)
                self.pwm_A.start(0)
                self.pwm_A.ChangeDutyCycle(speed)
        return direction

    def resume(self):
        self.__flag.set()

    def move_forward(self):        
        self.status='forward'
        self.resume()

    def _move_forward(self):
        self.motor_left(1, left_forward, self.speed)
        self.motor_right(1, right_forward, self.speed)

    def move_backward(self):
        self.status='backward'
        self.resume()

    def _move_backward(self):
        self.motor_left(1, left_backward, self.speed)
        self.motor_right(1, right_backward, self.speed)

    def turn_right(self):
        self.status='turn_right'
        self.resume()

    def _turn_right(self):
        self.motor_left(1, left_forward, self.speed)
        self.motor_right(1, right_forward, self.speed*self.radius)

    def turn_left(self):
        self.status='turn_left'
        self.resume()

    def _turn_left(self):
        self.motor_left(1, left_forward, self.speed*self.radius)
        self.motor_right(1, right_forward, self.speed)
    
    def stop(self): 
        self.status='stop'

        self.resume()

    def exit(self):
        self.status='exit'
        self.resume()

    def process(self):
        if(self.status=='stop'):        
            self.motorStop()
            self.__flag.clear()
        elif(self.status=='forward'):   self._move_forward()
        elif(self.status=='backward'):   self._move_backward()
        elif(self.status=='turn_right'):   self._turn_right()
        elif(self.status=='turn_left'):   self._turn_left()


def move(speed, direction, turn, radius=0.6):   # 0 < radius <= 1  
    #speed = 100
    if direction == 'forward':
        if turn == 'right':
            print("working");
            motor_left(0, left_backward, int(speed*radius))
            motor_right(1, right_forward, speed)
        elif turn == 'left':
            motor_left(1, left_forward, speed)
            motor_right(0, right_backward, int(speed*radius))
        else:
            motor_left(1, left_forward, speed)
            motor_right(1, right_forward, speed)
    elif direction == 'backward':
        if turn == 'right':
            motor_left(0, left_forward, int(speed*radius))
            motor_right(1, right_backward, speed)
        elif turn == 'left':
            motor_left(1, left_backward, speed)
            motor_right(0, right_forward, int(speed*radius))
        else:
            motor_left(1, left_backward, speed)
            motor_right(1, right_backward, speed)
    elif direction == 'no':
        if turn == 'right':
            motor_left(1, left_backward, speed)
            motor_right(1, right_forward, speed)
        elif turn == 'left':
            motor_left(1, left_forward, speed)
            motor_right(1, right_backward, speed)
        else:
            motorStop()
    else:
        pass




def destroy():
    motorStop()
    GPIO.cleanup()             # Release resource


if __name__ == '__main__':
    motor=Motor(100)
    motor.start()
    motor.move_forward()
    time.sleep(10)
    motor.stop()
    motor.exit()

    print("done")
    

