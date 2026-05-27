import os
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from openpyxl import Workbook, load_workbook

class BaruaBookStorePOS(App):
    def build(self):
        self.cart = []
        self.storage = "/storage/emulated/0/Download" if os.path.exists("/storage/emulated/0/Download") else os.getcwd()
        
        root = ScrollView()
        main = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10), size_hint_y=None)
        main.bind(minimum_height=main.setter('height'))
        
        main.add_widget(Label(text="BARUA BOOK STORE", font_size='22sp', bold=True, color=(0.2, 0.6, 1, 1), size_hint_y=None, height=dp(50)))
        
        self.inputs = {}
        for hint in ["Customer Name", "Phone No", "Address", "Book/Item Name", "Price", "Qty", "Discount"]:
            ti = TextInput(hint_text=hint, size_hint_y=None, height=dp(45), multiline=False)
            self.inputs[hint] = ti
            main.add_widget(ti)
        
        btn_add = Button(text="➕ ADD ITEM TO CART", size_hint_y=None, height=dp(50), background_color=(0, 0.6, 0.2, 1))
        btn_add.bind(on_press=self.add_to_cart)
        main.add_widget(btn_add)
        
        main.add_widget(Label(text="--- LIVE CART ---", size_hint_y=None, height=dp(30)))
        self.cart_view = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5))
        self.cart_view.bind(minimum_height=self.cart_view.setter('height'))
        main.add_widget(self.cart_view)
        
        btn_gen = Button(text="🖨️ GENERATE A4 PROFESSIONAL PDF", size_hint_y=None, height=dp(60), background_color=(0.1, 0.4, 0.8, 1), bold=True)
        btn_gen.bind(on_press=self.generate_a4_bill)
        main.add_widget(btn_gen)
        
        root.add_widget(main)
        return root

    def add_to_cart(self, inst):
        name = self.inputs["Book/Item Name"].text
        price = self.inputs["Price"].text
        qty = self.inputs["Qty"].text or "1"
        if name and price:
            total = (float(price) * int(qty)) - float(self.inputs["Discount"].text or 0)
            item_data = {'item': name, 'qty': qty, 'total': total}
            self.cart.append(item_data)
            self.cart_view.add_widget(Label(text=f"{name} x{qty} = Rs.{total}", size_hint_y=None, height=dp(30)))
            self.inputs["Book/Item Name"].text = ""; self.inputs["Price"].text = ""; self.inputs["Qty"].text = ""; self.inputs["Discount"].text = ""

    def generate_a4_bill(self, inst):
        if not self.cart: return
        file_id = datetime.now().strftime("%Y%m%d%H%M%S")
        full_path = os.path.join(self.storage, f"A4_Invoice_{file_id}.pdf")
        
        c = canvas.Canvas(full_path, pagesize=letter)
        w, h = letter
        
        # Header
        c.setFillColorRGB(0.1, 0.2, 0.4)
        c.rect(0, h-120, w, 120, fill=1, stroke=0)
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 30)
        c.drawString(50, h-60, "BARUA BOOK STORE")
        c.setFont("Helvetica", 12)
        c.drawString(50, h-90, "Birpara, Near Harimandir, High School Road | Ph: 8509288951")
        
        # Bill To
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, h-160, "BILL TO:")
        c.setFont("Helvetica", 12)
        c.drawString(50, h-180, f"Customer: {self.inputs['Customer Name'].text}")
        c.drawString(50, h-200, f"Contact: {self.inputs['Phone No'].text}")
        c.drawString(50, h-220, f"Address: {self.inputs['Address'].text}")
        
        # Table Header
        c.setFillColorRGB(0.9, 0.9, 0.9)
        c.rect(50, h-270, 500, 30, fill=1, stroke=0)
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(60, h-262, "ITEM DESCRIPTION")
        c.drawString(300, h-262, "QTY")
        c.drawString(450, h-262, "AMOUNT (Rs.)")
        
        y = h - 300
        grand_total = 0
        for i in self.cart:
            c.setFont("Helvetica", 12)
            c.drawString(60, y, i['item'])
            c.drawString(300, y, str(i['qty']))
            c.drawRightString(520, y, f"{i['total']:.2f}")
            grand_total += i['total']
            y -= 30
            c.line(50, y+20, 550, y+20)
            
        # Total Box
        c.setFillColorRGB(0.1, 0.2, 0.4)
        c.rect(350, y-30, 200, 40, fill=1, stroke=0)
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(360, y-20, f"TOTAL: Rs. {grand_total:.2f}")
        
        c.save()
        self.cart = []
        self.cart_view.clear_widgets()
        for i in self.inputs: self.inputs[i].text = ""

if __name__ == "__main__":
    BaruaBookStorePOS().run()
