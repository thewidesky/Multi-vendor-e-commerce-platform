-- 插入Vendor数据
INSERT INTO Vendor (V_ID, Business_Name, Geo_Presence, V_Account, V_Secret) VALUES
(20001, 'ChicDress Boutique', 'Paris, France', 'chicdress101', 'secret12345'),
(20002, 'LadyStyle Fashion', 'Milan, Italy', 'ladystyle102', 'secret67890'),
(20003, 'GlamourGown Co.', 'New York, USA', 'glamourgown103', 'secret54321');

-- 插入Category数据
INSERT INTO Category (Category_ID, Category_Name, Description) VALUES
(10001, 'Hooded_sweatshirt', 'Hooded_sweatshirt'),
(10002, 'Blouses', 'Blouses'),
(10003, 'T-shirt', 'T-shirt'),
(10004, 'Outerwear', 'Outerwear'),
(10005, 'Pant', 'Pant'),
(10006, 'Skirt', 'Skirt');

-- 插入Product数据（修正V_ID为模拟数据中的值）
INSERT INTO Product (P_ID, V_ID, Category_ID, P_Name, Price, Stock, P_Status) VALUES
(1, 20001, 10001, 'Hoodie with Pockets', 49.99, 50, 1),
(2, 20002, 10002, 'Silk Blouse', 29.99, 30, 1),
(3, 20003, 10003, 'Basic T-shirt', 19.99, 100, 1),
(4, 20001, 10004, 'Denim Jacket', 69.99, 40, 1),
(5, 20002, 10005, 'High-Waist Jeans', 59.99, 60, 1),
(6, 20003, 10006, 'A-Line Skirt', 39.99, 80, 1),
(7, 20001, 10004, 'Leather Jacket', 89.99, 30, 1),
(8, 20002, 10005, 'Wide-Leg Pants', 54.99, 50, 1),
(9, 20003, 10006, 'Frock', 34.99, 120, 1),
(10, 20001, 10001, 'Hooded Sweatshirt', 49.99, 60, 1),
(11, 20002, 10002, 'Button-Up Blouse', 29.99, 40, 1),
(12, 20003, 10003, 'Tank Top', 14.99, 150, 1),
(13, 20001, 10004, 'Windbreaker', 59.99, 35, 1),
(14, 20002, 10005, 'Shorts', 49.99, 70, 1),
(15, 20003, 10006, 'Pleated Skirt', 39.99, 90, 1),
(16, 20001, 10001, 'Hoodie with Zipper', 47.99, 80, 1),
(17, 20002, 10002, 'Cardigan', 32.99, 25, 1);

-- 插入Tag数据
INSERT INTO Tag (T_ID, Tag_Name) VALUES
(1, 'Casual Wear'),
(2, 'Formal Wear'),
(3, 'Street Style'),
(4, 'Eco-Friendly'),
(5, 'Summer Essentials'),
(6, 'Knitwear'),
(7, 'Plus Size'),
(8, 'Cute Style'),
(9, 'Mature Style'),
(10, 'Commuter Style');

-- 插入Product_Tag数据
INSERT INTO Product_Tag (P_ID, T_ID) VALUES
(1,1), (1,3), (1,10),
(2,2), (2,9), (2,4),
(3,1), (3,5), (3,10),
(4,3), (4,10), (4,4),
(5,2), (5,10), (5,5),
(6,1), (6,5), (6,8),
(7,7), (7,3), (7,10),
(8,1), (8,5), (8,10),
(9,1), (9,8), (9,9),
(10,1), (10,5), (10,3),
(11,1), (11,2), (11,9),
(12,1), (12,5), (12,8),
(13,4), (13,10),
(14,1), (14,5), (14,3),
(15,1), (15,5), (15,8),
(16,1), (16,5), (16,3),
(17,2), (17,9), (17,4);

-- 插入Customer数据
INSERT INTO Customer (C_ID, C_Name, Geo_Presence, C_Account, C_Secret) VALUES
(1, 'Alice Johnson', 'New York, USA', 'alice123', 'secret001'),
(2, 'Bob Smith', 'London, UK', 'bob456', 'secret002'),
(3, 'Clara Lee', 'Seoul, South Korea', 'clara789', 'secret003');

-- 插入Feedback数据
INSERT INTO Feedback (C_ID, V_ID, Comment, Rating) VALUES
(1,20001, 'Great service and quality products!',5),
(2,20002, 'The delivery was a bit slow, but the products were good.',3),
(3,20003, 'Excellent customer support and fast delivery.',4),
(1,20002, 'Loved the variety of products available.',4),
(2,20003, 'Not satisfied with the product quality.',2),
(3,20001, 'Very happy with my purchase!',5),
(1,20003, 'Could be better, but overall satisfactory.',3),
(2,20001, 'Fast delivery and good quality. Highly recommended!',5),
(3,20002, 'Average experience. Nothing special.',3);

-- 插入Shipping数据
INSERT INTO Shipping (S_ID, C_ID, S_Location, S_IsDefault) VALUES
(1,1, '123 Main Street, New York, NY, USA',1),
(2,2, '456 Park Avenue, London, UK',0),
(3,3, '789 Sejong Road, Seoul, South Korea',1),
(4,1, '321 Broadway, New York, NY, USA',0),
(5,2, '654 Oxford Street, London, UK',1),
(6,3, '987 Gangnam Avenue, Seoul, South Korea',0),
(7,1, '111 Wall Street, New York, NY, USA',0),
(8,2, '222 Regent Street, London, UK',0),
(9,3, '333 Yeouido Boulevard, Seoul, South Korea',0),
(10,1, '444 Times Square, New York, NY, USA',0);

-- 插入Records数据（修正字段名Toal为Total）
INSERT INTO Records (R_ID, S_ID, C_ID, Toal, R_Status, R_Date) VALUES
(1,1,1,125.5,1,'2025-02-20'),
(2,2,2,89.99,1,'2025-02-21'),
(3,3,3,234.75,0,'2025-02-22'),
(4,4,1,99.99,1,'2025-02-23'),
(5,5,2,150,1,'2025-02-24'),
(6,6,3,75.5,0,'2025-02-25'),
(7,7,1,200,1,'2025-02-26'),
(8,8,2,110.99,0,'2025-02-27'),
(9,9,3,180.5,1,'2025-02-28'),
(10,10,1,65.75,1,'2025-03-01');

-- 插入Records Detail数据（表名用反引号包裹）
INSERT INTO `Records Detail` (RD_ID, R_ID, P_ID, Price, Quantity, Subtotal) VALUES
(1,1,1,49.99,2,99.98),
(2,1,3,19.99,1,19.99),
(3,2,2,29.99,3,89.97),
(4,2,7,89.99,1,89.99),
(5,3,5,59.99,2,119.98),
(6,3,10,49.99,1,49.99),
(7,4,12,14.99,5,74.95),
(8,4,14,49.99,2,99.98),
(9,5,4,69.99,1,69.99),
(10,5,9,34.99,3,104.97);

-- 插入Manager数据
INSERT INTO Manager (M_ID,M_name,M_Secret) VALUES 
(1,"Manger",'secret009');