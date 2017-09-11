import socket
from PIL import Image
from Tkinter import Tk
from tkFileDialog import askopenfilename

XMAX = 1080
YMAX = 1920
PORT = 6000
NEWDATA = '1\n'
SUCCESS = '2\n'
HOST = 'localhost'
ADDR = (HOST, PORT)


def socket_config():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(ADDR)
    return s


def display_menu():
    print("Low Flux Android Menu")
    print("1) Clear Screen")
    print("2) Set full Shade")
    print("3) Set a Matrix")
    print("4) Set an Image")
    result = int(raw_input("Enter your choice: "))
    return result


def main():
    sock = socket_config()
    head(sock)

def head(sock):
    result = display_menu()
    if result == 1:
        sendblank(sock, 0)
    elif result == 2:
        shade = int(raw_input("Enter the shade(0-255): "))
        sendblank(sock, shade)
    elif result == 3:
        sendMat(sock)
    elif result == 4:
        sendIMG(sock)
    else:
        print("invalid option please repick...")
        head(sock)


def sendIMG(s):
    print("Please select the image you wish to send")
    Tk().withdraw()
    filename = askopenfilename()
    img = Image.open(filename).convert('LA')
    px = img.load()
    print(img.size)

    s.send(NEWDATA)
    s.recv(10)
    s.send(str(img.size[0])+':'+str(img.size[1])+'\n')
    s.recv(10)

    for i in range(img.size[0]):  # for every pixel:
        for j in range(img.size[1]):
            temp = px[i, j]
            s.send(str(abs(255-temp[0])) + ',')

    s.send('\n')
    head(s)


def sendMat(s):
    print("Matrix Options")
    print("1) Single center pixel")
    print("2) Evenly distrbuted pixels")
    result = int(raw_input("Enter your option : "))
    if result == 1:
        sendSingle(s)
    if result == 2:
        sendEven(s)


def sendSingle(s):
    shade = str(raw_input("What intensity do you want the pixel: "))
    shade2 = str(raw_input("What intensity do you want the surounding pixels"))
    s.send(NEWDATA)
    s.recv(10)
    s.send(str(XMAX) + ':' + str(YMAX) + '\n')
    s.recv(10)
    for i in range(0, XMAX):
        for j in range(0, YMAX):
            if (i == XMAX / 2) and (j == YMAX / 2):
                s.send(str(shade) + ',')
            else:
                s.send(str(shade2) + ',')
    s.send('\n')
    head(s)


def sendEven(s):
    disy = int(raw_input("how far appart do you want the bright pixels verticly?: "))
    disx = int(raw_input("how far appart do you want the bright pixels horazontaly?: "))
    shade = int(raw_input("At what intensity do you want the bright pixels?: "))
    shade2 = int(raw_input("at what intensity do you want the dark pixels?: "))
    s.send(NEWDATA)
    s.recv(10)
    s.send(str(XMAX) + ':' + str(YMAX) + '\n')
    s.recv(10)
    for i in range(0, XMAX):
        for j in range(0, YMAX):
            if (i % disx == 0) and (j % disy == 0):
                s.send(str(shade) + ',')
            else:
                s.send(str(shade2) + ',')
    s.send('\n')
    head(s)


def sendblank(s, shade):
    s.send(NEWDATA)
    s.recv(10)
    s.send(str(XMAX) + ':' + str(YMAX) + '\n')
    s.recv(10)
    for i in range(0, XMAX):
        for j in range(0, YMAX):
            s.send(str(shade) + ',')
    s.send('\n')
    head(s)


main()
