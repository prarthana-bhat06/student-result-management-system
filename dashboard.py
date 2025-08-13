from tkinter import *
import sqlite3
from course_module import CourseClass
from student_module import StudentClass
from result_module import ResultClass
from view_module import ViewClass

class RMS:
    def __init__(self, root, username="Admin"):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#d6eaff")  # Modern light gray-blue background

        # === Top Banner ===
        top_frame = Frame(self.root, bg="#033054", height=70)
        top_frame.pack(side=TOP, fill=X)

        # Title (left)
        title_lbl = Label(top_frame, text="Student Result Management System",
                          font=("goudy old style", 28, "bold"), bg="#033054", fg="white")
        title_lbl.pack(side=LEFT, padx=20)

        # Logout & Exit buttons (top-right)
        btn_exit = Button(top_frame, text="Exit", font=("goudy old style", 12, "bold"),
                          bg="#607d8b", fg="white", cursor="hand2", command=self.exit_app)
        btn_exit.pack(side=RIGHT, padx=10, pady=15)

        btn_logout = Button(top_frame, text="Logout", font=("goudy old style", 12, "bold"),
                            bg="#f44336", fg="white", cursor="hand2", command=self.logout)
        btn_logout.pack(side=RIGHT, padx=10, pady=15)

        # === Main Buttons ===
        btn_course = Button(self.root, text="Course", font=("goudy old style", 20, "bold"),
                            bg="#2196f3", fg="white", cursor="hand2", width=15, height=4, command=self.open_course)
        btn_course.place(x=150, y=120)

        btn_student = Button(self.root, text="Student", font=("goudy old style", 20, "bold"),
                             bg="#4caf50", fg="white", cursor="hand2", width=15, height=4, command=self.open_student)
        btn_student.place(x=450, y=120)

        btn_result = Button(self.root, text="Result", font=("goudy old style", 20, "bold"),
                            bg="#f44336", fg="white", cursor="hand2", width=15, height=4, command=self.open_result)
        btn_result.place(x=750, y=120)

        btn_view = Button(self.root, text="View", font=("goudy old style", 20, "bold"),
                          bg="#607d8b", fg="white", cursor="hand2", width=15, height=4, command=self.open_view)
        btn_view.place(x=1050, y=120)

        # === Info Labels ===
        self.lbl_course = Label(self.root, text="Total Courses\n[ 0 ]",
                                font=("goudy old style", 20), bg="#ff5722", fg="white", bd=5, relief=RIDGE)
        self.lbl_course.place(x=150, y=300, width=300, height=100)

        self.lbl_student = Label(self.root, text="Total Students\n[ 0 ]",
                                 font=("goudy old style", 20), bg="#9c27b0", fg="white", bd=5, relief=RIDGE)
        self.lbl_student.place(x=500, y=300, width=300, height=100)

        self.lbl_result = Label(self.root, text="Total Results\n[ 0 ]",
                                font=("goudy old style", 20), bg="#009688", fg="white", bd=5, relief=RIDGE)
        self.lbl_result.place(x=850, y=300, width=300, height=100)

        # Refresh counts
        self.update_counts()

    def update_counts(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM course")
            total_courses = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM student")
            total_students = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM result")
            total_results = cur.fetchone()[0]

            self.lbl_course.config(text=f"Total Courses\n[ {total_courses} ]")
            self.lbl_student.config(text=f"Total Students\n[ {total_students} ]")
            self.lbl_result.config(text=f"Total Results\n[ {total_results} ]")
        except:
            pass
        finally:
            con.close()

    def open_course(self):
        self.new_win = Toplevel(self.root)
        self.app = CourseClass(self.new_win)
        self.new_win.protocol("WM_DELETE_WINDOW", lambda: [self.new_win.destroy(), self.update_counts()])

    def open_student(self):
        self.new_win = Toplevel(self.root)
        self.app = StudentClass(self.new_win)
        self.new_win.protocol("WM_DELETE_WINDOW", lambda: [self.new_win.destroy(), self.update_counts()])

    def open_result(self):
        self.new_win = Toplevel(self.root)
        self.app = ResultClass(self.new_win)
        self.new_win.protocol("WM_DELETE_WINDOW", lambda: [self.new_win.destroy(), self.update_counts()])

    def open_view(self):
        self.new_win = Toplevel(self.root)
        self.app = ViewClass(self.new_win)
        self.new_win.protocol("WM_DELETE_WINDOW", lambda: [self.new_win.destroy(), self.update_counts()])

    def logout(self):
        from login import Login
        self.root.destroy()
        root_login = Tk()
        Login(root_login)
        root_login.mainloop()

    def exit_app(self):
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    RMS(root)
    root.mainloop()
