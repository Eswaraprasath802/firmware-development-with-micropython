from machine import Timer
import time

def track(timer):
    print("I am in timer()")

def recurring(timer):
    print("I am in recurring()")
    
tracker= Timer()
tim = Timer()
tracker.init(period=2000, mode=Timer.PERIODIC, callback=track)
tim.init(period=5000, mode=Timer.PERIODIC, callback=recurring)

while True:
    time.sleep(2)
    print("hai")