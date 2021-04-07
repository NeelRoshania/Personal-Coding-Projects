
-- **************************************************************************************************************
--     189 Department Salary
--     https://leetcode.com/problems/department-highest-salary/
--     Status: Solved
-- **************************************************************************************************************

-- left join Department and Employee
with emp_dept as (
select
    e.Name as Employee,
    e.Salary as Salary,
    d.Name as Department
from Employee as e
left join Department as d
on e.DepartmentId = d.Id 
),

-- # Get max salaries for each department
max_salaries_per_dept as (
select 
distinct(Department) as department, max(Salary) as max_salary
from emp_dept
group by Department
)

select
e.Department, e.Employee, e.Salary
from emp_dept as e, max_salaries_per_dept as m
where (e.Department = m.department) and (e.Salary = m.max_salary) 


-- **************************************************************************************************************
--     262 Trips And Users
--     https://leetcode.com/problems/trips-and-users/
--     Status: Solved
-- **************************************************************************************************************

-- get unbanned users and drivers
WITH unbanned_users AS (
    SELECT * 
    FROM Users
    WHERE (Banned = 'No') AND role IN ('client', 'driver')

    -- get unbanned user id's 
),

-- extract unbanned clients and drivers from Trips and date range
    valid_trips AS (
    SELECT *
    FROM Trips AS trips
    WHERE   (trips.Client_Id IN (SELECT Users_Id FROM unbanned_users)) AND
            (trips.Driver_Id IN (SELECT Users_Id FROM unbanned_users)) AND
            (trips.Request_at BETWEEN '2013-10-01' AND '2013-10-03')
    )

-- determine cancellation rate
SELECT
    Request_at AS Day,
    cast(sum(case when status like 'cancelled%' then 1.00 else 0.00 end) /
    COUNT(status) AS DECIMAL(10, 2)) AS 'Cancellation Rate'
FROM valid_trips
GROUP BY Request_at
ORDER BY Day

-- **************************************************************************************************************
--     185 Department Top Three salaries
--     https://leetcode.com/problems/department-top-three-salaries/submissions/
--     Status: Not Solved
-- **************************************************************************************************************

-- left join department and employee
with emp_dep as (
    select 
        d.Name as Department,
        e.Name as Employee,
        e.Salary as Salary
    from Employee as e
    left join Department as d
    on e.DepartmentID = d.Id
),

-- rank salaries by partitioning by department
ranked_salaries as (
    select 
    Department,
    Employee,
    Salary,
    rank() over( partition by Department order by Salary desc ) as rank
    from emp_dep
)

-- return the final table
select
    Department,
    Employee,
    Salary
from ranked_salaries