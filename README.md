# 🚖 Uber EDA Project

This project is an **Exploratory Data Analysis (EDA)** of Uber's ride request data. The main objectives are to identify patterns in customer demand, supply availability, and peak hour bottlenecks that affect service reliability.

## 📊 Key Objectives

- Identify the **demand-supply gap** and its business implications
- Analyze **peak hours** and their correlation with trip status (Completed, Cancelled, No Cars Available)
- Uncover patterns based on **pickup points** (City vs Airport)
- Suggest actionable insights to improve Uber’s service quality

## 🧾 Dataset

- Source: Provided by [Labmentix] during internship
- Time Period: Includes request and drop timestamps
- Key Columns: Request ID, Pickup Point, Driver ID, Status, Timestamps

> 📁 The dataset has been cleaned and wrangled for accurate analysis.

## 📌 Key Findings

- Morning and evening **peak hours show maximum cancellations or unavailability**.
- **Airport to City** rides experience higher no-car-available incidents.
- **City to Airport** rides face more cancellations due to driver reluctance during high traffic.

## 📈 Visualizations

More than 20 meaningful charts were created using:
- Univariate, Bivariate, and Multivariate Analysis
- Matplotlib & Seaborn
- Business context embedded in insights

## 🛠 Tools & Technologies

- Python
- Pandas, NumPy
- Seaborn, Matplotlib
- Jupyter Notebook

## 📁 Repository Structure
