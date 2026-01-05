from machine import UART, freq
import time

uart = UART(0, 9600, timeout=10)

command_buf = []
history = []
history_index = 0

ESC = '\x1b'
FULL_PROMPT = '\r\n> '
INLINE_PROMPT = '> '

RESET   = f"{ESC}[0m"
RED     = f"{ESC}[31m"
GREEN   = f"{ESC}[32m"
YELLOW  = f"{ESC}[33m"
CYAN    = f"{ESC}[36m"
WHITE   = f"{ESC}[37m"

def printc(message, color=GREEN):
    uart.write(color.encode())
    uart.write(message.encode())
    uart.write(RESET.encode())

def welcome():
    printc("Welcome to Selfmade Ninja Academy\r\n", YELLOW)

def clear_screen():
    uart.write(b'\x1b[2J\x1b[H')

def shell_prompt():
    uart.write(FULL_PROMPT.encode())

def shell_prompt_inline():
    uart.write(INLINE_PROMPT.encode())

def cmd_hello():
    printc("HELLO\r\n")

def cmd_freq():
    printc(str(freq()) + "\r\n")

def cmd_help():
    printc("Available commands:\r\n", CYAN)
    for cmd in commands:
        printc(f"  - {cmd}\r\n", WHITE)

def cmd_clear():
    clear_screen()

commands = {
    "hello": cmd_hello,
    "freq":  cmd_freq,
    "help":  cmd_help,
    "clear": cmd_clear,
}

def command_exec(command):
    global history_index
    uart.write(b"\r\n")

    if command in commands:
        commands[command]()
    else:
        printc(f"Invalid Command: {command}\r\n", RED)

    if command.strip():
        if not history or history[-1] != command:
            history.append(command)

    history_index = len(history)

clear_screen()
welcome()
shell_prompt()

while True:
    if not uart.any():
        continue

    ch_bytes = uart.read(1)
    if not ch_bytes:
        continue

    try:
        ch = ch_bytes.decode()
    except:
        continue

    # ENTER
    if ch in ('\r', '\n'):
        cmd = "".join(command_buf)
        command_exec(cmd)
        command_buf = []
        shell_prompt()

    # BACKSPACE (BS or DEL)
    elif ch in ('\x08', '\x7f'):
        if command_buf:
            command_buf.pop()
            uart.write(b'\b \b')

    # ESCAPE SEQUENCES
    elif ch == '\x1b':
        seq = uart.read(2)
        if not seq or len(seq) < 2:
            continue

        if seq == b'[A':  # UP
            if history:
                history_index = max(0, history_index - 1)
                command_buf = list(history[history_index])
                uart.write(b'\x1b[2K\r')
                shell_prompt_inline()
                uart.write("".join(command_buf).encode())

        elif seq == b'[B':  # DOWN
            if history_index < len(history) - 1:
                history_index += 1
                command_buf = list(history[history_index])
            else:
                history_index = len(history)
                command_buf = []

            uart.write(b'\x1b[2K\r')
            shell_prompt_inline()
            uart.write("".join(command_buf).encode())

    # TAB AUTOCOMPLETE
    elif ch == '\t':
        current = "".join(command_buf)
        matches = [c for c in commands if c.startswith(current)]

        if len(matches) == 1:
            rest = matches[0][len(current):]
            for r in rest:
                command_buf.append(r)
                uart.write(r.encode())

        elif len(matches) > 1:
            uart.write(b'\r\n')
            for m in matches:
                uart.write(m.encode() + b' ')
            uart.write(b'\r\n')
            uart.write(b'\x1b[2K\r')
            shell_prompt_inline()
            uart.write("".join(command_buf).encode())

    # NORMAL CHARACTER
    else:
        command_buf.append(ch)
        uart.write(ch.encode())
