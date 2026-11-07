
CREATE TABLE Employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100),
    department VARCHAR(50),
    salary DECIMAL(10, 2)
);

INSERT INTO Employees (employee_id, employee_name, department, salary)
VALUES
(1, 'User One', 'IT', 50000),
(2, 'User Two', 'HR', 45000);

SELECT employee_id, employee_name, salary
FROM Employees
WHERE salary > 40000;

UPDATE Employees
SET salary = 55000
WHERE employee_id = 1;

DELETE FROM Employees
WHERE employee_id = 2;

ALTER TABLE Employees ADD email VARCHAR(100);

DROP TABLE OldEmployees;
