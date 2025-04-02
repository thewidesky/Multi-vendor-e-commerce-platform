import tkinter as tk
from tkinter import ttk

class AdministratorFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.init_ui()

    def init_ui(self):
        # 创建返回按钮
        self.back_button = tk.Button(self, text="Back to Login")
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
        self.add_button = tk.Button(self.button_frame, text="Add Vendor")
        self.delete_button = tk.Button(self.button_frame, text="Delete Vendor")
        self.change_button = tk.Button(self.button_frame, text="Change Vendor Information")

        # 放置按钮
        self.add_button.pack(side='left', padx=5)
        self.delete_button.pack(side='left', padx=5)
        self.change_button.pack(side='left', padx=5)

        # 配置网格权重
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # 添加测试数据
        self.insert_test_data()

    def insert_test_data(self):
        # 插入一些测试数据
        test_data = [
            (1, "ABC Electronics", "Hong Kong"),
            (2, "XYZ Trading", "Shanghai"),
            (3, "Global Imports", "Beijing"),
            (4, "Tech Solutions", "Shenzhen"),
            (5, "Best Supplies", "Guangzhou")
        ]
        for item in test_data:
            self.vendor_list.insert('', 'end', values=item)

def main():
    root = tk.Tk()
    root.title("Vendor Management System - Administrator")
    root.geometry("800x600")
    app = AdministratorFrame(root)
    app.pack(fill='both', expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()