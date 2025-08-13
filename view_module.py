from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk

class ViewClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System - View Records")
        self.root.geometry("1000x500+150+150")
        self.root.config(bg="white")
        self.root.focus_force()

        # Variables
        self.var_search = StringVar()

        # Title
        title = Label(self.root, text="View Student Results",
                      font=("goudy old style", 20, "bold"),
                      bg="#033054", fg="white").place(x=10, y=15, width=980, height=35)

        # Search Panel
        lbl_search = Label(self.root, text="Search by Roll No / Name", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=70)
        txt_search = Entry(self.root, textvariable=self.var_search, font=("goudy old style", 15), bg='lightyellow').place(x=250, y=70, width=200)
        btn_search = Button(self.root, text="Search", font=("goudy old style", 15, "bold"),
                            bg="#2196f3", fg="white", cursor="hand1", command=self.search).place(x=470, y=70, width=100, height=28)
        btn_show_all = Button(self.root, text="Show All", font=("goudy old style", 15, "bold"),
                              bg="#607d8b", fg="white", cursor="hand1", command=self.show).place(x=580, y=70, width=100, height=28)

        # Table Frame
        self.C_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_Frame.place(x=10, y=120, width=980, height=350)

        scrolly = Scrollbar(self.C_Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.C_Frame, orient=HORIZONTAL)
        self.ViewTable = ttk.Treeview(self.C_Frame,
                                      columns=("roll", "name", "email", "gender", "dob", "contact", "course", "marks_obt", "total_marks", "percentage", "grade"),
                                      xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.ViewTable.xview)
        scrolly.config(command=self.ViewTable.yview)

        # Table Headings
        self.ViewTable.heading("roll", text="Roll No")
        self.ViewTable.heading("name", text="Name")
        self.ViewTable.heading("email", text="Email")
        self.ViewTable.heading("gender", text="Gender")
        self.ViewTable.heading("dob", text="D.O.B")
        self.ViewTable.heading("contact", text="Contact")
        self.ViewTable.heading("course", text="Course")
        self.ViewTable.heading("marks_obt", text="Marks Obtained")
        self.ViewTable.heading("total_marks", text="Total Marks")
        self.ViewTable.heading("percentage", text="Percentage")
        self.ViewTable.heading("grade", text="Grade")

        self.ViewTable["show"] = 'headings'
        for col in self.ViewTable["columns"]:
            self.ViewTable.column(col, width=100)

        self.ViewTable.pack(fill=BOTH, expand=1)

        # Load all data initially
        self.show()

    def show(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("""
                SELECT s.roll, s.name, s.email, s.gender, s.dob, s.contact, s.course,
                       r.marks_obt, r.total_marks, r.percentage, r.grade
                FROM student s
                LEFT JOIN result r ON s.roll = r.roll
            """)
            rows = cur.fetchall()
            self.ViewTable.delete(*self.ViewTable.get_children())
            for row in rows:
                self.ViewTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def search(self):
        key = self.var_search.get()
        if key == "":
            messagebox.showerror("Error", "Search field is required", parent=self.root)
            return
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("""
                SELECT s.roll, s.name, s.email, s.gender, s.dob, s.contact, s.course,
                       r.marks_obt, r.total_marks, r.percentage, r.grade
                FROM student s
                LEFT JOIN result r ON s.roll = r.roll
                WHERE s.roll LIKE ? OR s.name LIKE ?
            """, ('%' + key + '%', '%' + key + '%'))
            rows = cur.fetchall()
            self.ViewTable.delete(*self.ViewTable.get_children())
            for row in rows:
                self.ViewTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    obj = ViewClass(root)
    root.mainloop()
