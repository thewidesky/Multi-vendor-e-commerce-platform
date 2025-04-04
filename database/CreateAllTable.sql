CREATE TABLE IF NOT EXISTS Vendor (
    V_ID INT NOT NULL AUTO_INCREMENT COMMENT 'Vendor ID',
    Business_Name VARCHAR(255) NOT NULL COMMENT 'Vendor Name',
    Geo_Presence VARCHAR(255) NOT NULL COMMENT 'Vendor Place',
    V_Account VARCHAR(255) NOT NULL COMMENT 'Vendor Account',
    V_Secret VARCHAR(255) NOT NULL COMMENT 'Vendor Secret',
    PRIMARY KEY (V_ID)
) 
ENGINE=InnoDB 
DEFAULT CHARSET=utf8mb4 
COMMENT='存储供应商基本信息';


CREATE TABLE IF NOT EXISTS Manager (
    M_ID INT NOT NULL AUTO_INCREMENT COMMENT 'Manager ID',
    M_Name VARCHAR(255) NOT NULL COMMENT 'Manager Name',
    M_Secret VARCHAR(255) NOT NULL COMMENT 'Manager Secret',
    PRIMARY KEY (M_ID)
) 
ENGINE=InnoDB 
DEFAULT CHARSET=utf8mb4 
COMMENT='管理员信息';


CREATE TABLE IF NOT EXISTS Category (
    Category_ID INT NOT NULL AUTO_INCREMENT COMMENT 'Category ID',
    Category_Name VARCHAR(255) NOT NULL COMMENT 'Category Name',
    Description VARCHAR(255) DEFAULT NULL COMMENT 'Description',
    PRIMARY KEY (Category_ID)
) 
ENGINE=InnoDB 
DEFAULT CHARSET=utf8mb4 
COMMENT='存储商品分类信息';


CREATE TABLE IF NOT EXISTS Product (
    P_ID INT NOT NULL AUTO_INCREMENT COMMENT 'Product ID',
    V_ID INT NOT NULL COMMENT 'Vendor of Product',
    Category_ID INT NOT NULL COMMENT 'Category of Product',
    P_Name VARCHAR(255) NOT NULL COMMENT 'Product Name',
    Price DECIMAL(10,2) NOT NULL COMMENT 'Product Price',
    Stock INT NOT NULL COMMENT 'Product Stock',
    P_Status INT DEFAULT NULL COMMENT 'Status of Product',
    P_Picture VARCHAR(255) DEFAULT NULL COMMENT 'Picture of Product',
    PRIMARY KEY (P_ID),
    FOREIGN KEY (V_ID) REFERENCES Vendor(V_ID) ON DELETE CASCADE,
    FOREIGN KEY (Category_ID) REFERENCES Category(Category_ID) ON DELETE RESTRICT
) 
ENGINE=InnoDB 
DEFAULT CHARSET=utf8mb4 
COMMENT='存储商品信息';


CREATE TABLE IF NOT EXISTS Tag (
    T_ID INT NOT NULL AUTO_INCREMENT COMMENT 'Tag ID',
    Tag_Name VARCHAR(255) NOT NULL COMMENT 'Tag Name',
    PRIMARY KEY (T_ID),
    -- 唯一索引，防止Tag_Name字段重复
    UNIQUE INDEX idx_tag_name (Tag_Name)
) 
ENGINE=InnoDB 
DEFAULT CHARSET=utf8mb4 
COMMENT='存储商品标签信息';


CREATE TABLE IF NOT EXISTS Product_Tag (
    P_ID INT NOT NULL COMMENT 'Product ID',
    T_ID INT NOT NULL COMMENT 'Tag ID',
    PRIMARY KEY (P_ID, T_ID),
    FOREIGN KEY (P_ID) REFERENCES Product(P_ID) ON DELETE CASCADE,
    FOREIGN KEY (T_ID) REFERENCES Tag(T_ID) ON DELETE CASCADE
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COMMENT='商品与标签的多对多关联关系';


CREATE TABLE IF NOT EXISTS Customer (
    C_ID INT NOT NULL AUTO_INCREMENT COMMENT 'Customer ID',
    C_Name VARCHAR(255) NOT NULL COMMENT 'Customer Name',
    Geo_Presence VARCHAR(255) NOT NULL COMMENT 'Vendor Place',
    C_Account VARCHAR(255) NOT NULL COMMENT 'Customer Account',
    C_Secret VARCHAR(255) NOT NULL COMMENT 'Customer Secret',
    PRIMARY KEY (C_ID)
) 
ENGINE=InnoDB 
DEFAULT CHARSET=utf8mb4 
COMMENT='存储客户账户信息';


CREATE TABLE IF NOT EXISTS Feedback (
    C_ID INT NOT NULL COMMENT 'Customer ID',
    V_ID INT NOT NULL COMMENT 'Vendor ID',
    Comment VARCHAR(255) DEFAULT NULL COMMENT 'Comment Content',
    Rating INT DEFAULT NULL COMMENT 'Ratting Number',
    -- 联合主键 (C_ID, V_ID) 表示 一个客户对同一商家只能有一条反馈
    PRIMARY KEY (C_ID, V_ID),
    FOREIGN KEY (C_ID) REFERENCES Customer(C_ID),
    FOREIGN KEY (V_ID) REFERENCES Vendor(V_ID)
) 
ENGINE=InnoDB 
DEFAULT CHARSET=utf8mb4 
COMMENT='存储客户对商家的反馈';


CREATE TABLE IF NOT EXISTS Shipping (
    S_ID INT NOT NULL AUTO_INCREMENT COMMENT 'Shipping ID',
    C_ID INT NOT NULL COMMENT 'Customer ID',
    S_Location VARCHAR(255) NOT NULL COMMENT 'Vendor Place',
    S_IsDefault BOOLEAN NOT NULL DEFAULT FALSE COMMENT 'Default or NOT',
    PRIMARY KEY (S_ID),
    FOREIGN KEY (C_ID) REFERENCES Customer(C_ID) ON DELETE CASCADE
)
ENGINE=InnoDB 
DEFAULT CHARSET=utf8mb4 
COMMENT='存储配送信息';


CREATE TABLE IF NOT EXISTS Records (
    R_ID INT NOT NULL COMMENT 'Record ID',
    S_ID INT NOT NULL COMMENT 'Shipping ID',
    C_ID INT NOT NULL COMMENT 'Customer ID',
    Toal DECIMAL(10,2) NOT NULL COMMENT 'Total Money',
    R_Status BOOLEAN NOT NULL COMMENT 'Record Status',
    R_Date DATE NOT NULL COMMENT 'Date Time', -- 将Dtae修改为R_Date,因为Date是SQL关键词
    PRIMARY KEY (R_ID),
    FOREIGN KEY (S_ID) REFERENCES Shipping(S_ID),
    FOREIGN KEY (C_ID) REFERENCES Customer(C_ID)
) 
ENGINE=InnoDB 
DEFAULT CHARSET=utf8mb4 
COMMENT='存储交易记录';


CREATE TABLE IF NOT EXISTS `Records Detail` (
    RD_ID INT NOT NULL AUTO_INCREMENT COMMENT 'Record Detail ID',
    R_ID INT NOT NULL COMMENT 'Record ID',
    P_ID INT NOT NULL COMMENT 'Product ID',
    Price DECIMAL(10,2) NOT NULL CHECK (Price >= 0) COMMENT 'Product Price',
    Quantity INT NOT NULL COMMENT 'Quantity of Product', 
    Subtotal DECIMAL(10,2) NOT NULL COMMENT 'Subtotal Price',
    PRIMARY KEY (RD_ID),
    FOREIGN KEY (R_ID) REFERENCES Records(R_ID) ON DELETE CASCADE,
    FOREIGN KEY (P_ID) REFERENCES Product(P_ID)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COMMENT='存储交易明细（商品级记录）';