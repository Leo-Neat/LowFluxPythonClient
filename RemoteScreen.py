import numpy as np
import socket
from PIL import Image
from Tkinter import Tk
from tkFileDialog import askopenfilename
import math



PORT = 6000
NEWDATA = '1\n'
SUCCESS = '2\n'
DISCONNECT = '3\n'
HOST = 'localhost'
ADDR = (HOST, PORT)


class RemoteScreen:

    __s = None
    screen = None
    width = 0
    height = 0

    def __init__(self, w, h):

        self.width = w
        self.height = h
        self.screen = np.zeros((w, h))
        self.__sock = self.__socket_config()

    def __socket_config(self):
        print("Attemping to establish connection with device...")
        print("Port: " + str(PORT))
        print("Host: " + HOST)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(ADDR)
        except Exception, e:
            print str(e)
        print("Connection established")
        return s

    def send_screen(self):
        print("Sending Screen")
        self.__sock.send(NEWDATA)
        self.__sock.recv(10)
        self.__sock.send(str(self.width) + ':' + str(self.height) + '\n')
        self.__sock.recv(10)
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.__sock.send(str(int(self.screen[x, y]))+',')
        self.__sock.send('\n')
        print("Screen sent successfully")

    def disconnect(self):
        self.__sock.send(DISCONNECT)
        print("Successfully disconnected")

    def change_pixel(self, px, py, val):
        self.screen[px, py] = val

    def turn_black(self):
        self.screen = np.zeros((self.width, self.height))

    def turn_color(self, val):
        for x in range(0,self.width):
            for y in range(0, self.height):
                self.screen[x, y] = val

    def use_image(self):
        Tk().withdraw()
        filename = askopenfilename()
        img = Image.open(filename).convert('LA')
        width, height = img.size
        if width == self.width and height == self.height:
            px = img.load()
            for i in range(img.size[0]):  # for every pixel:
                for j in range(img.size[1]):
                    temp = px[i, j]
                    self.screen[i, j] = temp[0]
        else:
            print("Error, the image has incorrect size, it needs the dims: " + str(self.width) + ", " + str(self.height))

    def even_distro(self, xspace, yspace, bval, dval):
        for x in range(0,self.width):
            for y in range(0, self.height):
                if(x % xspace == 0) and (y % yspace == 0):
                    self.screen[x, y] = bval
                else:
                    self.screen[x, y] = dval

    def circle(self, radius, bval, dval, xpos, ypos):
        for x in range(0, self.width):
            for y in range(0, self.height):
                if math.sqrt(((x-xpos)**2)+((y-ypos)**2)) < radius:
                    self.screen[x, y] = bval
                else:
                    self.screen[x, y] = dval






