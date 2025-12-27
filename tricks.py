import time
start=time.ticks_ms()

for  i in range(1000):
    print(i)
    
delta=time.ticks_diff(time.ticks_ms(),start)
print("after loop"+str(delta)+"ms")
