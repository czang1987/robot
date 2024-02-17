#!/usr/bin/env python3
# File name   : servo.py
# Description : Control Motor
# Product     : RaspRover
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2019/02/23
from __future__ import division
import time
import RPi.GPIO as GPIO
import sys
import Adafruit_PCA9685
import numpy as np
'''
change this form 1 to 0 to reverse servos
'''
class Servos:
    def __init__(self):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)

        self.look_max = 500
        self.look_min = 100

        self.org_pos = 300
        self.look_direction=True
#        self.clean_all()


    def ctrl_range(self,raw, max_genout, min_genout):
        print(raw,min_genout,max_genout)
        raw=np.clip(raw,min_genout,max_genout)
        print(raw)
        return int(raw)
        '''
        if raw > self.max_genout:
            raw_output = self.max_genout
        elif raw < min_genout:
            raw_output = min_genout
        else:
            raw_output = raw
        return int(raw_output)
        '''


    def camera_ang(self,direction, ang=50):
        print(direction)
        if self.look_direction:
            if direction == 'lookdown':
                self.org_pos+=ang
                self.org_pos = self.ctrl_range(self.org_pos, self.look_max, self.look_min)      
            elif direction == 'lookup':
                self.org_pos-=ang
                self.org_pos = self.ctrl_range(self.org_pos, self.look_max, self.look_min)
            elif direction == 'home':
                self.org_pos = 300
        else:
            if direction == 'lookdown':
                self.org_pos-=ang
                self.org_pos = self.ctrl_range(self.org_pos, self.look_max, self.look_min)
            elif direction == 'lookup':
                self.org_pos+=ang
                self.org_pos = self.ctrl_range(self.org_pos, self.look_max, self.look_min)
            elif direction == 'home':
                self.org_pos = 300  

        self.pwm.set_all_pwm(0,self.org_pos)


    def clean_all(self):
        self.pwm.set_all_pwm(0, 0)


if __name__ == '__main__':
    servos=Servos()
    servos.camera_ang("lookdown")
