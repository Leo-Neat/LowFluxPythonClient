"""
*   Leo Neat
*   Jet Propulsion Laboratory
*   Division 38 Optics
*   leo.s.neat@jpl.nasa.gov
*
*   LowFluxClient.py
*       This class is essentially the text based user interface for the RemoteScreen class. This class makes it so
*   all of the required commands are called in the right order and It should be used as a guide to how the Remote Screen
*   class functions.
*
"""

import time
import RemoteScreen
from PIL import Image


def display_menu():
    # Function to display all of the options the user has when running this program
    # Note: Correct input is assumed

    print("")
    print("")
    print("_______________________")
    print("*Low Flux Android Menu*")
    print("_______________________")
    print("1) Clear Screen")
    print("2) Set flat field")
    print("3) Set a Matrix")
    print("4) Set an Image")
    print("5) Disconnect")
    print("6) Set Time Delay")
    print("7) View Current Display")
    print("8) Set Screen Brightness")
    result = int(raw_input("Enter your choice: "))
    return result


def head():
    #   This is the main body for the LowFlux client script. This is where all of the decided is done and is just a
    # lot of if statements that correspond to options that are performable by the remote screen.

    screen.print_state()
    result = display_menu()
    if result == 1:
        screen.set_off()
        screen.send_screen()
        head()
    elif result == 2:
        val = int(raw_input("What intensity do you want the screen(0-255): "))
        depth = int(raw_input("What depth do you want to put the field(0=R, 1=G, 2=B): "))
        screen.set_off()
        screen.set_flatfield(val, depth)
        screen.send_screen()
        head()
    elif result == 3:
        ret = matmenu()
        if ret  == 1:
            rad = int(raw_input("Enter the radius: "))
            bval = int(raw_input("Enter the circle pixel values[0-255]: "))
            dval = int(raw_input("Enter the outer pixel values[0-255]: "))
            cx = int(raw_input("Enter the center x pixel: "))
            cy = int(raw_input("Enter the center y pixel: "))
            depth = int(raw_input("What depth do you want to put the field(0=R, 1=G, 2=B): "))
            screen.set_circle(depth, rad, bval, dval, cx, cy)
            screen.send_screen()
        elif ret == 2:
            xspace = int(raw_input("Enter the distance between the pixels x values: "))
            yspace = int(raw_input("Enter the distance between the pixels y values: "))
            bval   = int(raw_input("Enter the selected pixels value[0-255]: "))
            dval   = int(raw_input("Enter the non selected pixels value[0-255]: "))
            depth = int(raw_input("What depth do you want to put the field(0=R, 1=G, 2=B): "))
            screen.set_sparsefeild(depth, xspace, yspace, bval, dval)
            screen.send_screen()
        elif ret == 3:
            px = int(raw_input("Enter the x value of the pixel you want to change: "))
            py = int(raw_input("Enter the y value of the pixel you want to change: "))
            pz = int(raw_input("Enter the z value of the pixel you want to change: "))
            inten = int(raw_input("Enter the intensity of the pixel you want to change: "))
            screen.set_pixel(px, py, pz, inten)
            screen.send_screen()
        else:
            print("invalid opt, returning to main screen")
        head()
    elif result == 4:
        screen.set_image()
        screen.send_screen()
        head()
    elif result == 5:
        screen.disconnect()
    elif result == 6:
        newtime = int(raw_input("Please Enter the Delay you want in ms(0 is always on): "))
        newsleep = int(raw_input("Please Enter the length of time you want the image to say on(ms): "))
        screen.set_time(newtime, newsleep)
        head()
    elif result == 7:
        img = Image.open("img.bmp")
        img.show()
        head()
    elif result == 8:
        brightness = int(raw_input("Please enter the new screen brighness(0-255): "))
        screen.set_phone_brightness(brightness)
        head()
    else:
        print("invalid option please repick...")
        head()


def matmenu():
    # This is the menu that is printed when the user decides that they want to use a matrix as input

    print("1) Send a Circle")
    print("2) Send a Grid")
    print("3) Set an individual Pixel")
    ret = int(raw_input("Enter your choice:"))
    return ret

# Global Screen what acts as the main data type
# Note that the screen resolution is hardcoded
screen = RemoteScreen.RemoteScreen()
head()                                              # Prompt menus to open
