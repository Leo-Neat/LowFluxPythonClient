import RemoteScreen



def display_menu():
    print("Low Flux Android Menu")
    print("1) Clear Screen")
    print("2) Set full Shade")
    print("3) Set a Matrix")
    print("4) Set an Image")
    print("5) Disconnect")
    result = int(raw_input("Enter your choice: "))
    return result


def head():
    result = display_menu()
    if result == 1:
        screen.turn_black()
        screen.send_screen()
        head()
    elif result == 2:
        val = int(raw_input("What intensity do you want the screen(0-255): "))
        screen.turn_color(val)
        screen.send_screen()
        head()
    elif result == 3:
        ret = matmenu()
        if ret  == 1:
            rad = int(raw_input("Enter the radius: "))
            bval = int(raw_input("Enter the circle pixel values(0-255): "))
            dval = int(raw_input("Enter the outer pixel values(0-255): "))
            cx = int(raw_input("Enter the center x pixel: "))
            cy = int(raw_input("Enter the center y pixel: "))
            screen.circle(rad, bval, dval,cx, cy)
            screen.send_screen()
        elif ret == 2:
            xspace = int(raw_input("Enter the distance between the pixels x values: "))
            yspace = int(raw_input("Enter the distance between the pixels y values: "))
            bval   = int(raw_input("Enter the selected pixels value(0-255): "))
            dval   = int(raw_input("Enter the non selected pixels value(0-255): "))
            screen.even_distro(xspace, yspace, bval, dval)
            screen.send_screen()

        elif ret == 3:
            px = int(raw_input("Enter the x value of the pixel you want to change: "))
            py = int(raw_input("Enter the y value of the pixel you want to change: "))
            inten = int(raw_input("Enter the intensity of the pixel you want to change: "))
            screen.change_pixel(px, py, inten)
            screen.send_screen()
        else:
            print("invalid opt, returning to main screen")
        head()
    elif result == 4:
        screen.use_image()
        screen.send_screen()
        head()
    elif result == 5:
        screen.disconnect()
    else:
        print("invalid option please repick...")
        head()


def matmenu():
    print("1) Send a Circle")
    print("2) Send a Grid")
    print("3) Set an individual Pixel")
    ret = int(raw_input("Enter your choice:"))
    return ret

screen = RemoteScreen.RemoteScreen(1080, 1920)
head()