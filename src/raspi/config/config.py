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

# Phases of the system
PHASE_STARTUP = 'startup'
PHASE_FIND_CUBE = 'find_cube'
PHASE_GRAB_CUBE = 'grab_cube'
PHASE_ROUND_ONE = 'round_one'
PHASE_ROUND_TWO = 'round_two'
PHASE_FIND_STOP = 'find_stop'
PHASE_STOPPING = 'stopping'
PHASE_FINISHED = 'finished'

PHASE_TO_INT = {
    PHASE_STARTUP: 0,
    PHASE_FIND_CUBE: 1,
    PHASE_GRAB_CUBE: 2,
    PHASE_ROUND_ONE: 3,
    PHASE_ROUND_TWO: 4,
    PHASE_FIND_STOP: 5,
    PHASE_STOPPING: 6,
    PHASE_FINISHED: 7,
}
