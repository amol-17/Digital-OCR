from tkinter import *
from tkinter import filedialog
import tkinter.messagebox as tmsg
import tkinter.scrolledtext as scrolledtext
import cv2
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
cong = r'--oem 2 --psm 6'
filename = ''

def browse():
    global filename

    statusVar.set("Browsing File...")
    sbar.update()

    filename_ = filedialog.askopenfile()
    browse_text = Entry(frame_top, width=100)
    browse_text.grid(row=2, column=2)
    if filename_:
        filename = filename_.name
        browse_text.insert(0, filename_.name)
        browse_text.grid(row=2, column=2)
    statusVar.set("Ready to work")

def convert():

    statusVar.set("Converting...")
    sbar.update()
    import time
    time.sleep(2)
    # A text file is created and flushed
    file = open("recognized.txt", "w+")
    file.write("")
    file.close()

    newResult = ''
    if filename:
        img = Image.open(filename)
        result = pytesseract.image_to_string(img, config=cong)
        s = 'abcdefghijklhmnoprstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        for i in result:
            if i in s:
                newResult = newResult + i
            if i == ' ':
                newResult += ' '
            if i == '\n':
                newResult += '\n'
        file = open('recognized.txt', 'w+')
        file.write(newResult)
        file.close()

        # to read contents and display it in text gui window
        file = open("recognized.txt", "r")
        text2show = file.read()

        show_text.insert(INSERT, text2show)
        show_text.pack()
        file.close()
    else:
        tmsg.showerror('Error', 'File not selected or Invalid path')
    statusVar.set("Ready to work")

def exit_confirm():
    choice = tmsg.askyesno('Sure Exit?', 'Are you sure you want to quit?')
    if choice == True:
        root.quit()

def save_text():

    statusVar.set("Saving text...")
    sbar.update()

    f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None:
        return
    txt2save = str(show_text.get(0.0, END))
    f.write(txt2save)
    f.close()
    statusVar.set("Ready to work")


def camera():
    global filename

    statusVar.set("Saving text...")
    sbar.update()
    tmsg.showinfo('To capture Image', 'Press "S" to save, "Q" to quit')
    key = cv2.waitKey(1)
    webcam = cv2.VideoCapture(0)
    while True:
        try:
            check, frame = webcam.read()
            cv2.imshow("Capturing", frame)
            key = cv2.waitKey(1)
            if key == ord('s'):
                cv2.imwrite(filename='saved_img.png', img=frame)
                webcam.release()
                img_new = cv2.imread('saved_img.png', cv2.IMREAD_GRAYSCALE)
                img_new = cv2.imshow("Captured Image", img_new)
                cv2.waitKey(1650)
                cv2.destroyAllWindows()
                # print("Processing image...")
                img_ = cv2.imread('saved_img.png', cv2.IMREAD_ANYCOLOR)
                # print("Converting RGB image to grayscale...")
                gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
                # print("Converted RGB image to grayscale...")
                print("Resizing image to scale...")
                img_ = cv2.resize(gray, (700,600))
                # print("Resized...")
                img_resized = cv2.imwrite(filename='saved_img-final.png', img=img_)
                print("Image saved!")
                filename = 'saved_img-final.png'
                browse_text.insert(0, filename)
                browse_text.grid(row=2, column=2)

                break
            elif key == ord('q'):
                print("Turning off camera.")
                webcam.release()
                print("Camera off.")
                print("Program ended.")
                cv2.destroyAllWindows()
                break

        except(KeyboardInterrupt):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break
    statusVar.set("Ready to work")

def clearTxt():
    show_text.delete("0.0", "end")

def helpDesk():
    tmsg.showinfo('Help Desk', 'Send us your queries at: \nEmail: devopsofficial@microg.com')

def checkUpdate():
    statusVar.set("Checking for update...")
    sbar.update()
    import time
    time.sleep(3)
    tmsg.showinfo('Update', " No new update available \nCheck again later")
    statusVar.set("Ready")

def contribute():
    p = tmsg.askyesnocancel('Feedback', 'Do you like our product? ')
    if p == True:
        tmsg.showinfo("Feedback", "Thank you for loving our product.\nWe will keep improving")
    if p == False:
        tmsg.showinfo("Feedback", "Thank you for valuable feedback.\nWe will work harder")

root = Tk()
root.geometry('1080x720')
root.title('Digital OCR')

# photo = PhotoImage(file = 'ICON.png')
# root.iconphoto(False, photo)

# menu
main_menu = Menu(root)
sub_menu1 = Menu(main_menu,  tearoff= 0)
sub_menu1.add_command(label= 'Open File', command=browse)
sub_menu1.add_command(label= 'Save', command=save_text)
sub_menu1.add_separator()
sub_menu1.add_command(label= 'Save AS', command=save_text)
sub_menu1.add_command(label= 'Exit', command=exit_confirm)

sub_menu2 = Menu(main_menu, tearoff=0)
sub_menu2.add_command(label='Help', command=helpDesk)
sub_menu2.add_command(label='Check for update', command=checkUpdate)
sub_menu2.add_command(label='Feedback', command=contribute)

root.config(menu=main_menu)
main_menu.add_cascade(label='File', menu=sub_menu1)
main_menu.add_cascade(label='About', menu=sub_menu2)
# menu close

# img_button_green = PhotoImage(file='green pill.png')
# img_button_red = PhotoImage(file='red button.png')
# img_button_yellow = PhotoImage(file='yellow button.png')
# img_button_blue = PhotoImage(file='blue pill.png.')

frame_top = Frame(root, borderwidth=8, bg='light yellow', relief=RIDGE)
frame_top.pack(side=TOP, anchor='nw', fill=X)

camera_button = Button(frame_top, text='Open Camera', command=camera).grid(padx=10, pady=10, row=1, column=1)

browse_button = Button(frame_top, text='Browse file...  ', command=browse).grid(row=2, column=1, padx=10, pady='10')
browse_text = Entry(frame_top, width=100)
browse_text.insert(0, '')
browse_text.grid(row=2, column=2)
open_button = Button(frame_top, text='Open & Convert', width=13, command=convert).grid(row=2, column=6, padx=20)

frame_mid = Frame(root, borderwidth=8, bg='light yellow', relief=RIDGE)
frame_mid.pack(side=TOP, fill =X, pady=2)

Label(frame_mid, text='Extracted Text...').pack(anchor='nw')

show_text = scrolledtext.ScrolledText(frame_mid, undo=True, height=15)
show_text['font'] = ('lucidas', '13')
show_text.pack(fill=X, padx=2, pady=5)

save_txt_button = Button(frame_mid, text='Save file...', width=13, command=save_text).pack(side=RIGHT, padx=10, pady=10)
clear_txt_button = Button(frame_mid, text='Clear text', command=clearTxt, width=13).pack(side=RIGHT, padx=10)
frame_bottom = Frame(root, relief=FLAT, bg='light yellow', borderwidth=10)
frame_bottom.pack(side=BOTTOM, fill=BOTH, expand=True)

#status bar
statusVar = StringVar()
statusVar.set("Ready")
sbar = Label(frame_bottom, textvariable=statusVar, relief=SUNKEN, anchor='w')
sbar.pack(side=BOTTOM, fill=X)

exit_button = Button(frame_bottom, text='Exit', width=13, command=exit_confirm).pack(anchor='se', side=RIGHT, padx=10, pady=12)
convert_button = Button(frame_bottom, text='Convert', width=13, command=convert).pack(anchor="se", side=RIGHT, padx=10, pady=12)

root.mainloop()