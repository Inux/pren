'''
Configuration of the Raspberry
'''

# Controlflow Parameters

# - speed values
SPEED_CUBE_SEARCH = 10 #mm/s
SPEED_MAXIMAL_LIMIT = 3500 #mm/s
SPEED_NUMBER_DETECTION_LIMIT = 3500 #mm/s
SPEED_STOP_SEARCH = 1000 #mm/s

# - crane poll time and waittime until finished
CRANE_POLL_TIME = 0.1
CRANE_WAIT_TIME = 5

# - distances of the parcour
DISTANCE_ROUND_MM = 10000
DISTANCE_STOP_MAX = 10000 # distance to last stop signal


# Component Parameters ----------------------------------------------

# - heartbeat intervall in milliseconds and heartbeat invalidate time
HB_INTERVAL = 200 #ms
HB_INVALIDATE_TIME = 650 #ms


# Tiny Config
RESEND_TINY_MESSAGES = False
MASTER_UART_INTERFACE_TINY = "/dev/ttyTiny"
MASTER_UART_BAUD = 115200
MASTER_UART_INTERFACE_PC = "/dev/ttys010" #Simulate on MacOs -> 'socat -d -d pty,raw,echo=0 pty,raw,echo=0' then 'screen /dev/ttys005'


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

PHASE_DELAY = 5 # in seconds (Delay some phases - especially those which are running very fast!)
