-- 创建数据库
CREATE DATABASE BILLIONAIRES
    DEFAULT CHARACTER SET = 'utf8mb4';

-- 使用数据库
USE BILLIONAIRES;

-- 创建Billionaire表
CREATE TABLE IF NOT EXISTS Billionaire (
    personName VARCHAR(255) PRIMARY KEY,
    age INT,
    gender VARCHAR(10),
    `rank` INT,
    finalWorth DOUBLE,
    source VARCHAR(255),
    country VARCHAR(255),
    city VARCHAR(255),
    countryOfCitizenship VARCHAR(255),
    organization VARCHAR(255),
    selfMade VARCHAR(10),
    status VARCHAR(10),
    birthDate DATE,
    lastName VARCHAR(255),
    firstName VARCHAR(255),
    title VARCHAR(255),
    date DATE,
    state VARCHAR(255),
    residenceStateRegion VARCHAR(255),
    birthYear INT,
    birthMonth INT,
    birthDay INT
);

-- 创建Industry表
CREATE TABLE IF NOT EXISTS Industry (
    industryId INT AUTO_INCREMENT PRIMARY KEY,
    industryName VARCHAR(255),
    category VARCHAR(255)
);

-- 创建BillionaireIndustry表
CREATE TABLE IF NOT EXISTS BillionaireIndustry (
    personName VARCHAR(255),
    industryId INT,
    FOREIGN KEY (personName) REFERENCES Billionaire(personName),
    FOREIGN KEY (industryId) REFERENCES Industry(industryId)
);

-- 创建Country表
CREATE TABLE IF NOT EXISTS Country (
    country VARCHAR(255) PRIMARY KEY,
    cpi_country DOUBLE,
    cpi_change_country DOUBLE,
    gdp_country VARCHAR(255),
    gross_tertiary_education_enrollment DOUBLE,
    gross_primary_education_enrollment_country DOUBLE,
    life_expectancy_country DOUBLE,
    tax_revenue_country_country DOUBLE,
    total_tax_rate_country DOUBLE,
    population_country DOUBLE,
    latitude_country DOUBLE,
    longitude_country DOUBLE
);
