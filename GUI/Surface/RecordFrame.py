import tkinter as tk
from tkinter import ttk
# from models.Records import Records
from datetime import datetime

class RecordFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.init_ui()

    def init_ui(self):
        # 创建返回按钮（顶部）
        self.back_button = ttk.Button(self, text="Back to Buy")
        self.back_button.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        # 创建记录显示区域（中间）
        # 创建一个Frame来容纳Treeview和滚动条
        self.record_frame = ttk.Frame(self)
        self.record_frame.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')

        # 创建Treeview
        self.record_list = ttk.Treeview(
            self.record_frame,
            columns=('Record_ID', 'Shipping_ID', 'Total', 'Status', 'DateTime'),
            show='headings'
        )

        # 设置列标题
        self.record_list.heading('Record_ID', text='Record ID')
        self.record_list.heading('Shipping_ID', text='Shipping ID')
        self.record_list.heading('Total', text='Total Money')
        self.record_list.heading('Status', text='Status')
        self.record_list.heading('DateTime', text='Date Time')

        # 设置列宽
        self.record_list.column('Record_ID', width=100)
        self.record_list.column('Shipping_ID', width=100)
        self.record_list.column('Total', width=100)
        self.record_list.column('Status', width=100)
        self.record_list.column('DateTime', width=150)

        # 创建垂直滚动条
        self.scrollbar = ttk.Scrollbar(
            self.record_frame,
            orient='vertical',
            command=self.record_list.yview
        )
        self.record_list.configure(yscrollcommand=self.scrollbar.set)

        # 布局Treeview和滚动条
        self.record_list.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='right', fill='y')

        # 配置网格权重
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # 添加测试数据
        self.insert_test_data()

    def insert_test_data(self):
        # 创建测试数据
        test_data = [
            (1, 101, 299.99, True, '2024-01-15'),
            (2, 102, 159.50, False, '2024-01-16'),
            (3, 103, 499.99, True, '2024-01-17'),
            (4, 104, 79.99, True, '2024-01-18'),
            (5, 105, 899.99, False, '2024-01-19')
        ]

        # 插入测试数据到Treeview
        for item in test_data:
            self.record_list.insert('', 'end', values=item)

# 用于测试的main函数
if __name__ == '__main__':
    root = tk.Tk()
    root.title('购买记录界面')
    root.geometry('800x600')
    
    app = RecordFrame(root)
    app.pack(fill='both', expand=True)
    
    root.mainloop()