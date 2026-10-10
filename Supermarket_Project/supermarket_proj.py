# name=input("Enter Your Name: ")

# list= '''
# Wheat       -     Rs 60/kg
# Tomato      -     Rs 34/kg
# boost       -     Rs 30/kg
# Milk        -     Rs 120/litre
# Biscuits    -     Rs 35/pack
# chicken     -     Rs 180/kg
# Shampoo     -     Rs 50/liter
# eggs        -     Rs 114/kg
# Coffee      -     Rs 190/kg
# '''

# price=0
# totalprice=0
# item_list=[]
# quantity_list=[]
# price_list=[]

# items={'wheat': 60,
#     'tomato': 34,
#     'boost': 30,
#     'milk': 120,
#     'biscuits': 35,
#     'chicken': 180,
#     'toys': 50,
#     'eggs': 114,
#     'coffee': 190
# }

# while True:
#       option1=input("press 1 for list or 2 for exit: ")
#       if option1=="2":
#             print("Thanks for shopping")
#             break
#       elif option1=="1":
#             print(list)
#             while True:
#                   option2=input("press 1 for buy or 2 for exit ")
#                   if option2=="2":
#                         print("Thanks for shopping")
#                         break
#                   elif option2=="1":
#                         item=input("Enter your items to buy: ").lower()
#                         if item in items:
#                               qty_item=input("Enter quantity: ")
#                               if qty_item.isdigit():
#                                     quantity = int(qty_item)
#                                     price=quantity*items[item]
#                                     totalprice+=price
#                                     item_list.append(item)
#                                     quantity_list.append(qty_item)
#                                     price_list.append(price)
#                               else:
#                                     print("not available quantity") 
#                         else:
#                               print("selected item is not here") 

#             if totalprice>0:
#                   tax=(totalprice*18)/100
#                   final_price=totalprice+tax

#                   print("="*100)
#                   print("\t\t\t\t\tSRI'S SUPERMARKET")
#                   print("="*100)
#                   print("Name\t: ",name)
#                   print("-"*100)
#                   print("S.No\t\tItem\t\tQuantity\t\tPrice")
#                   print("-"*100)

#                   for i in range(len(item_list)):
#                         print(i+1,"\t\t",item_list[i],
#                               "        ",quantity_list[i],
#                               "        ",price_list[i])
#                   print("-"*100)      
#                   print("Total amount: ",totalprice)
#                   print("Tax applied: ",tax)
#                   print("Final amount: ",final_price)
#                   print("-"*100)
#                   print("\t\t\t\tThank you visit again")
#                   print("-"*100)

                


"""
Supermarket Bill Generation System (Tkinter)
Run with:  python supermarket_billing.py
"""

import os
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox, filedialog

# -------------------- SETTINGS (change these easily) --------------------
PRODUCTS = {
    "Rice (1 kg)": 60.0,
    "Wheat Flour (1 kg)": 45.0,
    "Sugar (1 kg)": 42.0,
    "Milk (1 L)": 56.0,
    "Eggs (12 pcs)": 84.0,
    "Cooking Oil (1 L)": 150.0,
    "Tea Powder (250 g)": 120.0,
    "Biscuits": 30.0,
}
DISCOUNT_LIMIT = 1000.0   # discount applies when subtotal exceeds this
DISCOUNT_RATE = 0.10      # 10% discount
GST_RATE = 0.05           # 5% GST
BILL_FOLDER = "saved_bills"


class SupermarketBillApp:
    """Main application window."""

    def __init__(self, root):
        self.root = root
        self.root.title("Supermarket Bill Generation System")
        self.root.geometry("1050x640")

        self.cart = []            # list of dicts: name, qty, price
        self.current_bill = None  # (bill_number, bill_text) once generated

        self.build_customer_frame()
        self.build_product_frame()
        self.build_cart_frame()
        self.build_totals_frame()
        self.build_bill_frame()

    # -------------------- UI BUILDING --------------------

    def build_customer_frame(self):
        frame = ttk.LabelFrame(self.root, text="Customer Details")
        frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        ttk.Label(frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.name_var, width=22).grid(row=0, column=1)

        ttk.Label(frame, text="Mobile:").grid(row=0, column=2, padx=5)
        self.mobile_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.mobile_var, width=15).grid(row=0, column=3, padx=(0, 5))

    def build_product_frame(self):
        frame = ttk.LabelFrame(self.root, text="Add Product")
        frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # Editable combobox: pick a product or type a new one
        ttk.Label(frame, text="Product:").grid(row=0, column=0, padx=5, pady=5)
        self.product_var = tk.StringVar()
        self.product_box = ttk.Combobox(
            frame, textvariable=self.product_var,
            values=list(PRODUCTS.keys()), width=22
        )
        self.product_box.grid(row=0, column=1)
        self.product_box.bind("<<ComboboxSelected>>", self.on_product_select)

        ttk.Label(frame, text="Price:").grid(row=0, column=2, padx=5)
        self.price_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.price_var, width=8).grid(row=0, column=3)

        ttk.Label(frame, text="Qty:").grid(row=0, column=4, padx=5)
        self.qty_var = tk.StringVar(value="1")
        ttk.Entry(frame, textvariable=self.qty_var, width=5).grid(row=0, column=5)

        ttk.Button(frame, text="Add to Cart", command=self.add_to_cart).grid(
            row=0, column=6, padx=10)

    def build_cart_frame(self):
        frame = ttk.LabelFrame(self.root, text="Shopping Cart")
        frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        columns = ("product", "qty", "price", "total")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
        for col, title, width in [
            ("product", "Product", 190), ("qty", "Qty", 50),
            ("price", "Unit Price", 80), ("total", "Total", 90),
        ]:
            self.tree.heading(col, text=title)
            self.tree.column(col, width=width, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        scroll = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")

    def build_totals_frame(self):
        frame = ttk.LabelFrame(self.root, text="Bill Summary")
        frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.subtotal_lbl = ttk.Label(frame, text="Subtotal: 0.00")
        self.discount_lbl = ttk.Label(frame, text="Discount: 0.00")
        self.tax_lbl = ttk.Label(frame, text="GST: 0.00")
        self.final_lbl = ttk.Label(frame, text="Payable: 0.00", font=("Arial", 11, "bold"))
        for i, lbl in enumerate(
            [self.subtotal_lbl, self.discount_lbl, self.tax_lbl, self.final_lbl]
        ):
            lbl.grid(row=0, column=i, padx=10, pady=5)

        buttons = ttk.Frame(self.root)
        buttons.grid(row=4, column=0, padx=10, pady=5, sticky="ew")
        for text, cmd in [
            ("Remove Selected", self.remove_selected),
            ("Generate Bill", self.generate_bill),
            ("Save Bill", self.save_bill),
            ("Open Previous Bill", self.open_bill),
            ("Clear All", self.clear_all),
        ]:
            ttk.Button(buttons, text=text, command=cmd).pack(side="left", padx=3)

    def build_bill_frame(self):
        frame = ttk.LabelFrame(self.root, text="Bill Preview")
        frame.grid(row=0, column=1, rowspan=5, padx=10, pady=5, sticky="nsew")
        self.bill_text = tk.Text(frame, width=50, font=("Courier", 10), state="disabled")
        self.bill_text.pack(fill="both", expand=True, padx=5, pady=5)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)

    # -------------------- PRODUCT / CART ACTIONS --------------------

    def on_product_select(self, event=None):
        """Show the product's price automatically."""
        price = PRODUCTS.get(self.product_var.get())
        if price is not None:
            self.price_var.set(f"{price:.2f}")

    def add_to_cart(self):
        name = self.product_var.get().strip()
        if not name:
            messagebox.showerror("Invalid Input", "Please enter or select a product.")
            return
        try:
            qty = int(self.qty_var.get())
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Quantity must be a whole number greater than 0.")
            return
        try:
            price = float(self.price_var.get())
            if price <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Price must be a number greater than 0.")
            return

        # If the same product at the same price exists, just increase quantity
        for item in self.cart:
            if item["name"] == name and item["price"] == price:
                item["qty"] += qty
                break
        else:
            self.cart.append({"name": name, "qty": qty, "price": price})

        self.product_var.set("")
        self.price_var.set("")
        self.qty_var.set("1")
        self.refresh_cart()

    def remove_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a product to remove.")
            return
        index = self.tree.index(selected[0])
        del self.cart[index]
        self.refresh_cart()

    def refresh_cart(self):
        """Redraw the Treeview and recalculate the totals."""
        self.tree.delete(*self.tree.get_children())
        for item in self.cart:
            total = item["qty"] * item["price"]
            self.tree.insert("", "end", values=(
                item["name"], item["qty"], f"{item['price']:.2f}", f"{total:.2f}"))

        subtotal, discount, tax, final = self.calculate_totals()
        self.subtotal_lbl.config(text=f"Subtotal: {subtotal:.2f}")
        self.discount_lbl.config(text=f"Discount: {discount:.2f}")
        self.tax_lbl.config(text=f"GST: {tax:.2f}")
        self.final_lbl.config(text=f"Payable: {final:.2f}")
        self.current_bill = None  # cart changed, so the old bill is outdated

    def calculate_totals(self):
        subtotal = sum(i["qty"] * i["price"] for i in self.cart)
        discount = subtotal * DISCOUNT_RATE if subtotal > DISCOUNT_LIMIT else 0.0
        tax = (subtotal - discount) * GST_RATE
        return subtotal, discount, tax, subtotal - discount + tax

    # -------------------- BILL GENERATION --------------------

    def generate_bill(self):
        name = self.name_var.get().strip()
        mobile = self.mobile_var.get().strip()
        if not name or not all(c.isalpha() or c.isspace() for c in name):
            messagebox.showerror("Invalid Input", "Enter a valid customer name (letters only).")
            return
        if not (mobile.isdigit() and len(mobile) == 10):
            messagebox.showerror("Invalid Input", "Mobile number must be exactly 10 digits.")
            return
        if not self.cart:
            messagebox.showerror("Empty Cart", "Add at least one product to the cart.")
            return

        now = datetime.now()
        bill_number = "SM" + now.strftime("%Y%m%d%H%M%S")  # unique per second
        subtotal, discount, tax, final = self.calculate_totals()

        line = "=" * 48
        lines = [
            line, "        SUPERMARKET BILL", line,
            f"Bill No : {bill_number}",
            f"Date    : {now.strftime('%d-%m-%Y %H:%M:%S')}",
            f"Customer: {name}",
            f"Mobile  : {mobile}",
            "-" * 48,
            f"{'Product':<22}{'Qty':>4}{'Price':>10}{'Total':>12}",
            "-" * 48,
        ]
        for item in self.cart:
            total = item["qty"] * item["price"]
            lines.append(
                f"{item['name'][:21]:<22}{item['qty']:>4}{item['price']:>10.2f}{total:>12.2f}")
        lines += [
            "-" * 48,
            f"{'Subtotal':<36}{subtotal:>12.2f}",
            f"{'Discount':<36}{-discount:>12.2f}",
            f"{'GST (' + str(int(GST_RATE * 100)) + '%)':<36}{tax:>12.2f}",
            line,
            f"{'PAYABLE AMOUNT':<36}{final:>12.2f}",
            line, "     Thank you! Visit again.",
        ]
        text = "\n".join(lines)
        self.show_bill(text)
        self.current_bill = (bill_number, text)

    def show_bill(self, text):
        self.bill_text.config(state="normal")
        self.bill_text.delete("1.0", "end")
        self.bill_text.insert("end", text)
        self.bill_text.config(state="disabled")

    # -------------------- SAVE / OPEN / CLEAR --------------------

    def save_bill(self):
        if self.current_bill is None:
            messagebox.showwarning("No Bill", "Generate the bill before saving.")
            return
        bill_number, text = self.current_bill
        os.makedirs(BILL_FOLDER, exist_ok=True)
        path = os.path.join(BILL_FOLDER, f"{bill_number}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        messagebox.showinfo("Saved", f"Bill saved to:\n{path}")

    def open_bill(self):
        os.makedirs(BILL_FOLDER, exist_ok=True)
        path = filedialog.askopenfilename(
            initialdir=BILL_FOLDER, title="Open Saved Bill",
            filetypes=[("Text files", "*.txt")])
        if path:
            with open(path, encoding="utf-8") as f:
                self.show_bill(f.read())

    def clear_all(self):
        self.cart.clear()
        self.name_var.set("")
        self.mobile_var.set("")
        self.refresh_cart()
        self.show_bill("")


if __name__ == "__main__":
    root = tk.Tk()
    SupermarketBillApp(root)
    root.mainloop()
