import tkinter as tk
from tkinter import ttk
from tkinter import StringVar

class ChangeProductFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        # 创建并配置输入框和标签
        entries = [
            ('Vendor_id', ''),
            ('Category_id', ''),
            ('Product_name', ''),
            ('Product_Price', ''),
            ('Product_Stock', '')
            # ('Product_Status', '')
        ]

        # 使用字典存储Entry组件
        self.entries = {}

        # 创建并布局所有输入框
        for i, (label, placeholder) in enumerate(entries):
            # 创建标签
            tk.Label(self, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='e')
            
            # 创建Entry组件
            entry = ttk.Entry(self, width=30)
            entry.insert(0, placeholder)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky='w')
            
            # 存储Entry组件的引用
            self.entries[label] = entry

            # 绑定焦点事件
            # entry.bind('<FocusIn>', lambda e, entry=entry, placeholder=placeholder: 
            #           self.on_entry_click(e, entry, placeholder))
            # entry.bind('<FocusOut>', lambda e, entry=entry, placeholder=placeholder: 
            #           self.on_focus_out(e, entry, placeholder))

        Options = [
            '在售',
            '缺货'
        ]

        variables = StringVar(self)
        variables.set(Options[0])

        self.product_status_label = ttk.Label(self,text="Product_status")
        self.product_status_label.grid(row=len(self.entries), column=1, padx=10, pady=5, sticky='w')
        self.product_status_dropdown = ttk.OptionMenu(self,variables,*Options)
        self.product_status_dropdown.grid(row=len(self.entries), column=2, padx=10, pady=5, sticky='w')

        # 创建确认按钮
        self.sure_change_button = ttk.Button(self, text='Sure Change the Product information.')
        self.sure_change_button.grid(row=len(entries), column=0, columnspan=2, pady=20)

        def back_to_vendor():
            self.controller.title('供应商管理界面')
            self.controller.geometry('800x600')
            # 跳转至供应商管理系统界面
            self.controller.show_frame("VendorManagementFrame")
        # 创建返回按钮
        self.back_btn = ttk.Button(self, text='Back', command=back_to_vendor)
        self.back_btn.grid(row=len(entries)+1, column=0, columnspan=2, pady=20)

        # 配置网格权重
        self.grid_columnconfigure(1, weight=1)

        # 将主框架放置到窗口中
        self.grid(sticky='nsew')

    def receive_product_values(self, values):
        print(values)
        # length = min(len(self.entries), len(values))
        # print(length)
        print(list(self.entries))
        # for (i, label) in list(enumerate(self.entries)):
        #     if (i < length):
        #         print("Label :" + str(label) + ", " + "Values: " + str(values[i]))
        #         self.entries[label].delete(0,'end')
        #         self.entries[label].insert(0,values[i])
        #     else:
        #         self.entries[label].delete(0,'end')
        self.entries['Vendor_id'].delete(0,'end')
        self.entries['Vendor_id'].insert(0,values[0])
        self.entries['Product_name'].delete(0,'end')
        self.entries['Product_name'].insert(0,values[1])
        self.entries['Product_Price'].delete(0,'end')
        self.entries['Product_Price'].insert(0,values[2])
        self.entries['Product_Stock'].delete(0,'end')
        self.entries['Product_Stock'].insert(0,values[3])
        self.entries['Product_Status'].delete(0,'end')
        self.entries['Product_Status'].insert(0,values[4])
            
   

