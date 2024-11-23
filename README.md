# Currency Exchange Rate Monitoring & Email Notification System

This project collects real-time currency exchange data using an API, processes and stores it in a database, and monitors specific conditions to send email notifications via AWS Simple Email Service (SES).

## Overview

The system integrates multiple technologies and services to gather, process, and analyze currency exchange rates:

- **API**: Fetches real-time exchange rate data.
- **Docker**: Containerizes the application for easy deployment.
- **Apache Airflow**: Orchestrates and schedules workflows.
- **PostgreSQL**: Works as the backend database for Airflow orchestration.
- **Celery**: Handles asynchronous tasks, like data fetching.
- **AWS Glue**: Transforms and catalogs data.
- **S3 Buckets**: Stores raw and transformed data.
- **AWS Athena**: Queries transformed data.
- **AWS Redshift**: Data warehousing solution for further analytics.
- **Looker, Quicksight, Power BI**: Data visualization tools for business insights dashboards.
- **AWS SES**: Serve as a gateway to sends email notifications based on specific conditions.

## Features

- **Scheduled-time data collection**: Fetches currency exchange data from an API on defined interval.
- **Data transformation**: Transforms raw data using AWS Glue.
- **Email notifications**: Sends email alerts when specific conditions on currency exchange rates are met.
- **Data visualization**: Leverages Looker, Quicksight, and Power BI for generating insightful reports.
- **Automated workflows**: Apache Airflow orchestrates all tasks, with Celery managing asynchronous tasks.

## Architecture

1. **Data Ingestion**:
    - The system fetches currency exchange data from an external API.
    - The data is stored in raw format in S3 bucket with in raw dirctory.

2. **Data Processing & Storage**:
    - AWS Glue crawls the data, transforming it into any usable/desirable format.
    - AWS Glue serves as a fundamental block to send emails when the system detects specific thresholds or conditions related to the currency exchange rates breaches, AWS SES is integrated within the script to do that.
    - Transformed data is saved back to S3 and cataloged for further use.
    - Transformed data can be saved to a datalake like AWS Redshift for further analytical purposes.
  
3. **Data Analysis**:
    - AWS Athena queries the transformed data via AWS DataCatalog.
    - Or if the data is loaded into AWS Redshift cluster then we can use any of the visualization tools to further work on building and fulfilling our needs.

4. **Visualization**:
    - Tools like Looker, Quicksight, and Power BI are used to visualize the data.
  

## Prerequisites

To run this project locally, you'll need:

- Dockers
- Python 3.x
- AWS account with SES, Glue, Athena, S3, and Redshift access
- AWS CLI set up and configured


![AWS Currency exchange](https://github.com/user-attachments/assets/9064b4e6-25be-49e2-ae79-e18357569003)



Email Alerting based Implementation
![image](https://github.com/user-attachments/assets/25a01a1b-0639-4a6e-82bf-d77a845d0120)



