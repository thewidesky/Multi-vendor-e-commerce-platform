import tkinter as tk
from tkinter import font as tkfont
from GUI.Surface.LoginFrame import LoginFrame
from GUI.Surface.VendorManagementFrame import VendorManagementFrame
from GUI.Surface.AddProductFrame import AddProductFrame
from GUI.Surface.AddVendorFrame import AddVendorFrame
from GUI.Surface.AdministratorFrame import AdministratorFrame
from GUI.Surface.ChangeProductFrame import ChangeProductFrame
from GUI.Surface.ChangeVendorFrame import ChangeVendorFrame
from GUI.Surface.RecordFrame import RecordFrame
from GUI.Surface.UserFrame import UserFrame
from services.Services import check_user_type



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
        for F in (LoginFrame, VendorManagementFrame, AddProductFrame,AdministratorFrame,AddVendorFrame,ChangeVendorFrame,UserFrame, RecordFrame,ChangeProductFrame):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        #开始时直接跳转至登录界面
        self.show_frame("LoginFrame")

    
    def show_frame(self, page_name):
        """跳转到界面"""
        frame = self.frames[page_name]
        frame.tkraise()
    
    def reset_login(self):
        """重置登录界面"""
        print('reset_login called')
        self.frames['LoginFrame'].username_entry.delete(0,'end')
        self.frames['LoginFrame'].password_entry.delete(0,'end')

    def change_size_title(self, size, title):
        """调整窗口大小与标题"""
        self.geometry(size)
        self.title(title)



if __name__ == "__main__":
    # 测试用户类型检查功能
    test_cases = [
        ('Alice Johnson', 'secret001'),  # 管理员测试用例
        ('ChicDress Boutique', 'secret12345'),  # 普通用户测试用例
        ('fashion_store', 'vendor456'),  # 供应商测试用例
        ('Manger','secret009'),
        ('Manger','111')
    ]
    for username, password in test_cases:
        user_type = check_user_type(username, password)
        print('用户名: {} -> 用户类型: {}'.format(username, user_type))

    app = MainApplication()
    app.mainloop()