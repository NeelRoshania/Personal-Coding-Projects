-- If the demo table exists, drop it.
IF OBJECT_ID('dbo.demo') IS NOT NULL 
    DROP TABLE dbo.demo;

-- Create a new demo table.
CREATE TABLE demo (
    num INTEGER
);

-- Populate the demo table.
INSERT INTO demo
    (num)
VALUES 
    (10),
    (33),
    (45),
    (76);

-- Here is the solution, written with a Common Table Expression (CTE).
WITH demo_table_with_row_num AS (SELECT *,
                                        ROW_NUMBER() OVER(ORDER BY (SELECT NULL)) AS row_num
                                 FROM demo
                                )
SELECT num,
       -- COALESCE returns the first NON-NULL value. If you remove it, the dif value for num = 10 is NULL. I replaced it with a 0.
       COALESCE(num - LAG(num) OVER(ORDER BY row_num), 0) AS dif 
FROM demo_table_with_row_num;