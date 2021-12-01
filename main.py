import os
import numpy as np
import cv2
import natsort
import xlwt
from global_histogram_stretching import stretching
from hsvStretching import HSVStretching
from sceneRadiance import sceneRadianceRGB


import tkinter as tk
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog

def dispayImage(displayImage):
    ImagetoDisplay = displayImage.resize((900, 600), Image.ANTIALIAS)
    ImagetoDisplay = ImageTk.PhotoImage(ImagetoDisplay)
    showWindow.config(image=ImagetoDisplay)
    showWindow.photo_ref = ImagetoDisplay
    showWindow.pack()
filename = ""
def importButton_callback():
    global originalImage, filename
    filename = filedialog.askopenfilename()
    print("fn : " + str(filename))
    originalImage = Image.open(filename)
    dispayImage(originalImage)

def saveButton_callback():
    global address
    # folder = "C:/Users/Administrator/Desktop/UnderwaterImageEnhancement/NonPhysical/ICM"
    folder = "D:"

    path = folder + "/InputImages"
    files = os.listdir(path)
    files = natsort.natsorted(files)

    for i in range(len(files)):
        file = files[i]
        filepath = path + "/" + file
        print("FP : " + str(filepath))
        if(filepath == filename) :
            print("equal : " + str(filepath))
            prefix = file.split('.')[0]
            if os.path.isfile(filepath):
                print('********    file   ********', file)
                # img = cv2.imread('InputImages/' + file)
                img = cv2.imread(folder + '/InputImages/' + file)
                img = stretching(img)
                sceneRadiance = sceneRadianceRGB(img)
                # cv2.imwrite(folder + '/OutputImages/' + Number + 'Stretched.jpg', sceneRadiance)
                sceneRadiance = HSVStretching(sceneRadiance)
                sceneRadiance = sceneRadianceRGB(sceneRadiance)
                cv2.imwrite(folder + '/OutputImages/' + prefix + '_ICM.jpg', sceneRadiance)
            break
    address=folder + '/OutputImages/' + prefix + '_ICM.jpg'
    im=Image.open(address)
    im.show()

def closeButton_callback():
    window.destroy()

window = tk.Tk()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window.geometry(f'{screen_width}x{screen_height}')

Frame1 = tk.Frame(window, height=20, width=200)
Frame1.pack(anchor=tk.N)

importButton = tk.Button(Frame1, text="Import", padx=10, pady=5, command=importButton_callback)
importButton.grid(row=0, column=0)

saveButton = tk.Button(Frame1, text="Save", padx=10, pady=5, command=saveButton_callback)
saveButton.grid(row=0, column=1)

closeButton = tk.Button(Frame1, text="Close", padx=10, pady=5, command=closeButton_callback)
closeButton.grid(row=0, column=2)

showWindow = tk.Label(window)
showWindow.pack()
tk.mainloop()