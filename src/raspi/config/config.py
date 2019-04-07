'''
Configuration of the Raspberry
'''

# Master variables
MASTER_UART_INTERFACE_TINY = "/dev/tty.usbserial-FTH0EPKT" #"/dev/ttys002" #Simulate on MacOs -> 'socat -d -d pty,raw,echo=0 pty,raw,echo=0'
MASTER_UART_BAUD = 115200

# Slave variables
