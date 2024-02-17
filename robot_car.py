
from robot.util.robotLight import RobotLight
from robot.util.move import Motor
import threading,time

class RobotCar():
    def __init__(self,speed=50):
        self.light=RobotLight()
        self.light.start()
        self.motor=Motor(speed,0.01)
        self.motor.start()

    def test(self,mode):
        if(mode=='breath_on'): self.light.breath(70,70,255)
        elif(mode=='light_off'):  self.light.pause()
        elif(mode=='move_forward'):  self.motor.move_forward()
        elif(mode=='stop'):   self.motor.stop()
        elif(mode=='move_backward'):  self.motor.move_backward()
        elif(mode=='turn_right'):   self.motor.turn_right()
        elif(mode=='turn_left'):   self.motor.turn_left()
        elif(mode=='exit'):   
            self.motor.exit()
            self.light.exit()







if __name__=='__main__':
    car=RobotCar(60)
    t=10
    car.test("breath_on")
    car.test("move_backward")
    time.sleep(5)
    car.test("move_forward")
    time.sleep(5)
    car.test("stop")
    car.test("light_off")
    car.test('exit')
    '''
    car.test("turn_right");
    time.sleep(t)
    car.test("turn_left");
    time.sleep(t)
    car.test("move_backward")
    time.sleep(t)
    car.test("stop")
    car.test("light_off")
    car.test('exit')
    '''
