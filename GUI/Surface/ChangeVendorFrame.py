import tkinter as tk
# from models.Vendor import Vendor

class ChangeVendorFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.init_components()
        self.layout_components()

    def init_components(self):
        # 创建并配置所有输入框和按钮
        self.vendor_id_entry = tk.Entry(self)

        self.business_name_entry = tk.Entry(self)

        self.geo_presence_entry = tk.Entry(self)

        self.vendor_account_entry = tk.Entry(self)

        self.vendor_secret_entry = tk.Entry(self)

        def back_to_admin():
            """返回管理系统界面"""
            self.clear_entries()
            self.controller.change_size_title('800x600','管理系统界面',)
            self.controller.show_frame("AdministratorFrame")

        def confirm_add():
            """确认添加，返回管理系统界面"""
            #TO DO
            #添加逻辑
            back_to_admin()
            self.clear_entries()

        self.sure_changed_button = tk.Button(self, text="Confirm Changed the Vendor information.", command=confirm_add)
        self.back_to_admin_button = tk.Button(self, text="Back to Admin", command=back_to_admin)

    def layout_components(self):
        # 使用网格布局排列组件
        self.vendor_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
        tk.Label(self, text="Vendor ID:").grid(row=0, column=0, padx=10, pady=5, sticky='e')

        self.business_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
        tk.Label(self, text="Business Name:").grid(row=1, column=0, padx=10, pady=5, sticky='e')

        self.geo_presence_entry.grid(row=2, column=1, padx=10, pady=5, sticky='ew')
        tk.Label(self, text="Location:").grid(row=2, column=0, padx=10, pady=5, sticky='e')

        self.vendor_account_entry.grid(row=3, column=1, padx=10, pady=5, sticky='ew')
        tk.Label(self, text="Account:").grid(row=3, column=0, padx=10, pady=5, sticky='e')

        self.vendor_secret_entry.grid(row=4, column=1, padx=10, pady=5, sticky='ew')
        tk.Label(self, text="Secret:").grid(row=4, column=0, padx=10, pady=5, sticky='e')

        self.sure_changed_button.grid(row=5, column=0, columnspan=2, pady=20)
        self.back_to_admin_button.grid(row=6, column=0, columnspan=2, pady=20)

        # 配置列权重使得输入框可以水平拉伸
        self.grid_columnconfigure(1, weight=1)
    
    def receive_vendor_value(self, values):
        """接收其他Frame传来的信息"""
        self.vendor_id_entry.insert(0,values[0])
        self.business_name_entry.insert(0,values[0])
        self.geo_presence_entry.insert(0,values[0])

    def clear_entries(self):
        """离开界面时清空所有entry"""
        self.vendor_id_entry.delete(0,'end')
        self.business_name_entry.delete(0,'end')
        self.geo_presence_entry.delete(0,'end')
        self.vendor_account_entry.delete(0,'end')
        self.vendor_secret_entry.delete(0,'end')


