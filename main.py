import tkinter as tk
from tkinter import ttk
import sqlite3

class App(tk.Tk):
    def __init__(self, cur):
        super().__init__()

        self.title("LifeFitness App")
        self.geometry("910x540")
        self.navbar = None 
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
       
        self.frames = {}

        # Add each page class here
        # we are using the actual class here and not an instance of the class
        for Page in (LoginPage, HomePage,overDueBalancePage):
            # Page() creates a new instance of the current class we are iterating over
            # by passing in self we can access the methods of this class within every page class (showFrame())
            frame = Page(self.container, self,cur)
            #store the instance within the frames property
            self.frames[Page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Initally show the LoginPage
        self.show_frame(LoginPage)

    def show_frame(self, page):
        frame = self.frames[page]
        # tkraise and classes is the standard for switching between pages
        frame.tkraise()

    def logout(self,page):
        self.show_frame(page)
        # hide navbar
        self.navbar.pack_forget()
        self.navbar = None

    def create_navbar(self):
        if self.navbar:
            return 
        
        self.navbar = tk.Frame(self, bg="#ddd", height=50) 
        self.navbar.pack(fill="x") 

        tk.Button(self.navbar, text="Home", command=lambda: self.show_frame(HomePage)).pack(side="top",pady="10") 
        tk.Button(self.navbar, text="Overdue", command=lambda: self.show_frame(overDueBalancePage)).pack(side="top",pady="10") 
        tk.Button(self.navbar, text="Logout", command=lambda: self.logout(LoginPage)).pack(side="top",pady="10")


class LoginPage(tk.Frame):
    def __init__(self, parent, controller, cur):
        super().__init__(parent)
        # instatiate the frame as you would instantiate a normal frame
        tk.Label(self, text="Login", font=("Arial", 18)).pack(pady=20)

        tk.Label(self, text="Username").pack()
        self.username = tk.Entry(self)
        self.username.pack()

        tk.Label(self, text="Password").pack()
        self.password = tk.Entry(self, show="*")
        self.password.pack()

        tk.Button(
            self,
            text="Login",
            command=lambda: self.try_login(controller)
        ).pack(pady=20)

        self.message = tk.Label(self, text="", fg="red")
        self.message.pack()

    def try_login(self, controller):
        user = self.username.get()
        pwd = self.password.get()

        # temp login logic
        # replace with envvars + database hashed query
        if user == "root" and pwd == "toor":
            controller.create_navbar()
            controller.show_frame(HomePage)
        else:
            self.message.config(text="Invalid credentials")

class HomePage(tk.Frame):
    def __init__(self, parent, controller, cur):
        super().__init__(parent)
        #  instatiate the frame as you would instantiate a normal frame
        tk.Label(self, text="Welcome!", font=("Arial", 18)).pack(pady=20)


class overDueBalancePage(tk.Frame):
    def __init__(self,parent,controller,cur):
        super().__init__(parent)
        tk.Label(self, text="OverDue Balances", font=("Arial", 18)).pack(pady=20)
        self.cur = cur
        columns = ("Name", "Amount Due", "Phone Number", "Email")

        table = ttk.Treeview(self, columns=columns, show="headings")
        table.pack(fill="both", expand=True)

        for col in columns:
            table.heading(col, text=col)

        for row in self.fetch_overdue_data():
            print("currentRow",row)
            rowData = {
                "Name": row["name"],
                "Amount Due": row["amountOwed"],
                "Phone Number": row["phoneNumber"],
                "Email": row["email"]
            }
            table.insert("", "end", values=rowData)

    def fetch_overdue_data(self):
        rows = self.cur.execute("SELECT * FROM users")
        rows = self.cur.fetchall()
        for row in rows:
            print(row)
        return rows

def printDatabaseContents(cur):
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    for row in rows:
        print(row)


if __name__ == "__main__":
    conn = sqlite3.connect("overdueBalances.db")
    conn.row_factory = sqlite3.Row  # This makes rows behave like dictionaries
    cur = conn.cursor()
    app = App(cur)
    app.mainloop()
    
