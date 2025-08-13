from tkinter import *
from tkinter import messagebox
import sqlite3
import dashboard  # Make sure dashboard.py is in the same folder

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Student Result Management System")
        self.root.geometry("400x300+500+200")
        self.root.config(bg="white")

        # ===== Title =====
        title_lbl = Label(self.root, text="Login", font=("goudy old style", 24, "bold"), bg="white", fg="#033054")
        title_lbl.pack(pady=20)

        # ===== Username =====
        lbl_user = Label(self.root, text="Username", font=("goudy old style", 15), bg="white", fg="#033054")
        lbl_user.pack()
        self.txt_user = Entry(self.root, font=("goudy old style", 15), bg="lightyellow")
        self.txt_user.pack(pady=5)

        # ===== Password =====
        lbl_pass = Label(self.root, text="Password", font=("goudy old style", 15), bg="white", fg="#033054")
        lbl_pass.pack()
        self.txt_pass = Entry(self.root, font=("goudy old style", 15), bg="lightyellow", show="*")
        self.txt_pass.pack(pady=5)

        # ===== Login Button =====
        btn_login = Button(self.root, text="Login", font=("goudy old style", 15, "bold"), bg="#4caf50", fg="white",
                           cursor="hand2", command=self.login)
        btn_login.pack(pady=20)

    def login(self):
        username = self.txt_user.get().strip()
        password = self.txt_pass.get().strip()

        if username == "" or password == "":
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
            return

        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        row = cur.fetchone()
        con.close()

        if row is None:
            messagebox.showerror("Error", "Invalid Username or Password!", parent=self.root)
        else:
            self.root.destroy()
            root_dash = Tk()
            dashboard.RMS(root_dash, username=username)
            root_dash.mainloop()

if __name__ == "__main__":
    root = Tk()
    Login(root)
    root.mainloop()
