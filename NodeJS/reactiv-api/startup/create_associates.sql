CREATE TABLE associate 
(
    ID INT AUTO_INCREMENT PRIMARY KEY, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
    firstName VARCHAR(255), 
    lastName VARCHAR(255), 
    department VARCHAR(255)
);

INSERT INTO associate (firstName, lastName, department) VALUES ('Neel', 'Roshania', 'EHS');