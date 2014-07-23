
import AIOUSB as AU
from DIOfunctions import settings

def list_devices():
    result = AU.AIOUSB_Init()
    deviceMask = AU.GetDevices()
    index = 0
    a_set_of_devices = []
    counter = 0
    a_device = settings()
    while deviceMask > 0 and len(devices) < number_devices :
        if (deviceMask & 1 ) != 0: #what is the purpose of this?, 1 will never be 0
            obj = AU.GetDeviceInfo( index ) #I presume this gets information
            if obj.PID == USB_DIO_32 or obj.PID == USB_DIO_16A : #if the device if of the correct kind
                a_set_of_devices.append(a_device)
                a_set_of_devices[counter].device_index = index
                counter = counter + 1
        index = index + 1 #change index
        deviceMask >>= 1 #what does this do?
    try:
        a_set_of_devices = a_set_of_devices[0]
    except IndexError:
        print "No devices were found. Please make sure you have at least one ACCES I/O Products USB device plugged into your computer"
        sys.exit(1)
    return a_set_of _devices
















