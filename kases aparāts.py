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
        window_width = 350
        window_height = 800
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.root.resizable(False, False)

        root.grid_columnconfigure(1, weight=1)

        # Language selection
        self.language = tk.StringVar(value="Latvian")
        language_menu = tk.OptionMenu(root, self.language, "Latvian", "English", "Russian", "Spanish", command=self.change_language)
        language_menu.grid(row=50, column=0, columnspan=2, sticky="we", padx=10, pady=5)

        # Item name
        self.name_label = tk.Label(root, text="Item name:")
        self.name_label.grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=1, column=1, sticky="we", padx=10, pady=5)

        # Price
        self.price_label = tk.Label(root, text="Price:")
        self.price_label.grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.price_entry = tk.Entry(root)
        self.price_entry.grid(row=2, column=1, sticky="we", padx=10, pady=5)

        # Quantity
        self.qty_label = tk.Label(root, text="Quantity:")
        self.qty_label.grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.qty_entry = tk.Entry(root)
        self.qty_entry.grid(row=3, column=1, sticky="we", padx=10, pady=5)

        # Add Item button
        self.add_button = tk.Button(root, text="Add Item", bg="lightgreen", command=self.add_item)
        self.add_button.grid(row=4, column=0, columnspan=2, sticky="we", padx=10, pady=5)

        # Items display
        self.items_display = tk.Text(root, width=30, height=8)
        self.items_display.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        # Total
        self.total_label = tk.Label(root, text="Total: 0.00$")
        self.total_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        # Discount
        self.discount_label = tk.Label(root, text="Discount(%)")
        self.discount_label.grid(row=7, column=0, columnspan=2, padx=10, pady=(10, 2))
        self.discount_entry = tk.Entry(root)
        self.discount_entry.grid(row=8, column=0, columnspan=2, sticky="we", padx=10, pady=2)

        self.discount_button = tk.Button(root, text="Apply Discount", bg="yellowgreen", command=self.apply_discount)
        self.discount_button.grid(row=9, column=0, columnspan=2, sticky="we", padx=10, pady=5)

        # Payment
        self.payment_label = tk.Label(root, text="Enter Payment Amount")
        self.payment_label.grid(row=10, column=0, columnspan=2, padx=10, pady=(10, 2))
        self.payment_entry = tk.Entry(root)
        self.payment_entry.grid(row=11, column=0, columnspan=2, sticky="we", padx=10, pady=2)

        tk.Label(root, text="Payment Method").grid(row=12, column=0, columnspan=2, padx=10, pady=(10, 2))
        self.payment_method = tk.StringVar()
        self.payment_method.set("Cash")
        self.payment_options = tk.OptionMenu(root, self.payment_method, "Cash", "Card", "Mobile")
        self.payment_options.grid(row=13, column=0, columnspan=2, sticky="we", padx=10, pady=2)

        # PAY button
        self.pay_button = tk.Button(root, text="PAY", bg="skyblue", command=self.process_payment)
        self.pay_button.grid(row=14, column=0, columnspan=2, sticky="we", padx=10, pady=10)

        # Clear
        self.clear_button = tk.Button(root, text="Clear", bg="red", command=self.clear_all)
        self.clear_button.grid(row=15, column=0, columnspan=2, sticky="we", padx=10, pady=(5, 10))

    def change_language(self, *args):
        lang = self.language.get()

        if lang == "Latvian":
            self.name_label.config(text="Preces nosaukums:")
            self.price_label.config(text="Cena:")
            self.qty_label.config(text="Skaits:")
            self.discount_label.config(text="Atlaide(%)")
            self.payment_label.config(text="Ievadīt maksājuma summu")
            self.payment_options.config(values=("Nauda", "Kartes", "Mobilais"))
            self.add_button.config(text="Pievienot preci")
            self.discount_button.config(text="Piemērot atlaidi")
            self.pay_button.config(text="Maksāt")
            self.clear_button.config(text="Notīrīt")
        
        elif lang == "English":
            self.name_label.config(text="Item name:")
            self.price_label.config(text="Price:")
            self.qty_label.config(text="Quantity:")
            self.discount_label.config(text="Discount(%)")
            self.payment_label.config(text="Enter Payment Amount")
            self.payment_options.config(values=("Cash", "Card", "Mobile"))
            self.add_button.config(text="Add Item")
            self.discount_button.config(text="Apply Discount")
            self.pay_button.config(text="PAY")
            self.clear_button.config(text="Clear")

        elif lang == "Russian":
            self.name_label.config(text="Название товара:")
            self.price_label.config(text="Цена:")
            self.qty_label.config(text="Количество:")
            self.discount_label.config(text="Скидка(%)")
            self.payment_label.config(text="Введите сумму платежа")
            self.payment_options.config(values=("Наличные", "Карта", "Мобильный"))
            self.add_button.config(text="Добавить товар")
            self.discount_button.config(text="Применить скидку")
            self.pay_button.config(text="ОПЛАТИТЬ")
            self.clear_button.config(text="Очистить")
        
        elif lang == "Spanish":
            self.name_label.config(text="Nombre del artículo:")
            self.price_label.config(text="Precio:")
            self.qty_label.config(text="Cantidad:")
            self.discount_label.config(text="Descuento(%)")
            self.payment_label.config(text="Ingresar monto del pago")
            self.payment_options.config(values=("Efectivo", "Tarjeta", "Móvil"))
            self.add_button.config(text="Agregar artículo")
            self.discount_button.config(text="Aplicar descuento")
            self.pay_button.config(text="PAGAR")
            self.clear_button.config(text="Limpiar")

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
