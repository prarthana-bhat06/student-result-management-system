from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3

class ResultClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()

        title = Label(self.root, text="Manage Student Results",
                      font=("goudy old style", 20, "bold"),
                      bg="#033054", fg="white").place(x=10, y=15, width=1180, height=35)

        # Variables
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_course = StringVar()
        self.var_marks_obtained = StringVar()
        self.var_total_marks = StringVar()
        self.var_percentage = StringVar()
        self.var_grade = StringVar()
        self.var_search = StringVar()
        self.selected_result_id = None

        # Student selection
        lbl_roll = Label(self.root, text="Select Student", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=60)
        self.cmb_student = ttk.Combobox(self.root, textvariable=self.var_roll, font=("goudy old style", 15), state='readonly')
        self.cmb_student.place(x=150, y=60, width=200)
        self.cmb_student.bind("<<ComboboxSelected>>", self.fetch_student_details)

        lbl_name = Label(self.root, text="Name", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=100)
        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg='lightyellow', state='readonly').place(x=150, y=100, width=200)

        lbl_course = Label(self.root, text="Course", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=140)
        txt_course = Entry(self.root, textvariable=self.var_course, font=("goudy old style", 15), bg='lightyellow', state='readonly').place(x=150, y=140, width=200)

        lbl_marks_obt = Label(self.root, text="Marks Obtained", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=180)
        txt_marks_obt = Entry(self.root, textvariable=self.var_marks_obtained, font=("goudy old style", 15), bg='lightyellow').place(x=150, y=180, width=200)

        lbl_total_marks = Label(self.root, text="Total Marks", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=220)
        txt_total_marks = Entry(self.root, textvariable=self.var_total_marks, font=("goudy old style", 15), bg='lightyellow').place(x=150, y=220, width=200)

        lbl_percentage = Label(self.root, text="Percentage", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=260)
        txt_percentage = Entry(self.root, textvariable=self.var_percentage, font=("goudy old style", 15), bg='lightyellow', state='readonly').place(x=150, y=260, width=200)

        lbl_grade = Label(self.root, text="Grade", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=300)
        txt_grade = Entry(self.root, textvariable=self.var_grade, font=("goudy old style", 15), bg='lightyellow', state='readonly').place(x=150, y=300, width=200)

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
        lbl_search = Label(self.root, text="Search by Roll No", font=("goudy old style", 15, 'bold'), bg='white').place(x=550, y=60)
        txt_search = Entry(self.root, textvariable=self.var_search, font=("goudy old style", 15), bg='lightyellow').place(x=730, y=60, width=180)
        btn_search = Button(self.root, text="Search", font=("goudy old style", 15, "bold"),
                            bg="#2196f3", fg="white", cursor="hand1", command=self.search).place(x=930, y=60, width=120, height=28)

        # Table frame
        self.C_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_Frame.place(x=550, y=100, width=630, height=340)

        scrolly = Scrollbar(self.C_Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.C_Frame, orient=HORIZONTAL)
        self.ResultTable = ttk.Treeview(self.C_Frame,
                                        columns=("rid", "roll", "name", "course", "marks_obt", "total_marks", "percentage", "grade"),
                                        xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.ResultTable.xview)
        scrolly.config(command=self.ResultTable.yview)

        self.ResultTable.heading("rid", text="ID")
        self.ResultTable.heading("roll", text="Roll No")
        self.ResultTable.heading("name", text="Name")
        self.ResultTable.heading("course", text="Course")
        self.ResultTable.heading("marks_obt", text="Marks Obtained")
        self.ResultTable.heading("total_marks", text="Total Marks")
        self.ResultTable.heading("percentage", text="Percentage")
        self.ResultTable.heading("grade", text="Grade")

        self.ResultTable["show"] = 'headings'
        for col in self.ResultTable["columns"]:
            self.ResultTable.column(col, width=100)

        self.ResultTable.pack(fill=BOTH, expand=1)
        self.ResultTable.bind("<ButtonRelease-1>", self.get_data)

        # Create table in DB
        self.create_table()
        self.fetch_students()
        self.show()

    def create_table(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS result(
                        rid INTEGER PRIMARY KEY AUTOINCREMENT,
                        roll TEXT UNIQUE,
                        name TEXT,
                        course TEXT,
                        marks_obt TEXT,
                        total_marks TEXT,
                        percentage TEXT,
                        grade TEXT
                    )""")
        con.commit()
        con.close()

    def fetch_students(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        cur.execute("SELECT roll FROM student")
        rows = cur.fetchall()
        student_list = [row[0] for row in rows] if rows else []
        self.cmb_student['values'] = student_list
        con.close()

    def fetch_student_details(self, ev):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        cur.execute("SELECT name, course FROM student WHERE roll=?", (self.var_roll.get(),))
        row = cur.fetchone()
        if row:
            self.var_name.set(row[0])
            self.var_course.set(row[1])
        con.close()

    def calculate_grade(self):
        try:
            marks_obt = float(self.var_marks_obtained.get())
            total_marks = float(self.var_total_marks.get())
            if total_marks <= 0:
                return
            percentage = (marks_obt / total_marks) * 100
            self.var_percentage.set(f"{percentage:.2f}")
            if percentage >= 90:
                self.var_grade.set("A+")
            elif percentage >= 80:
                self.var_grade.set("A")
            elif percentage >= 70:
                self.var_grade.set("B+")
            elif percentage >= 60:
                self.var_grade.set("B")
            elif percentage >= 50:
                self.var_grade.set("C")
            else:
                self.var_grade.set("F")
        except:
            pass

    def add(self):
        self.calculate_grade()
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_roll.get() == "" or self.var_marks_obtained.get() == "" or self.var_total_marks.get() == "":
                messagebox.showerror("Error", "All fields are required", parent=self.root)
                return
            cur.execute("SELECT * FROM result WHERE roll=?", (self.var_roll.get(),))
            row = cur.fetchone()
            if row:
                messagebox.showerror("Error", "Result for this Roll No already exists", parent=self.root)
            else:
                cur.execute("INSERT INTO result (roll, name, course, marks_obt, total_marks, percentage, grade) VALUES (?,?,?,?,?,?,?)",
                            (self.var_roll.get(), self.var_name.get(), self.var_course.get(),
                             self.var_marks_obtained.get(), self.var_total_marks.get(),
                             self.var_percentage.get(), self.var_grade.get()))
                con.commit()
                messagebox.showinfo("Success", "Result added successfully", parent=self.root)
                self.show()
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM result")
        rows = cur.fetchall()
        self.ResultTable.delete(*self.ResultTable.get_children())
        for row in rows:
            self.ResultTable.insert('', END, values=row)
        con.close()

    def get_data(self, ev):
        f = self.ResultTable.focus()
        content = self.ResultTable.item(f)
        row = content["values"]
        if row:
            self.selected_result_id = row[0]
            self.var_roll.set(row[1])
            self.var_name.set(row[2])
            self.var_course.set(row[3])
            self.var_marks_obtained.set(row[4])
            self.var_total_marks.set(row[5])
            self.var_percentage.set(row[6])
            self.var_grade.set(row[7])

    def update(self):
        self.calculate_grade()
        if self.selected_result_id is None:
            messagebox.showerror("Error", "Select a result to update", parent=self.root)
            return
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("UPDATE result SET roll=?, name=?, course=?, marks_obt=?, total_marks=?, percentage=?, grade=? WHERE rid=?",
                        (self.var_roll.get(), self.var_name.get(), self.var_course.get(),
                         self.var_marks_obtained.get(), self.var_total_marks.get(),
                         self.var_percentage.get(), self.var_grade.get(),
                         self.selected_result_id))
            con.commit()
            messagebox.showinfo("Success", "Result updated successfully", parent=self.root)
            self.show()
            self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        if self.selected_result_id is None:
            messagebox.showerror("Error", "Select a result to delete", parent=self.root)
            return
        ans = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
        if ans:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            cur.execute("DELETE FROM result WHERE rid=?", (self.selected_result_id,))
            con.commit()
            messagebox.showinfo("Delete", "Result deleted successfully", parent=self.root)
            self.show()
            self.clear()
            con.close()

    def clear(self):
        self.var_roll.set("")
        self.var_name.set("")
        self.var_course.set("")
        self.var_marks_obtained.set("")
        self.var_total_marks.set("")
        self.var_percentage.set("")
        self.var_grade.set("")
        self.var_search.set("")
        self.selected_result_id = None

    def search(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM result WHERE roll LIKE ?", ('%' + self.var_search.get() + '%',))
        rows = cur.fetchall()
        self.ResultTable.delete(*self.ResultTable.get_children())
        for row in rows:
            self.ResultTable.insert('', END, values=row)
        con.close()


if __name__ == "__main__":
    root = Tk()
    obj = ResultClass(root)
    root.mainloop()
