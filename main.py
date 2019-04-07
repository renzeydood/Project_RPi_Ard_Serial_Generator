import time as t
from os import path

start_byte = "!"
stop_byte = "~"
total_arduino_to_rpi = 8
total_rpi_to_arduino = 8

# Depending on IDE, pylint will nag if tabs is used instead of spacings
#tab = "\t"
tab = "    "


def rpi_code_main():
    return "from Ard_interface import *\n" + \
        "from message_structure import *\n" + \
        "from Queue import Queue\n" + \
        "from threading import Thread\n" + \
        "\n" + \
        "port = '/dev/ttyACM0'\n" + \
        "baudrate = 19200\n" + \
        "x = 0\n" + \
        "\n" + \
        "class main():\n" + \
        tab + "def __init__(self):\n" + \
        tab + tab + "self.ard = Ard_interface(port, baudrate)\n" + \
        tab + tab + "self.msg_to_ard = SENDMessage()\n" + \
        tab + tab + "self.msg_from_ard = RCVDMessage()\n" + \
        "\n" + \
        tab + "def start_connection(self):\n" + \
        tab + tab + "self.ard.connect()\n" + \
        tab + tab + "print('Arduino connected')\n"


def rpi_code_interface():
    return ""


def rpi_code_message_struct():
    return "ARD_ENC = 'utf-8'\n" + \
        "START = '!'\n" + \
        "STOP = '~'\n" + \
        "MAX_BYTE_FROM_SERVER = 8 # Includes start and end bytes (RCVD)\n" + \
        "MAX_BYTE_FROM_CLIENT = 9 # Includes start and end bytes (SEND)\n" + \
        "\n" + \
        "def int_to_bytes(data):\n" + \
        tab + "return chr(data >> 7) + chr(data & 0x7F)\n" + \
        "def bytes_to_int(u, l):\n" + \
        tab + "return u << 7 | l\n" + \
        "\n" + \
        "class RCVDMessage():\n" + \
        tab + "def __init__(self):\n" + \
        tab + tab + "pass\n" + \
        tab + "def destruct(self, data):\n" + \
        tab + tab + "pass\n" + \
        "\n" + \
        "class SENDMessage():\n" + \
        tab + "def __init__(self):\n" + \
        tab + tab + "pass\n" + \
        tab + "def contruct(self):\n" + \
        tab + tab + "return (START + STOP).encode()\n"


def ard_code_main():
    return "#include \"message_structure.h\"\n" + \
        "\n" + \
        "void setup()\n" + \
        "{\n" + \
        "\tSerial.begin(19200);\n" + \
        "\tmemset(&msgRCVD, 0, sizeof(RCVDMessage));\n" + \
        "\tmemset(&msgSEND, 0, sizeof(SENDMessage));\n" + \
        "\n" + \
        "\tdelay(500);\n" + \
        "}\n" + \
        "\n" + \
        "void loop()\n" + \
        "{\n" + \
        "\t//Wait for start event\n" + \
        "\tusbReceiveMSG(&msgRCVD); //Process incoming message packet\n" + \
        "\tdelay(RPI_DELAY);\n" + \
        "\tusbSendMSG(&msgRCVD);\n" + \
        "}\n"


def ard_code_message_struct():
    return "#define lowByte(w) ((uint8_t)((w)&0x7f))\n" + \
        "#define highByte(w) ((uint8_t)((w) >> 7))\n" + \
        "\n" + \
        "const uint8_t START = '!';\n" + \
        "const uint8_t STOP = '~';\n" + \
        "const uint8_t MAX_BYTE_DATA = 8;\n" + \
        "\n" + \
        "struct RCVDMessage\n" + \
        "{\n" + \
        "\tuint8_t type;\n" + \
        "};\n" + \
        "\n" + \
        "struct SENDMessage\n" + \
        "{\n" + \
        "\tuint8_t type;\n" + \
        "};\n" + \
        "\n"


def createFile(dest):
    print(dest)
    filename = "message_struct.py"

    if not(path.isfile(dest + filename)):
        f = open(dest + filename, 'w')
        f.write(rpi_code_message_struct())
        f.close()

    elif(input("Overwrite {} file? (Y/n)".format(filename)) == "Y"):
        f = open(dest + filename, 'w')
        f.write(rpi_code_message_struct())
        f.close()


def main():
    print("*******************************************")
    print("Options will run in sequence:")
    print("1. Start byte")
    print("2. Stop byte")
    print("3. Number of data to send (Arduino to RPi)")
    print("4. Data type and name")
    print("5. Number of data to send (RPi to Arduino)")
    print("6. Data type and name")
    print("*******************************************")

    readinput = input("1. Start byte (Should be unique): ")
    if(len(readinput) < 2 and (31 < ord(readinput) < 127)):
        start_byte = readinput
    else:
        print("Invalid")

    readinput = input("2. Stop byte (Should be unique): ")
    if(31 < ord(readinput) < 127):
        stop_byte = readinput
    else:
        print("Invalid")

    readinput = input("3. Number of data to send (Arduino to RPi): ")
    if(47 < ord(readinput) < 58):
        total_arduino_to_rpi = int(readinput)
        data = [total_arduino_to_rpi]
    else:
        print("Invalid")

    for x in data:
        readinput = input("4. Data {} - Name: ").format(x)
        data[x] = readinput
        readinput = input("4. Data {} - Type (int/char): ").format(x)


if __name__ == '__main__':
    #destination = ""
    # createFile(destination)
    # print("Done!!")
    main()
