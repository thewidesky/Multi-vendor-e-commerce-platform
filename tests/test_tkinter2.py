import tkinter as tk
from tkinter import ttk
import sys
import os

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.Product import Product

class VendorManagementFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.init_ui()

    def init_ui(self):
        # 配置主窗口
        self.master.title('供应商管理系统')
        self.master.geometry('800x600')

        # 创建搜索区域（顶部）
        search_frame = ttk.Frame(self)
        search_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky='ew')

        # 搜索输入框
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        self.search_entry.insert(0, 'Use the Product name to search.')
        self.search_entry.grid(row=0, column=0, padx=5)

        # 搜索按钮
        self.search_button = ttk.Button(search_frame, text='Search')
        self.search_button.grid(row=0, column=1, padx=5)

        # 创建产品列表区域（中间）
        # 使用Treeview替代Listbox，提供更好的表格式显示
        self.product_tree = ttk.Treeview(self, columns=('ID', 'Name', 'Price', 'Stock', 'Status'), show='headings')
        
        # 设置列标题
        self.product_tree.heading('ID', text='产品ID')
        self.product_tree.heading('Name', text='产品名称')
        self.product_tree.heading('Price', text='价格')
        self.product_tree.heading('Stock', text='库存')
        self.product_tree.heading('Status', text='状态')

        # 设置列宽度
        self.product_tree.column('ID', width=80)
        self.product_tree.column('Name', width=200)
        self.product_tree.column('Price', width=100)
        self.product_tree.column('Stock', width=100)
        self.product_tree.column('Status', width=100)

        # 添加垂直滚动条
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.product_tree.yview)
        self.product_tree.configure(yscrollcommand=scrollbar.set)

        # 布局产品列表和滚动条
        self.product_tree.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky='nsew')
        scrollbar.grid(row=1, column=2, pady=5, sticky='ns')

        # 创建按钮区域（底部）
        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

        # 添加产品按钮
        self.add_button = ttk.Button(button_frame, text='Add_Product')
        self.add_button.pack(side=tk.LEFT, padx=5)

        # 修改产品按钮
        self.change_button = ttk.Button(button_frame, text='Change Product information')
        self.change_button.pack(side=tk.LEFT, padx=5)

        # 删除按钮
        self.delete_button = ttk.Button(button_frame, text='Delete')
        self.delete_button.pack(side=tk.LEFT, padx=5)

        # 返回登录按钮
        self.back_button = ttk.Button(button_frame, text='Back to Login')
        self.back_button.pack(side=tk.LEFT, padx=5)

        # 配置网格权重，使产品列表区域可以自适应扩展
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # 将主框架放置到窗口中
        self.grid(row=0, column=0, sticky='nsew')

        # 添加测试数据
        self.add_test_data()

    def add_test_data(self):
        # 添加一些测试数据到产品列表
        test_data = [
            (1, '笔记本电脑', 5999.00, 50, '在售'),
            (2, '智能手机', 3999.00, 100, '在售'),
            (3, '无线耳机', 999.00, 200, '在售'),
            (4, '平板电脑', 4999.00, 30, '缺货'),
            (5, '智能手表', 1999.00, 80, '在售')
        ]
        
        for item in test_data:
            self.product_tree.insert('', 'end', values=item)

# 测试代码
if __name__ == '__main__':
    root = tk.Tk()
    app = VendorManagementFrame(root)
    root.mainloop()