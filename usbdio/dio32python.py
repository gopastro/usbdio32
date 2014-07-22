#better functions by rex
import sys
import time
import AIOUSB as AU
AU.AIOUSB_Init()
device_index = 0 #assumes only one device connected
writeBuffer = AU.DIOBuf(32)

def replace_a_letter (old_string, letter_position, new_letter):
    """
    replace_a_letter takes the following arguements:
    old_string- the string in which you wish to change a letter
    letter_position- the zero-based position to the letter you wish to change
    new_letter - waht you wish to change to letter to
    replace_a_letter returns the modified string
    """
    new_letter_2 = str(new_letter) # make sure the new letter is a string
    old_string_2 = str(old_string) #make sure it is a string
    string_list = list(old_string_2) #turn string into a list
    string_list[letter_position] = new_letter_2 #replace the letter at the desired position in the list
    new_string = ''.join(string_list) # turn the list into a string
    return new_string

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

def Change_outputMask(the_settings, newMask):
    """
    Change_outputMask takes the following arguements:
    settings- in the form of the class settings
    the new Mask- a four bit number coresponding to the four ports of the device, each 1 means an output the ports are ordered: DCBA
    Change_outputMask returns the modified settings, after running update_settings
    """
    new_Mask = str(newMask)
    AU.AIOChannelMaskSetMaskFromStr( the_settings.outputMask, new_Mask )
    the_settings = update_settings(the_settings)
    return the_settings

def Change_outputMask_port( port_letter, io, first_settings):
    letter = str(port_letter)
    new_letter = letter.lower()
    places = {}
    places["a"] = 3
    places["b"] = 2
    places["c"] = 1
    places["d"] = 0
    newMask_string = replace_a_letter(first_settings.outputMask, places[new_letter], io)
    new_settings = Change_outputMask(first_settings, newMask_string)
    return new_settings

def update_settings (first_settings):
    """
    update settings takes the following arguements:
    settings- the settings in the form of the class: settings
    it returns the settings, now with attributes modified to be up-to-date with the buffers 
    e.g. settings.writeBuffer_byte_a will more accuratly reflect settings.writeBuffer
    """
    result = AU.DIO_Configure( 0, AU.AIOUSB_FALSE, first_settings.outputMask, first_settings.writeBuffer)
    read= AU.DIO_ReadAll(0, first_settings.readBuffer)
    letters = ["a", "b", "c", "d"]
    index = {} #set position of bits on board
    index["a"] = 24
    index["b"] = 16
    index["c"] = 8
    index["d"] = 0
    places = {}
    places["a"] = 3
    places["b"] = 2
    places["c"] = 1
    places["d"] = 0
    outputMask_String = str(first_settings.outputMask)
    new_settings = first_settings #initalize write so that the loop does not wipe out the writeBuffer
    for letter in letters: #go through all lettters
        port_position = places[letter]
        for num in xrange(8): #go through all the bits in each
            bit_position = num + index[letter]
            if port_position == 3:
                new_settings.readBuffer_byte_a[num] = first_settings.readBuffer[bit_position]
                new_settings.writeBuffer_byte_a[num] = first_settings.writeBuffer[bit_position]
            if port_position == 2:
                new_settings.readBuffer_byte_b[num] = first_settings.readBuffer[bit_position]
                new_settings.writeBuffer_byte_b[num] = first_settings.writeBuffer[bit_position]
            if port_position == 1:
                new_settings.readBuffer_byte_c[num] = first_settings.readBuffer[bit_position]
                new_settings.writeBuffer_byte_c[num] = first_settings.writeBuffer[bit_position]
            if port_position == 0:
                new_settings.readBuffer_byte_d[num] = first_settings.readBuffer[bit_position]
                new_settings.writeBuffer_byte_d[num] = first_settings.writeBuffer[bit_position]
        if outputMask_String[port_position] == str(1): #if the outputMask for the selected port is configured for output
            if port_position == 3:
                new_settings.readBuffer_byte_a = AU.DIOBuf(8)
            if port_position == 2:
                new_settings.readBuffer_byte_b = AU.DIOBuf(8)
            if port_position == 1:
                new_settings.readBuffer_byte_c = AU.DIOBuf(8)
            if port_position == 0:
                new_settings.readBuffer_byte_d = AU.DIOBuf(8)
        if outputMask_String[port_position] == str(0): #if the outputMask for the selected port is configured for input
            if port_position == 3:
                new_settings.writeBuffer_byte_a = AU.DIOBuf(8)
            if port_position == 2:
                new_settings.writeBuffer_byte_b = AU.DIOBuf(8)
            if port_position == 1:
                new_settings.writeBuffer_byte_c = AU.DIOBuf(8)
            if port_position == 0:
                new_settings.writeBuffer_byte_d = AU.DIOBuf(8)
    return new_settings

def set_bit (letter, num, new_bit, Current_settings):
    """
    set_bit takes the following arguements:
    letter- the letter of the port of the bit to be set
    num- the number inside the port of the bit to be set (0-7)
    new_bit - a 1 or a 0, what the new bit should be (1 for high 0 for low)
    Current_settings - the current settings
    set_bit will return the modified settings after running update_settings
    """
    old_letter = str(letter)
    new_letter = old_letter.lower() #work with lower case letters to avoid errors
    index = {} #set position of bits on board
    index["a"] = 24
    index["b"] = 16
    index["c"] = 8
    index["d"] = 0
    places = {}
    places["a"] = 3
    places["b"] = 2
    places["c"] = 1
    places["d"] = 0
    Current_settings.writeBuffer_bit = new_bit
    port_position = places[new_letter]
    if new_letter != "all":
        bit_position = num + index[new_letter]
    result = 0
    io= 1
    if io == 1: #if output is selected
        new_settings = Change_outputMask_port( new_letter, io, Current_settings)
        AU.DIOBufSetIndex( new_settings.writeBuffer, bit_position, new_bit) #channge the writeBuffer in the settings
        result = AU.DIO_Configure( 0, AU.AIOUSB_FALSE, new_settings.outputMask, new_settings.writeBuffer) #truly change the device
        print AU.DIOBufToString(new_settings.writeBuffer)
        present_settings = update_settings(new_settings) #return the current writeBuffer
        return present_settings
    if io == 0: #if input is selected
        new_settings = Change_outputMask_port( new_letter, io, Current_settings)
        new_settings = update_settings(new_settings)
        return new_settings

def read_bit (letter, number, first_settings):
    """
    read_bit takes in the letter of the port, the number of the bit in that port (0-7) and the settings. 
    The function returns the    modified settings. 
    The information on the bit that was read is stored inside the settings as settings.readBuffer_bit
    """
    old_letter = str(letter)
    new_letter = old_letter.lower() #work with lower case letters to avoid errors
    index = {} #set position of bits on board
    index["a"] = 24
    index["b"] = 16
    index["c"] = 8
    index["d"] = 0
    places = {}
    places["a"] = 3
    places["b"] = 2
    places["c"] = 1
    places["d"] = 0
    port_position = places[new_letter]
    bit_position = number + index[new_letter]
    outputMask_string = str(first_settings.outputMask)
    if outputMask_string[port_position] == str(0):
        Current_settings = first_settings
        read = AU.DIO_ReadAll(0, Current_settings.readBuffer)#the default state for the bits is high, connecting them to the ground will set them low
    else:
        print "outputMask was not configured for input in port: %s, "  %(new_letter)
        #Current_settings = Change_outputMask_port( new_letter, 0, first_settings)
        #read = AU.DIO_ReadAll(0, Current_settings.readBuffer)
    Current_settings = update_settings(Current_settings)
    Current_settings.readBuffer_bit = Current_settings.readBuffer[bit_position]
    return Current_settings

def reset (present_settings, all_bits):
    """
    reset takes two arguements: the settings and what all bit should be set to (either a 1 or a 0). 
    reset returns the modified settings 
    """
    letters = ["a", "b", "c", "d"]
    new_settings = present_settings #initalize write so that the loop does not wipe out the writeBuffer
    for letter in letters: #go through all ports
        for num in xrange(8): #go through all the letters in each
            present_settings = new_settings # update the writeBuffer
            print "%s %d" %(letter, num)
            new_settings = set_bit (letter, num, all_bits, present_settings)
    new_settings = update_settings(new_settings)
    return new_settings


def set_up():
    """
    the function set_up takes no inputs. it will set all ports to output, all bits to low and it will return the settings
    """
    import sys
    import time
    import AIOUSB as AU
    AU.AIOUSB_Init()
    Initial_Settings = settings()
    First_Settings = reset(Initial_Settings, 0)
    Initial_Settings = update_settings(First_Settings)
    return Initial_Settings

def write_byte( byte, port, old_settings):
    """
    write_byte takes in an eight character set of 1s and 0s , the port they will be written to (a,b,c or d) and the settings. write_byte returns the modified settings. set_bit runs update_settings so, the function write_byte will update settings, this in turn will read all the bytes so write_byte also functions as a read_byte
    """
    old_port = str(port)
    new_port = old_port.lower()
    old_byte = str(byte)
    new_byte = old_byte.lower()
    places = {}
    places["a"] = 3
    places["b"] = 2
    places["c"] = 1
    places["d"] = 0    
    port_position = places[new_port]
    settings = old_settings
    for num in xrange(8):
        bit = new_byte[num]
        new_bit = int(bit)
        settings = set_bit( new_port, num, new_bit, settings) 

    return settings

def bi_to_dec (bi):
    """
    takes in a binary number and returns a decimal number
    """
    bi_str = str(bi)
    dec = int( bi_str, 2)
    return dec

def dec_to_bi (dec):
    """
    takes in a decimal number and returns a binary number
    """
    if int(dec) == 0:
        bi = int(0)
        return bi
    bi_old = bin(dec)
    bi_new = bi_old[2:]
    bi = int(bi_new)
    return bi

def choose_byte (port, io, settings):
    choosen_byte = AU.DIOBuf(8)
    if type(port) == str:
        old_port = port.lower()
        if old_port == "a":
            if io == 1:
                choosen_byte = settings.writeBufffer_byte_a
            if io == 0:
                choosen_byte = settings.readBuffer_byte_a
        if old_port == "b":
            if io == 1:
                choosen_byte = settings.writeBufffer_byte_b
            if io == 0:
                choosen_byte = settings.readBuffer_byte_b
        if old_port == "c":
            if io == 1:
                choosen_byte = settings.writeBufffer_byte_c
            if io == 0:
                choosen_byte = settings.readBuffer_byte_c
        if old_port == "d":
            if io == 1:
                choosen_byte = settings.writeBufffer_byte_d
            if io == 0:
                choosen_byte = settings.readBuffer_byte_d
    if type(port) == int:
        if old_port == 3:
            if io == 1:
                choosen_byte = settings.writeBufffer_byte_a
            if io == 0:
                choosen_byte = settings.readBuffer_byte_a
        if old_port == 2:
            if io == 1:
                choosen_byte = settings.writeBufffer_byte_b
            if io == 0:
                choosen_byte = settings.readBuffer_byte_b
        if old_port == 1:
            if io == 1:
                choosen_byte = settings.writeBufffer_byte_c
            if io == 0:
                choosen_byte = settings.readBuffer_byte_c
        if old_port == 0:
            if io == 1:
                choosen_byte = settings.writeBufffer_byte_d
            if io == 0:
                choosen_byte = settings.readBuffer_byte_d
    return choosen_byte



















