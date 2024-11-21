# Currency Exchange Rate Monitoring & Email Notification System

This project collects real-time currency exchange data using an API, processes and stores it in a database, and monitors specific conditions to send email notifications via AWS Simple Email Service (SES).

## Overview

The system integrates multiple technologies and services to gather, process, and analyze currency exchange rates:

- **API**: Fetches real-time exchange rate data.
- **Docker**: Containerizes the application for easy deployment.
- **PostgreSQL**: Stores exchange rate data temporarily before processing.
- **Apache Airflow**: Orchestrates and schedules workflows.
- **Celery**: Handles asynchronous tasks, like data fetching.
- **AWS Glue**: Transforms and catalogs data.
- **S3 Buckets**: Stores raw and transformed data.
- **AWS Athena**: Queries transformed data.
- **AWS Redshift**: Data warehousing solution for further analytics.
- **Looker, Quicksight, Power BI**: Data visualization tools for business insights.
- **AWS SES**: Sends email notifications based on specific conditions.

## Features

- **Real-time data collection**: Fetches currency exchange data from an API.
- **Data transformation**: Transforms raw data using AWS Glue.
- **Email notifications**: Sends email alerts when specific conditions on currency exchange rates are met.
- **Data visualization**: Leverages Looker, Quicksight, and Power BI for generating insightful reports.
- **Automated workflows**: Apache Airflow orchestrates all tasks, with Celery managing asynchronous tasks.

## Architecture

1. **Data Ingestion**:
    - The system fetches currency exchange data from an external API.
    - The data is stored temporarily in a PostgreSQL database.

2. **Data Processing & Storage**:
    - The data is transferred to an S3 bucket for raw storage.
    - AWS Glue crawls the data, transforming it into a usable format.
    - Transformed data is saved back to S3 and cataloged.
  
3. **Data Analysis**:
    - AWS Athena queries the transformed data.
    - The data is further processed and loaded into AWS Redshift for advanced analytics.

4. **Visualization**:
    - Tools like Looker, Quicksight, and Power BI are used to visualize the data.
  
5. **Email Alerts**:
    - AWS SES sends an email when the system detects specific thresholds or conditions related to the currency exchange rates.

## Prerequisites

To run this project locally, you'll need:

- Docker
- Python 3.x
- PostgreSQL
- Apache Airflow
- AWS account with SES, Glue, Athena, S3, and Redshift access
- AWS CLI set up and configured

