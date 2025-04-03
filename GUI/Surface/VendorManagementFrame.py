import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
import os

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from models.Product import Product

class VendorManagementFrame(tk.Frame):
    def __init__(self, parent,controller):
        super().__init__(parent)
        self.controller = controller
        self.init_ui()

    def init_ui(self):

        # 存储vendor_id的变量
        self.vendor_id = 0

        # 创建搜索区域（顶部）
        search_frame = ttk.Frame(self)
        search_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky='ew')

        # 搜索输入框
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        # self.search_entry.insert(0, 'Use the Product name to search.')
        self.search_entry.grid(row=0, column=0, padx=5)

        # 搜索按钮
        def search_product():
            """通过商品名搜索商品"""
            product_name = self.search_entry.get()
            product_name = product_name.strip()
            test_data = [
            (1, '笔记本电脑', 5999.00, 50, '在售'),
            (2, '智能手机', 3999.00, 100, '在售'),
        ]
            if product_name != "":
                print(product_name)
                self.reload_product_data(test_data)
            else:
                messagebox.showwarning(title="No product Name", message="You need to input a product name before pressing button")
                
        self.search_button = ttk.Button(search_frame, text='Search Product Name', command=search_product)
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

        def go_to_add():
            """跳转到添加商品界面"""
            self.controller.change_size_title('800x600','添加产品')
            self.controller.show_frame("AddProductFrame")

        # def delete_product():
        #     """删除商品"""
        #     if self.get_current_product():
        #         print(self.get_current_product())
        #     else:
        #         messagebox.showwarning(title="选取错误", message="必须先选中一个商品！")

        def go_to_change():
            """跳转至修改商品界面"""
            if self.get_current_product():
                self.controller.change_size_title('800x600','修改产品')
                self.controller.show_frame("ChangeProductFrame")
                self.controller.frames["ChangeProductFrame"].receive_product_values(self.get_current_product())
            else:
                messagebox.showwarning(title="选取错误", message="必须先选中一个商品！")
        # 删除按钮
        # self.delete_button = ttk.Button(button_frame, text='Delete', command=delete_product)
        # self.delete_button.pack(side=tk.LEFT, padx=5)

        #添加按钮
        self.add_button = ttk.Button(button_frame, text='添加商品', command=go_to_add)
        self.add_button.pack(side=tk.LEFT, padx=5)

        #修改按钮
        self.change_button = ttk.Button(button_frame, text='修改商品', command=go_to_change)
        self.change_button.pack(side=tk.LEFT, padx=5)

        #返回登录界面方法
        def back_to_login():
            self.controller.change_size_title('500x500','登录界面')
            # 跳转至登录界面
            self.controller.show_frame("LoginFrame")
            # 重置登录界面
            self.controller.reset_login()
        # 返回登录按钮
        self.back_button = ttk.Button(button_frame, text='返回登录', command=back_to_login)
        self.back_button.pack(side=tk.LEFT, padx=5)

        # 配置网格权重，使产品列表区域可以自适应扩展
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # 将主框架放置到窗口中
        self.grid(row=0, column=0, sticky='nsew')

        test_data = [
            (1, '笔记本电脑', 5999.00, 50, '在售'),
            (2, '智能手机', 3999.00, 100, '在售'),
            (3, '无线耳机', 999.00, 200, '在售'),
            (4, '平板电脑', 4999.00, 30, '缺货'),
            (5, '智能手表', 1999.00, 80, '在售')
        ]

        # 添加测试数据
        self.reload_product_data(test_data)

    def reload_product_data(self, product_data):
        """重新加载商品信息"""
        # 如果Treeview不为空，则删除Treeview中所有item
        if len(self.product_tree.get_children()) != 0:
            self.product_tree.delete(*self.product_tree.get_children())
        # Treeview重新插入product_data中的item
        for item in product_data:
            self.product_tree.insert('', 'end', values=item)


    def get_current_product(self):
        """获取当前商品信息"""
        # 如果当前Treeview选取不为空，则返回当前product的信息，否则返回None
        if self.product_tree.focus() != "":    
            current_product_values = self.product_tree.item(self.product_tree.focus())['values']
            print(current_product_values)
            return current_product_values
        else:
            return None
        
    def receive_vendor_data(self, data):
        """获取vendor相关信息(id)"""
        self.vendor_id = data[0]
