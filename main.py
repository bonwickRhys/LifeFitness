import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
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
        sender_email="lifefitnessautomatic@gmail.com",
        app_password="app_password_here"
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
    def __init__(self, parent, controller):
        self.controller = controller
        super().__init__(parent)

        tk.Label(self, text="OverDue Balances", font=("Arial", 18)).pack(pady=20)

        columns = ("Name", "Amount Due", "Phone Number", "Email", "Send Email")

        self.table = ttk.Treeview(self, columns=columns, show="headings")
        self.table.pack(fill="both", expand=True)

        for col in columns:
            self.table.heading(col, text=col)

        # Insert rows
        for row in self.fetch_overdue_data():
            rowData = (
                row["name"],
                row["amount"],
                row["phone"],
                row["email"],
                "Send Email"
            )
            self.table.insert("", "end", values=rowData)

        # Bind click event
        self.table.bind("<Button-1>", self.on_table_click)

    def fetch_overdue_data(self):
        return self.controller.db.query("SELECT * FROM overdue")
    
    def on_table_click(self, event):
        region = self.table.identify("region", event.x, event.y)
        if region != "cell":
            return

        row_id = self.table.identify_row(event.y)
        col_id = self.table.identify_column(event.x)

        # "Send Email" is the 5th column → #5
        if col_id == "#5":
            values = self.table.item(row_id, "values")
            name = values[0]
            email = values[3]
            amount = values[1] 
            self.open_email_popup(name, email, amount)
    def open_email_popup(self, name, email, amount):
        win = tk.Toplevel(self)
        win.title(f"Email {name}")
        win.geometry("400x300")

        tk.Label(win, text=f"To: {email}", font=("Arial", 12)).pack(pady=10)

        tk.Label(win, text="Message:", font=("Arial", 10)).pack()
        message_box = tk.Text(win, height=10, width=40)
        message_box.pack(pady=5)

        send_btn = tk.Button(
            win,
            text="Send Email",
            command=lambda: self.send_email_action(email, message_box.get("1.0", "end"), amount)
        )
        send_btn.pack(pady=10)
    def send_email_action(self, email, message, amount):
        success, msg = self.controller.email_service.send_email(
            to_email=email,
            user_message=message,
            amount=amount
        )

        if success:
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)



if __name__ == "__main__":

    # fake data

    app = App()
    app.mainloop()
    
