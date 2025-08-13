# Automated Financial Data Pipeline

## Overview
This is a personal data engineering project I built to strengthen my skills in data pipelines, big data processing, and cloud integration.
It automates the process of collecting stock market data, cleaning and transforming it using PySpark, and storing it securely in Azure Data Lake Gen2.
I wanted to work on a real-world use case where automation, scalability, and security all come together — and the stock market provided the perfect dataset for it.

## Why I built this 
As part of my journey in AI/ML and data engineering, I wanted to:
Learn how to design and implement an end-to-end ETL pipeline.
Get hands-on experience with PySpark for large-scale data transformation.
Integrate with Azure to understand cloud storage and access control.
Automate workflows using Jenkins for real-time scheduling.
This project gave me the opportunity to combine Python, big data frameworks, and cloud technologies in a practical way.

## Features
Automated Data Ingestion – Fetches daily stock data from Yahoo Finance.
Data Transformation with PySpark – Cleans, structures, and optimizes data.
Cloud Storage with Azure Data Lake Gen2 – Organizes raw and processed data securely.
Secure Credentials Management – Uses Azure Key Vault and RBAC for access control.
Jenkins Orchestration – Fully automated daily data refresh.

## Future Enhancements
Add interactive dashboards for visualizing stock trends.
Include advanced financial metrics and KPIs.
Support real-time streaming from live stock APIs.
Implement alert notifications for significant stock movements.

## Technologies Used

* **Programming Language:** Python (with yfinance for API calls). 
* **Big Data Framework:** PySpark (for transformations and processing). 
* **Cloud Platform:** Microsoft Azure (Azure Data Lake Gen2 for storage).
* **Automation Tool:** Jenkins (for pipeline orchestration and monitoring).
* **Security:** Azure Key Vault and RBAC for secure credential and access management. 

## Setup and Usage
1. Prerequisites
Python 3.8+ installed
Azure Data Lake Gen2 account

2. Installation
pip install -r requirements.txt

4. Configuration
Create a .env file:

AZURE_STORAGE_ACCOUNT_NAME=your_account_name
AZURE_STORAGE_ACCOUNT_KEY=your_access_key

4. Run
python data_collector.py
python data_transform.py
python azure_upload.py
