
-- Customer table
CREATE TABLE Customer_1(
    Customer_ID INT PRIMARY KEY,
    Name VARCHAR(50),
    Phone VARCHAR(15),
    Address VARCHAR(100)
);

-- Account table
CREATE TABLE Account_1 (
    Account_No INT PRIMARY KEY,
    Customer_ID INT,
    Balance DECIMAL(10,2),
    Type VARCHAR(20),
    FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID)
);

-- Transaction table
CREATE TABLE Transaction_customer (
    Transaction_ID INT PRIMARY KEY,
    Account_No INT,
    Date DATE,
    Amount DECIMAL(10,2),
    Type VARCHAR(10),
    FOREIGN KEY (Account_No) REFERENCES Account(Account_No)
);
