import tkinter as tk
from tkinter import ttk
import sqlite3

class App(tk.Tk):
    def __init__(self):
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
            frame = Page(self.container, self)
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
    def __init__(self, parent, controller):
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
    def __init__(self, parent, controller):
        super().__init__(parent)
        #  instatiate the frame as you would instantiate a normal frame
        tk.Label(self, text="Welcome!", font=("Arial", 18)).pack(pady=20)


class overDueBalancePage(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        tk.Label(self, text="OverDue Balances", font=("Arial", 18)).pack(pady=20)

        columns = ("Name", "Amount Unpaid", "Phone Number", "Email")

        table = ttk.Treeview(self, columns=columns, show="headings")
        table.pack(fill="both", expand=True)

        for col in columns:
            table.heading(col, text=col)

        table.insert("", "end", values=("John Smith", 25.00, "07584710472","johnSmith@yahoo.com"))
        table.insert("", "end", values=("Test 1", 25.60, "0988865239", "test1@mail.com"))
        table.insert("", "end", values=("Test 2", 400.00, "06876435670","test2@mail.com"))
    
def databaseTest(cur):
    # this function loops a 100 times and adds some random test data to the database
    import random
    for i in range(100):
        name = f"Test User {i}"
        amountOwed = round(random.uniform(10.0, 500.0), 2)
        phoneNumber = f"07{random.randint(10000000, 99999999)}"
        email = f"test{i}@mail.com"

        cur.execute("INSERT INTO users (name, amountOwed, phoneNumber, email) VALUES (?, ?, ?, ?)",
                    (name, amountOwed, phoneNumber, email))
def printDatabaseContents(cur):
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    for row in rows:
        print(row)



if __name__ == "__main__":
    app = App()
    # Connect to a database (creates file if it doesn't exist)
    conn = sqlite3.connect("overdueBalances.db")
    # Create a cursor to run SQL commands
    cur = conn.cursor()
   #if the user does not owe anything, they will not be added to the database
   #if the amountOwed is 0 they will be removed from the database
    cur.execute(""" CREATE TABLE IF NOT EXISTS users ( 
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT NOT NULL, amountOwed REAL NOT NULL, 
                phoneNumber TEXT NOT NULL, 
                email TEXT NOT NULL ) """)
    
    databaseTest(cur)
    printDatabaseContents(cur)
    app.mainloop()
    conn.close()
