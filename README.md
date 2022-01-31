# Kitronik-Pico-Simply-Servos-MicroPython
A class and example code to use the Kitronik Simply Servos board for Raspberry Pi Pico. (www.kitronik.co.uk/5339)

This is the microPython version. For CircuitPython see: https://github.com/KitronikLtd/Kitronik-Pico-Simply-Servos-CircuitPython

To use save SimpyServos.py file onto the Pico so it can be imported

## Import SimplyServos.py and construct an instance:
    import SimplyServos
    board = SimplyServos.KitronikSimplyServos()

This will initialise the PIO and set them to drive the servo pins.

## Drive a Servo by degrees:
    board.goToPosition(servo, degrees)
where:
* servo => 1 to 8
* degrees => 0-180

## Drive a Servo by pulse width:
    board.goToPeriod(servo, period)
where:
* servo => 1 to 8
* period => 500 - 2500 
	period is the pulse width in microseconds


This code is designed to be used as a module. See: https://kitronik.co.uk/blogs/resources/modules-micro-python-and-the-raspberry-pi-pico for more information
