import tkinter as tk
from tkinter import messagebox
import datetime
import os

class CashRegister:
    def __init__(self, root):
        self.root = root
        self.root.title("Cash Register")

        self.items = []
        self.total = 0.0
        self.total_without_vat = 0.0
        self.vat_rate = 0.21  # 21% PVN

        # Center the window
        window_width = 450
        window_height = 800
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.root.resizable(False, False)

        root.grid_columnconfigure(1, weight=1)

        # Create login window for password
        self.password_window()

    def password_window(self):
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Enter Password")
        self.login_window.geometry("300x150")
        
        # Add password entry and buttons
        self.password_label = tk.Label(self.login_window, text="Enter Password:")
        self.password_label.pack(pady=10)

        self.password_entry = tk.Entry(self.login_window, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self.login_window, text="Login", command=self.check_password)
        self.login_button.pack(pady=10)

        self.error_label = tk.Label(self.login_window, text="", fg="red")
        self.error_label.pack()

    def check_password(self):
        password = self.password_entry.get()
        correct_password = "1234"  # Change this to your desired password

        if password == correct_password:
            self.login_window.destroy()
            self.ask_for_bag()  # Ask about the bag
        else:
            self.error_label.config(text="Incorrect password. Try again.")

    def ask_for_bag(self):
        # Create a window asking about the bag
        self.bag_window = tk.Toplevel(self.root)
        self.bag_window.title("Do you need a bag?")
        self.bag_window.geometry("300x200")
        
        # Ask if the user needs a bag
        self.bag_label = tk.Label(self.bag_window, text="Maisiņ vaig?")
        self.bag_label.pack(pady=10)

        self.bag_var = tk.StringVar(value="No")
        self.bag_option = tk.OptionMenu(self.bag_window, self.bag_var, "Nē", "Jā")
        self.bag_option.pack(pady=5)

        self.size_label = tk.Label(self.bag_window, text="Maisiņa izmērs:")
        self.size_label.pack(pady=5)

        self.size_var = tk.StringVar(value="Small")
        self.size_option = tk.OptionMenu(self.bag_window, self.size_var, "Mazs", "Liels")
        self.size_option.pack(pady=5)

        self.confirm_button = tk.Button(self.bag_window, text="Confirm", command=self.confirm_bag_choice)
        self.confirm_button.pack(pady=10)

    def confirm_bag_choice(self):
        # Get the selected options
        needs_bag = self.bag_var.get() == "Yes"
        bag_size = self.size_var.get()

        # Close the bag selection window
        self.bag_window.destroy()

        # If the user needs a bag, store that information and proceed to the cash register
        self.needs_bag = needs_bag
        self.bag_size = bag_size

        # Now open the main cash register window
        self.create_cash_register_ui()

    def create_cash_register_ui(self):
        # Item name
        self.name_label = tk.Label(self.root, text="Item name:")
        self.name_label.grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=1, column=1, sticky="we", padx=10, pady=5)

        # Price
        self.price_label = tk.Label(self.root, text="Price:")
        self.price_label.grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.price_entry = tk.Entry(self.root)
        self.price_entry.grid(row=2, column=1, sticky="we", padx=10, pady=5)

        # Quantity
        self.qty_label = tk.Label(self.root, text="Quantity:")
        self.qty_label.grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.qty_entry = tk.Entry(self.root)
        self.qty_entry.grid(row=3, column=1, sticky="we", padx=10, pady=5)

        # Add Item button
        self.add_button = tk.Button(self.root, text="Add Item", bg="lightgreen", command=self.add_item)
        self.add_button.grid(row=4, column=0, columnspan=2, sticky="we", padx=10, pady=5)

        # Items display
        self.items_display = tk.Text(self.root, width=30, height=8)
        self.items_display.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        # Total
        self.total_label = tk.Label(self.root, text="Total: 0.00$")
        self.total_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        # Discount
        self.discount_label = tk.Label(self.root, text="Discount(%)")
        self.discount_label.grid(row=7, column=0, columnspan=2, padx=10, pady=(10, 2))
        self.discount_entry = tk.Entry(self.root)
        self.discount_entry.grid(row=8, column=0, columnspan=2, sticky="we", padx=10, pady=2)

        self.discount_button = tk.Button(self.root, text="Apply Discount", bg="yellowgreen", command=self.apply_discount)
        self.discount_button.grid(row=9, column=0, columnspan=2, sticky="we", padx=10, pady=5)

        # Payment
        self.payment_label = tk.Label(self.root, text="Enter Payment Amount")
        self.payment_label.grid(row=10, column=0, columnspan=2, padx=10, pady=(10, 2))
        self.payment_entry = tk.Entry(self.root)
        self.payment_entry.grid(row=11, column=0, columnspan=2, sticky="we", padx=10, pady=2)

        # Payment method
        tk.Label(self.root, text="Payment Method").grid(row=12, column=0, columnspan=2, padx=10, pady=(10, 2))
        self.payment_method = tk.StringVar()
        self.payment_method.set("Cash")
        self.payment_options = tk.OptionMenu(self.root, self.payment_method, "Cash", "Card", "Mobile")
        self.payment_options.grid(row=13, column=0, columnspan=2, sticky="we", padx=10, pady=2)

        # PAY button
        self.pay_button = tk.Button(self.root, text="PAY", bg="skyblue", command=self.process_payment)
        self.pay_button.grid(row=14, column=0, columnspan=2, sticky="we", padx=10, pady=10)

        # Clear
        self.clear_button = tk.Button(self.root, text="Clear", bg="red", command=self.clear_all)
        self.clear_button.grid(row=15, column=0, columnspan=2, sticky="we", padx=10, pady=(5, 10))

    def add_item(self):
        name = self.name_entry.get()
        try:
            price = float(self.price_entry.get())
            quantity = int(self.qty_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid price and quantity")
            return

        subtotal = price * quantity
        subtotal_wo_vat = subtotal / (1 + self.vat_rate)

        self.total += subtotal
        self.total_without_vat += subtotal_wo_vat
        self.items.append(f"{name} x{quantity} - {subtotal:.2f}$")
        self.update_display()

    def update_display(self):
        self.items_display.delete(1.0, tk.END)
        for item in self.items:
            self.items_display.insert(tk.END, item + "\n")
        vat_amount = self.total - self.total_without_vat
        self.total_label.config(
            text=f"Bez PVN: {self.total_without_vat:.2f}$ | PVN: {vat_amount:.2f}$ | Kopā: {self.total:.2f}$"
        )

    def apply_discount(self):
        try:
            discount_percent = float(self.discount_entry.get())
            self.total -= self.total * discount_percent / 100
            self.total_without_vat = self.total / (1 + self.vat_rate)
            self.update_display()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid discount percentage")

    def process_payment(self):
        try:
            payment = float(self.payment_entry.get())
            if payment < self.total:
                messagebox.showwarning("Warning", "Insufficient payment")
            else:
                change = payment - self.total
                method = self.payment_method.get()
                vat_amount = self.total - self.total_without_vat

                # Get current date and time
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Build receipt
                receipt = f"--- ČEKS ---\n"
                receipt += f"Datums: {timestamp}\n"
                receipt += "\n".join(self.items)
                receipt += f"\n\nSumma bez PVN: {self.total_without_vat:.2f}$"
                receipt += f"\nPVN (21%): {vat_amount:.2f}$"
                receipt += f"\nKopā (ar PVN): {self.total:.2f}$"
                receipt += f"\nSamaksāts: {payment:.2f}$"
                receipt += f"\nAtlikums: {change:.2f}$"
                receipt += f"\nApmaksas veids: {method}"

                # Include bag information in receipt
                if self.needs_bag:
                    receipt += f"\nMaisiņš: {self.bag_size}"

                # Show receipt in a message box
                messagebox.showinfo("Maksājums veikts", receipt)

                # Create filename with timestamp
                filename = f"receipt_{timestamp.replace(':', '-').replace(' ', '_')}.txt"
                print(f"Čeks tiek saglabāts šādā vietā: {filename}")  # Debugging line to check filename

                # Saglabāt čeku konkrētā vietā
                # Piemēram, ja vēlies saglabāt čeku uz C: diska, norādi pilnu ceļu:
                save_folder = "C:/Users/YourUsername/Documents"  # maini uz savu ceļu
                if not os.path.exists(save_folder):
                    os.makedirs(save_folder)  # Ja mape neeksistē, izveido to
                file_path = os.path.join(save_folder, filename)
                
                # Save receipt to file
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(receipt)
                print(f"Čeks saglabāts: {file_path}")  # Parādīs ceļu, kur saglabājās čeks

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid payment amount")

    def clear_all(self):
        self.name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.qty_entry.delete(0, tk.END)
        self.items_display.delete(1.0, tk.END)
        self.discount_entry.delete(0, tk.END)
        self.payment_entry.delete(0, tk.END)
        self.total = 0.0
        self.total_without_vat = 0.0
        self.items = []
        self.update_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = CashRegister(root)
    root.mainloop()
