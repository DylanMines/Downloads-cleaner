import os
import shutil
from tkinter import *

bg_color = "lightcyan"
text_color = "dimgrey"
button_color = "mediumturquoise"
button_active_color = "lightseagreen"
font = "Georga"

file_types = {
    "Pictures" : ["png","jpg","jpeg","gif","tiff","webp","av4","svg"],
    "Videos" : ["mp4","webm","mov","avi","mkv","wmv","avi",".3gp"],
    "Music" : ["mp3","wma","aac","wav","ogg","m4a"],
    "Documents" : ["pdf","docx","odt","xls","xlsx","zip","txt","ppt","psd"],
    "Applications" : ["exe","com","msi","appimage","dll","deb","ppa","rpm","flatpakref","swf"],
    "3D Objects" : ["obj","stl","3ds","fbx","3dm","iges","stp","step"],
    "Programming" : ["cpp","java","lua","py","c","js","json","html","css","mlx","mat"],
}

root = Tk()
size = [620,700]
root.geometry(str(size[0])+"x"+str(size[1]))
root.title("Download Cleaner")

class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

widgets = []
options = {}

class option:
    def __init__(self,name,file_types,selectScreen):
        frame = LabelFrame(selectScreen, text = name,bg = bg_color,fg = text_color,font=font)
        options[name] = BooleanVar()
        ChkButton = Checkbutton(frame,justify = LEFT,variable=options[name],bg = bg_color)
        #icon = PhotoImage(file=name+".png")
        #image = Label(frame,justify=LEFT,image=icon)
        #image.pack(side=LEFT)
        text = "("
        length = len(file_types[name])
        counter = 0
        for type in file_types[name]:
            text += type
            if counter < length-1:
                text += ", "
            counter+=1
        text += ")"
        label = Label(frame, text = text,bg = bg_color,fg = text_color,font=font)
        label.pack(side = RIGHT)
        ChkButton.pack(side = LEFT)
        frame.pack()

downloads = os.path.expanduser("~/Downloads")
files = [f for f in os.listdir(downloads) if os.path.isfile(os.path.join(downloads, f))]

def checkDirExist(path):
    isExist = os.path.exists(path)
    if not isExist:
        os.mkdir(path)
num_files = 0
def moveFiles(path,fileExts):
    for file in files:
        fileExt = os.path.splitext(file)[-1].lower()
        for ext in fileExts:
            if "."+ext == fileExt:
                #print(path+file)
                if os.path.isfile(path+"/"+file):
                    continue
                global num_files
                num_files+=1
                shutil.move(downloads+"/"+file, path)
def moveCategory(title):
    path = os.path.expanduser("~/"+title)
    checkDirExist(path)
    moveFiles(path, file_types[title])

selectScreen = Page(root,bg = bg_color)
loadingScreen = Page(root,bg = bg_color)
finishScreen = Page(root,bg = bg_color)

finish = Label(finishScreen,text = "Operation completed!",bg = bg_color,fg = text_color,font=font)
finish.pack(side = TOP,pady=20)

instructions = Label(selectScreen,
    text = "Select which files to move. Files will be moved to the location specified (ex. home/Pictures, home/Documents)",
    wraplength=size[0],bg = bg_color,fg = text_color,font=font)
instructions.pack(side = TOP,pady=15)

for location in file_types:
    widgets.append(option(location,file_types,selectScreen))


def go():
    loadingScreen.show()
    for selection in options:
        if options[selection].get() == True:
            moveCategory(selection)
    finishScreen.show()
    files_moved = Label(finishScreen,text = "Files moved: "+str(num_files),bg = bg_color,fg=text_color)
    files_moved.pack()
   
go_button = Button(selectScreen,text = "Clean!",command=go,bg = button_color,activebackground=button_active_color)
go_button.pack(side = BOTTOM,pady = 20)

def back():
    root.destroy()

back_button = Button(finishScreen,text = "Close",command=back,bg = button_color,activebackground=button_active_color)
back_button.pack(side = BOTTOM,pady = 20)

loadingLabel = Label(loadingScreen,text = "Please wait",bg = bg_color,fg = text_color,font=font)
loadingLabel.pack(pady=20)

container = Frame(root)
container.pack(side="top", fill="both", expand=True)

selectScreen.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
loadingScreen.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
finishScreen.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

selectScreen.show()

root.mainloop()