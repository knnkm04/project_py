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
from datetime import date
from tkinter import scrolledtext as tkst
from tkinter import filedialog


# ============================================

root = Tk()
root.geometry("1366x768")
root.attributes('-fullscreen',True)
root.title("DR>PHARMACy(ADMIN)")


user = StringVar()
passwd = StringVar()
fname = StringVar()
lname = StringVar()


with sqlite3.connect("D:\python\project_PY\Datdproject.db") as db:
    cur = db.cursor()
def random_emp_id(stringLength):
    Digits = string.digits
    strr=''.join(random.choice(Digits) for i in range(stringLength-3))
    return ('EMP'+strr)


def valid_phone(phn):
    if re.match(r"[0]\d{9}$", phn):
        return True
    return False
def valid_aadhar(aad):
    if aad.isdigit() and len(aad)==12:
        return True
    return False


class login_page:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.attributes('-fullscreen',True)
        top.title("Retail Manager(แอดมิน)")

        self.label1 = Label(root)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="D:\\python\\project_PY\\adminnn.png")
        self.label1.configure(image=self.img)
        

        self.entry1 = Entry(root)
        self.entry1.place(relx=0.373, rely=0.273, width=374, height=24)
        self.entry1.configure(highlightbackground="black",highlightthickness=1,highlightcolor="black")
        self.entry1.configure(font="-family {Poppins} -size 10")
        self.entry1.configure(relief="flat")
        self.entry1.configure(textvariable=user)

        self.entry2 = Entry(root)
        self.entry2.place(relx=0.373, rely=0.404, width=374, height=24)
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
        self.button1.configure(command=self.login)

        self.button2 = Button(root)
        self.button2.place(relx=0.055, rely=0.056, width=86, height=34)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#D2463E")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#D2463E")
        self.button2.configure(font="-family {Poppins SemiBold} -size 14")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""ย้อนกลับ""")
        self.button2.configure(command=self.back_to_future)

    def login(Event=None):
        global username
        username = user.get()
        password = passwd.get()
        
        # กำหนดรหัสผ่าน
        expected_username = "admin"
        expected_password = "290747"
        
        if username == expected_username and password == expected_password:
            messagebox.showinfo("หน้าล็อกอิน", "เข้าสู่ระบบสำเร็จ")
            page1.entry1.delete(0, END)
            page1.entry2.delete(0, END)
            root.withdraw()
            global adm
            global page2
            adm = Toplevel()
            adm.attributes('-fullscreen',True)
            page2 = Admin_Page(adm)
            page2.time()
            adm.protocol("WM_DELETE_WINDOW", exitt)
            adm.mainloop()
        else:
            messagebox.showerror("ผิดพลาด", "ชื่อและรหัสผ่านไม่ถูกต้อง")
            page1.entry2.delete(0, END)

    def back_to_future(Event=None):
        sure = messagebox.askyesno("back", "Are you sure you want to logout?",)
        if sure == True:
            os.environ['PYDEVD_DISABLE_FILE_VALIDATION'] = '1'
            root.withdraw()
            subprocess.Popen(["python", "D:\python\project_PY\minaAA.py"])
            root.deiconify()
            root.withdraw()

    
def exitt():
    sure = messagebox.askyesno(parent=root)
    if sure == True:
        adm.destroy()
        root.destroy()

def inventory():
    adm.withdraw()
    global inv
    global page3
    inv = Toplevel()
    inv.attributes('-fullscreen',True)
    page3 = Inventory(inv)
    page3.time()
    inv.protocol("WM_DELETE_WINDOW", exitt)
    inv.mainloop()


def employee():
    adm.withdraw()
    global emp
    global page5
    emp = Toplevel()
    page5 = Employee(emp)
    page5.time()
    emp.protocol("WM_DELETE_WINDOW", exitt)
    emp.mainloop()


def invoices():
    adm.withdraw()
    global invoice
    invoice = Toplevel()
    page7 = Invoice(invoice)
    page7.time()
    invoice.protocol("WM_DELETE_WINDOW", exitt)
    invoice.mainloop()

def about():
    pass

class Admin_Page:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.attributes('-fullscreen',True)
        top.title("หน้าต่างแอดมิน")

        self.label1 = Label(adm)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="D:\\python\\project_PY\\adminmain.png")
        self.label1.configure(image=self.img)

        self.message = Label(adm)
        self.message.place(relx=0.046, rely=0.057, width=62, height=30)
        self.message.configure(font="-family {Poppins} -size 12")
        self.message.configure(foreground="#000000")
        self.message.configure(background="#ffffff")
        self.message.configure(text="""admin""")
        self.message.configure(anchor="w")

        self.button1 = Button(adm)
        self.button1.place(relx=0.035, rely=0.116, width=80, height=15)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#248DA8")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#248DA8")
        self.button1.configure(font="-family {Poppins SemiBold} -size 10")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""ออกจากระบบ""")
        self.button1.configure(command=self.Logout)

        self.button2 = Button(adm)
        self.button2.place(relx=0.145, rely=0.658, width=180, height=63)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#248DA8")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#248DA8")
        self.button2.configure(font="-family {Poppins SemiBold} -size 32")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""คลังสินค้า""")
        self.button2.configure(command=inventory)

        self.button3 = Button(adm)
        self.button3.place(relx=0.427, rely=0.658, width=180, height=63)
        self.button3.configure(relief="flat")
        self.button3.configure(overrelief="flat")
        self.button3.configure(activebackground="#248DA8")
        self.button3.configure(cursor="hand2")
        self.button3.configure(foreground="#ffffff")
        self.button3.configure(background="#248DA8")
        self.button3.configure(font="-family {Poppins SemiBold} -size 32")
        self.button3.configure(borderwidth="0")
        self.button3.configure(text="""พนักงาน""")
        self.button3.configure(command=employee)

        self.button4 = Button(adm)
        self.button4.place(relx=0.725, rely=0.658, width=180, height=63)
        self.button4.configure(relief="flat")
        self.button4.configure(overrelief="flat")
        self.button4.configure(activebackground="#248DA8")
        self.button4.configure(cursor="hand2")
        self.button4.configure(foreground="#ffffff")
        self.button4.configure(background="#248DA8")
        self.button4.configure(font="-family {Poppins SemiBold} -size 32")
        self.button4.configure(borderwidth="0")
        self.button4.configure(text="""ใบเสร็จ""")
        self.button4.configure(command=invoices)



        self.clock = Label(adm)
        self.clock.place(relx=0.9, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)

    def Logout(self):
        sure = messagebox.askyesno("Logout", "Are you sure you want to logout?", parent=adm)
        if sure == True:
            os.environ['PYDEVD_DISABLE_FILE_VALIDATION'] = '1'
            adm.withdraw()
            subprocess.Popen(["python", "D:\python\project_PY\minaAA.py"])
            adm.deiconify()
            adm.withdraw()





class Inventory:
    def __init__(self, top=None):
        top.geometry("1366x768")
        root.attributes('-fullscreen',True)
        top.title("คลังสินค้า")

        self.label1 = Label(inv)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="D:\python\project_PY\inventory.png")
        self.label1.configure(image=self.img)

        self.message = Label(inv)
        self.message.place(relx=0.041, rely=0.055, width=70, height=25)
        self.message.configure(font="-family {Poppins} -size 10")
        self.message.configure(foreground="#000000")
        self.message.configure(background="#ffffff")
        self.message.configure(text="""admin""")
        self.message.configure(anchor="w")

        self.clock = Label(inv)
        self.clock.place(relx=0.9, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        self.entry1 = Entry(inv)
        self.entry1.place(relx=0.040, rely=0.286, width=240, height=28)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")

        self.button1 = Button(inv)
        self.button1.place(relx=0.231, rely=0.289, width=50, height=23)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#8EC6E6")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#000000")
        self.button1.configure(background="#8EC6E6")
        self.button1.configure(font="-family {Poppins SemiBold} -size 10")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""ค้นหา""")
        self.button1.configure(command=self.search_product)

        self.button2 = Button(inv)
        self.button2.place(relx=0.035, rely=0.106, width=80, height=23)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#8EC6E6")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#000000")
        self.button2.configure(background="#8EC6E6")
        self.button2.configure(font="-family {Poppins SemiBold} -size 12")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""ออกจากระบบ""")
        self.button2.configure(command=self.Logout)

        self.button3 = Button(inv)
        self.button3.place(relx=0.052, rely=0.432, width=306, height=28)
        self.button3.configure(relief="flat")
        self.button3.configure(overrelief="flat")
        self.button3.configure(activebackground="#8EC6E6")
        self.button3.configure(cursor="hand2")
        self.button3.configure(foreground="#000000")
        self.button3.configure(background="#8EC6E6")
        self.button3.configure(font="-family {Poppins SemiBold} -size 12")
        self.button3.configure(borderwidth="0")
        self.button3.configure(text="""เพิ่มผลิตภัณฑ์""")
        self.button3.configure(command=self.add_product)

        self.button4 = Button(inv)
        self.button4.place(relx=0.052, rely=0.5, width=306, height=28)
        self.button4.configure(relief="flat")
        self.button4.configure(overrelief="flat")
        self.button4.configure(activebackground="#8EC6E6")
        self.button4.configure(cursor="hand2")
        self.button4.configure(foreground="#000000")
        self.button4.configure(background="#8EC6E6")
        self.button4.configure(font="-family {Poppins SemiBold} -size 12")
        self.button4.configure(borderwidth="0")
        self.button4.configure(text="""อัปเดตผลิตภัณฑ์""")
        self.button4.configure(command=self.update_product)

        self.button5 = Button(inv)
        self.button5.place(relx=0.052, rely=0.57, width=306, height=28)
        self.button5.configure(relief="flat")
        self.button5.configure(overrelief="flat")
        self.button5.configure(activebackground="#8EC6E6")
        self.button5.configure(cursor="hand2")
        self.button5.configure(foreground="#000000")
        self.button5.configure(background="#8EC6E6")
        self.button5.configure(font="-family {Poppins SemiBold} -size 12")
        self.button5.configure(borderwidth="0")
        self.button5.configure(text="""ลบผลิตภัณฑ์""")
        self.button5.configure(command=self.delete_product)

        self.button6 = Button(inv)
        self.button6.place(relx=0.135, rely=0.885, width=76, height=23)
        self.button6.configure(relief="flat")
        self.button6.configure(overrelief="flat")
        self.button6.configure(activebackground="#8EC6E6")
        self.button6.configure(cursor="hand2")
        self.button6.configure(foreground="#000000")
        self.button6.configure(background="#8EC6E6")
        self.button6.configure(font="-family {Poppins SemiBold} -size 12")
        self.button6.configure(borderwidth="0")
        self.button6.configure(text="""ย้อนกลับ""")
        self.button6.configure(command=self.Exit)



        self.scrollbarx = Scrollbar(inv, orient=HORIZONTAL)
        self.scrollbary = Scrollbar(inv, orient=VERTICAL)

        self.tree = ttk.Treeview(inv)
        self.tree.place(relx=0.307, rely=0.203, width=880, height=550)
        self.tree.configure(
            yscrollcommand=self.scrollbary.set, xscrollcommand=self.scrollbarx.set
        )
        self.tree.configure(selectmode="extended")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.scrollbary.configure(command=self.tree.yview)
        self.scrollbarx.configure(command=self.tree.xview)

        self.scrollbary.place(relx=0.954, rely=0.203, width=22, height=548)
        self.scrollbarx.place(relx=0.307, rely=0.924, width=884, height=22)

        self.tree.configure(
            columns=(
                "Product ID",
                "Name",
                "Category",
                "Sub-Category",
                "In Stock",
                "MRP",
                "Cost Price",
                
            )
        )

        self.tree.heading("Product ID", text="Id ผลิตภัณฑ์", anchor=W)
        self.tree.heading("Name", text="ชื่อ", anchor=W)
        self.tree.heading("Category", text="ประเภทยา", anchor=W)
        self.tree.heading("Sub-Category", text="ชนิดยา", anchor=W)
        self.tree.heading("In Stock", text="คงเหลือ", anchor=W)
        self.tree.heading("MRP", text="ราคา", anchor=W)
        self.tree.heading("Cost Price", text="ต้นทุน", anchor=W)
        #self.tree.heading("Vendor No.", text="Vendor No.", anchor=W)

        self.tree.column("#0", stretch=NO, minwidth=0, width=0)
        self.tree.column("#1", stretch=NO, minwidth=0, width=80)
        self.tree.column("#2", stretch=NO, minwidth=0, width=260)
        self.tree.column("#3", stretch=NO, minwidth=0, width=100)
        self.tree.column("#4", stretch=NO, minwidth=0, width=120)
        self.tree.column("#5", stretch=NO, minwidth=0, width=80)
        self.tree.column("#6", stretch=NO, minwidth=0, width=80)
        self.tree.column("#7", stretch=NO, minwidth=0, width=80)
        #self.tree.column("#8", stretch=NO, minwidth=0, width=100)

        self.DisplayData()

    def DisplayData(self):
        cur.execute("SELECT * FROM products")
        fetch = cur.fetchall()
        for data in fetch:
            self.tree.insert("", "end", values=(data))

    def search_product(self):
        val = []
        for i in self.tree.get_children():
            val.append(i)
            for j in self.tree.item(i)["values"]:
                val.append(j)

        try:
            to_search = int(self.entry1.get())
        except ValueError:
            messagebox.showerror("Oops!!", "Invalid Product Id.", parent=inv)
        else:
            for search in val:
                if search==to_search:
                    self.tree.selection_set(val[val.index(search)-1])
                    self.tree.focus(val[val.index(search)-1])
                    messagebox.showinfo("Success!!", "Product ID: {} found.".format(self.entry1.get()), parent=inv)
                    break
            else: 
                messagebox.showerror("Oops!!", "Product ID: {} not found.".format(self.entry1.get()), parent=inv)
    
    sel = []
    def on_tree_select(self, Event):
        self.sel.clear()
        for i in self.tree.selection():
            if i not in self.sel:
                self.sel.append(i)

    def delete_product(self):
        val = []
        to_delete = []

        if len(self.sel)!=0:
            sure = messagebox.askyesno("Confirm", "Are you sure you want to delete selected products?", parent=inv)
            if sure == True:
                for i in self.sel:
                    for j in self.tree.item(i)["values"]:
                        val.append(j)
                
                for j in range(len(val)):
                    if j%8==0:
                        to_delete.append(val[j])
                
                for k in to_delete:
                    delete = "DELETE FROM products WHERE product_id = ?"
                    cur.execute(delete, [k])
                    db.commit()

                messagebox.showinfo("Success!!", "Products deleted from database.", parent=inv)
                self.sel.clear()
                self.tree.delete(*self.tree.get_children())

                self.DisplayData()
        else:
            messagebox.showerror("Error!!","Please select a product.", parent=inv)

    def update_product(self):
        if len(self.sel)==1:
            global p_update
            p_update = Toplevel()
            page9 = Update_Product(p_update)
            page9.time()
            #p_update.protocol("WM_DELETE_WINDOW", self.ex2)
            global valll
            valll = []
            for i in self.sel:
                for j in self.tree.item(i)["values"]:
                    valll.append(j)
        
                    
# นำค่าจาก valll ไปใส่ใน Entry ของหน้า Update_Product
            page9.entry1.insert(0, valll[1])
            page9.entry2.insert(0, valll[2])
            page9.entry3.insert(0, valll[4])
            page9.entry4.insert(0, valll[5])
            page9.entry6.insert(0, valll[3])
            page9.entry7.insert(0, valll[6])
#            page9.entry8.insert(0, valll[7])


        elif len(self.sel)==0:
                messagebox.showerror("Error","Please choose a product to update.", parent=inv)
        else:
            messagebox.showerror("Error","Can only update one product at a time.", parent=inv)

        p_update.mainloop()

    

    def add_product(self):
        global p_add
        global page4
        p_add = Toplevel()
        page4 = add_product(p_add)
        page4.time()
        p_add.mainloop()

    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)


    def Exit(self):
        inv.destroy()
        adm.deiconify()

    #def ex2(self):
    #    sure = messagebox.askyesno("Exit","Are you sure you want to exit?", parent=p_update)
    #    if sure == True:
    #        p_update.destroy()
    #        inv.deiconify()


    def Logout(self):
        sure = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if sure == True:
            root.deiconify()
            page1.entry1.delete(0, END)
            page1.entry2.delete(0, END)


class add_product:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.attributes('-fullscreen',True)
        top.title("Add Product")

        self.label1 = Label(p_add)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="D:\\python\\project_PY\\add_product_new.png")
        self.label1.configure(image=self.img)

        self.clock = Label(p_add)
        self.clock.place(relx=0.81, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        self.entry1 = Entry(p_add)
        self.entry1.place(relx=0.132, rely=0.296, width=996, height=30)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")


        self.entry2 = Entry(p_add)
        self.entry2.place(relx=0.132, rely=0.413, width=374, height=30)
        self.entry2.configure(font="-family {Poppins} -size 12")
        self.entry2.configure(relief="flat")

        self.r2 = p_add.register(self.testint)

        self.entry3 = Entry(p_add)
        self.entry3.place(relx=0.132, rely=0.529, width=374, height=30)
        self.entry3.configure(font="-family {Poppins} -size 12")
        self.entry3.configure(relief="flat")
        self.entry3.configure(validate="key", validatecommand=(self.r2, "%P"))

        self.entry4 = Entry(p_add)
        self.entry4.place(relx=0.132, rely=0.646, width=374, height=30)
        self.entry4.configure(font="-family {Poppins} -size 12")
        self.entry4.configure(relief="flat")
       

        self.entry6 = Entry(p_add)
        self.entry6.place(relx=0.527, rely=0.413, width=374, height=30)
        self.entry6.configure(font="-family {Poppins} -size 12")
        self.entry6.configure(relief="flat")
       

        self.entry7 = Entry(p_add)
        self.entry7.place(relx=0.527, rely=0.529, width=374, height=30)
        self.entry7.configure(font="-family {Poppins} -size 12")
        self.entry7.configure(relief="flat")
       

        #self.entry8 = Entry(p_add)
        #self.entry8.place(relx=0.527, rely=0.646, width=374, height=30)
        #self.entry8.configure(font="-family {Poppins} -size 12")
        #self.entry8.configure(relief="flat")
        #self.entry8.configure(validate="key", validatecommand=(self.r2, "%P"))
       

        self.button1 = Button(p_add)
        self.button1.place(relx=0.400, rely=0.836, width=96, height=34)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#8EC6E6")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#000000")
        self.button1.configure(background="#8EC6E6")
        self.button1.configure(font="-family {Poppins SemiBold} -size 14")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""เพิ่ม""")
        self.button1.configure(command=self.add)

        self.button2 = Button(p_add)
        self.button2.place(relx=0.53, rely=0.836, width=96, height=34)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#8EC6E6")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#000000")
        self.button2.configure(background="#8EC6E6")
        self.button2.configure(font="-family {Poppins SemiBold} -size 14")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""เคลียร์""")
        self.button2.configure(command=self.clearr)

        self.button3 = Button(p_add)
        self.button3.place(relx=0.815, rely=0.836, width=86, height=34)
        self.button3.configure(relief="flat")
        self.button3.configure(overrelief="flat")
        self.button3.configure(activebackground="#8EC6E6")
        self.button3.configure(cursor="hand2")
        self.button3.configure(foreground="#000000")
        self.button3.configure(background="#8EC6E6")
        self.button3.configure(font="-family {Poppins SemiBold} -size 14")
        self.button3.configure(borderwidth="0")
        self.button3.configure(text="""ย้อนกลับ""")
        self.button3.configure(command=self.back)

    def add(self):
        pqty = self.entry3.get()
        pcat = self.entry2.get()  
        pmrp = self.entry4.get()  
        pname = self.entry1.get()  
        psubcat = self.entry6.get()  
        pcp = self.entry7.get()  
        #pvendor = self.entry8.get()  
       

        if pname.strip():
            if pcat.strip():
                if psubcat.strip():
                    if pqty:
                        if pcp:
                            try:
                                float(pcp)
                            except ValueError:
                                messagebox.showerror("Oops!", "Invalid cost price.", parent=p_add)
                            else:
                                if pmrp:
                                    try:
                                        float(pmrp)
                                    except ValueError:
                                        messagebox.showerror("Oops!", "Invalid MRP.", parent=p_add)
                                    else:
                                        #if valid_phone(pvendor):
                                            file_pic = filedialog.askopenfilename()
                                            if file_pic:
                                                with open(file_pic, 'rb') as file:
                                                    picture = file.read()
                                            with sqlite3.connect("D:\python\project_PY\Datdproject.db") as db:
                                                cur = db.cursor()
                                            insert = (
                                                        "INSERT INTO products(product_name, product_cat, product_subcat, stock, mrp, cost_price,picture) VALUES(?,?,?,?,?,?,?)"
                                                    )
                                            cur.execute(insert, [pname, pcat, psubcat, int(pqty), float(pmrp), float(pcp),picture])
                                            db.commit()
                                            messagebox.showinfo("Success!!", "Product successfully added in inventory.", parent=p_add)
                                            p_add.destroy()
                                            page3.tree.delete(*page3.tree.get_children())
                                            page3.DisplayData()
                                            p_add.destroy()
                                        #else:
                                            #messagebox.showerror("Oops!", "Invalid phone number.", parent=p_add)
                                else:
                                    messagebox.showerror("Oops!", "Please enter MRP.", parent=p_add)
                        else:
                            messagebox.showerror("Oops!", "Please enter product cost price.", parent=p_add)
                    else:
                        messagebox.showerror("Oops!", "Please enter product quantity.", parent=p_add)
                else:
                    messagebox.showerror("Oops!", "Please enter product sub-category.", parent=p_add)
            else:
                messagebox.showerror("Oops!", "Please enter product category.", parent=p_add)
        else:
            messagebox.showerror("Oops!", "Please enter product name", parent=p_add)


    def clearr(self):
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)
        self.entry4.delete(0, END)
        self.entry6.delete(0, END)
        self.entry7.delete(0, END)
        self.entry8.delete(0, END)

    def back(self):
        p_add.destroy()

    def testint(self, val):
        if val.isdigit():
            return True
        elif val == "":
            return True
        return False

    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)


class Update_Product:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.attributes('-fullscreen',True)
        top.title("Add Product")

        self.label1 = Label(p_update)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="D:\\python\\project_PY\\update_product_new.png")
        self.label1.configure(image=self.img)

        #self.label2 = Label(p_update,text='name')
        #self.label2.place(x=170,y=200)
        #self.label3 = Label(p_update,text='category')
        #self.label3.place(x=170,y=300)
        #self.label4 = Label(p_update,text='stock')
        #self.label4.place(x=170,y=380)
        #self.label5 = Label(p_update,text='mrp')
        #self.label5.place(x=170,y=470)
        #self.label6 = Label(p_update,text='type')
        #self.label6.place(x=720,y=300)
        #self.label7 = Label(p_update,text='cost')
        #self.label7.place(x=720,y=380)
        #self.label8 = Label(p_update,text='code')
        #self.label8.place(x=720,y=470)

        self.clock = Label(p_update)
        self.clock.place(relx=0.81, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        self.entry1 = Entry(p_update)
        self.entry1.place(relx=0.135, rely=0.296, width=996, height=30)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")

        self.entry2 = Entry(p_update)
        self.entry2.place(relx=0.132, rely=0.413, width=374, height=30)
        self.entry2.configure(font="-family {Poppins} -size 12")
        self.entry2.configure(relief="flat")

        self.r2 = p_update.register(self.testint)

        self.entry3 = Entry(p_update)
        self.entry3.place(relx=0.132, rely=0.529, width=374, height=30)
        self.entry3.configure(font="-family {Poppins} -size 12")
        self.entry3.configure(relief="flat")
        self.entry3.configure(validate="key", validatecommand=(self.r2, "%P"))

        self.entry4 = Entry(p_update)
        self.entry4.place(relx=0.132, rely=0.646, width=374, height=30)
        self.entry4.configure(font="-family {Poppins} -size 12")
        self.entry4.configure(relief="flat")
       

        self.entry6 = Entry(p_update)
        self.entry6.place(relx=0.527, rely=0.413, width=374, height=30)
        self.entry6.configure(font="-family {Poppins} -size 12")
        self.entry6.configure(relief="flat")
       

        self.entry7 = Entry(p_update)
        self.entry7.place(relx=0.527, rely=0.529, width=374, height=30)
        self.entry7.configure(font="-family {Poppins} -size 12")
        self.entry7.configure(relief="flat")
       

        #self.entry8 = Entry(p_update)
        #self.entry8.place(relx=0.527, rely=0.646, width=374, height=30)
        #self.entry8.configure(font="-family {Poppins} -size 12")
        #self.entry8.configure(relief="flat")
       

        self.button1 = Button(p_update)
        self.button1.place(relx=0.400, rely=0.836, width=96, height=34)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#CF1E14")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#CF1E14")
        self.button1.configure(font="-family {Poppins SemiBold} -size 14")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""ยืนยัน""")
        self.button1.configure(command=self.update)

        self.button2 = Button(p_update)
        self.button2.place(relx=0.53, rely=0.836, width=96, height=34)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#CF1E14")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#CF1E14")
        self.button2.configure(font="-family {Poppins SemiBold} -size 14")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""เคลียร์""")
        self.button2.configure(command=self.clearr)

        self.button3 = Button(p_update)
        self.button3.place(relx=0.815, rely=0.836, width=86, height=34)
        self.button3.configure(relief="flat")
        self.button3.configure(overrelief="flat")
        self.button3.configure(activebackground="#CF1E14")
        self.button3.configure(cursor="hand2")
        self.button3.configure(foreground="#ffffff")
        self.button3.configure(background="#CF1E14")
        self.button3.configure(font="-family {Poppins SemiBold} -size 14")
        self.button3.configure(borderwidth="0")
        self.button3.configure(text="""ย้อนกลับ""")
        self.button3.configure(command=self.back)
        
    def update(self):
        pqty = self.entry3.get()
        pcat = self.entry2.get()  
        pmrp = self.entry4.get()  
        pname = self.entry1.get()  
        psubcat = self.entry6.get()  
        pcp = self.entry7.get()  
        #pvendor = self.entry8.get()  
       

        if pname.strip():
            if pcat.strip():
                if psubcat.strip():
                    if pqty:
                        if pcp:
                            try:
                                float(pcp)
                            except ValueError:
                                messagebox.showerror("Oops!", "Invalid cost price.", parent=p_update)
                            else:
                                if pmrp:
                                    try:
                                        float(pmrp)
                                    except ValueError:
                                        messagebox.showerror("Oops!", "Invalid MRP.", parent=p_update)
                                    else:
                                        #if valid_phone(pvendor):
                                            product_id = valll[0]
                                            with sqlite3.connect("D:\python\project_PY\Datdproject.db") as db:
                                                cur = db.cursor()
                                            update = (
                                            "UPDATE products SET product_name = ?, product_cat = ?, product_subcat = ?, stock = ?, mrp = ?, cost_price = ?  WHERE product_id = ?"
                                            )
                                            cur.execute(update, [pname, pcat, psubcat, int(pqty), float(pmrp), float(pcp), product_id])
                                            db.commit()
                                            messagebox.showinfo("Success!!", "Product successfully updated in inventory.", parent=p_update)
                                            valll.clear()
                                            Inventory.sel.clear()
                                            page3.tree.delete(*page3.tree.get_children())
                                            page3.DisplayData()
                                            p_update.destroy()
                                        #else:
                                        #    messagebox.showerror("Oops!", "Invalid phone number.", parent=p_update)
                                else:
                                    messagebox.showerror("Oops!", "Please enter MRP.", parent=p_update)
                        else:
                            messagebox.showerror("Oops!", "Please enter product cost price.", parent=p_update)
                    else:
                        messagebox.showerror("Oops!", "Please enter product quantity.", parent=p_update)
                else:
                    messagebox.showerror("Oops!", "Please enter product sub-category.", parent=p_update)
            else:
                messagebox.showerror("Oops!", "Please enter product category.", parent=p_update)
        else:
            messagebox.showerror("Oops!", "Please enter product name", parent=p_update)
    
    def clearr(self):
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)
        self.entry4.delete(0, END)
        self.entry6.delete(0, END)
        self.entry7.delete(0, END)
        self.entry8.delete(0, END)

    def testint(self, val):
        if val.isdigit():
            return True
        elif val == "":
            return True
        return False
    
    def back(self):
        p_update.destroy()

    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)
    


class Employee:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.attributes('-fullscreen',True)
        top.title("Employee Management")

        self.label1 = Label(emp)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="D:\\python\\project_PY\\employer.png")
        self.label1.configure(image=self.img)

        self.message = Label(emp)
        self.message.place(relx=0.046, rely=0.057, width=62, height=30)
        self.message.configure(font="-family {Poppins} -size 12")
        self.message.configure(foreground="#000000")
        self.message.configure(background="#ffffff")
        self.message.configure(text="""admin""")
        self.message.configure(anchor="w")
        
        self.clock = Label(emp)
        self.clock.place(relx=0.9, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        self.entry1 = Entry(emp)
        self.entry1.place(relx=0.040, rely=0.286, width=240, height=28)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")

        self.button1 = Button(emp)
        self.button1.place(relx=0.229, rely=0.289, width=76, height=23)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#76AEC3")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#76AEC3")
        self.button1.configure(font="-family {Poppins SemiBold} -size 10")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""Search""")
        self.button1.configure(command=self.search_emp)

        self.button2 = Button(emp)
        self.button2.place(relx=0.035, rely=0.116, width=80, height=15)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#76AEC3")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#76AEC3")
        self.button2.configure(font="-family {Poppins SemiBold} -size 12")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""ออกจากระบบ""")
        self.button2.configure(command=self.Logout)

        self.button3 = Button(emp)
        self.button3.place(relx=0.052, rely=0.432, width=306, height=28)
        self.button3.configure(relief="flat")
        self.button3.configure(overrelief="flat")
        self.button3.configure(activebackground="#76AEC3")
        self.button3.configure(cursor="hand2")
        self.button3.configure(foreground="#ffffff")
        self.button3.configure(background="#76AEC3")
        self.button3.configure(font="-family {Poppins SemiBold} -size 12")
        self.button3.configure(borderwidth="0")
        self.button3.configure(text="""เพิ่มพนักงาน""")
        self.button3.configure(command=self.add_emp)



        self.button5 = Button(emp)
        self.button5.place(relx=0.052, rely=0.57, width=306, height=28)
        self.button5.configure(relief="flat")
        self.button5.configure(overrelief="flat")
        self.button5.configure(activebackground="#76AEC3")
        self.button5.configure(cursor="hand2")
        self.button5.configure(foreground="#ffffff")
        self.button5.configure(background="#76AEC3")
        self.button5.configure(font="-family {Poppins SemiBold} -size 12")
        self.button5.configure(borderwidth="0")
        self.button5.configure(text="""ลบพนักงาน""")
        self.button5.configure(command=self.delete_emp)

        self.button6 = Button(emp)
        self.button6.place(relx=0.135, rely=0.885, width=76, height=23)
        self.button6.configure(relief="flat")
        self.button6.configure(overrelief="flat")
        self.button6.configure(activebackground="#76AEC3")
        self.button6.configure(cursor="hand2")
        self.button6.configure(foreground="#ffffff")
        self.button6.configure(background="#76AEC3")
        self.button6.configure(font="-family {Poppins SemiBold} -size 12")
        self.button6.configure(borderwidth="0")
        self.button6.configure(text="""ออก""")
        self.button6.configure(command=self.Exit)

        self.scrollbarx = Scrollbar(emp, orient=HORIZONTAL)
        self.scrollbary = Scrollbar(emp, orient=VERTICAL)
        self.tree = ttk.Treeview(emp)
        self.tree.place(relx=0.307, rely=0.203, width=880, height=550)
        self.tree.configure(
            yscrollcommand=self.scrollbary.set, xscrollcommand=self.scrollbarx.set
        )
        self.tree.configure(selectmode="extended")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.scrollbary.configure(command=self.tree.yview)
        self.scrollbarx.configure(command=self.tree.xview)

        self.scrollbary.place(relx=0.954, rely=0.203, width=22, height=548)
        self.scrollbarx.place(relx=0.307, rely=0.924, width=884, height=22)

        self.tree.configure(
            columns=(
                "Employee ID",
                "Employee Name",
                "Contact No.",
                "Address",
                "Password",
                "Designation"
            )
        )

        self.tree.heading("Employee ID", text="Employee ID", anchor=W)
        self.tree.heading("Employee Name", text="Employee Name", anchor=W)
        self.tree.heading("Contact No.", text="Contact No.", anchor=W)
        self.tree.heading("Address", text="Address", anchor=W)
        #self.tree.heading("Aadhar No.", text="Aadhar No.", anchor=W)
        self.tree.heading("Password", text="Password", anchor=W)
        self.tree.heading("Designation", text="Designation", anchor=W)

        self.tree.column("#0", stretch=NO, minwidth=0, width=0)
        self.tree.column("#1", stretch=NO, minwidth=0, width=80)
        self.tree.column("#2", stretch=NO, minwidth=0, width=260)
        self.tree.column("#3", stretch=NO, minwidth=0, width=100)
        self.tree.column("#4", stretch=NO, minwidth=0, width=198)
        self.tree.column("#5", stretch=NO, minwidth=0, width=80)
        #self.tree.column("#6", stretch=NO, minwidth=0, width=80)
        #self.tree.column("#7", stretch=NO, minwidth=0, width=80)

        self.DisplayData()

    def DisplayData(self):
        cur.execute("SELECT emp_id, name, contact_num, address, password, designation FROM employee ")
        fetch = cur.fetchall()
        for data in fetch: 
            self.tree.insert("", "end", values=(data))

    def search_emp(self):
        val = []
        for i in self.tree.get_children():
            val.append(i)
            for j in self.tree.item(i)["values"]:
                val.append(j)

        to_search = self.entry1.get()
        for search in val:
            if search==to_search:
                self.tree.selection_set(val[val.index(search)-1])
                self.tree.focus(val[val.index(search)-1])
                messagebox.showinfo("Success!!", "Employee ID: {} found.".format(self.entry1.get()), parent=emp)
                break
        else: 
            messagebox.showerror("Oops!!", "Employee ID: {} not found.".format(self.entry1.get()), parent=emp)
    
    sel = []
    def on_tree_select(self, Event):
        self.sel.clear()
        for i in self.tree.selection():
            if i not in self.sel:
                self.sel.append(i)

    def delete_emp(self):
        val = []
        to_delete = []

        if len(self.sel)!=0:
            sure = messagebox.askyesno("Confirm", "Are you sure you want to delete selected employee(s)?", parent=emp)
            if sure == True:
                for i in self.sel:
                    for j in self.tree.item(i)["values"]:
                        val.append(j)
                
                for j in range(len(val)):
                    if j%7==0:
                        to_delete.append(val[j])
                
                flag = 1

                for k in to_delete:
                    if k=="EMP0000":
                        flag = 0
                        break
                    else:
                        delete = "DELETE FROM employee WHERE emp_id = ?"
                        cur.execute(delete, [k])
                        db.commit()

                if flag==1:
                    messagebox.showinfo("Success!!", "Employee(s) deleted from database.", parent=emp)
                    self.sel.clear()
                    self.tree.delete(*self.tree.get_children())
                    self.DisplayData()
                else:
                    messagebox.showerror("Error!!","Cannot delete master admin.")
        else:
            messagebox.showerror("Error!!","Please select an employee.", parent=emp)

    

        

    def add_emp(self):
        global e_add
        e_add = Toplevel()
        page6 = add_employee(e_add)
        page6.time()
        e_add.protocol("WM_DELETE_WINDOW", self.ex)
        e_add.mainloop()


    def ex(self):
        e_add.destroy()
        self.tree.delete(*self.tree.get_children())
        self.DisplayData()   
    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)

    def Exit(self):
        emp.destroy()
        adm.deiconify()


    def Logout(self):
        sure = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if sure == True:
            emp.destroy()
            root.deiconify()
            
            page1.entry1.delete(0, END)
            page1.entry2.delete(0, END)


class add_employee:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.attributes('-fullscreen',True)
        top.title("Add Employee")

        self.label1 = Label(e_add)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="D:\\python\\project_PY\\add_employer.png")
        self.label1.configure(image=self.img)

        self.clock = Label(e_add)
        self.clock.place(relx=0.81, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        self.r1 = e_add.register(self.testint)
        self.r2 = e_add.register(self.testchar)

        self.entry1 = Entry(e_add)
        self.entry1.place(relx=0.132, rely=0.296, width=374, height=30)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")
        

        self.entry2 = Entry(e_add)
        self.entry2.place(relx=0.132, rely=0.413, width=374, height=30)
        self.entry2.configure(font="-family {Poppins} -size 12")
        self.entry2.configure(relief="flat")
        self.entry2.configure(validate="key", validatecommand=(self.r1, "%P"))

        #self.entry3 = Entry(e_add)
        #self.entry3.place(relx=0.132, rely=0.529, width=374, height=30)
        #self.entry3.configure(font="-family {Poppins} -size 12")
        #self.entry3.configure(relief="flat")
        #self.entry3.configure(validate="key", validatecommand=(self.r1, "%P"))

        self.entry4 = Entry(e_add)
        self.entry4.place(relx=0.527, rely=0.296, width=374, height=30)
        self.entry4.configure(font="-family {Poppins} -size 12")
        self.entry4.configure(relief="flat")
        self.entry4.configure(validate="key", validatecommand=(self.r2, "%P"))

        self.entry5 = Entry(e_add)
        self.entry5.place(relx=0.527, rely=0.413, width=374, height=30)
        self.entry5.configure(font="-family {Poppins} -size 12")
        self.entry5.configure(relief="flat")

        self.entry6 = Entry(e_add)
        self.entry6.place(relx=0.132, rely=0.529, width=374, height=30)
        self.entry6.configure(font="-family {Poppins} -size 12")
        self.entry6.configure(relief="flat")
        self.entry6.configure(show="*")

        self.button1 = Button(e_add)
        self.button1.place(relx=0.408, rely=0.836, width=96, height=34)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#76AEC3")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#76AEC3")
        self.button1.configure(font="-family {Poppins SemiBold} -size 14")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""ADD""")
        self.button1.configure(command=self.add)

        self.button2 = Button(e_add)
        self.button2.place(relx=0.526, rely=0.836, width=86, height=34)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#76AEC3")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#76AEC3")
        self.button2.configure(font="-family {Poppins SemiBold} -size 14")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""CLEAR""")
        self.button2.configure(command=self.clearr)

        self.button3 = Button(e_add)
        self.button3.place(relx=0.826, rely=0.836, width=86, height=34)
        self.button3.configure(relief="flat")
        self.button3.configure(overrelief="flat")
        self.button3.configure(activebackground="#76AEC3")
        self.button3.configure(cursor="hand2")
        self.button3.configure(foreground="#ffffff")
        self.button3.configure(background="#76AEC3")
                               
        self.button3.configure(font="-family {Poppins SemiBold} -size 14")
        self.button3.configure(borderwidth="0")
        self.button3.configure(text="""ย้อนกลับ""")
        self.button3.configure(command=self.back)



    def testint(self, val):
        if val.isdigit():
            return True
        elif val == "":
            return True
        return False

    def testchar(self, val):
        if val.isalpha():
            return True
        elif val == "":
            return True
        return False
    
    def back(self):
        e_add.destroy()

    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)

    
    def add(self):
        ename = self.entry1.get()
        econtact = self.entry2.get()
        #eaddhar = self.entry3.get()
        edes = self.entry4.get()
        eadd = self.entry5.get()
        epass = self.entry6.get()

        if ename.strip():
            if valid_phone(econtact):
                #if valid_aadhar(eaddhar):
                    if edes:
                        if eadd:
                            if epass:
                                emp_id = random_emp_id(7)
                                insert = (
                                            "INSERT INTO employee(emp_id, name, contact_num, address, password, designation) VALUES(?,?,?,?,?,?)"
                                        )
                                cur.execute(insert, [emp_id, ename, econtact, eadd, epass, edes])
                                db.commit()
                                messagebox.showinfo("Success!!", "Employee ID: {} successfully added in database.".format(emp_id), parent=e_add)
                                e_add.destroy()
                                page5.tree.delete(*page5.tree.get_children())
                                page5.DisplayData()
                                e_add.destroy()
                                
                            else:
                                messagebox.showerror("Oops!", "Please enter a password.", parent=e_add)
                        else:
                            messagebox.showerror("Oops!", "Please enter address.", parent=e_add)
                    else:
                        messagebox.showerror("Oops!", "Please enter designation.", parent=e_add)
                #else:
                #    messagebox.showerror("Oops!", "Invalid Aadhar number.", parent=e_add)
            else:
                messagebox.showerror("Oops!", "Invalid phone number.", parent=e_add)
        else:
            messagebox.showerror("Oops!", "Please enter employee name.", parent=e_add)

    def clearr(self):
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        #self.entry3.delete(0, END)
        self.entry4.delete(0, END)
        self.entry5.delete(0, END)
        self.entry6.delete(0, END)

class Invoice:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.attributes('-fullscreen',True)
        top.title("Invoices")

        self.label1 = Label(invoice)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="D:\python\project_PY\invoices.png")
        self.label1.configure(image=self.img)

        self.label2 = Label(invoice)
        self.label2.place(relx=0.052, rely=0.350, width=196, height=36)
        self.label2.configure(font="-family {Poppins} -size 14")
        self.label2.configure(anchor="w")
        self.label2.configure(background="#ffffff")
        self.label2.configure(foreground="#333333")
        self.label2.configure(bd=1,relief="solid")


        self.message = Label(invoice)
        self.message.place(relx=0.046, rely=0.055, width=50, height=30)
        self.message.configure(font="-family {Poppins} -size 10")
        self.message.configure(foreground="#000000")
        self.message.configure(background="#ffffff")
        self.message.configure(text="""admin""")
        self.message.configure(anchor="w")

        self.clock = Label(invoice)
        self.clock.place(relx=0.9, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        self.entry1 = Entry(invoice)
        self.entry1.place(relx=0.040, rely=0.286, width=240, height=28)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")

        self.entry2 =Entry(invoice)
        self.entry2.place(relx=0.4, rely=0.35, width=200, height=36)
        self.entry2.configure(font="-family {Poppins Light} -size 12")
        self.entry2.configure(foreground="#000000")
        self.entry2.configure(background="#ffffff")


        self.button1 = Button(invoice)
        self.button1.place(relx=0.229, rely=0.289, width=50, height=23)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#76AEC3")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#76AEC3")
        self.button1.configure(font="-family {Poppins SemiBold} -size 10")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""Search""")
        self.button1.configure(command=self.search_inv)

        self.button2 = Button(invoice)
        self.button2.place(relx=0.035, rely=0.11, width=76, height=20)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#76AEC3")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#76AEC3")
        self.button2.configure(font="-family {Poppins SemiBold} -size 12")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""Logout""")
        self.button2.configure(command=self.Logout)

        self.button3 = Button(invoice)
        self.button3.place(relx=0.052, rely=0.432, width=306, height=28)
        self.button3.configure(relief="flat")
        self.button3.configure(overrelief="flat")
        self.button3.configure(activebackground="#76AEC3")
        self.button3.configure(cursor="hand2")
        self.button3.configure(foreground="#ffffff")
        self.button3.configure(background="#76AEC3")
        self.button3.configure(font="-family {Poppins SemiBold} -size 12")
        self.button3.configure(borderwidth="0")
        self.button3.configure(text="""DELETE INVOICE""")
        self.button3.configure(command=self.delete_invoice)

        self.button4 = Button(invoice)
        self.button4.place(relx=0.135, rely=0.885, width=76, height=23)
        self.button4.configure(relief="flat")
        self.button4.configure(overrelief="flat")
        self.button4.configure(activebackground="#76AEC3")
        self.button4.configure(cursor="hand2")
        self.button4.configure(foreground="#ffffff")
        self.button4.configure(background="#76AEC3")
        self.button4.configure(font="-family {Poppins SemiBold} -size 12")
        self.button4.configure(borderwidth="0")
        self.button4.configure(text="""EXIT""")
        self.button4.configure(command=self.Exit)

        self.button5 = Button(invoice)
        self.button5.place(relx=0.052, rely=0.332, width=100, height=23)
        self.button5.configure(relief="flat")
        self.button5.configure(overrelief="flat")
        self.button5.configure(activebackground="#76AEC3")
        self.button5.configure(cursor="hand2")
        self.button5.configure(foreground="#ffffff")
        self.button5.configure(background="#76AEC3")
        self.button5.configure(font="-family {Poppins SemiBold} -size 12")
        self.button5.configure(borderwidth="0")
        self.button5.configure(text="""ดูยอดรายวัน""")
        self.button5.configure(bd=1,relief="solid")
        self.button5.configure(command=self.look_day)

        self.button6 = Button(invoice)
        self.button6.place(relx=0.122, rely=0.332, width=100, height=23)
        self.button6.configure(relief="flat")
        self.button6.configure(overrelief="flat")
        self.button6.configure(activebackground="#76AEC3")
        self.button6.configure(cursor="hand2")
        self.button6.configure(foreground="#ffffff")
        self.button6.configure(background="#76AEC3")
        self.button6.configure(font="-family {Poppins SemiBold} -size 12")
        self.button6.configure(borderwidth="0")
        self.button6.configure(text="""ดูยอดรายเดือน""")
        self.button6.configure(bd=1,relief="solid")
        self.button6.configure(command=self.look_month)

     
        self.scrollbarx = Scrollbar(invoice, orient=HORIZONTAL)
        self.scrollbary = Scrollbar(invoice, orient=VERTICAL)
        self.tree = ttk.Treeview(invoice)
        self.tree.place(relx=0.307, rely=0.203, width=880, height=550)
        self.tree.configure(
            yscrollcommand=self.scrollbary.set, xscrollcommand=self.scrollbarx.set
        )
        self.tree.configure(selectmode="extended")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Double-1>", self.double_tap)

        self.scrollbary.configure(command=self.tree.yview)
        self.scrollbarx.configure(command=self.tree.xview)

        self.scrollbary.place(relx=0.954, rely=0.203, width=22, height=548)
        self.scrollbarx.place(relx=0.307, rely=0.924, width=884, height=22)

        self.tree.configure(
            columns=(
                "Bill Number",
                "Date",
                "Customer Name",
                "Customer Phone No.",
            )
        )

        self.tree.heading("Bill Number", text="Bill Number", anchor=W)
        self.tree.heading("Date", text="Date", anchor=W)
        self.tree.heading("Customer Name", text="Customer Name", anchor=W)
        self.tree.heading("Customer Phone No.", text="Customer Phone No.", anchor=W)
        

        self.tree.column("#0", stretch=NO, minwidth=0, width=0)
        self.tree.column("#1", stretch=NO, minwidth=0, width=219)
        self.tree.column("#2", stretch=NO, minwidth=0, width=219)
        self.tree.column("#3", stretch=NO, minwidth=0, width=219)
        self.tree.column("#4", stretch=NO, minwidth=0, width=219)
        

        self.DisplayData()


    def DisplayData(self):
        cur.execute("SELECT bill_no, date, customer_name, customer_no FROM bill ")        
        fetch = cur.fetchall()
        for data in fetch:
            self.tree.insert("", "end", values=(data))

    sel = []
    def on_tree_select(self, Event):
        self.sel.clear()
        for i in self.tree.selection():
            if i not in self.sel:
                self.sel.append(i)

    def double_tap(self, Event):
        print("2")
        item = self.tree.identify('item', Event.x, Event.y)
        global bill_num
        bill_num = self.tree.item(item)['values'][0]
        print(bill_num)

        find_bill = "SELECT * FROM bill WHERE bill_no = ?"
        cur.execute(find_bill, [bill_num])
        results = cur.fetchall()
        if results:
            print(results)
            subprocess.Popen(['start', '', results[0][6]], shell=True)



        


    def delete_invoice(self):
        val = []
        to_delete = []

        if len(self.sel)!=0:
            sure = messagebox.askyesno("Confirm", "Are you sure you want to delete selected invoice(s)?", parent=invoice)
            if sure == True:
                for i in self.sel:
                    for j in self.tree.item(i)["values"]:
                        val.append(j)
                
                for j in range(len(val)):
                    if j%5==0:
                        to_delete.append(val[j])
                
                for k in to_delete:
                    delete = "DELETE FROM bill WHERE bill_no = ?"
                    cur.execute(delete, [k])
                    db.commit()

                messagebox.showinfo("Success!!", "Invoice(s) deleted from database.", parent=invoice)
                self.sel.clear()
                self.tree.delete(*self.tree.get_children())

                self.DisplayData()
        else:
            messagebox.showerror("Error!!","Please select an invoice", parent=invoice)

    def search_inv(self):
        val = []
        for i in self.tree.get_children():
            val.append(i)
            for j in self.tree.item(i)["values"]:
                val.append(j)

        to_search = self.entry1.get()
        for search in val:
            if search==to_search:
                self.tree.selection_set(val[val.index(search)-1])
                self.tree.focus(val[val.index(search)-1])
                messagebox.showinfo("Success!!", "Bill Number: {} found.".format(self.entry1.get()), parent=invoice)
                break
        else: 
            messagebox.showerror("Oops!!", "Bill NUmber: {} not found.".format(self.entry1.get()), parent=invoice)


    def look_day(self):
        day = self.entry1.get()
        print(day)
        insert = ("SELECT SUM(income) FROM bill WHERE date = ? ")
        cur.execute(insert, [day])
        db.commit()
        result = cur.fetchall()
        print(result[0][0])
        if result[0][0] == None:
            results = 0
            bath = "บาท"
            results = (results,bath,)
            self.label2.configure(text=results)
        else :
            bath = "บาท"
            results = (result,bath,)
            self.label2.configure(text=results)

    def look_month(self):
        month = self.entry1.get()
        print(month)
        insert = ("SELECT SUM(income) FROM bill WHERE month = ? ")
        cur.execute(insert, [month])
        db.commit()
        result = cur.fetchall()
        print(result[0][0])
        if result[0][0] == None:
            results = 0
            bath = "บาท"
            results = (results,bath,)
            self.label2.configure(text=results)
        else :
            bath = "บาท"
            results = (result,bath,)
            self.label2.configure(text=results)

    def Logout(self):
        sure = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if sure == True:
            invoice.destroy()
            root.deiconify()
            page1.entry1.delete(0, END)
            page1.entry2.delete(0, END)

    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)

    def Exit(self):
        invoice.destroy()
        adm.deiconify()

page1 = login_page(root)
root.bind("<Return>", login_page.login)
root.mainloop()
