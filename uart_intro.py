from machine import UART
import time
uart=UART(0,9600)
command=[]
shells='\r\n>'

def clrscr():
    uart.write(b'\x1b[2J\x1b[H')
    
def printc(message):
   uart.write(b'\x1b[31m' + message.encode('utf-8') + b'\x1b[0m')

def welcome():
    printc("Eswaraprasath's laptop")
    
def shell():
    uart.write(shells.encode())
    
def process(message):
    if message=="hello":
        uart.write("Hai how are you")
        shell()
    elif message=="freq":
        fr=str(machine.freq())
        uart.write(fr.encode())
        shell()
    else:
        uart.write("Invalid command")
        shell()
        

clrscr()
welcome()
shell()
while True:
    if uart.any()==True:
        buff=uart.read(1)
        if buff.decode()=='\r':
            shell()
            print(command)
            result = "".join(command)
            process(result)
            command=[]
        elif buff.decode()=='\x08':
            command.pop()
        else:
            uart.write(buff.decode())
            command.append(buff.decode())
        