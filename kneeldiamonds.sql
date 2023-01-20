
CREATE TABLE `Sizes`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `carets` NVARCHAR(160) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

CREATE TABLE `Styles`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `style` NVARCHAR(160) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

CREATE TABLE `Orders`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `metal_id` INTEGER NOT NULL,
	`size_id` INTEGER,
    `style_id` INTEGER,
    FOREIGN KEY(`style_id`) REFERENCES `Style`(`id`),
	FOREIGN KEY(`metal_id`) REFERENCES `Metal`(`id`),
	FOREIGN KEY(`size_id`) REFERENCES `Size`(`id`)
    
); 

DROP TABLE Orders


INSERT INTO `Metals` VALUES (null, 'Sterling Silver', 12.42);
INSERT INTO `Metals` VALUES (null, '14K Gold', 736.4); 
INSERT INTO `Metals` VALUES (null, '24K Gold', 1258.9); 
INSERT INTO `Metals` VALUES (null, 'Platinum', 795.45); 
INSERT INTO `Metals` VALUES (null, 'Palladium', 1241); 

INSERT INTO `Sizes` VALUES(null, 0.5, 405); 
INSERT INTO `Sizes` VALUES(null, 0.75, 782); 
INSERT INTO `Sizes` VALUES(null, 1, 1470); 
INSERT INTO `Sizes` VALUES(null, 1.5, 1997); 
INSERT INTO `Sizes` VALUES(null, 2, 3638); 

INSERT INTO `Styles` VALUES(null, 'Classic', 500); 
INSERT INTO `Styles` VALUES(null, 'Modern', 710); 
INSERT INTO `Styles` VALUES(null, 'Vintage', 965); 

INSERT INTO `Orders` VALUES(null, 1, 2, 3); 
INSERT INTO `Orders` VALUES(null, 3,2,1); 
INSERT INTO `Orders` VALUES(null, 2,2,2); 

SELECT
            o.id,
            o.metal_id,
            o.style_id,
            o.size_id, 
            m.metal metal_metal, 
            m.price metal_price
        FROM Orders o
        JOIN Metals m 
            ON m.id = o.metal_id