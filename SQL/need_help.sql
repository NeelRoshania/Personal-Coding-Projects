-- **************************************************************************************************************
--     SQL Basics: Simple WITH
--     https://www.codewars.com/kata/5820176255c3d23f360000a9/train/sql
--     Status: NOT SOLVED
-- **************************************************************************************************************

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

-- produce ranked table and order by specified columns
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

-- **************************************************************************************************************
--     SQL Basics: Simple NULL handling
--     https://www.codewars.com/kata/5811315e04adbbdb5000050e/train/sql
--     Status: NOT SOLVED
-- **************************************************************************************************************

-- Coalesce name and card_name to requred output if null
with processed_eusales as (
select
  id,
  coalesce(name, 'product name not found') as name, 
  nullif(NULL, price) as price,
  coalesce(card_name, 'card name not found') as card_name,
  card_number,
  transaction_date
from eusales
)

-- Then filter for price and remove null rows
select *
from processed_eusales
where (price > 50.00) and (price is not null);