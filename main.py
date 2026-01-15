import customtkinter as ctk
from tkinter import ttk, messagebox
from database import Database
from emailClient import EmailService

ctk.set_appearance_mode("dark")      # "light" or "dark"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FitLife App")
        self.geometry("910x540")

        # Main wrapper
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)

        # Navbar (created but NOT packed yet)
        self.navbar = ctk.CTkFrame(self.main_frame, height=60, fg_color="#1f1f1f")
        self.create_navbar()

        # Container BELOW navbar
        self.container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # DB + Email
        self.db = Database()
        self.email_service = EmailService(
            sender_email="lifefitnessautomatic@gmail.com",
            app_password=""
        )

        # Pages
        self.frames = {}
        for Page in (LoginPage, HomePage, OverDueBalancePage):
            frame = Page(self.container, self)
            self.frames[Page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, page):
        self.frames[page].tkraise()

    def logout(self, page):
        self.show_frame(page)
        self.navbar.pack_forget()

    def create_navbar(self):
        btn_frame = ctk.CTkFrame(self.navbar, fg_color="transparent")
        btn_frame.pack(expand=True)

        ctk.CTkButton(btn_frame, text="Home", width=120,
                      command=lambda: self.show_frame(HomePage)).pack(side="left", padx=20)

        ctk.CTkButton(btn_frame, text="Overdue", width=120,
                      command=lambda: self.show_frame(OverDueBalancePage)).pack(side="left", padx=20)

        ctk.CTkButton(btn_frame, text="Logout", width=120,
                      fg_color="#b30000", hover_color="#800000",
                      command=lambda: self.logout(LoginPage)).pack(side="left", padx=20)

    def showNavbar(self):
        self.navbar.pack(fill="x", side="top", before=self.container)


# ---------------- LOGIN PAGE ----------------

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        ctk.CTkLabel(self, text="Login", font=("Arial", 28)).pack(pady=30)

        ctk.CTkLabel(self, text="Username").pack()
        self.username = ctk.CTkEntry(self, width=250)
        self.username.pack(pady=5)

        ctk.CTkLabel(self, text="Password").pack()
        self.password = ctk.CTkEntry(self, width=250, show="*")
        self.password.pack(pady=5)

        ctk.CTkButton(self, text="Login", width=200,
                      command=lambda: self.try_login(controller)).pack(pady=20)

        self.message = ctk.CTkLabel(self, text="", text_color="red")
        self.message.pack()

    def try_login(self, controller):
        user = self.username.get()
        pwd = self.password.get()

        if user == "root" and pwd == "toor":
            controller.show_frame(HomePage)
            controller.showNavbar()
        else:
            self.message.configure(text="Invalid credentials")


# ---------------- HOME PAGE ----------------

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        ctk.CTkLabel(self, text="Welcome!", font=("Arial", 28)).pack(pady=40)


# ---------------- OVERDUE BALANCE PAGE ----------------

class OverDueBalancePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Overdue Balances", font=("Arial", 26)).pack(pady=20)

        # Styled Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2b2b2b",
                        foreground="white",
                        rowheight=30,
                        fieldbackground="#2b2b2b")
        style.map("Treeview", background=[("selected", "#1f6aa5")])

        columns = ("Name", "Amount Due", "Phone", "Email", "Send Email")

        self.table = ttk.Treeview(self, columns=columns, show="headings")
        self.table.pack(fill="both", expand=True, padx=20, pady=10)

        for col in columns:
            self.table.heading(col, text=col)

        for row in self.fetch_overdue_data():
            self.table.insert("", "end", values=(
                row["name"], row["amount"], row["phone"], row["email"], "Send Email"
            ))

        self.table.bind("<Button-1>", self.on_table_click)

    def fetch_overdue_data(self):
        return self.controller.db.query("SELECT * FROM overdue")

    def on_table_click(self, event):
        region = self.table.identify("region", event.x, event.y)
        if region != "cell":
            return

        row_id = self.table.identify_row(event.y)
        col_id = self.table.identify_column(event.x)

        if col_id == "#5":
            values = self.table.item(row_id, "values")
            name, amount, email = values[0], values[1], values[3]
            self.open_email_popup(name, email, amount)

    def open_email_popup(self, name, email, amount):
        win = ctk.CTkToplevel(self)
        win.title(f"Send Email to {email}")
        win.geometry("400x350")

        ctk.CTkLabel(win, text=f"To: {email}", font=("Arial", 16)).pack(pady=10)

        ctk.CTkLabel(win, text="Message:").pack()
        message_box = ctk.CTkTextbox(win, width=350, height=150)
        message_box.pack(pady=10)

        ctk.CTkButton(win, text="Send Email",
                      command=lambda: self.send_email_action(email, message_box.get("1.0", "end"), amount)
                      ).pack(pady=10)

    def send_email_action(self, email, message, amount):
        success, msg = self.controller.email_service.send_email(
            to_email=email,
            name="Customer",
            user_message=message,
            amount=amount
        )

        if success:
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app = App()
    app.mainloop()
