# fakeSerial.py

import src.raspi.lib.log as log

logger = log.getLogger("SoulTrain.movement.fakeserialdevice")

# a Serial class emulator
class FakeSerial:

    ## init(): the constructor.  Many of the arguments have default values
    # and can be skipped when calling the constructor.
    def __init__( self, port='COM1', baudrate = 19200, timeout=1,
                  bytesize = 8, parity = 'N', stopbits = 1, xonxoff=0,
                  rtscts = 0):
        self.name     = port
        self.port     = port
        self.timeout  = timeout
        self.parity   = parity
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.stopbits = stopbits
        self.xonxoff  = xonxoff
        self.rtscts   = rtscts
        self._isOpen  = True
        self._receivedData = ""
        self._data = "log,welcome to fake serial!\n"

    ## isOpen()
    # returns True if the port to the fake serial device is open.  False otherwise
    def isOpen( self ):
        return self._isOpen

    ## open()
    # opens the port
    def open( self ):
        self._isOpen = True

    ## close()
    # closes the port
    def close( self ):
        self._isOpen = False

    ## write()
    # writes a string of characters to the fake serial device
    def write( self, string ):
        logger.info("received: " + string.encode('utf-8'))
        self._receivedData += string

    ## read()
    # reads n characters from the fake serial device. Actually n characters
    # are read from the string _data and returned to the caller.
    def read( self, n=1 ):
        s = self._data[0:n]
        self._data = self._data[n:]
        #print( "read: now self._data = ", self._data )
        return s.encode('utf-8')

<<<<<<< HEAD
<<<<<<< HEAD
    ## in_waiting
    # checks if there is still a full line to read
    @property
=======
    ## in_waiting()
    # checks if there is still a full line to read
>>>>>>> run fake serial and fake accelometer on desktops
=======
    ## in_waiting
    # checks if there is still a full line to read
    @property
>>>>>>> small fixes and crane cmd handling
    def in_waiting( self ):
        try:
            returnIndex = self._data.index( "\n" )
            return bool(returnIndex)
        except ValueError:
            return False

    ## readline()
    # reads characters from the fake serial device until a \n is found.
    def readline( self ):
        try:
            returnIndex = self._data.index( "\n" )
            s = self._data[0:returnIndex+1]
            self._data = self._data[returnIndex+1:]
            return s.encode('utf-8')
        except ValueError:
            return "".encode('utf-8')

    ## __str__()
    # returns a string representation of the serial class
    def __str__( self ):
        return  "Serial<id=0xa81c10, open=%s>( port='%s', baudrate=%d," \
               % ( str(self.isOpen), self.port, self.baudrate ) \
               + " bytesize=%d, parity='%s', stopbits=%d, xonxoff=%d, rtscts=%d)"\
               % ( self.bytesize, self.parity, self.stopbits, self.xonxoff,
                   self.rtscts )
