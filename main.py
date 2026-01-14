import tkinter as tk
from tkinter import ttk
from database import Database
from emailClient import EmailService
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("LifeFitness App")
        self.geometry("910x540")
        self.navbar = None 
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.db = Database()
        self.email_service = EmailService(
        sender_email="yourgmail@gmail.com",
        app_password="YOUR_APP_PASSWORD"
    )

        self.frames = {}

        # Add each page class here
        # we are using the actual class here and not an instance of the class
        for Page in (LoginPage, HomePage,overDueBalancePage):
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
        self.controller = controller
        super().__init__(parent)
        tk.Label(self, text="OverDue Balances", font=("Arial", 18)).pack(pady=20)
        columns = ("Name", "Amount Due", "Phone Number", "Email")

        table = ttk.Treeview(self, columns=columns, show="headings")
        table.pack(fill="both", expand=True)

        for col in columns:
            table.heading(col, text=col)

        for row in self.fetch_overdue_data():
            print("currentRow",row)
            rowData = (
                row["name"],
                row["amount"],
                row["phone"],
                row["email"]
            )
            table.insert("", "end", values=rowData)

    def fetch_overdue_data(self):
        return self.controller.db.query("SELECT * FROM overdue")

if __name__ == "__main__":

    # fake data

    app = App()
    app.mainloop()
    
