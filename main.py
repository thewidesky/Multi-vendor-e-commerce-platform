import tkinter as tk
from tkinter import font as tkfont
from GUI.Surface.LoginFrame import LoginFrame
from GUI.loginscreen import LoginScreen
from GUI.Surface.VendorManagementFrame import VendorManagementFrame
from GUI.Surface.AddProductFrame import AddProductFrame



class MainApplication(tk.Tk):
    """App的主类(controller),其他frame可以通过self.controller.方法名 调用controller的方法"""
    def __init__(self):
        super().__init__()
        self.title('登录界面')
        self.geometry('500x500')
        
        # 创建容器框架
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # 界面集合
        # 可以从Frame中通过self.controller.frames['frame名字'].控件名 修改其他frame的控件
        self.frames = {}
        for F in (LoginFrame, VendorManagementFrame, AddProductFrame):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        #开始时直接跳转至登录界面
        # 配置主窗口
        
        self.show_frame("LoginFrame")

    
    # 跳转页面
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
    
    # 重置登录界面
    def reset_login(self):
        print('reset_login called')
        self.frames['LoginFrame'].username_entry.delete(0,'end')
        self.frames['LoginFrame'].password_entry.delete(0,'end')

    def change_size_title(self, size, title):
        self.geometry(size)
        self.title(title)


# class LoginFrame(tk.Frame):
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         self.controller = controller
#         self.create_widgets()
        
#     def create_widgets(self):
#         # 界面组件
#         lbl_title = tk.Label(self, text="供应商管理系统登录", font=('微软雅黑', 14))
#         lbl_title.pack(pady=20)
        
#         frm_input = tk.Frame(self)
#         tk.Label(frm_input, text="账号：").grid(row=0, column=0, padx=5, pady=5)
#         self.ent_username = tk.Entry(frm_input)
#         self.ent_username.grid(row=0, column=1, padx=5, pady=5)
        
#         tk.Label(frm_input, text="密码：").grid(row=1, column=0, padx=5, pady=5)
#         self.ent_password = tk.Entry(frm_input, show="*")
#         self.ent_password.grid(row=1, column=1, padx=5, pady=5)
        
#         frm_input.pack(pady=10)
        
#         btn_login = tk.Button(self, text="登录", width=15,
#                              command=lambda: self.controller.show_frame("VendorManagementFrame"))
        # btn_login.pack(pady=15)

# class SupplierFrame(tk.Frame):
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         self.controller = controller
#         self.create_widgets()
        
#     def create_widgets(self):
#         lbl_title = tk.Label(self, text="供应商管理界面", font=('微软雅黑', 14))
#         lbl_title.pack(pady=20)
        
#         # 示例功能按钮
#         tk.Button(self, text="返回登录", width=15,
#                 command=lambda: self.controller.show_frame("LoginFrame")).pack(pady=10)
#         tk.Button(self, text="供应商列表", width=15).pack(pady=5)
#         tk.Button(self, text="添加供应商", width=15).pack(pady=5)
#         tk.Button(self, text="库存管理", width=15).pack(pady=5)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()