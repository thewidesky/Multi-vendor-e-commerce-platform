import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
import os

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入所需的DAO类
from dao.product_dao import ProductDAO
from dao.product_search_dao import ProductSearchDAO
from dao.purchase_dao import PurchaseDAO
from models.Product import Product
from models.Records import Records
from models.RecordsDetail import RecordsDetail

class ECommerceApp:
    def __init__(self, root):
        self.root = root
        self.root.title('电商管理系统')
        self.root.geometry('800x600')

        # 初始化DAO对象
        self.product_dao = ProductDAO()
        self.product_search_dao = ProductSearchDAO()
        self.purchase_dao = PurchaseDAO()

        # 创建标签页控件
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')

        # 创建三个主要标签页
        self.product_frame = ttk.Frame(self.notebook)
        self.search_frame = ttk.Frame(self.notebook)
        self.purchase_frame = ttk.Frame(self.notebook)

        # 将标签页添加到notebook
        self.notebook.add(self.product_frame, text='产品目录管理')
        self.notebook.add(self.search_frame, text='产品搜索')
        self.notebook.add(self.purchase_frame, text='产品购买管理')

        # 初始化各个标签页的内容
        self.init_product_page()
        self.init_search_page()
        self.init_purchase_page()

    def init_product_page(self):
        # 供应商ID输入框和查询按钮
        vendor_frame = ttk.Frame(self.product_frame)
        vendor_frame.pack(pady=10)
        ttk.Label(vendor_frame, text='供应商ID:').pack(side=tk.LEFT)
        self.vendor_id_entry = ttk.Entry(vendor_frame)
        self.vendor_id_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(vendor_frame, text='查询产品', command=self.query_vendor_products).pack(side=tk.LEFT)

        # 产品列表
        self.product_tree = ttk.Treeview(self.product_frame, columns=('ID', '名称', '价格', '库存', '状态'), show='headings')
        self.product_tree.heading('ID', text='产品ID')
        self.product_tree.heading('名称', text='产品名称')
        self.product_tree.heading('价格', text='价格')
        self.product_tree.heading('库存', text='库存')
        self.product_tree.heading('状态', text='状态')
        self.product_tree.pack(pady=10, fill='both', expand=True)

        # 操作按钮框架
        btn_frame = ttk.Frame(self.product_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text='添加产品', command=self.show_add_product_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text='修改产品', command=self.show_edit_product_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text='删除产品', command=self.delete_product).pack(side=tk.LEFT, padx=5)

    def init_search_page(self):
        # 标签ID搜索框架
        search_frame = ttk.Frame(self.search_frame)
        search_frame.pack(pady=10)
        ttk.Label(search_frame, text='标签ID:').pack(side=tk.LEFT)
        self.tag_id_entry = ttk.Entry(search_frame)
        self.tag_id_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text='搜索产品', command=self.search_by_tag).pack(side=tk.LEFT)

        # 搜索结果列表
        self.search_tree = ttk.Treeview(self.search_frame, columns=('ID', '名称', '价格', '标签'), show='headings')
        self.search_tree.heading('ID', text='产品ID')
        self.search_tree.heading('名称', text='产品名称')
        self.search_tree.heading('价格', text='价格')
        self.search_tree.heading('标签', text='标签')
        self.search_tree.pack(pady=10, fill='both', expand=True)

    def init_purchase_page(self):
        # 客户ID查询框架
        customer_frame = ttk.Frame(self.purchase_frame)
        customer_frame.pack(pady=10)
        ttk.Label(customer_frame, text='客户ID:').pack(side=tk.LEFT)
        self.customer_id_entry = ttk.Entry(customer_frame)
        self.customer_id_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(customer_frame, text='查询订单', command=self.query_customer_orders).pack(side=tk.LEFT)

        # 订单列表
        self.order_tree = ttk.Treeview(self.purchase_frame, columns=('ID', '日期', '总额', '状态'), show='headings')
        self.order_tree.heading('ID', text='订单ID')
        self.order_tree.heading('日期', text='日期')
        self.order_tree.heading('总额', text='总额')
        self.order_tree.heading('状态', text='状态')
        self.order_tree.pack(pady=10, fill='both', expand=True)

        # 操作按钮
        btn_frame = ttk.Frame(self.purchase_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text='新建订单', command=self.show_add_order_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text='修改订单', command=self.show_edit_order_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text='删除订单', command=self.delete_order).pack(side=tk.LEFT, padx=5)

    def query_vendor_products(self):
        try:
            vendor_id = int(self.vendor_id_entry.get())
            products = self.product_dao.get_products_by_vendor(vendor_id)
            
            # 清空现有显示
            for item in self.product_tree.get_children():
                self.product_tree.delete(item)
            
            # 显示查询结果
            for product in products:
                self.product_tree.insert('', 'end', values=(
                    product.p_id,
                    product.p_name,
                    product.price,
                    product.stock,
                    product.p_status
                ))
        except ValueError:
            messagebox.showerror('错误', '请输入有效的供应商ID')
        except Exception as e:
            messagebox.showerror('错误', str(e))

    def show_add_product_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title('添加产品')
        dialog.geometry('300x400')

        # 输入字段
        ttk.Label(dialog, text='供应商ID:').pack(pady=5)
        vendor_id_entry = ttk.Entry(dialog)
        vendor_id_entry.pack()

        ttk.Label(dialog, text='分类ID:').pack(pady=5)
        category_id_entry = ttk.Entry(dialog)
        category_id_entry.pack()

        ttk.Label(dialog, text='产品名称:').pack(pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.pack()

        ttk.Label(dialog, text='价格:').pack(pady=5)
        price_entry = ttk.Entry(dialog)
        price_entry.pack()

        ttk.Label(dialog, text='库存:').pack(pady=5)
        stock_entry = ttk.Entry(dialog)
        stock_entry.pack()

        ttk.Label(dialog, text='状态:').pack(pady=5)
        status_entry = ttk.Entry(dialog)
        status_entry.pack()

        def save_product():
            try:
                product = Product(
                    p_id=None,  # 新产品，ID由数据库生成
                    v_id=int(vendor_id_entry.get()),
                    category_id=int(category_id_entry.get()),
                    p_name=name_entry.get(),
                    price=float(price_entry.get()),
                    stock=int(stock_entry.get()),
                    p_status=status_entry.get(),
                    p_picture=None  # 暂不处理图片
                )
                self.product_dao.create_product(product)
                messagebox.showinfo('成功', '产品添加成功')
                dialog.destroy()
                # 刷新产品列表
                self.query_vendor_products()
            except Exception as e:
                messagebox.showerror('错误', str(e))

        ttk.Button(dialog, text='保存', command=save_product).pack(pady=20)

    def show_edit_product_dialog(self):
        selected = self.product_tree.selection()
        if not selected:
            messagebox.showwarning('警告', '请先选择要修改的产品')
            return

        # 获取选中产品的ID
        product_id = self.product_tree.item(selected[0])['values'][0]
        try:
            product = self.product_dao.get_product_by_id(product_id)
            if not product:
                messagebox.showerror('错误', '产品不存在')
                return

            dialog = tk.Toplevel(self.root)
            dialog.title('修改产品')
            dialog.geometry('300x400')

            # 输入字段
            ttk.Label(dialog, text='供应商ID:').pack(pady=5)
            vendor_id_entry = ttk.Entry(dialog)
            vendor_id_entry.insert(0, str(product.v_id))
            vendor_id_entry.pack()

            ttk.Label(dialog, text='分类ID:').pack(pady=5)
            category_id_entry = ttk.Entry(dialog)
            category_id_entry.insert(0, str(product.category_id))
            category_id_entry.pack()

            ttk.Label(dialog, text='产品名称:').pack(pady=5)
            name_entry = ttk.Entry(dialog)
            name_entry.insert(0, product.p_name)
            name_entry.pack()

            ttk.Label(dialog, text='价格:').pack(pady=5)
            price_entry = ttk.Entry(dialog)
            price_entry.insert(0, str(product.price))
            price_entry.pack()

            ttk.Label(dialog, text='库存:').pack(pady=5)
            stock_entry = ttk.Entry(dialog)
            stock_entry.insert(0, str(product.stock))
            stock_entry.pack()

            ttk.Label(dialog, text='状态:').pack(pady=5)
            status_entry = ttk.Entry(dialog)
            status_entry.insert(0, product.p_status)
            status_entry.pack()

            def update_product():
                try:
                    product.v_id = int(vendor_id_entry.get())
                    product.category_id = int(category_id_entry.get())
                    product.p_name = name_entry.get()
                    product.price = float(price_entry.get())
                    product.stock = int(stock_entry.get())
                    product.p_status = status_entry.get()

                    self.product_dao.update_product(product)
                    messagebox.showinfo('成功', '产品更新成功')
                    dialog.destroy()
                    # 刷新产品列表
                    self.query_vendor_products()
                except Exception as e:
                    messagebox.showerror('错误', str(e))

            ttk.Button(dialog, text='更新', command=update_product).pack(pady=20)

        except Exception as e:
            messagebox.showerror('错误', str(e))

    def delete_product(self):
        selected = self.product_tree.selection()
        if not selected:
            messagebox.showwarning('警告', '请先选择要删除的产品')
            return

        if messagebox.askyesno('确认', '确定要删除选中的产品吗？'):
            try:
                product_id = self.product_tree.item(selected[0])['values'][0]
                self.product_dao.delete_product(product_id)
                messagebox.showinfo('成功', '产品删除成功')
                # 刷新产品列表
                self.query_vendor_products()
            except Exception as e:
                messagebox.showerror('错误', str(e))

    def search_by_tag(self):
        try:
            tag_id = int(self.tag_id_entry.get())
            products = self.product_search_dao.get_products_by_tag(tag_id)
            
            # 清空现有显示
            for item in self.search_tree.get_children():
                self.search_tree.delete(item)
            
            # 显示查询结果
            for product in products:
                # 获取产品的标签
                tags = self.product_search_dao.get_tags_by_product(product.p_id)
                tag_names = ', '.join([tag.tag_name for tag in tags])
                
                self.search_tree.insert('', 'end', values=(
                    product.p_id,
                    product.p_name,
                    product.price,
                    tag_names
                ))
        except ValueError:
            messagebox.showerror('错误', '请输入有效的标签ID')
        except Exception as e:
            messagebox.showerror('错误', str(e))

    def query_customer_orders(self):
        try:
            customer_id = int(self.customer_id_entry.get())
            orders = self.purchase_dao.get_purchases_by_customer(customer_id)
            
            # 清空现有显示
            for item in self.order_tree.get_children():
                self.order_tree.delete(item)
            
            # 显示查询结果
            for order in orders:
                self.order_tree.insert('', 'end', values=(
                    order.r_id,
                    order.r_date,
                    order.toal,
                    order.r_status
                ))
        except ValueError:
            messagebox.showerror('错误', '请输入有效的客户ID')
        except Exception as e:
            messagebox.showerror('错误', str(e))

    def show_add_order_dialog(self):
        # 实现新建订单的对话框
        pass

    def show_edit_order_dialog(self):
        # 实现修改订单的对话框
        pass

    def delete_order(self):
        # 实现删除订单的功能
        pass

if __name__ == '__main__':
    root = tk.Tk()
    app = ECommerceApp(root)
    root.mainloop()