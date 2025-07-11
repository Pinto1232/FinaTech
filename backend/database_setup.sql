-- FinaTech Database Setup Script
-- Run this script in SQL Server Management Studio or sqlcmd

-- Create database
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'FinaTechDB')
BEGIN
    CREATE DATABASE FinaTechDB;
END
GO

USE FinaTechDB;
GO

-- Create Users table
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Users' AND xtype='U')
BEGIN
    CREATE TABLE Users (
        id INT IDENTITY(1,1) PRIMARY KEY,
        name NVARCHAR(100) NOT NULL,
        email NVARCHAR(255) NOT NULL UNIQUE,
        created_at DATETIME2 DEFAULT GETDATE(),
        updated_at DATETIME2 DEFAULT GETDATE()
    );
END
GO

-- Create Transactions table
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Transactions' AND xtype='U')
BEGIN
    CREATE TABLE Transactions (
        id INT IDENTITY(1,1) PRIMARY KEY,
        user_id INT NOT NULL,
        amount DECIMAL(10,2) NOT NULL,
        transaction_type NVARCHAR(50) NOT NULL,
        created_at DATETIME2 DEFAULT GETDATE(),
        FOREIGN KEY (user_id) REFERENCES Users(id)
    );
END
GO

-- Create Events table for Event-Driven Architecture
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Events' AND xtype='U')
BEGIN
    CREATE TABLE Events (
        id INT IDENTITY(1,1) PRIMARY KEY,
        event_type NVARCHAR(100) NOT NULL,
        event_data NVARCHAR(MAX),
        timestamp DATETIME2 DEFAULT GETDATE(),
        processed BIT DEFAULT 0
    );
END
GO

-- Create indexes for better performance
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Users_Email')
BEGIN
    CREATE INDEX IX_Users_Email ON Users(email);
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Transactions_UserId')
BEGIN
    CREATE INDEX IX_Transactions_UserId ON Transactions(user_id);
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Events_Type_Timestamp')
BEGIN
    CREATE INDEX IX_Events_Type_Timestamp ON Events(event_type, timestamp);
END
GO

-- Insert sample data
IF NOT EXISTS (SELECT * FROM Users)
BEGIN
    INSERT INTO Users (name, email) VALUES 
    ('John Doe', 'john.doe@example.com'),
    ('Jane Smith', 'jane.smith@example.com'),
    ('Bob Johnson', 'bob.johnson@example.com');
END
GO

PRINT 'Database setup completed successfully!';