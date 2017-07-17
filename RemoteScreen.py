"""
*   Leo Neat
*   Jet Propulsion Laboratory
*   Division 38 Optics
*   leo.s.neat@jpl.nasa.gov
*
*   RemoteScreen.py
*       This class is aimed to control an android device connected to the computer this runs on
*   vis usb port. It relies on TCP socket comunication and uses ADB port forwarding in order to
*   Interface with the phone. The images that this class sends the phone are intended to be
*   imaged by an EMCCD Camera in order to evaluate its effectiveness with the coronagraph instrument.
*
"""

import numpy as np
import socket
from PIL import Image
from Tkinter import Tk
from tkFileDialog import askopenfilename
import math
import base64
import os

# Global Constants
PORT        = 6000                  # Predefined port Number, Needs to be the same as android side
NEWDATA     = '1\n'                 # Constants used for communicating with android device
SUCCESS     = '2\n'
DISCONNECT  = '3\n'
SETTIME     = '4\n'
GETSCREENDIM= '5\n'
HOST        = 'localhost'           # Socket descriptors
ADDR        = (HOST, PORT)


class RemoteScreen:

    # Remote Screen State Variables
    __sock  = None
    screen  = None                  # Underlying numpy array
    width   = 0
    height  = 0
    csdt    = 0                     # The Current Screen delay time
    csst    = 0                     # The Current Screen Show Time
    mode    = 'Not Set'             # The current State of accessing the screen


    def __init__(self):
        # Initializes the Remote screen class for controlling an android device connected via USB port
        # Note that adb needs to be added as an environment variable for this to work

        os.system("adb forward tcp:" + str(PORT) + " tcp:" + str(PORT)) # Port forwards the CPU port to phone port
        self.__sock = self.socket_config()
        self.get_screen_dim()
        self.screen = np.zeros((self.width, self.height, 3))                                  # Creates the underlying array for the screen
                                # initialize the socket used for communicating


    def socket_config(self):
        #   This function initializes the socket connection with the android device. It needs to be called after the
        # ADB forward command or it will raise an error. This function needs to be called before send_screen
        # is called, or their will be no connection to send the screen to.

        print("Attemping to establish connection with device...")
        print("Port: " + str(PORT))
        print("Host: " + HOST)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(ADDR)
        except Exception, e:
            print "Error unable to establish connection: "+ str(e)
            exit(1)
        print("Connection established")
        return s                                                        # Returns the Socket for communication

    # Gets the dimensions of the phone screen on the android side
    def get_screen_dim(self):
        self.__sock.send(GETSCREENDIM)
        self.__sock.recv(2)
        wstring, hstring = self.__sock.recv(100).split(',')
        self.width  = int(wstring)
        self.height = int(hstring)


    def send_screen(self):
        #   This function sends the current state of the screen to the android device screen. It is requried that the
        # __socket_config function is called before this or this function will not work. This should be called as
        # an updater method to sync the screen with the program.

        print("Sending Screen")                                             # Notifies Phone that new screen is sending
        self.__sock.send(NEWDATA)
        self.__sock.recv(10)
        self.__sock.send(str(self.width) + ':' + str(self.height) + '\n')   # Sending the screens dimensions
        self.__sock.recv(10)

        # New Base64 method, more resource efficient
        rgbArray = np.zeros((self.height, self.width, 3), 'uint8')
        rgbArray[..., 0] = np.transpose(self.screen[:, :, 0])
        rgbArray[..., 1] = np.transpose(self.screen[:, :, 1])
        rgbArray[..., 2] = np.transpose(self.screen[:, :, 2])
        img = Image.fromarray(rgbArray)
        img.save('img.bmp')                             # Convert Screen to base64
        img.show()
        with open("img.bmp", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        self.__sock.send(encoded_string + '\n')                 # Send as String

        print("Screen sent successfully")


    def set_time(self,new_time, new_sleep):
        #   Sets the time at which the image is shown on the android device. The first argument is the
        # amount of time that is spent between when the image is shown and when the image is not show.
        # The second argument is the length of time that the image is shown.

        self.csdt = new_time                                                # Update State variables for output
        self.csst = new_sleep
        self.__sock.send(SETTIME)                                           # Notify android of time message
        self.__sock.recv(10)
        self.__sock.send(str(new_time) + ':' + str(new_sleep) + '\n')       # Send values in formatted string


    def disconnect(self):
        # Sends a message to the android client that the user wants to disconnect
        # Note: What ever screen is left on the android will stay their until another client changes it

        self.mode = 'Disconnected'
        self.__sock.send(DISCONNECT)                                        # Notify android of disconnect
        print("Successfully disconnected")


    def set_pixel(self, px, py, pz, val):
        #   Changes an individual pixel value on the screen. The first argument is the x coordinate of the pixel,
        # the second argument is the y coordinate and the third is the intensity which is [0,255].
        # pz = R = 0, G = 1, B = 2

        self.check_param(1, self.width, px,"Pixel Width")
        self.check_param(1, self.height, py, "Pixel Height")
        self.check_param(0, 2, pz, "Pixel Depth")
        self.check_param(0, 255, val, "Pixel Value")

        self.mode = 'Individual Pixel'
        self.screen[px, py, pz] = val



    def set_off(self):
        #   Turns all of the pixels off effectively resetting the android screen

        self.mode = 'Off'
        self.screen = np.zeros((self.width, self.height, 3))


    def set_flatfield(self, val, depth):
        # Turns all of the pixels the intensity defined by the first argument.
        # Depth codes: R = 0, G = 1, B = 2

        self.check_param(0, 255, val, "Flat Value")
        self.check_param(0, 2, depth, "Flat Depth")
        self.mode = 'Flat Field'
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.screen[x, y, depth] = val


    def set_gray(self, val):

        self.check_param(0, 255, val, "Grey Value")
        # Turns the screen to a grey shade
        self.mode = 'grey'
        self.screen[:, :, :] = val


    def set_image(self):
        #   This method allows the user to pick an image for which they want the phone to be converted to.
        # It uses the Tkinter library to open up a file browser in order to select a picture to enter. The pictures
        # Dimension must match the given width and height or an error will occur.

        self.mode = 'Image'                                         # Open file browser
        Tk().withdraw()
        filename = askopenfilename()
        img = Image.open(filename)
        width, height = img.size
        if width == self.width and height == self.height:           # Check image dimensions
            px = img.load()
            self.check_param(self.width, self.width, width, "Image Width")
            self.check_param(self.height, self.height, height, "Image Height")
            for i in range(img.size[0]):  # for every pixel:        # Convert the screen to the image
                for j in range(img.size[1]):
                    for k in range(2):
                        temp = px[i, j]
                        self.screen[i,j,0] = temp[0]
                        self.screen[i, j, 1] = temp[1]
                        self.screen[i, j, 2] = temp[2]
        else:
            print("Error, the image has incorrect size, it needs the dims: " + str(self.width) + ", " + str(self.height))


    def set_sparsefeild(self, depth, xspace, yspace, bval, dval):
        #  This function allows the user to put a grid of pixels on to the android screen. The grid is defined by four
        # Parameters. The x and y space are integers that depict the distance in pixels between where you want the
        # bright spots. The bval is the intensity level of the bright spots [0,255] and the dval is the intensity of
        # the dark spots [0,255].

        self.check_param(0,2, depth, "Sparse Depth")
        self.check_param(1, 2000, xspace, "Sparse X Space")
        self.check_param(1, 2000, yspace, "Sparse Y Space")
        self.check_param(0, 255, bval, "Sparse Bright Value")
        self.check_param(0, 255, dval, "Sparse Dark Value")

        self.mode = "Even Distribution "
        for x in range(0,self.width):
            for y in range(0, self.height):
                if(x % xspace == 0) and (y % yspace == 0):          # Set specified pixels to specified values
                    self.screen[x, y, depth] = bval
                else:
                    self.screen[x, y, depth] = dval


    def set_circle(self, depth, radius, bval, dval, xpos, ypos):
        #   This allows the user to draw a circle on the screen based upon the given parameters. Like above the
        # bval and dval represent the intensity of the bright and dark pixels [0,255]. The x and y pos are the
        # position of the center of the circle.

        self.check_param(0, 2, depth, "Circle Depth")
        self.check_param(1, 2000, radius, "Circle Radius")
        self.check_param(0, 255, bval, "Circle Bright Value")
        self.check_param(0, 2, dval, "Circle Dark Value")
        self.check_param(1, 2000, radius, "Y Position")
        self.check_param(1, 2000, radius, "X Position")

        self.mode = "Circle"
        for x in range(0, self.width):
            for y in range(0, self.height):
                if math.sqrt(((x - xpos) ** 2) + ((y - ypos) ** 2)) < radius:
                    self.screen[x, y, depth] = bval
                else:
                    self.screen[x, y, depth] = dval


    def print_state(self):
        #   This class acts as a toString method. It allows the user to see what the current state of the screen is
        # with out the full array being printed.

        print("")
        print("")
        print("______________________")
        print("*Current Screen State*")
        print("______________________")
        print("Mode: " + self.mode)
        print("Current Screen Delay Time(ms): " + str(self.csdt))
        print("Current Screen Show Time(ms): " + str(self.csst))
        print("Current Width: " + str(self.width))
        print("Current Height: " + str(self.height))
        print("Current Port#: " + str(PORT))



    def check_param(self, min, max, param, fun):
        # checks to see if the parameter is within viable values. This is to help prevent the android
        # application from unexpected crashes

        if(param >= min and param <= max):
                return True
        else:
            print("Error, you have passed an out of bounds [" +str(min) + ", " + str(max)+ "]  "
                "parameter in value " + fun + ". System will now exit.")
            exit(1)

