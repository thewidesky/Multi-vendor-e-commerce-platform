import tkinter as tk
from tkinter import ttk
# from models.Product import Product
# from models.ProductTag import ProductTag

class UserFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.init_ui()

    def init_ui(self):
        # 创建顶部搜索区域
        search_frame = tk.Frame(self)
        search_frame.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky='ew')

        # 搜索输入框和按钮
        self.product_search = ttk.Entry(search_frame)
        self.product_search.insert(0, 'Write Product id there.')
        self.product_search.grid(row=0, column=0, padx=5)
        self.product_search.bind('<FocusIn>', lambda e: self.on_entry_click(e, self.product_search, 'Use the Product id to search.'))
        self.product_search.bind('<FocusOut>', lambda e: self.on_focus_out(e, self.product_search, 'Use the Product id to search.'))

        self.tag_search = ttk.Entry(search_frame)
        self.tag_search.insert(0, 'Write Tag id to there.')
        self.tag_search.grid(row=0, column=2, padx=5)
        self.tag_search.bind('<FocusIn>', lambda e: self.on_entry_click(e, self.tag_search, 'Use the Tag id to search.'))
        self.tag_search.bind('<FocusOut>', lambda e: self.on_focus_out(e, self.tag_search, 'Use the Tag id to search.'))

        ttk.Button(search_frame, text='Search By Product').grid(row=0, column=1, padx=5)
        ttk.Button(search_frame, text='Search By Tag').grid(row=0, column=3, padx=5)

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
            (3, 2, 1, 'Test Product 3', 199.99, 75)
        ]
        for item in test_data:
            self.tree.insert('', 'end', values=item)

        # 布局Treeview和Scrollbar
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        # 创建底部按钮区域
        button_frame = tk.Frame(self)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text='Buy Product').pack(side='left', padx=5)
        ttk.Button(button_frame, text='Back to Login').pack(side='left', padx=5)

        # 配置grid权重
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

    def on_entry_click(self, event, entry, default_text):
        if entry.get() == default_text:
            entry.delete(0, 'end')
            entry.config(foreground='black')

    def on_focus_out(self, event, entry, default_text):
        if entry.get() == '':
            entry.insert(0, default_text)
            entry.config(foreground='gray')

def main():
    root = tk.Tk()
    root.title('User Interface')
    root.geometry('800x600')
    app = UserFrame(root)
    app.pack(fill='both', expand=True)
    root.mainloop()

if __name__ == '__main__':
    main()