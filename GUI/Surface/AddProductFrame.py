import tkinter as tk
from tkinter import ttk
import sys
import os

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.Product import Product

class AddProductFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.init_ui()

    def init_ui(self):

        # 创建并配置输入框和标签
        entries = [
            ('Vendor_id', 'Please write your Vendor_id.'),
            ('Category_id', 'Please write your Category_id.'),
            ('Product_name', 'Please write your Product_name.'),
            ('Product_Price', 'Please write your Product_price.'),
            ('Product_Stock', 'Please write your Product_stock.'),
            ('Product_Status', 'Please write your Product_status (allow null).'),
            ('Product_Picture', 'Please write your Product_picture (allow null).')
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
            entry.bind('<FocusIn>', lambda e, entry=entry, placeholder=placeholder: 
                      self.on_entry_click(e, entry, placeholder))
            entry.bind('<FocusOut>', lambda e, entry=entry, placeholder=placeholder: 
                      self.on_focus_out(e, entry, placeholder))

        # 创建确认按钮
        self.sure_add_button = ttk.Button(self, text='Sure add the Product.')
        self.sure_add_button.grid(row=len(entries), column=0, columnspan=2, pady=20)

        def back_to_vendor():
            # self.controller.title('供应商管理界面')
            # self.controller.geometry('800x600')
            self.controller.change_size_title('800x600','供应商管理界面')
            # 跳转至供应商管理系统界面
            self.controller.show_frame("VendorManagementFrame")
        # 创建返回按钮
        self.back_btn = ttk.Button(self, text='Back', command=back_to_vendor)
        self.back_btn.grid(row=len(entries)+1, column=0, columnspan=2, pady=20)

        # 配置网格权重
        self.grid_columnconfigure(1, weight=1)

        # 将主框架放置到窗口中
        # self.grid(padx=20, pady=20, sticky='nsew')
        self.grid(sticky='nsew')

    def on_entry_click(self, event, entry, placeholder):
        """当输入框获得焦点时，如果显示的是占位符则清空"""
        if entry.get() == placeholder:
            entry.delete(0, 'end')
            entry.configure(foreground='black')

    def on_focus_out(self, event, entry, placeholder):
        """当输入框失去焦点时，如果为空则显示占位符"""
        if entry.get() == '':
            entry.insert(0, placeholder)
            entry.configure(foreground='gray')

# 测试代码
# if __name__ == '__main__':
#     root = tk.Tk()
#     app = AddProductFrame(root)
#     root.mainloop()