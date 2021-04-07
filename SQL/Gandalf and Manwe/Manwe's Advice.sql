/*

Remove ALL comments to successfully pass the test.

s1 = Subquery 1.
s2 = Subquery 2. 

*/

SELECT s1.id AS category_id,
       s1.category,
       s2.title,
       s2.views,
       s2.post_id
FROM categories AS s1
     -- Use LEFT JOIN so that we keep all categories regardless of whether the category has any posts.
     -- LATERAL iterates over each row in s1 and allows us to use the s1 columns (id and category) in the next subquery.
     LEFT JOIN LATERAL (SELECT p.title,
                               p.views,
                               p.id AS post_id
                        FROM posts AS p
                        WHERE p.category_id = s1.id
                        -- ORDER BY views and id to break a tie.
                        ORDER BY p.views DESC,
                                 p.id ASC
                        -- For every category, only return the two posts with the most views.
                        LIMIT 2
                       ) AS s2
    -- 'ON true' looks weird, but it is okay because we already join the rows accordingly in the WHERE clause above.
    -- See 'ON true' as 'While True' in Python. Just join the columns because we already did the check above.
    ON true
ORDER BY s1.category ASC,
         s2.views DESC,
         s2.post_id ASC

/*
 
---------------------------------------------------------------
What s1 looks like (CONCEPTUALLY):
---------------------------------------------------------------
category_id    category
1              'art'
2              'business'
3              'sport'


---------------------------------------------------------------
What s2 looks like (CONCEPTUALLY):
---------------------------------------------------------------
category_id (invisible)  title    views    post_id
(1)                      'aaa'    9234     234
(1)                      'bbb'    9234     712    
----> Only the first two rows get selected.
(1)                      'ccc'    9234     800

(2)                      ...
(3)                      ...


---------------------------------------------------------------
Result set (CONCEPTUALLY):
---------------------------------------------------------------
category_id    category    title    views    post_id
1              'art'       'aaa'    9234     234
1              'art'       'bbb'    9234     712  
...

*/