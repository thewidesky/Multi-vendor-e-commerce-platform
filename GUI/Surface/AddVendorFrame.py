import tkinter as tk
# from models.Vendor import Vendor

class AddVendorFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.init_components()
        self.layout_components()

    def init_components(self):
        # 创建并配置所有输入框和按钮
        self.vendor_id_entry = tk.Entry(self)
        self.vendor_id_entry.insert(0, "Please write your Vendor_id.")
        self.vendor_id_entry.bind('<FocusIn>', lambda e: self.on_entry_click(e, self.vendor_id_entry))
        self.vendor_id_entry.bind('<FocusOut>', lambda e: self.on_focus_out(e, self.vendor_id_entry, "Please write your Vendor_id."))
        self.vendor_id_entry.config(fg='grey')

        self.business_name_entry = tk.Entry(self)
        self.business_name_entry.insert(0, "Please write your Business name.")
        self.business_name_entry.bind('<FocusIn>', lambda e: self.on_entry_click(e, self.business_name_entry))
        self.business_name_entry.bind('<FocusOut>', lambda e: self.on_focus_out(e, self.business_name_entry, "Please write your Business name."))
        self.business_name_entry.config(fg='grey')

        self.geo_presence_entry = tk.Entry(self)
        self.geo_presence_entry.insert(0, "Please write your Location.")
        self.geo_presence_entry.bind('<FocusIn>', lambda e: self.on_entry_click(e, self.geo_presence_entry))
        self.geo_presence_entry.bind('<FocusOut>', lambda e: self.on_focus_out(e, self.geo_presence_entry, "Please write your Location."))
        self.geo_presence_entry.config(fg='grey')

        self.vendor_account_entry = tk.Entry(self)
        self.vendor_account_entry.insert(0, "Please write your Account.")
        self.vendor_account_entry.bind('<FocusIn>', lambda e: self.on_entry_click(e, self.vendor_account_entry))
        self.vendor_account_entry.bind('<FocusOut>', lambda e: self.on_focus_out(e, self.vendor_account_entry, "Please write your Account."))
        self.vendor_account_entry.config(fg='grey')

        self.vendor_secret_entry = tk.Entry(self)
        self.vendor_secret_entry.insert(0, "Please write your Secret.")
        self.vendor_secret_entry.bind('<FocusIn>', lambda e: self.on_entry_click(e, self.vendor_secret_entry))
        self.vendor_secret_entry.bind('<FocusOut>', lambda e: self.on_focus_out(e, self.vendor_secret_entry, "Please write your Secret."))
        self.vendor_secret_entry.config(fg='grey')

        def back_to_admin():
            """返回管理系统界面"""
            self.controller.change_size_title('800x600','管理系统界面',)
            self.controller.show_frame("AdministratorFrame")

        def confirm_add():
            """确认添加，返回管理系统界面"""
            #TO DO
            #添加逻辑

        self.sure_added_button = tk.Button(self, text="Confirmed Added the Vendor information", command=confirm_add)
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

        self.sure_added_button.grid(row=5, column=0, columnspan=2, pady=20)

        self.back_to_admin_button.grid(row=6, column=0, columnspan=2, pady=20)

        # 配置列权重使得输入框可以水平拉伸
        self.grid_columnconfigure(1, weight=1)

    def on_entry_click(self, event, entry):
        if entry.get() in ["Please write your Vendor_id.", 
                          "Please write your Business name.",
                          "Please write your Location.",
                          "Please write your Account.",
                          "Please write your Secret."]:
            entry.delete(0, tk.END)
            entry.config(fg='black')

    def on_focus_out(self, event, entry, default_text):
        if entry.get() == '':
            entry.insert(0, default_text)
            entry.config(fg='grey')

