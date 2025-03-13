# Multi-vendor-e-commerce-platform
A multi vendor e-commerce platform with the following functions: supplier management, product catalog management, product discovery, product purchase, and order modification.

# 请首先在config.py当中配置本地电脑的SQL
包括用户名与密码等

# 建立SQL的表格
进入db_initializer.py当中，在main函数中将文件位置换为CreateAllTable.sql，然后运行
# 插入数据
进入db_initializer.py当中，在main函数中将文件位置换为Init_Insert.sql，然后运行
# 重置，删除所有的表格
进入db_initializer.py当中，在main函数中将文件位置换为DeleteAllTable.sql，然后运行

# 后端接口功能描述
供应商管理：--Vendor.py
1.获得所有供应商的信息
2.将新供应商信息插入数据库当中
3.根据供应商的ID删除相应的数据库数据
4.根据供应商的ID修改相应的数据库数据

产品目录管理：--Product_dao.py
1.根据供应商的ID，查看供应商所提供的所有产品的信息
2.根据供应商的ID和产品的信息，向数据库中插入产品相关的信息
3.根据产品的ID，查看产品相关的信息
4.根据产品的ID，删除数据库中相关产品信息
5.根据产品的ID，修改产品相关的信息

产品搜索管理(有关系的表为tag、product_tag、product)：--product_search_dao.py
1.用户根据标签ID，发现对应的产品信息。
2.根据产品的ID，发现对应的标签相关信息。

产品购买管理(有关系的表为records、records detail)：--purchase_dao.py
1.向数据库插入购买记录以及购买记录细节，注意同步性
2.根据客户的ID，查看对应的购买记录和购买记录细节
3.能够修改购买记录以及购买记录细节
4.能够删除购买记录以及购买记录细节

管理员信息管理：--manager_dao.py
1.查找所有管理员的信息
2.根据管理员ID查找相应的信息
3.根据管理员ID修改相应的信息
4.根据管理员ID删除相应的信息
5.向数据库中写入一个管理员信息

商品评论管理(与feedback有关)：--feedback_dao.py
1.根据顾客的ID获取评论
2.根据商家的ID获取评论