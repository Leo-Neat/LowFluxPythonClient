# Leo Neat
# JPL Division 38
# WFIRST-CGI
# 9/7/2017
#
# This is a UI that helps control the low flux scene android app.
# This UI allows the user to place certian pixels in certian locations at varing intensity.
# It is required that a remote screen instance be passed in to this class for it to work

import numpy as np
from tkinter import *
from PIL import ImageTk, Image
from matplotlib import pyplot as plt

class LowFluxSceneUI:

    __remote_screen = None                  # The Low flux controller
    __screen_width  = 0                     # Width of the remote screen
    __screen_height = 0
    __screen_xcenter= 0                     # Center of the Remote Screen location
    __screen_ycenter= 0
    __base_screen   = None                  # The underlying array for the UI
    __green         = False
    __red           = False
    __blue          = False
    __intensity     = None
    __master        = None                  # Tkinter root
    __panel         = None

    def __init__(self, rs):
        """
        rs is an instance of the remote screen class used for combination purposes
        this class will not function with out a pre-initialized remote screen being passed in
        """

        self.__remote_screen                        = rs
        self.__screen_width, self.__screen_height   = self.__remote_screen.get_pixel_dims()
        self.__screen_width = self.__screen_width + 20
        self.__screen_height = self.__screen_height + 20
        self.__screen_xcenter                       = self.__remote_screen.XCENTER
        self.__screen_ycenter                       = self.__remote_screen.YCENTER
        self.__base_screen                          = np.zeros([self.__screen_width,self.__screen_height,3])
        self.__master                               = Toplevel()
        self.UI_setup()
        self.__master.mainloop()



    def UI_setup(self):
        label = Label(self.__master, text="Low Flux Scene UI",font=(None, 15))
        label.grid(row=0, column=1)
        send_button = Button(self.__master, text="Send Screen", command=self.send_current_screen)
        send_button.grid(row =2, column=0)
        clear_button = Button(self.__master, text="Clear Screen", command=self.clear_screen)
        clear_button.grid(row=2,column=1)
        close_button = Button(self.__master, text="Close", command=self.__master.quit)
        close_button.grid(row=2,column=2)
        green_box   = Checkbutton(self.__master, text="Green", command=self.set_green)
        red_box     = Checkbutton(self.__master, text="Red", command=self.set_red)
        blue_box    = Checkbutton(self.__master, text="Blue", command=self.set_blue)
        green_box.grid(row=3,column=2)
        red_box.grid(row=3,column=1)
        blue_box.grid(row=3,column=0)
        label3 = Label(self.__master, text="Pixel Intensity [0,255]:")
        self.__intensity = Entry(self.__master, bd=5)
        label3.grid(row=4,column=0)
        self.__intensity.grid(row=4,column=1)
        img = ImageTk.PhotoImage(Image.fromarray(self.__base_screen.astype('uint8')))
        print(img)
        self.__panel = Label(self.__master, image=img)
        self.__panel.image = img
        self.__panel.grid(columnspan=3,row=1)
        self.__panel.bind("<Button 1>",self.set_pix)




    def set_pix(self,event):
        # outputting x and y coords to console
        var = self.__intensity.get()
        try:
            res = int(var)
        except ValueError:
            print("Error you have not input an intensity!")
            return None

        self.set_base_screen_pixel(event.y, event.x, res)
        self.update_screen()


    def update_screen(self):
        img = ImageTk.PhotoImage(Image.fromarray(self.__base_screen.astype('uint8')))
        self.__panel.configure(image=img)
        self.__panel.image = img


    def send_current_screen(self):
        """
        Uses the remote screen class to send the current screen to the android app
        """

        self.__remote_screen.set_mat(self.__base_screen)
        self.__remote_screen.send_screen()

    def clear_screen(self):
        """
        clears the UI's base screen, but does not send it
        """

        self.__base_screen = np.zeros([self.__screen_width,self.__screen_height,3])
        self.update_screen()

    def set_base_screen_pixel(self, px_loc, py_loc, val):
        """
        The color will be which ever color is checked

        :param px_loc:   The x location of the pixle you are setting
        :param py_loc:   THe y location of the pixle you are setting
        :return:
        """

        if self.__green:
            self.__base_screen[px_loc,py_loc,1] = val
        if self.__blue:
            self.__base_screen[px_loc, py_loc, 2] = val
        if self.__red:
            self.__base_screen[px_loc, py_loc, 0] = val

        if not(self.__red or self.__green or self.__blue):
            print("Error no color option was selected")


    def set_green(self):
        if self.__green == False:
            self.__green = True
        else:
            self.__green = False

    def set_red(self):
        if self.__red == False:
            self.__red = True
        else:
            self.__red = False

    def set_blue(self):
        if self.__blue == False:
            self.__blue = True
        else:
            self.__blue = False

