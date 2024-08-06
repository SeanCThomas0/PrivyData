# PrivyData

## Overview

This project is a web application designed to analyze student data while ensuring the privacy of individual records through differential privacy techniques. Differential privacy offers rigorous privacy guarantees, allowing data analysis without compromising individual confidentiality. The OpenDP library is integral to implementing these privacy-preserving measures.

## Tools and Technologies

### Flask

[Flask](https://flask.palletsprojects.com/) is a micro web framework for Python, used to create RESTful APIs for managing data queries and interactions within the application.

### SQLite

[SQLite](https://www.sqlite.org/) is employed as the database engine to store student records in a lightweight, relational database.

### Python

[Python](https://www.python.org/) serves as the primary programming language for backend logic and data processing.

### NumPy

[NumPy](https://numpy.org/) is utilized for numerical operations and statistical computations, such as calculating means and standard deviations.

### Nginx

[Nginx](https://www.nginx.com/) is used as a web server and reverse proxy to handle HTTP requests efficiently and securely.

### Ansible

[Ansible](https://www.ansible.com/) automates deployment and configuration management, ensuring consistency across environments.

### Travis CI

[Travis CI](https://travis-ci.org/) provides continuous integration services to automate testing and deployment processes.

## Differential Privacy with OpenDP

Differential privacy is a framework that ensures individual data points remain confidential even when aggregate data is analyzed. In this project, we use the OpenDP library to apply differential privacy to various data queries and analyses. Here’s a detailed explanation of how OpenDP is leveraged:

1. **Integration of OpenDP:**
   - OpenDP is a comprehensive library for differential privacy that provides tools to apply privacy mechanisms to data. We import OpenDP’s modules to access various privacy-preserving transformations and measurements.

2. **Data Transformation and Noise Addition:**
   - We use OpenDP’s functionality to add noise to statistical outputs, thereby protecting individual data points. For example, we utilize the Laplace mechanism from OpenDP to introduce noise into aggregate statistics such as counts, sums, and means. This noise masks individual contributions while preserving the overall utility of the data.

3. **Implementation Details:**
   - **Data Preparation:** We use OpenDP’s transformations to process raw data into a format suitable for privacy analysis. This includes converting data into dataframes and selecting relevant columns.
   - **Casting and Imputation:** OpenDP’s transformation functions are used to cast data types (e.g., converting string representations of numbers into integers) and handle missing values with default imputation.
   - **Privacy Measurement:** We apply OpenDP’s measurement tools to evaluate the privacy budget for each query. This involves calculating the amount of noise required to achieve a desired level of differential privacy and estimating the privacy expenditure for various queries.

4. **Privacy Budget Management:**
   - OpenDP provides tools for estimating and managing the privacy budget, which balances privacy and utility. We use OpenDP’s utilities to perform binary searches for optimal noise scales and to evaluate the privacy guarantees (epsilon) for our statistical releases.

5. **Aggregate Privacy Releases:**
   - By applying differential privacy to aggregate statistics (e.g., mean, sum), we ensure that the results provide useful insights without disclosing sensitive information about any individual. OpenDP’s library allows us to release these statistics in a differentially private manner.

6. **Privacy Compliance:**
   - The application adheres to differential privacy standards using OpenDP to ensure compliance with privacy regulations. This provides users with strong assurances that their data remains confidential and protected from re-identification.
