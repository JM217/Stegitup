# Final Year Project - Security - Bsc Computer Science with Cyber Security
# Author - Joseph McLean
# Description - This tool is to provide a way to both embed and extract text
# from an image file

from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import numpy as np
import math
import hashlib

global path_image

image_display_size = 300, 300


def on_click():
    # Step 1.5
    global path_image
    # use the tkinter filedialog library to open the file using a dialog box.
    # obtain the image of the path
    path_image = filedialog.askopenfilename()
    # load the image using the path
    load_image = Image.open(path_image)
    # set the image into the GUI using the thumbnail function from tkinter
    load_image.thumbnail(image_display_size, Image.ANTIALIAS)
    # load the image as a numpy array for efficient computation and change the type to unsigned integer
    np_load_image = np.asarray(load_image)
    np_load_image = Image.fromarray(np.uint8(np_load_image))
    render = ImageTk.PhotoImage(np_load_image)
    img = Label(app, image=render)
    img.image = render
    img.place(x=20, y=50)


def encode_input_to_image():
    # Step 2
    global path_image
    text = txt.get(1.0, "end-1c")
    data = hashlib.sha1(text.encode('utf-8'))
    hexDigest = data.hexdigest()

    # load the image
    img = cv2.imread(path_image)
    # display the characters in ASCII.
    data = [format(ord(i), '08b') for i in hexDigest]
    _, width, _ = img.shape
    # algorithm to encode the image
    PixReq = len(data) * 3

    RowReq = PixReq / width
    RowReq = math.ceil(RowReq)

    count = 0
    charCount = 0

    for i in range(RowReq + 1):

        while (count < width and charCount < len(data)):
            char = data[charCount]
            charCount += 1

            for index_k, k in enumerate(char):
                if ((k == '1' and img[i][count][index_k % 3] % 2 == 0) or (
                        k == '0' and img[i][count][index_k % 3] % 2 == 1)):
                    img[i][count][index_k % 3] -= 1
                if (index_k % 3 == 2):
                    count += 1
                if (index_k == 7):
                    if (charCount * 3 < PixReq and img[i][count][2] % 2 == 1):
                        img[i][count][2] -= 1
                    if (charCount * 3 >= PixReq and img[i][count][2] % 2 == 0):
                        img[i][count][2] -= 1
                    count += 1
        count = 0
    # Step 6
    # Write the encoded image into a new file
    cv2.imwrite("./encoded_image.png", img)
    # Display the success label.
    success_label = Label(app, text="Embedding complete!",
                          bg='lavender', font=("Times New Roman", 20))
    success_label.place(x=160, y=300)


def extract():
    # load the image and convert it into a numpy array
    load = Image.open("./encoded_image.png")
    load.thumbnail(image_display_size, Image.ANTIALIAS)
    load = np.asarray(load)
    load = Image.fromarray(np.uint8(load))
    render = ImageTk.PhotoImage(load)
    img = Label(app, image=render)
    img.image = render
    img.place(x=20, y=50)

    # Algorithm to extract the data from the image
    img = cv2.imread("./encoded_image.png")
    data = []
    stop = False
    for index_i, i in enumerate(img):
        i.tolist()
        for index_j, j in enumerate(i):
            if ((index_j) % 3 == 2):
                # first pixel
                data.append(bin(j[0])[-1])
                # second pixel
                data.append(bin(j[1])[-1])
                # third pixel
                if (bin(j[2])[-1] == '1'):
                    stop = True
                    break
            else:
                # first pixel
                data.append(bin(j[0])[-1])
                # second pixel
                data.append(bin(j[1])[-1])
                # third pixel
                data.append(bin(j[2])[-1])
        if (stop):
            break

    message = []
    # join all the bits to form letters (ASCII Representation)
    for i in range(int((len(data) + 1) / 8)):
        message.append(data[i * 8:(i * 8 + 8)])
    # join all the letters to form the message.
    message = [chr(int(''.join(i), 2)) for i in message]
    message = ''.join(message)
    message_label = Label(app, text=message, bg='lavender', font=("Times New Roman", 20))
    message_label.place(x=30, y=400)


# GUI - optional objective 1 for this project
app = Tk()
app.configure(background='lavender')
app.title("JJM's Steganography Tool")
app.geometry('600x500')
# create a button to perform to choose an image
on_click_button = Button(app, text="Choose Image", bg='white', fg='black', command=on_click)
on_click_button.place(x=340, y=230)
# create a textbox and have it wrap text
txt = Text(app, wrap=WORD, width=30)
txt.place(x=340, y=55, height=165)
# create a button to perform the embed process against an image
embed_button = Button(app, text="Embed", bg='white', fg='black', command=encode_input_to_image)
embed_button.place(x=435, y=230)
# craete a button to perfrom the extract process against an image
extract_button = Button(app, text="Extract", bg='white', fg='black', command=extract)
extract_button.place(x=500, y=230)
app.mainloop()
