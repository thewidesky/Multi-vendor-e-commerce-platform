import tkinter as tk

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
        
        #登录不同角色界面逻辑(目前只有供应商)
        def login():
            if (True):
                self.controller.change_size_title('800x600','供应商管理界面',)
                # 跳转至供应商管理系统界面
                self.controller.show_frame("VendorManagementFrame")
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

# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Supplier Management System")
    
#     # 设置窗口初始尺寸
#     root.geometry("500x500")
    
#     # 创建登录界面实例
#     login_frame = LoginFrame(root)
#     login_frame.pack(expand=True, fill="both", padx=20, pady=10)
    
#     root.mainloop()