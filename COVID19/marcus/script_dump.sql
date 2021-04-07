-- Here is the solution, written with a Common Table Expression (CTE).
WITH demo_table_with_row_num AS (SELECT *,
                                        ROW_NUMBER() OVER(ORDER BY (SELECT NULL)) AS row_num
                          
                          FROM `covid19-2020-272000.covid19.cases`
                                )
SELECT date, case_type, country_region, cases,
       -- COALESCE returns the first NON-NULL value. If you remove it, the dif value for num = 10 is NULL. I replaced it with a 0.
       COALESCE(cases - LAG(cases) OVER(ORDER BY row_num), 0) AS dif 
FROM demo_table_with_row_num
WHERE case_type IN ("confirmed") AND country_region in ("US")
ORDER BY 
  country_region DESC,
  dif DESC


-- Growth Factor

-- Here is the solution, written with a Common Table Expression (CTE).
WITH demo_table_with_row_num AS (SELECT *,
                                        ROW_NUMBER() OVER(ORDER BY (SELECT NULL)) AS row_num
                                 FROM `covid19-2020-272000.covid19.cases` 
                                )
SELECT date, country_region, case_type, cases,
       -- COALESCE returns the first NON-NULL value. If you remove it, the dif value for num = 10 is NULL. I replaced it with a 0.
       COALESCE(cases / NULLIF(LAG(cases) OVER(ORDER BY row_num), 0), 0) AS dif 
FROM demo_table_with_row_num
WHERE case_type in ("confirmed") AND country_region in ("US")
ORDER BY date DESC;
