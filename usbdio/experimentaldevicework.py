
import AIOUSB as AU

class Device:
    outputMask = AU.NewAIOChannelMaskFromStr("1111")
    readBuffer = AU.DIOBuf(MAX_DIO_BYTES )
    writeBuffer = AU.DIOBuf( MAX_DIO_BYTES )
    name = ""
    serialNumber = 0
    index = 0
    numDIOBytes = 0
    numCounters = 0
    productID = 0
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

class settings:
    writeBuffer = AU.DIOBuf(32)
    readBuffer = AU.DIOBuf(32)
    readBuffer_bit = AU.DIOBuf(1)
    readBuffer_byte_a = AU.DIOBuf(8)
    readBuffer_byte_b = AU.DIOBuf(8)
    readBuffer_byte_c = AU.DIOBuf(8)
    readBuffer_byte_d = AU.DIOBuf(8)
    writeBuffer_bit = AU.DIOBuf(1)
    writeBuffer_byte_a = AU.DIOBuf(8)
    writeBuffer_byte_b = AU.DIOBuf(8)
    writeBuffer_byte_c = AU.DIOBuf(8)
    writeBuffer_byte_d = AU.DIOBuf(8)
    outputMask = AU.NewAIOChannelMaskFromStr("1111")
    device_index = 0 # new

result = AU.AIOUSB_Init() #required by GetDevices
devicesFound = 0
deviceMask = AU.GetDevices() #returns an integer
index = 0

AU.AIOUSB_ListDevices()

while deviceMask > 0 and len(devices) < number_devices :
    if (deviceMask & 1 ) != 0: #what is the purpose of this?, 1 will never be 0
        obj = AU.GetDeviceInfo( index ) #I presume this gets information
        if obj.PID == USB_DIO_32 or obj.PID == USB_DIO_16A : #if the device if of the correct kind
            devices.append( Device( index=index, productID=obj.PID, numDIOBytes=obj.DIOBytes,numCounters=obj.Counters )) #add to the array of devices
    index = index + 1 #change index
    deviceMask >>= 1 #what does this do?
try:
    device = devices[0]
except IndexError:
    print """No devices were found. Please make sure you have at least one 
ACCES I/O Products USB device plugged into your computer"""
    sys.exit(1)

