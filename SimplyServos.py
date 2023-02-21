# Pico Kitronik Simply Servos 
# Uses the PIO state machines to drive a servo.
# This is the Micro Python version. 
from machine import Pin
from rp2 import PIO, StateMachine, asm_pio

# List of which StateMachines we have used
usedSM = [False, False, False, False, False, False, False, False]

class KitronikSimplyServos:
    #Servo 0 degrees -> pulse of 0.5ms, 180 degrees 2.5ms
    #pulse train freq 50hz - 20mS
    #1uS is freq of 1000000
    #servo pulses range from 500 to 2500usec and overall pulse train is 20000usec repeat.
    #servo pins on the Simply Servos board are: GP2, GP3, GP4, GP5, GP6, GP7, GP8, GP9 for servos 1-8 in order
    maxServoPulse = 2500
    minServoPulse = 500
    pulseTrain = 20000
    degreesToUS = 2000/180
    
    #this code drives a pwm on the PIO. It is running at 2Mhz, which gives the PWM a 1uS resolution. 
    @asm_pio(sideset_init=PIO.OUT_LOW)
    def _servo_pwm():
    #first we clear the pin to zero, then load the registers. Y is always 20000 - 20uS, x is the pulse 'on' length.     
        pull(noblock) .side(0)
        mov(x, osr) # Keep most recent pull data stashed in X, for recycling by noblock
        mov(y, isr) # ISR must be preloaded with PWM count max
    #This is where the looping work is done. the overall loop rate is 1Mhz (clock is 2Mhz - we have 2 instructions to do)    
        label("loop")
        jmp(x_not_y, "skip") #if there is 'excess' Y number leave the pin alone and jump to the 'skip' label until we get to the X value
        nop()         .side(1)
        label("skip")
        jmp(y_dec, "loop") #count down y by 1 and jump to pwmloop. When y is 0 we will go back to the 'pull' command
             
    #simply stops and starts the servo PIO, so the pin could be used for soemthing else.
    def registerServo(self,servo):
        if(not self.servos[servo].active()):
            self.servos[servo].active(1)

    def deregisterServo(self, servo):
        if(self.servos[servo].active()):
            self.servos[servo].active(0)
 
    # goToPosition takes a degree position for the servo to goto. 
    # 0degrees->180 degrees is 0->2000us, plus offset of 500uS
    #1 degree ~ 11uS.
    #This function does the sum then calls goToPeriod to actually poke the PIO 
    def goToPosition(self,servo, degrees):
        pulseLength = int(degrees*self.degreesToUS + 500)
        self.goToPeriod(servo,pulseLength)
    
    def goToPeriod(self,servo, period):
        if(period < 500):
            period = 500
        if(period >2500):
            period =2500
        #check if servo SM is active, otherwise we are trying to control a thing we do not have control over
        if self.servos[servo].active():
            self.servos[servo].put(period)
        else:
            raise Exception("TRYING TO CONTROL UNREGISTERED SERVO") #harsh, but at least you'll know

    #Class initialisation
    #defaults to the standard pins and freq for the kitronik board, but could be overridden
    def __init__(self, numberOfServos = 8):
        servoPins = [2,3,4,5,6,7,8,9]
        self.servos = []
        #connect the servos by default on construction - advanced uses can disconnect them if required.
        for i in range(numberOfServos):
            for j in range(8): # StateMachine range from 0 to 7
                if usedSM[i]:
                    continue # Ignore this index if already used
                try:
                    self.servos.append(StateMachine(j, self._servo_pwm, freq=2000000, sideset_base=Pin(servoPins[i])))
                    usedSM[i] = True # Set this index to used
                    break # Have claimed the SM, can leave now
                except ValueError:
                    pass # External resouce has SM, move on
                if i == 7:
                    # Cannot find an unused SM
                    raise ValueError("Could not claim a StateMachine, all in use")
                
            self.servos[i].put(self.pulseTrain)
            self.servos[i].exec("pull()")
            self.servos[i].exec("mov(isr, osr)")
            # Pre set X to be half of a full pulse (90 degrees)
            self.servos[i].put(1500) # Change this between 500 to 2500 for 0 to 180 degrees initial position
            self.registerServo(i)
      
