__author__ = "macaw"
import os
import subprocess
from tkinter import *
from tkinter import messagebox

def Exit():
    sure = messagebox.askyesno("Exit","คุณต้องการออกหรือไม่", parent=main)
    if sure == True:
        main.destroy()

def emp():
    os.environ['PYDEVD_DISABLE_FILE_VALIDATION'] = '1'
    main.withdraw()
    subprocess.Popen(["python", "D:\python\project_PY\AA1final.py"])
    main.deiconify()
    main.withdraw()
    

def adm():
    os.environ['PYDEVD_DISABLE_FILE_VALIDATION'] = '1'
    main.withdraw()
    subprocess.Popen(["python", "D:\python\project_PY\AA2final.py"])
    main.deiconify()
    main.withdraw()
    
    
main = Tk()
main.geometry("1366x768")
main.attributes('-fullscreen',True)
main.title("DR.PHARMACY")
main.resizable(0, 0)
main.protocol("WM_DELETE_WINDOW", Exit)

label1 = Label(main)
label1.place(relx=0, rely=0, width=1366, height=768)
img = PhotoImage(file="D:\python\project_PY\APmain.png")
label1.configure(image=img)

button1 = Button(main)
button1.place(x=990, y=270, width=164, height=90)
button1.configure(relief="flat")
button1.configure(overrelief="flat")
button1.configure(activebackground="#ffffff")
button1.configure(cursor="hand2")
button1.configure(foreground="#ffffff")
button1.configure(background="#ffffff")
button1.configure(borderwidth="0")
img2 = PhotoImage(file="D:\python\project_PY\EMP.png")
button1.configure(image=img2)
button1.configure(command=emp)

button2 = Button(main)
button2.place(x=990, y=600, width=164, height=90)
button2.configure(relief="flat")
button2.configure(overrelief="flat")
button2.configure(activebackground="#ffffff")
button2.configure(cursor="hand2")
button2.configure(foreground="#ffffff")
button2.configure(background="#ffffff")
button2.configure(borderwidth="0")
img3 = PhotoImage(file="D:\python\project_PY\MP.png")
button2.configure(image=img3)
button2.configure(command=adm)

button3 = Button(main)
button3.place(x=1180, y=40, width=86, height=34)
button3.configure(relief="flat")
button3.configure(overrelief="flat")
button3.configure(activebackground="#CF1E14")
button3.configure(cursor="hand2")
button3.configure(foreground="#ffffff")
button3.configure(background="#CF1E14")
button3.configure(font="-family {Poppins SemiBold} -size 14")
button3.configure(borderwidth="0")
button3.configure(text="""ย้อนกลับ""")
button3.configure(command=Exit)

main.mainloop()


