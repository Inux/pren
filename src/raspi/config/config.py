'''
Configuration of the Raspberry
'''

# Master variables
MASTER_UART_INTERFACE_TINY = "/dev/ttyTiny"
MASTER_UART_BAUD = 115200

MASTER_UART_INTERFACE_PC = "/dev/ttys004"
#Simulate on MacOs -> 'socat -d -d pty,raw,echo=0 pty,raw,echo=0' then 'screen /dev/ttys005'


# Tiny Config
RESEND_TINY_MESSAGES = False
