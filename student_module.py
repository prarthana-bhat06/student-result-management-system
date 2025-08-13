from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class StudentClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()

        # Title
        title = Label(self.root, text="Manage Student Details",
                      font=("goudy old style", 20, "bold"),
                      bg="#033054", fg="white").place(x=10, y=15, width=1180, height=35)

        # Variables
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_contact = StringVar()
        self.var_adm_date = StringVar()
        self.var_course = StringVar()
        self.var_search = StringVar()
        self.selected_student_id = None

        # Widgets
        lbl_roll = Label(self.root, text="Roll No", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=60)
        txt_roll = Entry(self.root, textvariable=self.var_roll, font=("goudy old style", 15), bg='lightyellow').place(x=150, y=60, width=200)

        lbl_name = Label(self.root, text="Name", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=100)
        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg='lightyellow').place(x=150, y=100, width=200)

        lbl_email = Label(self.root, text="Email", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=140)
        txt_email = Entry(self.root, textvariable=self.var_email, font=("goudy old style", 15), bg='lightyellow').place(x=150, y=140, width=200)

        lbl_gender = Label(self.root, text="Gender", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=180)
        cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender, values=("Male", "Female", "Other"),
                                  font=("goudy old style", 15), state='readonly', justify=CENTER)
        cmb_gender.place(x=150, y=180, width=200)
        cmb_gender.current(0)

        lbl_dob = Label(self.root, text="D.O.B", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=220)
        txt_dob = Entry(self.root, textvariable=self.var_dob, font=("goudy old style", 15), bg='lightyellow').place(x=150, y=220, width=200)

        lbl_contact = Label(self.root, text="Contact", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=260)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15), bg='lightyellow').place(x=150, y=260, width=200)

        lbl_adm_date = Label(self.root, text="Admission Date", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=300)
        txt_adm_date = Entry(self.root, textvariable=self.var_adm_date, font=("goudy old style", 15), bg='lightyellow').place(x=150, y=300, width=200)

        lbl_course = Label(self.root, text="Course", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=340)
        self.cmb_course = ttk.Combobox(self.root, textvariable=self.var_course,
                                       font=("goudy old style", 15), state='readonly', justify=CENTER)
        self.cmb_course.place(x=150, y=340, width=200)
        self.fetch_courses()

        # Buttons
        btn_add = Button(self.root, text="Save", font=("goudy old style", 15, "bold"),
                         bg="#2196f3", fg="white", cursor="hand1", command=self.add).place(x=400, y=60, width=110, height=40)
        btn_update = Button(self.root, text="Update", font=("goudy old style", 15, "bold"),
                            bg="#4caf50", fg="white", cursor="hand1", command=self.update).place(x=400, y=110, width=110, height=40)
        btn_delete = Button(self.root, text="Delete", font=("goudy old style", 15, "bold"),
                            bg="#f44336", fg="white", cursor="hand1", command=self.delete).place(x=400, y=160, width=110, height=40)
        btn_clear = Button(self.root, text="Clear", font=("goudy old style", 15, "bold"),
                           bg="#607d8b", fg="white", cursor="hand1", command=self.clear).place(x=400, y=210, width=110, height=40)

        # Search panel
        lbl_search = Label(self.root, text="Roll No / Name", font=("goudy old style", 15, 'bold'), bg='white').place(x=550, y=60)
        txt_search = Entry(self.root, textvariable=self.var_search, font=("goudy old style", 15), bg='lightyellow').place(x=700, y=60, width=180)
        btn_search = Button(self.root, text="Search", font=("goudy old style", 15, "bold"),
                            bg="#2196f3", fg="white", cursor="hand1", command=self.search).place(x=900, y=60, width=120, height=28)

        # Table frame
        self.C_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_Frame.place(x=550, y=100, width=630, height=340)

        scrolly = Scrollbar(self.C_Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.C_Frame, orient=HORIZONTAL)
        self.StudentTable = ttk.Treeview(self.C_Frame,
                                         columns=("sid", "roll", "name", "email", "gender", "dob", "contact", "adm_date", "course"),
                                         xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.StudentTable.xview)
        scrolly.config(command=self.StudentTable.yview)

        self.StudentTable.heading("sid", text="ID")
        self.StudentTable.heading("roll", text="Roll No")
        self.StudentTable.heading("name", text="Name")
        self.StudentTable.heading("email", text="Email")
        self.StudentTable.heading("gender", text="Gender")
        self.StudentTable.heading("dob", text="D.O.B")
        self.StudentTable.heading("contact", text="Contact")
        self.StudentTable.heading("adm_date", text="Admission Date")
        self.StudentTable.heading("course", text="Course")

        self.StudentTable["show"] = 'headings'
        for col in self.StudentTable["columns"]:
            self.StudentTable.column(col, width=100)

        self.StudentTable.pack(fill=BOTH, expand=1)
        self.StudentTable.bind("<ButtonRelease-1>", self.get_data)

        # Create table in DB
        self.create_table()
        self.show()

    def create_table(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS student(
                        sid INTEGER PRIMARY KEY AUTOINCREMENT,
                        roll TEXT UNIQUE,
                        name TEXT,
                        email TEXT,
                        gender TEXT,
                        dob TEXT,
                        contact TEXT,
                        adm_date TEXT,
                        course TEXT
                    )""")
        con.commit()
        con.close()

    def fetch_courses(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        cur.execute("SELECT name FROM course")
        rows = cur.fetchall()
        course_list = [row[0] for row in rows] if rows else ["No Course"]
        self.cmb_course['values'] = course_list
        if course_list:
            self.cmb_course.current(0)
        con.close()

    def add(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_roll.get() == "" or self.var_name.get() == "":
                messagebox.showerror("Error", "Roll No & Name are required", parent=self.root)
                return
            cur.execute("SELECT * FROM student WHERE roll=?", (self.var_roll.get(),))
            row = cur.fetchone()
            if row:
                messagebox.showerror("Error", "Roll No already exists", parent=self.root)
            else:
                cur.execute("INSERT INTO student (roll, name, email, gender, dob, contact, adm_date, course) VALUES (?,?,?,?,?,?,?,?)",
                            (self.var_roll.get(), self.var_name.get(), self.var_email.get(), self.var_gender.get(),
                             self.var_dob.get(), self.var_contact.get(), self.var_adm_date.get(), self.var_course.get()))
                con.commit()
                messagebox.showinfo("Success", "Student added successfully", parent=self.root)
                self.show()
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM student")
        rows = cur.fetchall()
        self.StudentTable.delete(*self.StudentTable.get_children())
        for row in rows:
            self.StudentTable.insert('', END, values=row)
        con.close()

    def get_data(self, ev):
        f = self.StudentTable.focus()
        content = self.StudentTable.item(f)
        row = content["values"]
        if row:
            self.selected_student_id = row[0]
            self.var_roll.set(row[1])
            self.var_name.set(row[2])
            self.var_email.set(row[3])
            self.var_gender.set(row[4])
            self.var_dob.set(row[5])
            self.var_contact.set(row[6])
            self.var_adm_date.set(row[7])
            self.var_course.set(row[8])

    def update(self):
        if self.selected_student_id is None:
            messagebox.showerror("Error", "Select a student to update", parent=self.root)
            return
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("UPDATE student SET roll=?, name=?, email=?, gender=?, dob=?, contact=?, adm_date=?, course=? WHERE sid=?",
                        (self.var_roll.get(), self.var_name.get(), self.var_email.get(), self.var_gender.get(),
                         self.var_dob.get(), self.var_contact.get(), self.var_adm_date.get(), self.var_course.get(),
                         self.selected_student_id))
            con.commit()
            messagebox.showinfo("Success", "Student updated successfully", parent=self.root)
            self.show()
            self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        if self.selected_student_id is None:
            messagebox.showerror("Error", "Select a student to delete", parent=self.root)
            return
        ans = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
        if ans:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            cur.execute("DELETE FROM student WHERE sid=?", (self.selected_student_id,))
            con.commit()
            messagebox.showinfo("Delete", "Student deleted successfully", parent=self.root)
            self.show()
            self.clear()
            con.close()

    def clear(self):
        self.var_roll.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Male")
        self.var_dob.set("")
        self.var_contact.set("")
        self.var_adm_date.set("")
        self.var_course.set("")
        self.var_search.set("")
        self.selected_student_id = None

    def search(self):
        key = self.var_search.get()
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM student WHERE roll LIKE ? OR name LIKE ?", ('%' + key + '%', '%' + key + '%'))
        rows = cur.fetchall()
        self.StudentTable.delete(*self.StudentTable.get_children())
        for row in rows:
            self.StudentTable.insert('', END, values=row)
        con.close()


if __name__ == "__main__":
    root = Tk()
    obj = StudentClass(root)
    root.mainloop()
