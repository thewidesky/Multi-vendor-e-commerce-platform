import tkinter as tk
from tkinter import ttk
# from models.Records import Records
from datetime import datetime

class RecordFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        def back_to_user():
            """返回用户界面"""
            self.controller.change_size_title('800x600','用户界面',)
            self.controller.show_frame("UserFrame")

        # 创建返回按钮（顶部）
        self.back_button = ttk.Button(self, text="Back to Buy", command=back_to_user)
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

        test_data = [
            (1, 101, 299.99, True, '2024-01-15'),
            (2, 102, 159.50, False, '2024-01-16'),
            (3, 103, 499.99, True, '2024-01-17'),
            (4, 104, 79.99, True, '2024-01-18'),
            (5, 105, 899.99, False, '2024-01-19')
        ]

        # 添加测试数据
        self.reload_record(test_data)

    def reload_record(self, record_data):
        """record_list重新加载购买记录信息"""
        if len(self.record_list.get_children()) != 0:
            self.record_list.delete(*self.record_list.get_children())
        for item in record_data:
            self.record_list.insert('', 'end', values=item)
    
    def get_current_record(self):
        """获取当前的商品信息"""  
        if (self.record_list.focus() != ""):    
            current_record_values = self.record_list.item(self.record_list.focus())['values']
            print(current_record_values)
    
