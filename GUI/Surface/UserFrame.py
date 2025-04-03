import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
# from models.Product import Product
# from models.ProductTag import ProductTag

class UserFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.init_ui()

    def reload_product(self,product_data):
        """Treeview重新加载商品信息"""
        if len(self.tree.get_children()) != 0:
            self.tree.delete(*self.tree.get_children())
        # 重新从product_data添加数据到tree
        for item in product_data:
            self.tree.insert('', 'end', values=item)


    def init_ui(self):

        #存储user_id的变量
        self.user_id = 0

        # 创建顶部搜索区域
        search_frame = tk.Frame(self)
        search_frame.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky='ew')

        # 搜索输入框和按钮
        self.product_search_entry = ttk.Entry(search_frame)
        self.product_search_entry.insert(0, 'Write Product id there.')
        self.product_search_entry.grid(row=0, column=0, padx=5)

        self.tag_search_entry = ttk.Entry(search_frame)
        self.tag_search_entry.insert(0, 'Write Tag id to there.')
        self.tag_search_entry.grid(row=0, column=2, padx=5)

        def search_product():
            """通过Product名筛选搜索"""
            product_name = self.product_search_entry.get()
            product_name = product_name.strip()
            if len(product_name) != 0:
                print("Product_name: " + product_name)
            else:
                if len(product_name) == 0:
                    messagebox.showwarning(title="PRODUCT NAME ERROR", message="Product Name cannot be EMPTY!")
                else:
                    messagebox.showwarning(title="PRODUCT NAME ERROR", message="The Product Name : " + product_name + " you enter is INVALID")             
                

        def search_tag():
            """通过Tag名筛选搜索"""
            tag_name = self.tag_search_entry.get()
            tag_name = tag_name.strip()
            if len(tag_name) != 0:
                print("Tag_name: " + tag_name)
            else:
                if len(tag_name) == 0:
                    messagebox.showwarning(title="TAG ERROR", message="Tag Name cannot be EMPTY!")
                else:
                    messagebox.showwarning(title="TAG ERROR", message="The Tag: " + tag_name + " you enter is INVALID")
        
        self.search_product_button = ttk.Button(search_frame, text='Search By Product', command=search_product).grid(row=0, column=1, padx=5)
        self.search_tag_button = ttk.Button(search_frame, text='Search By Tag', command=search_tag).grid(row=0, column=3, padx=5)

        # 创建产品列表区域
        list_frame = tk.Frame(self)
        list_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=10)

        # 创建Treeview和Scrollbar
        self.tree = ttk.Treeview(list_frame, columns=('p_id', 'v_id', 'category_id', 'p_name', 'price', 'stock'),
                                show='headings')
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # 设置列标题
        self.tree.heading('p_id', text='Product ID')
        self.tree.heading('v_id', text='Vendor ID')
        self.tree.heading('category_id', text='Category ID')
        self.tree.heading('p_name', text='Product Name')
        self.tree.heading('price', text='Price')
        self.tree.heading('stock', text='Stock')

        # 设置列宽度
        for col in self.tree['columns']:
            self.tree.column(col, width=100)

        # 添加测试数据
        test_data = [
            (1, 1, 1, 'Test Product 1', 99.99, 100),
            (2, 1, 2, 'Test Product 2', 149.99, 50),
            (3, 2, 1, 'Test Product 3', 199.99, 75),
            (1, 1, 1, 'Test Product 1', 99.99, 100),
            (2, 1, 2, 'Test Product 2', 149.99, 50),
            (3, 2, 1, 'Test Product 3', 199.99, 75),
            (1, 1, 1, 'Test Product 1', 99.99, 100),
            (2, 1, 2, 'Test Product 2', 149.99, 50),
            (3, 2, 1, 'Test Product 3', 199.99, 75),
            (1, 1, 1, 'Test Product 1', 99.99, 100),
            (2, 1, 2, 'Test Product 2', 149.99, 50),
            (3, 2, 1, 'Test Product 3', 199.99, 75),
            (1, 1, 1, 'Test Product 1', 99.99, 100),
            (2, 1, 2, 'Test Product 2', 149.99, 50),
            (3, 2, 1, 'Test Product 3', 199.99, 75),
            (1, 1, 1, 'Test Product 1', 99.99, 100),
            (2, 1, 2, 'Test Product 2', 149.99, 50),
            (3, 2, 1, 'Test Product 3', 199.99, 75),
            (1, 1, 1, 'Test Product 1', 99.99, 100),
            (2, 1, 2, 'Test Product 2', 149.99, 50),
            (3, 2, 1, 'Test Product 3', 199.99, 75),
            (1, 1, 1, 'Test Product 1', 99.99, 100),
            (2, 1, 2, 'Test Product 2', 149.99, 50),
            (3, 2, 1, 'Test Product 3', 199.99, 75),
            (1, 1, 1, 'Test Product 1', 99.99, 100),
            (2, 1, 2, 'Test Product 2', 149.99, 50),
            (3, 2, 1, 'Test Product 3', 199.99, 75),
            (1, 1, 1, 'Test Product 1', 99.99, 100),
            (2, 1, 2, 'Test Product 2', 149.99, 50),
            (3, 2, 1, 'Test Product 3', 199.99, 75),
            (1, 1, 1, 'Test Product 1', 99.99, 100),
            (2, 1, 2, 'Test Product 2', 149.99, 50),
            (3, 2, 1, 'Test Product 3', 199.99, 75)
        ]

        self.reload_product(product_data=test_data)

        # 布局Treeview和Scrollbar
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        # 创建底部按钮区域
        button_frame = tk.Frame(self)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        def get_current_item():
            """获取当前的商品信息"""          
            current_item_values = self.tree.item(self.tree.focus())['values']
            print(current_item_values)

        def buy_product():
            """购买商品逻辑"""
            if(self.tree.focus() == ""):
                messagebox.showwarning(title="Selected Product", message="You need to select a PRODUCT first!")
            else:
                get_current_item()
                print("Buy product")
                messagebox.showinfo(title="Successful", message="You successfully bought this item")
        
        def show_record():
            """显示商品购买记录界面"""
            self.controller.change_size_title('800x600','购买记录',)
            self.controller.show_frame("RecordFrame")
        #     test_data = [
        #     (1, 101, 299.99, True, '2024-01-15'),
        #     (2, 102, 159.50, False, '2024-01-16'),
        # ]
        #     self.controller.frames["RecordFrame"].reload_record(test_data)

        def back_to_login():
            """返回登录界面"""
            self.controller.change_size_title('500x500','登录界面',)
            self.controller.show_frame("LoginFrame")

        ttk.Button(button_frame, text='Buy Product', command=buy_product).pack(side='left', padx=5)
        ttk.Button(button_frame, text='Show Buy Record',command=show_record).pack(side='left', padx=5)
        ttk.Button(button_frame, text='Back to Login',command=back_to_login).pack(side='left', padx=5)
        

        # 配置grid权重
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

    def receive_user_data(self,data):
        """获取user相关信息"""
        self.user_id = data[0]
    
