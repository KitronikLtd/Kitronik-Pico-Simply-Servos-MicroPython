#example usage of the Simply Servos class - sets all servos to 0 then 180

from SimplyServos import KitronikSimplyServos
from time import sleep

servos = KitronikSimplyServos()

while True:
    for i in range(1, 9):
        servos.goToPosition(i,0)
    sleep(1)
    for i in range(1, 9):
        servos.goToPosition(i,180)
    sleep(1)
