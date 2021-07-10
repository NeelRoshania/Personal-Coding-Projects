-- **************************************************************************************************************
--     SQL Basics: Simple JOIN and RANK
--     https://www.codewars.com/kata/58094559c47d323ebd000035/train/sql
--     Status: Solved
-- **************************************************************************************************************

SELECT
  p.id, 
  p.name as name,
  COUNT(s.sale) as sale_count,
  RANK() OVER (PARTITION BY p.id ORDER BY p.id DESC) as sale_rank
FROM people AS p
LEFT JOIN sales AS s
ON p.id = s.people_id
GROUP BY p.id
GROUP BY sale_rank ASC

-- learnings
--   - no need for a CTE, can transition straight into group by after the left join
--   - https://codingsight.com/grouping-data-using-the-over-and-partition-by-functions/
--     - count(gender) over(Partition By gender order by gender desc) as total_gender
--       - For the given gender, apply count(gender) to that specific gender only
--       - Sort the whole table by gender?

-- **************************************************************************************************************
--     SQL Basics: SQL Basics Up and Down
--     https://www.codewars.com/kata/595a3ba3843b0cbf8e000004/train/sql
--     Status: Solved
-- **************************************************************************************************************

SELECT
CASE WHEN MOD(SUM(number1), 2) = 0 THEN MAX(number1) ELSE MIN(number1) END AS number1,
CASE WHEN MOD(SUM(number2), 2) = 0 THEN MAX(number2) ELSE MIN(number2) END AS number2
FROM numbers AS n


-- **************************************************************************************************************
--     SQL Bug Fixing: Fix the QUERY - Totaling
--     https://www.codewars.com/kata/582cba7d3be8ce3a8300007c/train/sql
--     Status: Solved
-- **************************************************************************************************************

SELECT 
  CAST(s.transaction_date AS DATE) as day,
  d.name as department,
  COUNT(s.id) as sale_count
FROM 
  department as d
JOIN 
  sale as s 
ON d.id = s.department_id
GROUP BY 
  day, 
  d.name
ORDER BY
DAY ASC

-- **************************************************************************************************************
--     SQL Basics: Simple table totaling.
--     https://www.codewars.com/kata/5809575e166583acfa000083/train/sql
--     Status: NOT SOLVED
-- **************************************************************************************************************

SELECT
  RANK() OVER( PARTITION BY clan ORDER BY SUM(points) DESC) AS "rank",
  CASE WHEN clan != '' THEN clan ELSE 'no clan specified' END AS "clan",
  SUM(points) as total_points,
  COUNT(name) as total_people
FROM people
GROUP BY clan
ORDER BY total_points DESC;

-- **************************************************************************************************************
--     SQL Basics: Simple UNION ALL.
--     https://www.codewars.com/kata/58112f8004adbbdb500004fe/train/sql
--     Status: SOLVED
-- **************************************************************************************************************

SELECT
  'US' AS location,
  us.*
FROM ussales AS us
WHERE price > 50.00

UNION ALL

SELECT
  'EU' AS location,
  eu.*
FROM eusales AS eu
WHERE price > 50.00
ORDER BY 
LOCATION DESC,
id ASC;

-- **************************************************************************************************************
--     SQL Basics: Simple WITH
--     https://www.codewars.com/kata/5811501c2d35672d4f000146/train/sql
--     Status: SOLVED
-- **************************************************************************************************************

WITH special_sales AS (
SELECT
s.*
FROM sales AS s
WHERE price > 90.00
)

-- left join sales id's with special_sales
SELECT 
d.*
FROM departments AS d
WHERE d.id IN (SELECT department_id FROM special_sales);

-- **************************************************************************************************************
--     SQL Basics: Simple NULL handling
--     https://www.codewars.com/kata/5811315e04adbbdb5000050e/train/sql
--     Status: SOLVED
-- **************************************************************************************************************

-- Process flow,
--   - Return a string if an entry is null
--     - Use NULLIF() to return null if string is empty
--     - Use COALESCE() to return the first non-null entry in a list **with the desired string

SELECT
ID,
COALESCE(NULLIF(name, ''), '[product name not found]') AS name,
price,
COALESCE(nullif(card_name, '' ), '[card name not found]') AS card_name,
card_number,
transaction_date
FROM eusales
WHERE price > 50.00 AND price IS NOT null

-- **************************************************************************************************************
--     SQL Basics: Using LATERAL JOIN To Get Top N per Group
--     https://www.codewars.com/kata/5820176255c3d23f360000a9/train/sql
--     Status: SOLVED BY MANWE
-- **************************************************************************************************************


-- ROW NUMBER METHOD

-- left join posts with categories and rank by views
with post_categories as (
select 
  row_number() over( partition by c.category order by views desc) as "rank",
  c.id as category_id,
  c.category as category,
  p.title,
  p.views,
  p.id as post_id
from posts as p
left join categories as c
on p.category_id = c.id
)

-- produce ranked table and order by specified columns - NOT SOLVED
select 
  category_id,
  category,
  title,
  views,
  post_id
from post_categories
where (rank < 3) or (rank is null)
order by
category asc,
views desc,
post_id asc

-- LATERAL JOIN METHOD - NOT SOLVED

-- select categories
select
      l1.id as category_id,
      l1.category,
      l2.title,
      l2.views,
      l2.id as post_id
from  categories as l1

-- lateral left join posts
left join lateral (
                    select *
                    from posts
                    where category_id = l1.id
                    order by  views desc,
                              id asc
                    limit 2
                          
) as l2
on true

-- where condition


-- order by
order by  l1.category asc,
          l2.views desc,
          l2.id asc;
          

-- **************************************************************************************************************
--     Count IP Address
--     https://www.codewars.com/kata/526989a41034285187000de4/train/sql
--     Status: Not Solved
-- **************************************************************************************************************


-- sum all differences of ip address components
SELECT id,

          -- cast final solution to bigint
          CAST((
          
          -- multiply difference between last and first digits to the power of 1, 2, 3, 4 respectively
          (CAST(SPLIT_PART(last, '.', 1) AS bigint) - CAST(SPLIT_PART(first, '.', 1) AS bigint))*256^3 +
          (CAST(SPLIT_PART(last, '.', 2) AS bigint) - CAST(SPLIT_PART(first, '.', 2) AS bigint))*256^2 +
          (CAST(SPLIT_PART(last, '.', 3) AS bigint) - CAST(SPLIT_PART(first, '.', 3) AS bigint))*256^1 +
          (CAST(SPLIT_PART(last, '.', 4) AS bigint) - CAST(SPLIT_PART(first, '.', 4) AS bigint))*256^0
          
          ) AS bigint) AS ips_between
          
FROM ip_addresses 

-- **************************************************************************************************************
--     Two actors who cast together the most
--     https://www.codewars.com/kata/5818bde9559ff58bd90004a2/train/sql
--     Status: Not Solved
-- **************************************************************************************************************

-- CTE
WITH collaborations AS (
  SELECT
    fa.actor_id,
    fa.film_id,
    CONCAT(act.first_name,' ',act.last_name) as "actor",
    flm.title
  FROM film_actor as fa
  LEFT JOIN actor AS act ON fa.actor_id = act.actor_id
  LEFT JOIN film AS flm ON fa.film_id = flm.film_id
)

-- GET COMBINATIONS WITH CROSS JOIN
SELECT
  first_collab.actor_id   AS "actor_first_id",
  second_collab.actor_id  AS "actor_second_id",
  (SELECT COUNT(*) FROM (
    -- SELECT FILM_ID WHERE FIRST_ACTOR AND SECOND_ACTOR IN ACTOR_ID
    SELECT
      COUNT(DISTINCT c.film_id)
    FROM collaborations AS c
    WHERE c.actor_id IN (first_collab.actor_id, second_collab.actor_id)
    GROUP BY c.film_id
    HAVING COUNT(c.film_id) > 1
  ) AS cnt_collab)        AS collaboration_cnt
FROM (
      --   first actor
      SELECT 
        DISTINCT actor_id
      FROM collaborations AS collab
) AS first_collab

CROSS JOIN (
      --   second_actor
      SELECT 
        DISTINCT actor_id
      FROM collaborations AS collab
) AS second_collab
WHERE first_collab.actor_id < second_collab.actor_id
-- ORDER BY first_collab.actor_id ASC, second_collab.actor_id ASC;
ORDER BY collaboration_cnt DESC;

-- -- GET COMBINATIONS BY GROUPING ACTOR AND TITLE
-- SELECT 
--   COUNT(*)
-- FROM (
--   SELECT
--     COUNT(c.film_id)
--   FROM collaborations AS c
--   WHERE (c.actor_id IN (165, 166))
--   GROUP BY c.film_id
--   HAVING COUNT(c.film_id) > 1
--   ORDER BY "count" DESC
-- ) as test


