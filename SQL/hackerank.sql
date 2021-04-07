-- **************************************************************************************************************
--     Triangle
--     https://www.hackerrank.com/challenges/what-type-of-triangle/problem?isFullScreen=true
--     Status: Solved
-- **************************************************************************************************************

select 
    case
        when ((A + B) < C) or (((A + C) < B)) then 'Not A Triangle'
        when (A != B) or (B != C) or (A != C) then 'Scalene'
        when (A = B) or (B = C) or (A = C) then 'Isosceles'
        when (A = B) and (B = C) then 'Equilateral'
        else null end as traingle_type
from TRIANGLES