import tkinter as tk
from tkinter import messagebox
from services.Services import check_user_type,get_data_by_user

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
        self.configure_layout()


    def create_widgets(self):
        # 创建界面组件
        self.app_label = tk.Label(self, text="Multi-vendor-e-commerce-platform")
        self.username_label = tk.Label(self, text="UserName")
        self.username_entry = tk.Entry(self)
        
        self.password_label = tk.Label(self, text="Password")
        self.password_entry = tk.Entry(self, show="*")
        # 切换密码的显示和隐藏
        def toggle_password():
            if self.password_entry.cget('show') == "":
                self.password_entry.config(show = "*")
                self.change_psd_button.config(text = "Show")
            else: 
                self.password_entry.config(show = "")
                self.change_psd_button.config(text = "Hide")
        self.change_psd_button = tk.Button(self, text="Show", command= toggle_password)
        
        #登录不同角色界面逻辑(目前只能写死)
        def login():
            username = self.username_entry.get()
            username = username.strip()
            password = self.password_entry.get()
            password = password.strip()
            # 判断当前username和password，不能为空
            if len(username) == 0 or len(password) == 0:
                messagebox.showwarning(title="用户名密码为空",message="用户名或者密码不能为空")
            else:
                (type,id) = (check_user_type(username=username, password=password))
                if type == "Vendor":
                # 跳转至供应商管理系统界面的情况
                    product_data = get_data_by_user(username=username,password=password)
                    # print(product_data)
                    self.controller.change_size_title('800x600','供应商管理界面',)
                    self.controller.show_frame("VendorManagementFrame")
                    # VendorManagementFrame调用reload_product_data方法重新载入数据
                    self.controller.frames["VendorManagementFrame"].reload_product_data(product_data)
                    # 用一个List存储需要发送到其他界面的数据
                    send_data = list()
                    # 存储当前的用户id
                    send_data.append(id)
                    # VendorManagementFrame调用receive_vendor_data方法获取vendor_id等数据
                    self.controller.frames["VendorManagementFrame"].receive_vendor_data(send_data)
                elif type == "Manager":
                # 跳转至管理系统界面的情况
                    vendor_data = get_data_by_user(username=username,password=password)
                    self.controller.change_size_title('800x600','管理系统界面',)
                    self.controller.show_frame("AdministratorFrame")
                    self.controller.frames["AdministratorFrame"].reload_vendor_data(vendor_data)
                    send_data = list()
                    send_data.append(id)
                    self.controller.frames["AdministratorFrame"].receive_manager_data(send_data)
                elif type == "Customer":
                # 跳转至用户界面的情况
                    product_data = get_data_by_user(username=username,password=password)
                    self.controller.change_size_title('800x600','用户界面',)
                    self.controller.show_frame("UserFrame")
                    self.controller.frames['UserFrame'].reload_product(product_data)
                    send_data = list()
                    send_data.append(id)
                    self.controller.frames["UserFrame"].receive_user_data(send_data)
                elif type == "Password Error":
                # 密码验证错误的情况
                    messagebox.showwarning(title="密码错误",message="密码验证失败,请重新输入")


        self.login_button = tk.Button(self, text="Login",command = login)

    def configure_layout(self):
        # 配置网格布局
        self.grid_columnconfigure(1, weight=1)
        
        # 第一行：应用标题
        self.app_label.grid(row=0, column=0, columnspan=3, pady=20)
        
        # 第二行：用户名组件
        self.username_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.username_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # 第三行：密码组件
        self.password_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.change_psd_button.grid(row=2, column=2, padx=5, pady=5)
        
        # 第四行：登录按钮
        self.login_button.grid(row=3, column=0, columnspan=3, pady=15, ipadx=20)

