import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class AdministratorFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.init_ui()

    def init_ui(self):
         
        def back_to_login():
            """返回登录界面"""
            self.controller.change_size_title('500x500','登录界面',)
            self.controller.show_frame("LoginFrame")
        # 创建返回按钮
        self.back_button = tk.Button(self, text="Back to Login", command=back_to_login)
        self.back_button.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        # 创建供应商信息显示区域（带滚动条的Treeview）
        # 创建一个Frame来容纳Treeview和滚动条
        self.vendor_frame = tk.Frame(self)
        self.vendor_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky='nsew')

        # 创建Treeview
        self.vendor_list = ttk.Treeview(self.vendor_frame, columns=('ID', 'Business Name', 'Location'), show='headings')
        self.vendor_list.heading('ID', text='ID')
        self.vendor_list.heading('Business Name', text='Business Name')
        self.vendor_list.heading('Location', text='Location')

        # 设置列宽
        self.vendor_list.column('ID', width=50)
        self.vendor_list.column('Business Name', width=200)
        self.vendor_list.column('Location', width=150)

        # 创建滚动条
        self.scrollbar = ttk.Scrollbar(self.vendor_frame, orient='vertical', command=self.vendor_list.yview)
        self.vendor_list.configure(yscrollcommand=self.scrollbar.set)

        # 放置Treeview和滚动条
        self.vendor_list.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='right', fill='y')

        # 创建按钮框架
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # 创建管理按钮
        def go_to_add():
            """前往添加商户界面"""
            self.controller.change_size_title('800x600','添加商户界面',)
            self.controller.show_frame("AddVendorFrame")
        
        def delete_vendor():
            """删除商户"""
            print("delete vendor")
            self.get_current_vendor()

        def go_to_change():
            """前往修改用户界面"""
            if self.vendor_list.focus() != "":
                self.controller.change_size_title('800x600','修改商户界面',)
                self.controller.show_frame("ChangeVendorFrame")
                self.controller.frames["ChangeVendorFrame"].receive_vendor_value(self.get_current_vendor())
            else:
                messagebox.showwarning(title="Empty Vendor Selection", message="You need to select a vendor before pressing the button!")
            

        self.add_button = tk.Button(self.button_frame, text="Add Vendor",command=go_to_add)
        self.delete_button = tk.Button(self.button_frame, text="Delete Vendor", command=delete_vendor)
        self.change_button = tk.Button(self.button_frame, text="Change Vendor Information", command=go_to_change)

        # 放置按钮
        self.add_button.pack(side='left', padx=5)
        self.delete_button.pack(side='left', padx=5)
        self.change_button.pack(side='left', padx=5)

        # 配置网格权重
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        test_data = [
            (1, "ABC Electronics", "Hong Kong"),
            (2, "XYZ Trading", "Shanghai"),
            (3, "Global Imports", "Beijing"),
            (4, "Tech Solutions", "Shenzhen"),
            (5, "Best Supplies", "Guangzhou")
        ]

        self.reload_vendor_data(test_data)


    def reload_vendor_data(self, vendor_data):
        """重新载入商户信息"""
        if len(self.vendor_list.get_children()) != 0:
            self.vendor_list.delete(*self.vendor_list.get_children())
        for item in vendor_data:
            self.vendor_list.insert('', 'end', values=item)
    
    def get_current_vendor(self):
        """获取当前商户信息"""
        if self.vendor_list.focus() != "":    
            current_vendor_values = self.vendor_list.item(self.vendor_list.focus())['values']
            print(current_vendor_values)
            return current_vendor_values
        else:
            return None

