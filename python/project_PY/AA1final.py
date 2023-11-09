#==================imports===================
import sqlite3
import re
import random
import string
import os
import subprocess
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from time import strftime
import datetime
from datetime import date,datetime
from tkinter import scrolledtext as tkst
from PIL import Image,ImageTk
from io import BytesIO
from reportlab.lib.pagesizes import  inch
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import webbrowser
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
import subprocess
from reportlab.lib import colors  # Add this import line


# Provide the full path to the "TH Sarabun New" font file
font_path = r"D:\python\project_PY\font\THSarabunNew.ttf"

# Register the "TH Sarabun New" font
pdfmetrics.registerFont(TTFont('THSarabunNew', font_path))

#============================================



root = Tk()

root.geometry("1366x768")
root.attributes('-fullscreen',True)
root.title("DR.PHARMACY (ส่วนพนักงานร้าน)")


user = StringVar()
passwd = StringVar()
fname = StringVar()
lname = StringVar()
new_user = StringVar()
new_passwd = StringVar()
 

cust_name = StringVar()
cust_num = StringVar()
cust_new_bill = StringVar()
cust_search_bill = StringVar()
bill_dates = StringVar()

pdf_data = []


with sqlite3.connect("D:\python\project_PY\Datdproject.db") as db:
    cur = db.cursor()

def random_bill_number(stringLength):
    lettersAndDigits = string.ascii_letters.upper() + string.digits
    strr=''.join(random.choice(lettersAndDigits) for i in range(stringLength-2))
    return ('BB'+strr)




def login(Event=None):
    global username
    username = user.get()
    password = passwd.get()

    with sqlite3.connect("D:\python\project_PY\Datdproject.db") as db:
        cur = db.cursor()
    find_user = "SELECT * FROM employee WHERE emp_id = ? and password = ?"
    cur.execute(find_user, [username, password])
    results = cur.fetchall()

    if username == "exit" and password == "exit" :
        sure = messagebox.askyesno("ปิดโปรแกรม","คุณต้องการออกจากโปรแกรมใช่ไหม?", parent=root)
        if sure == True:
            os.environ['PYDEVD_DISABLE_FILE_VALIDATION'] = '1'
            root.withdraw()
            subprocess.Popen(["python", "D:\python\project_PY\minaAA.py"])
            root.deiconify()
            root.withdraw()

    elif results:
        messagebox.showinfo("หน้าล็อคอิน", "เข้าสู่ระบบสำเร็จ")
        page1.entry1.delete(0, END)
        page1.entry2.delete(0, END)
        root.withdraw()
        global biller
        global page2
        biller = Toplevel()
        biller.attributes('-fullscreen',True)
        page2 = bill_window(biller)
        page2.time()
        biller.protocol("WM_DELETE_WINDOW", exitt)
        biller.mainloop()

    else:
        messagebox.showerror("ผิดพลาด", "ชื่อหรือรหัสผ่านไม่ถูกต้อง")
        page1.entry2.delete(0, END)



def logout():
    sure = messagebox.askyesno("ออกจากระบบ", "คุณต้องการออกจากระบบใช่ไหม?", parent=biller)
    if sure == True:
        biller.destroy()
        root.deiconify()
        page1.entry1.delete(0, END)
        page1.entry2.delete(0, END)

class login_page:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("ล็อคอิน พนักงานร้าน")

        self.label1 = Label(root)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="D:\python\project_PY\empoyerrim.png")
        self.label1.configure(image=self.img)

        self.entry1 = Entry(root)
        self.entry1.place(relx=0.353, rely=0.293, width=374, height=24)
        self.entry1.configure(highlightbackground="black",highlightthickness=1,highlightcolor="black")
        self.entry1.configure(font="-family {Poppins} -size 10")
        self.entry1.configure(relief="flat")
        self.entry1.configure(textvariable=user)

        self.entry2 = Entry(root)
        self.entry2.place(relx=0.353, rely=0.404, width=374, height=24)
        self.entry2.configure(highlightbackground="black",highlightthickness=1,highlightcolor="black")
        self.entry2.configure(font="-family {Poppins} -size 10")
        self.entry2.configure(relief="flat")
        self.entry2.configure(show="*")
        self.entry2.configure(textvariable=passwd)

        self.button1 = Button(root)
        self.button1.place(relx=0.366, rely=0.685, width=356, height=43)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#D2463E")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#D2463E")
        self.button1.configure(font="-family {Poppins SemiBold} -size 20")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""เข้าสู่ระบบ""")
        self.button1.configure(command=login)


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Item:
    def __init__(self, name, price, qty):
        self.product_name = name
        self.price = price
        self.qty = qty

class Cart:
    def __init__(self):
        self.items = []
        self.dictionary = {}

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self):
        self.items.pop()

    def remove_items(self):
        self.items.clear()

    def total(self):
        total = 0.0
        for i in self.items:
            total += i.price * i.qty
        return total

    def isEmpty(self):
        if len(self.items)==0:
            return True
        
    def allCart(self):
        for i in self.items:
            if (i.product_name in self.dictionary):
                self.dictionary[i.product_name] += i.qty
            else:
                self.dictionary.update({i.product_name:i.qty})


def exitt():
    sure = messagebox.askyesno("ปิดโปรแกรม","คุณต้องการออกจากโปรแกรมใช่ไหม?", parent=biller)
    if sure == True:
        biller.destroy()
        root.destroy()


class bill_window:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.attributes('-fullscreen',True)
        top.resizable(0, 0)
        top.title("ระบบคิดเงิน")

        self.label = Label(biller)
        self.label.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file=r"D:\python\project_PY\billy.png")
        self.label.configure(image=self.img)

        self.label1 = Label(biller)
        self.label1.place(relx=0.775, rely=0.530, width=160, height=160)
        self.label1.configure(state="normal")

        self.message = Label(biller)
        self.message.place(relx=0.034, rely=0.055, width=80, height=30)
        self.message.configure(highlightthickness=0,highlightcolor="black")
        self.message.configure(font="-family {Poppins} -size 10")
        self.message.configure(foreground="#000000")
        self.message.configure(background="#ffffff")
        self.message.configure(text=username)
        self.message.configure(anchor="w")

        self.clock = Label(biller)
        self.clock.place(relx=0.9, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        self.entry1 = Entry(biller)
        self.entry1.place(relx=0.515, rely=0.23, width=230, height=24)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")
        self.entry1.configure(textvariable=cust_name)

        self.entry2 = Entry(biller)
        self.entry2.place(relx=0.802, rely=0.23, width=230, height=24)
        self.entry2.configure(font="-family {Poppins} -size 12")
        self.entry2.configure(relief="flat")
        self.entry2.configure(textvariable=cust_num)

        self.entry3 = Entry(biller)
        self.entry3.place(relx=0.105, rely=0.23, width=240, height=24)
        self.entry3.configure(font="-family {Poppins} -size 12")
        self.entry3.configure(relief="flat")
        self.entry3.configure(textvariable=cust_search_bill)

        self.button1 = Button(biller)
        self.button1.place(relx=0.034, rely=0.104, width=78, height=23)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#76AEC3")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#000000")
        self.button1.configure(background="#76AEC3")
        self.button1.configure(font="-family {Poppins SemiBold} -size 12")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""ออกจากระบบ""")
        self.button1.configure(command=logout)

        self.button2 = Button(biller)
        self.button2.place(relx=0.312, rely=0.234, width=80, height=23)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#325E6D")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#325E6D")
        self.button2.configure(font="-family {Poppins SemiBold} -size 10")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""ค้นหาใบเสร็จ""")
        self.button2.configure(command=self.search_bill)

        self.button3 = Button(biller)
        self.button3.place(relx=0.586, rely=0.877, width=86, height=25)
        self.button3.configure(relief="flat")
        self.button3.configure(overrelief="flat")
        self.button3.configure(activebackground="#76AEC3")
        self.button3.configure(cursor="hand2")
        self.button3.configure(foreground="#000000")
        self.button3.configure(background="#76AEC3")
        self.button3.configure(font="-family {Poppins SemiBold} -size 12")
        self.button3.configure(borderwidth="0")
        self.button3.configure(text="""คิดเงิน""")
        self.button3.configure(command=self.pay_bill)
        self.button3.configure(state="disabled")        

        self.button4 = Button(biller)
        self.button4.place(relx=0.682, rely=0.877, width=86, height=25)
        self.button4.configure(relief="flat")
        self.button4.configure(overrelief="flat")
        self.button4.configure(activebackground="#76AEC3")
        self.button4.configure(cursor="hand2")
        self.button4.configure(foreground="#000000")
        self.button4.configure(background="#76AEC3")
        self.button4.configure(font="-family {Poppins SemiBold} -size 12")
        self.button4.configure(borderwidth="0")
        self.button4.configure(text="""สร้างใบเสร็จ""")
        self.button4.configure(command=self.gen_bill)
        self.button4.configure(state="disabled")

        self.button5 = Button(biller)
        self.button5.place(relx=0.779, rely=0.877, width=86, height=25)
        self.button5.configure(relief="flat")
        self.button5.configure(overrelief="flat")
        self.button5.configure(activebackground="#76AEC3")
        self.button5.configure(cursor="hand2")
        self.button5.configure(foreground="#000000")
        self.button5.configure(background="#76AEC3")
        self.button5.configure(font="-family {Poppins SemiBold} -size 12")
        self.button5.configure(borderwidth="0")
        self.button5.configure(text="""เคลียร์""")
        self.button5.configure(command=self.clear_bill)

        self.button6 = Button(biller)
        self.button6.place(relx=0.868, rely=0.877, width=86, height=25)
        self.button6.configure(relief="flat")
        self.button6.configure(overrelief="flat")
        self.button6.configure(activebackground="#76AEC3")
        self.button6.configure(cursor="hand2")
        self.button6.configure(foreground="#000000")
        self.button6.configure(background="#76AEC3")
        self.button6.configure(font="-family {Poppins SemiBold} -size 12")
        self.button6.configure(borderwidth="0")
        self.button6.configure(text="""ออก""")
        self.button6.configure(command=exitt)

        self.button7 = Button(biller)
        self.button7.place(relx=0.626, rely=0.763, width=86, height=26)
        self.button7.configure(relief="flat")
        self.button7.configure(overrelief="flat")
        self.button7.configure(activebackground="#76AEC3")
        self.button7.configure(cursor="hand2")
        self.button7.configure(foreground="#000000")
        self.button7.configure(background="#76AEC3")
        self.button7.configure(font="-family {Poppins SemiBold} -size 12")
        self.button7.configure(borderwidth="0")
        self.button7.configure(text="""เพิ่มเข้าตะกร้า""")
        self.button7.configure(command=self.add_to_cart)

        #self.button8 = Button(biller)
        #self.button8.place(relx=0.829, rely=0.763, width=86, height=26)
        #self.button8.configure(relief="flat")
        #self.button8.configure(overrelief="flat")
        #self.button8.configure(activebackground="#76AEC3")
        #self.button8.configure(cursor="hand2")
        #self.button8.configure(foreground="#000000")
        #self.button8.configure(background="#76AEC3")
        #self.button8.configure(font="-family {Poppins SemiBold} -size 12")
        #self.button8.configure(borderwidth="0")
        #self.button8.configure(text="""เคลียร์""")
        #self.button8.configure(command=self.clear_selection)

        self.button9 = Button(biller)
        self.button9.place(relx=0.726, rely=0.763, width=86, height=26)
        self.button9.configure(relief="flat")
        self.button9.configure(overrelief="flat")
        self.button9.configure(activebackground="#76AEC3")
        self.button9.configure(cursor="hand2")
        self.button9.configure(foreground="#000000")
        self.button9.configure(background="#76AEC3")
        self.button9.configure(font="-family {Poppins SemiBold} -size 12")
        self.button9.configure(borderwidth="0")
        self.button9.configure(text="""นำออก""")
        self.button9.configure(command=self.remove_product)

        text_font = ("Poppins", "8")
        self.combo1 = ttk.Combobox(biller)
        self.combo1.place(relx=0.594, rely=0.408, width=477, height=26)

        find_category = "SELECT product_cat FROM products"
        cur.execute(find_category)
        result1 = cur.fetchall()
        cat = []
        for i in range(len(result1)):
            if(result1[i][0] not in cat):
                cat.append(result1[i][0])

        self.combo1.configure(values=cat)
        self.combo1.configure(state="readonly")
        self.combo1.configure(font="-family {Poppins} -size 8")
        self.combo1.option_add("*TCombobox*Listbox.font", text_font)
        self.combo1.option_add("*TCombobox*Listbox.selectBackground", "#D2463E")

        self.combo2 = ttk.Combobox(biller)
        self.combo2.place(relx=0.594, rely=0.479, width=477, height=26)
        self.combo2.configure(font="-family {Poppins} -size 8")
        self.combo2.option_add("*TCombobox*Listbox.font", text_font) 
        self.combo2.configure(state="disabled")

        self.combo3 = ttk.Combobox(biller)
        self.combo3.place(relx=0.594, rely=0.551, width=120, height=26)
        self.combo3.configure(state="disabled")
        self.combo3.configure(font="-family {Poppins} -size 8")
        self.combo3.option_add("*TCombobox*Listbox.font", text_font)

        self.entry4 = ttk.Entry(biller)
        self.entry4.place(relx=0.594, rely=0.629, width=120, height=26)
        self.entry4.configure(font="-family {Poppins} -size 8")
        self.entry4.configure(foreground="#000000")
        self.entry4.configure(state="disabled")

        self.Scrolledtext1 = tkst.ScrolledText(top)
        self.Scrolledtext1.place(relx=0.040, rely=0.580, width=695, height=275)
        self.Scrolledtext1.configure(borderwidth=0)
        self.Scrolledtext1.configure(font="-family {Podkova} -size 8")
        self.Scrolledtext1.configure(state="disabled")

        self.combo1.bind("<<ComboboxSelected>>", self.get_category)
        
    def get_category(self, Event):
        self.entry4.delete(0, END)
        self.entry4.configure(state="disabled")
        self.combo2.configure(state="readonly")
        self.combo2.set('')
        self.combo3.set('')
        find_subcat = "SELECT product_subcat FROM products WHERE product_cat = ?"
        cur.execute(find_subcat, [self.combo1.get()])
        result2 = cur.fetchall()
        subcat = []
        for j in range(len(result2)):
            if(result2[j][0] not in subcat):
                subcat.append(result2[j][0])
        
        self.combo2.configure(values=subcat)
        self.combo2.bind("<<ComboboxSelected>>", self.get_subcat)
        self.combo3.configure(state="disabled")

    def get_subcat(self, Event):
        self.combo3.configure(state="readonly")
        self.combo3.set('')
        find_product = "SELECT product_name FROM products WHERE product_cat = ? and product_subcat = ?"
        cur.execute(find_product, [self.combo1.get(), self.combo2.get()])
        result3 = cur.fetchall()
        pro = []
        for k in range(len(result3)):
            pro.append(result3[k][0])



        self.combo3.configure(values=pro)
        self.combo3.bind("<<ComboboxSelected>>", self.show_qty)



    def show_qty(self, Event):
        self.entry4.configure(state="normal")
        self.qty_label = Label(biller)
        self.qty_label.place(relx=0.594, rely=0.664, width=82, height=26)
        self.qty_label.configure(font="-family {Poppins} -size 8")
        self.qty_label.configure(anchor="w")

        product_name = self.combo3.get()
        find_qty = "SELECT stock FROM products WHERE product_name = ?"
        cur.execute(find_qty, [product_name])
        results = cur.fetchone()
        self.qty_label.configure(text="คงเหลือ : {}".format(results[0]))
        self.qty_label.configure(background="#ffffff")
        self.qty_label.configure(foreground="#333333")
        self.show_picture()


    def show_picture(self):
        i=0
        product_name = self.combo3.get()
        print(product_name)
        find_picture = "SELECT picture FROM products WHERE product_name = ?"
        cur.execute(find_picture, [product_name])
        results = cur.fetchone()
        if results and results[0]:
            print("มีข้อมูล")
            image_product = Image.open(BytesIO(results[0]))
            target_width, target_height = 150, 150
            image_products = image_product.resize((target_width, target_height))
            img_products = ImageTk.PhotoImage(image_products)


            self.label1.configure(image=img_products)
            self.label1.img = img_products
        else:
            print("ไม่มีข้อมูล")
            img_no_photo = PhotoImage(file=r"D:\python\project_PY\NOT_FOUND.png")
            self.label1.configure(image=img_no_photo)
            self.label1.img = img_no_photo
            


    cart = Cart()
    def add_to_cart(self):
        global pdf_data
        self.Scrolledtext1.configure(state="normal")
        strr = self.Scrolledtext1.get('1.0', END)
        if strr.find('Total')==-1:
            product_name = self.combo3.get()
            if(product_name!=""):
                product_qty = self.entry4.get()
                find_mrp = "SELECT mrp, stock FROM products WHERE product_name = ?"
                cur.execute(find_mrp, [product_name])
                results = cur.fetchall()
                stock = results[0][1]
                mrp = results[0][0]
                if product_qty.isdigit()==True:
                    if (stock-int(product_qty))>=0:
                        sp = mrp*int(product_qty)
                        item = Item(product_name, mrp, int(product_qty))
                        self.cart.add_item(item)
                        pdf_data.append((product_name, product_qty, sp),)

                        self.Scrolledtext1.configure(state="normal")
                        bill_text = "{}\t\t\t\t\t\t{}\t\t\t\t\t   {}\n".format(product_name, product_qty, sp)
                        self.Scrolledtext1.insert('insert', bill_text)
                        self.Scrolledtext1.configure(state="disabled")
                    else:
                        messagebox.showerror("ผิดพลาด!", "สินค้าหมด โปรดเช็คจำนวน", parent=biller)
                else:
                    messagebox.showerror("ผิดพลาด!", "จำนวนไม่ถูกต้อง", parent=biller)
            else:
                messagebox.showerror("ผิดพลาด!", "เลือกสินค้าก่อน", parent=biller)
        else:
            self.Scrolledtext1.delete('1.0', END)
            new_li = []
            li = strr.split("\n")
            for i in range(len(li)):
                if len(li[i])!=0:
                    if li[i].find('Total')==-1:
                        new_li.append(li[i])
                    else:
                        break
            for j in range(len(new_li)-1):
                self.Scrolledtext1.insert('insert', new_li[j])
                self.Scrolledtext1.insert('insert','\n')
            product_name = self.combo3.get()
            if(product_name!=""):
                product_qty = self.entry4.get()
                find_mrp = "SELECT mrp, stock, product_id FROM products WHERE product_name = ?"
                cur.execute(find_mrp, [product_name])
                results = cur.fetchall()
                stock = results[0][1]
                mrp = results[0][0]
                if product_qty.isdigit()==True:
                    if (stock-int(product_qty))>=0:
                        sp = results[0][0]*int(product_qty)
                        item = Item(product_name, mrp, int(product_qty))
                        self.cart.add_item(item)
                        pdf_data.append((product_name, product_qty, sp),)
                        self.Scrolledtext1.configure(state="normal")
                        bill_text = "{}\t\t\t\t\t\t{}\t\t\t\t\t   {}\n".format(product_name, product_qty, sp)
                        
                        
                        self.Scrolledtext1.insert('insert', bill_text)
                        self.Scrolledtext1.configure(state="disabled")
                    else:
                        messagebox.showerror("ผิดพลาด!", "สินค้าหมด โปรดเช็คจำนวน", parent=biller)
                else:
                    messagebox.showerror("ผิดพลาด!", "จำนเวนไม่ถูกต้อง", parent=biller)
            else:
                messagebox.showerror("ผิดพลาด!", "เลือกสินค้าก่อน", parent=biller)
        def total_bill(self):
            if self.cart.isEmpty():
                messagebox.showerror("ผิดพลาด!", "เพิ่มสินค้าก่อน", parent=biller)
            else:
                self.Scrolledtext1.configure(state="normal")
                strr = self.Scrolledtext1.get('1.0', END)
                if strr.find('Total')==-1:
                    self.Scrolledtext1.configure(state="normal")
                    divider = "\n\n\n"+("─"*61)
                    self.Scrolledtext1.insert('insert', divider)
                    total = "\nTotal\t\t\t\t\t\t\t\t\t\t\t {}".format(self.cart.total())
                    self.Scrolledtext1.insert('insert', total)
                    divider2 = "\n"+("─"*61)
                    self.Scrolledtext1.insert('insert', divider2)
                    self.Scrolledtext1.configure(state="disabled")
                else:
                    return
        
        total_bill(self)
        self.clear_selection()

    def remove_product(self):
        if(self.cart.isEmpty()!=True):
            self.Scrolledtext1.configure(state="normal")
            strr = self.Scrolledtext1.get('1.0', END)
            if strr.find('Total')==-1:
                try:
                    self.cart.remove_item()
                except IndexError:
                    messagebox.showerror("ผิดพลาด!", "ตะกร้าว่างเปล่า", parent=biller)
                else:
                    self.Scrolledtext1.configure(state="normal")
                    get_all_bill = (self.Scrolledtext1.get('1.0', END).split("\n"))
                    new_string = get_all_bill[:len(get_all_bill)-3]
                    self.Scrolledtext1.delete('1.0', END)
                    for i in range(len(new_string)):
                        self.Scrolledtext1.insert('insert', new_string[i])
                        self.Scrolledtext1.insert('insert','\n')
                    
                    self.Scrolledtext1.configure(state="disabled")
            else:
                try:
                    self.cart.remove_item()
                except IndexError:
                    messagebox.showerror("ผิดพลาด!", "ตะกร้าว่างเปล่า", parent=biller)
                else:
                    self.Scrolledtext1.delete('1.0', END)
                    new_li = []
                    li = strr.split("\n")
                    for i in range(len(li)):
                        if len(li[i])!=0:
                            if li[i].find('Total')==-1:
                                new_li.append(li[i])
                            else:
                                break
                    new_li.pop()
                    for j in range(len(new_li)-1):
                        self.Scrolledtext1.insert('insert', new_li[j])
                        self.Scrolledtext1.insert('insert','\n')
                    self.Scrolledtext1.configure(state="disabled")

        else:
            messagebox.showerror("ผิดพลาด!", "เพิ่มสินค้าก่อน", parent=biller)




    def wel_bill(self):
        self.name_message = Text(biller)
        self.name_message.place(relx=0.119, rely=0.452, width=176, height=30)
        self.name_message.configure(font="-family {Podkova} -size 10")
        self.name_message.configure(borderwidth=0)
        self.name_message.configure(background="#ffffff")

        self.num_message = Text(biller)
        self.num_message.place(relx=0.484, rely=0.452, width=90, height=30)
        self.num_message.configure(font="-family {Podkova} -size 10")
        self.num_message.configure(borderwidth=0)
        self.num_message.configure(background="#ffffff")

        self.bill_message = Text(biller)
        self.bill_message.place(relx=0.104, rely=0.477, width=176, height=26)
        self.bill_message.configure(font="-family {Podkova} -size 10")
        self.bill_message.configure(borderwidth=0) 
        self.bill_message.configure(background="#ffffff")

        self.bill_date_message = Text(biller)
        self.bill_date_message.place(relx=0.457, rely=0.477, width=90, height=26)
        self.bill_date_message.configure(font="-family {Podkova} -size 10")
        self.bill_date_message.configure(borderwidth=0)
        self.bill_date_message.configure(background="#ffffff")













    def pay_bill(self):
        self.label1.configure(image=None)

        global total_last,money
        paybill = Toplevel()
        paybill.geometry("700x500")
        paybill.title("Pay_bills")
 
        money = 0

        self.labelpay = Label(paybill)
        self.labelpay.place(relx=0, rely=0, width=700, height=500)
        self.imgpaybill = PhotoImage(file="D:\python\project_PY\cal_num.png")
        self.labelpay.configure(image=self.imgpaybill)



        self.label2 = Label(paybill)
        self.label2.place(relx=0.46, rely=0.33, width=100, height=20)
        self.label2.configure(font="-family {Poppins} -size 14")
        self.label2.configure(anchor="w")

        self.label3 = Label(paybill)
        self.label3.place(relx=0.46, rely=0.555, width=100, height=20)
        self.label3.configure(font="-family {Poppins} -size 14")
        self.label3.configure(anchor="w")
        self.label3.configure(background="#ffffff")
        self.label3.configure(foreground="#333333")
        
        self.label2.configure(text="{}".format(self.cart.total()))
        self.label2.configure(background="#ffffff")
        self.label2.configure(foreground="#333333")


        def cal_money():
      
            global total_last,money
            total = int(self.cart.total())
            money = int(self.entry5.get())
            if money < total:
                messagebox.showerror("Oops!!", "จำนวนเงินไม่พอ", parent=paybill)
            else:
                total_last = money-total
                self.label3.configure(text="{}".format(total_last))
                self.label3.configure(background="#ffffff")
                self.label3.configure(foreground="#333333")
                


        def submit_cal_money():
            self.button4.configure(state="normal")
            self.entry5.delete(0,END)
            paybill.withdraw()

       
 

        self.button1 = Button(paybill)
        self.button1.place(relx=0.3, rely=0.740, width=78, height=23)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#76AEC3")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#000000")
        self.button1.configure(background="#76AEC3")
        self.button1.configure(font="-family {Poppins SemiBold} -size 12")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""คิดเงิน""")
        self.button1.configure(command=cal_money)

        self.button2 = Button(paybill)
        self.button2.place(relx=0.590, rely=0.740, width=78, height=23)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#76AEC3")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#000000")
        self.button2.configure(background="#76AEC3")
        self.button2.configure(font="-family {Poppins SemiBold} -size 12")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""ยืนยัน""")
        self.button2.configure(command=submit_cal_money)

        self.entry5 = Entry(paybill)
        self.entry5.place(relx=0.46, rely=0.445, width=100, height=24)
        self.entry5.configure(font="-family {Poppins} -size 14")
        self.entry5.configure(relief="flat")
        self.entry5.configure(textvariable=money)


        paybill.mainloop()




    state = 1
    def gen_bill(self):
        global pdf_data,total_last,money
        print('1')
        if self.state == 1:
            strr = self.Scrolledtext1.get('1.0', END)
            self.wel_bill()
            if(cust_name.get()==""):
                messagebox.showerror("ผิดพลาด!", "กรุณากรอกชื่อลูกค้า", parent=biller)
            elif(cust_num.get()==""):
                messagebox.showerror("ผิดพลาด!", "กรุณากรอกเบอร์โทรศัพท์", parent=biller)
            elif(self.cart.isEmpty()):
                messagebox.showerror("ผิดพลาด!", "ตะกร้าว่างเปล่า", parent=biller)
            else: 
                if strr.find('Total')==-1:
                    self.total_bill()
                    self.gen_bill()
                else:
                    self.name_message.insert(END, cust_name.get())
                    self.name_message.configure(state="disabled")
            
                    self.num_message.insert(END, cust_num.get())
                    self.num_message.configure(state="disabled")
            
                    cust_new_bill.set(random_bill_number(8))

                    self.bill_message.insert(END, cust_new_bill.get())
                    self.bill_message.configure(state="disabled")
                
                    bill_dates=datetime.now()
                    day = bill_dates.strftime("%d/%m/%Y")
                    month = bill_dates.strftime("%m/%Y")
                    day_name = bill_dates.strftime("%d%m%Y")
                    time = bill_dates.strftime("%H%M%S")

                    self.bill_date_message.insert(END,day)
                    self.bill_date_message.configure(state="disabled")


                    def generate_bill():

                        print(pdf_data)
           

                        title_style = ParagraphStyle(
                            name='TitleStyle',
                            fontSize=16,
                            fontName='THSarabunNew',
                            alignment=0,
                            spaceAfter=12,
                        )

                        content_style = ParagraphStyle(
                            name='TitleStyle',
                            fontSize=16,
                            fontName='THSarabunNew',
                            alignment=2,
                            spaceAfter=12,
                        )


                        title_table = ParagraphStyle(
                            name='TitleStyle',
                            fontSize=16,
                            fontName='THSarabunNew',
                            alignment=0,
                            spaceAfter=12,
                            leading=14
                        )
                        # Define a separate style for larger titles
                        larger_title_style = ParagraphStyle(
                            name='LargerTitleStyle',
                            fontSize=22,  # Increase the font size to 24
                            fontName='THSarabunNew',
                            alignment=1,
                            spaceAfter=12,
                        )

                        # Define the content style with "TH Sarabun New" font


                        def generate_report():

                            file_name =(r"D:\python\project_PY\pdf\receipt_"+day_name+"_"+time+".pdf")
                            print(file_name)

                            doc = SimpleDocTemplate(file_name, pagesize=letter)
                            story = []
                            
                            # Add a title to the report
                            title1 = Paragraph("ใบเสร็จรับเงิน", larger_title_style)  # Use the larger_title_style for these titles
                            story.append(title1)

                            title2 = Paragraph("BILL", larger_title_style)
                            story.append(title2)

                            # Add some spacing
                            spacing_paragraph = Paragraph("<br/><br/>", title_style)  # Empty paragraph with line breaks
                            story.append(spacing_paragraph)

                            title3 = Paragraph("เลขที่ใบเสร็จ : {}".format(cust_new_bill.get()), title_style)
                            story.append(title3)

                            title4 = Paragraph("วันที่ : {}".format(day), title_style)
                            story.append(title4)

                            title5 = Paragraph("ชื่อลูกค้า : {}".format(cust_name.get()), title_style) 
                            story.append(title5)

                            title6 = Paragraph("เบอร์โทรศัพท์ : {}".format(cust_num.get()), title_style)
                            story.append(title6)


                            # Add some spacing
                            spacing_paragraph = Paragraph("<br/><br/>", title_style)  # Empty paragraph with line breaks
                            story.append(spacing_paragraph)

                            table_data = [
                                ['รายการ', 'จำนวน', 'ราคาต่อหน่วย'],
                            ]

                            data = table_data+pdf_data

                            # Create the first table with a specified width
                            table_width =235  # You can adjust this width as needed
                            col_widths = [table_width, table_width / 2, table_width / 2]
                            table = Table(data, colWidths=col_widths)

                            # Apply styles to the first table
                            table_style = TableStyle([
                                ('BACKGROUND', (0, 0), (-1, 0), colors.white),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                ('ALIGN', (0, 0), (1, 0), 'LEFT'),
                                ('ALIGN', (1, 0), (2, 0), 'CENTER'),
                                ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                                ('ALIGN', (1, 1), (1, -1), 'CENTER'),
                                ('ALIGN', (2, 1), (2, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'THSarabunNew'),
                                ('FONTNAME', (0, 1), (-1, -1), 'THSarabunNew'),
                                ('FONTSIZE', (0, 0), (-1, -1), 13),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                                ('GRID', (0, 0), (-1, -1), 1, colors.white)
                            ])

                            table.setStyle(table_style)
                        

                            # Append the first table to the story
                            story.append(table)

                            # Add some spacing (an empty paragraph with line breaks) between the two tables
                            spacing_paragraph = Paragraph("<br/><br/>", title_style)
                            story.append(spacing_paragraph)
                            spacing_paragraph = Paragraph("<br/><br/>", title_style)  # Empty paragraph with line breaks
                            story.append(spacing_paragraph)
                            # Append the second table to the story
                            title7 = Paragraph("รวมทั้งสิ้น : {} บาท".format(self.cart.total()), content_style)
                            story.append(title7)

                            title8 = Paragraph("ได้รับมาจำนวน : {} บาท".format(money), content_style)
                            story.append(title8)

                            title9 = Paragraph("มีเงินทอน : {} บาท".format(total_last), content_style)
                            story.append(title9)
                            # Build the PDF report
                            doc.build(story)
                            pdf_data.clear()
                            insert = ('''UPDATE bill SET pdf_path = ? WHERE bill_no = ?''')
                            cur.execute(insert, [file_name,cust_new_bill.get()])
                            db.commit()
                            self.clear_bill()
                            subprocess.Popen(['start', '',file_name], shell=True)


                            # Open the PDF report with the default PDF viewer (on Windows)
                        if __name__ == '__main__':
                            generate_report()
                        messagebox.showinfo("ใบเสร็จ","ดำเนินการเสร็จสิ้น")

          
                    insert = (
                        "INSERT INTO bill(bill_no, date, customer_name, customer_no, bill_details, month, income) VALUES(?,?,?,?,?,?,?)"
                    )
                    cur.execute(insert, [cust_new_bill.get(),day, cust_name.get(), cust_num.get(), self.Scrolledtext1.get('1.0', END), month, self.cart.total()])
                    db.commit()
                    print(self.cart.items)
                    print(self.cart.allCart())
                    for name, qty in self.cart.dictionary.items():

                        update_qty = "UPDATE products SET stock = stock - ? WHERE product_name = ?"
                        cur.execute(update_qty, [qty, name])
                        db.commit()
                    messagebox.showinfo("Success!!", "Bill Generated", parent=biller)
                    self.entry1.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
                    self.entry2.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
                    self.state = 0
                    generate_bill()
        else:
            return








                    
        
     
    def clear_bill(self):
        self.wel_bill()
        self.clear_selection()
        self.entry1.configure(state="normal")
        self.entry2.configure(state="normal")
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)
        self.name_message.configure(state="normal")
        self.num_message.configure(state="normal")
        self.bill_message.configure(state="normal")
        self.bill_date_message.configure(state="normal")
        self.Scrolledtext1.configure(state="normal")
        self.name_message.delete(1.0, END)
        self.num_message.delete(1.0, END)
        self.bill_message.delete(1.0, END)
        self.bill_date_message.delete(1.0, END)
        self.Scrolledtext1.delete(1.0, END)
        self.name_message.configure(state="disabled")
        self.num_message.configure(state="disabled")
        self.bill_message.configure(state="disabled")
        self.bill_date_message.configure(state="disabled")
        self.Scrolledtext1.configure(state="disabled")
        self.button3.configure(state="disabled")        
        self.cart.remove_items()

        self.state = 1
        self.combo1.configure(state="readonly")


    def clear_selection(self):
        self.entry4.delete(0, END)
        self.button3.configure(state="normal")        
        self.combo1.configure(state="normal")
        self.combo2.configure(state="normal")
        self.combo3.configure(state="normal")
        self.combo1.delete(0, END)
        self.combo2.delete(0, END)
        self.combo3.delete(0, END)
        self.combo1.configure(state="readonly")
        self.combo2.configure(state="disabled")
        self.combo3.configure(state="disabled")
        self.entry4.configure(state="disabled")
        self.button4.configure(state="disabled")
        self.qty_label.place_forget()
        self.label1.configure(image='')

             
    def search_bill(self):
        find_bill = "SELECT * FROM bill WHERE bill_no = ?"
        cur.execute(find_bill, [cust_search_bill.get().rstrip()])
        results = cur.fetchall()
        if results:
            print(results)
            subprocess.Popen(['start', '', results[0][6]], shell=True)



        else:
            messagebox.showerror("ผิดพลาด!!", "หาใบเสร็จไม่เจอ", parent=biller)
            self.entry3.delete(0, END)
            
    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)

    






        

    




page1 = login_page(root)
root.bind("<Return>", login)
root.mainloop()

'''
    def generate_bill(bill_no):
        bill_no = cust_new_bill.get()


        def pdf():
            # ค้นหาค่าลำดับที่ล่าสุดจาก SQLite
            generate_bill = "SELECT * FROM bill WHERE bill_no = ?"  #เลือกข้อมูลล่าสุด
            cur.execute(generate_bill, (bill_no))
            last_id = cur.fetchone()[0]#ดึงข้อมูลคอลัมแรกมา คือลำดับล่าสุดของsqlite


            custom_page_size = (5 * inch, 3 * inch)
            # สร้างไฟล์ PDF
            current_datetime = datetime.datetime.now()
            pdf_file_name = f'queue_{current_datetime.strftime("%Y%m%d_%H%M%S")}.pdf'
            doc = SimpleDocTemplate(pdf_file_name, pagesize=custom_page_size) #คลาสในโมดูล reportlab.platypus ที่ใช้สร้างเอกสาร PDF โดยรับพารามิเตอร์หลักสองตัวคือ pdf_file_name = name และ pagesize.=papersize
            # สร้างสไตล์ข้อความ
            styles = getSampleStyleSheet()
            style = ParagraphStyle(name='CustomStyle', parent=styles['Normal'], fontSize=40) 
            # สร้างเนื้อหา PDF
            content = []
            content.append(Paragraph(f"Queue : {last_id}", style))
            # สร้าง PDF และบันทึกไฟล์
            doc.build(content)
            i = messagebox.askyesno("ใบเสร็จ","ต้องการใบเสร็จหรือไม่??")
            if i:
                pdf2()
            else:
                messagebox.showinfo("ใบเสร็จ","ดำเนินการเสร็จสิ้น")
                # root.deiconify()
        def pdf2():
            # 1. ดึงข้อมูลจาก SQLite
            # ค้นหาค่าลำดับที่ล่าสุดจาก SQLite
            generate_bill = "SELECT * FROM bill WHERE bill_no = ?"  #เลือกข้อมูลล่าสุด
            cur.execute(generate_bill, (bill_no))
            data_from_sqlite = cur.fetchone()[0]#ดึงข้อมูลคอลัมแรกมา คือลำดับล่าสุดของsqlite

            custom_page_size = (6 * inch, 5 * inch)
            # 2. สร้าง PDF
            current_datetime = datetime.datetime.now()
            pdf_file_name = f'receipt_{current_datetime.strftime("%Y%m%d_%H%M%S")}.pdf'  
            doc = SimpleDocTemplate(pdf_file_name, pagesize=custom_page_size)
            styles = getSampleStyleSheet()
            custom_style = ParagraphStyle(name='CustomStyle', parent=styles['Normal'], fontSize=16)
            messagebox.showinfo("ใบเสร็จ","ดำเนินการเสร็จสิ้น")
            # 3. เขียนข้อมูลลงใน PDF
            content = []
            for row in data_from_sqlite:
                # สร้างข้อมูลจากข้อมูลใน SQLite
                data_to_write = f"bill<br /><br />Bill Number : {row[0]}<br /><br />Costumer Name : {row[2]}                Time: {row[1]}<br /><br />Phone Number: {row[3]}<br /><br />{row[4]}<br />"
                # เขียนข้อมูลลงใน PDF ด้วย Paragraph
                content.append(Paragraph(data_to_write, custom_style))
            # สร้าง PDF และบันทึกไฟล์
            doc.build(content)
'''
def wel_bill(self):
        self.name_message = Text(biller)
        self.name_message.place(relx=0.119, rely=0.452, width=176, height=30)
        self.name_message.configure(font="-family {Podkova} -size 10")
        self.name_message.configure(borderwidth=0)
        self.name_message.configure(background="#ffffff")

        self.num_message = Text(biller)
        self.num_message.place(relx=0.484, rely=0.452, width=90, height=30)
        self.num_message.configure(font="-family {Podkova} -size 10")
        self.num_message.configure(borderwidth=0)
        self.num_message.configure(background="#ffffff")

        self.bill_message = Text(biller)
        self.bill_message.place(relx=0.104, rely=0.477, width=176, height=26)
        self.bill_message.configure(font="-family {Podkova} -size 10")
        self.bill_message.configure(borderwidth=0) 
        self.bill_message.configure(background="#ffffff")

        self.bill_date_message = Text(biller)
        self.bill_date_message.place(relx=0.457, rely=0.477, width=90, height=26)
        self.bill_date_message.configure(font="-family {Podkova} -size 10")
        self.bill_date_message.configure(borderwidth=0)
        self.bill_date_message.configure(background="#ffffff")
    
def receive_payment(self):
    if self.cart.isEmpty():
        messagebox.showerror("ผิดพลาด!", "เพิ่มสินค้าก่อน", parent=biller)
    else:
        payment_str = simpledialog.askstring("รับเงิน", "ป้อนจำนวนเงินที่ลูกค้าจ่าย:")
        if payment_str is not None:
            try:
                payment = float(payment_str)
                total = self.cart.total()
                if payment >= total:
                    change = payment - total
                    messagebox.showinfo("รับเงินสำเร็จ", f"รับเงิน: Rs. {payment}\nเงินทอน: Rs. {change}")
                    self.cart.clear_cart()
                    self.update_cart_display()
                    self.update_total()
                else:
                    messagebox.showerror("ขาดแพง", f"จำนวนเงินไม่เพียงพอ ยอดรวมคือ: Rs. {total}")
            except ValueError:
                messagebox.showerror("ผิดพลาด!", "ป้อนจำนวนเงินไม่ถูกต้อง", parent=biller)