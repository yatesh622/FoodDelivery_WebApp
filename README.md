# 🍽️ Food Delivery Customer & Restaurant Analytics System

## 📌 Project Overview

The Food Delivery Analytics Project is an end-to-end Business Intelligence and Data Analytics solution developed to analyze customer behavior, restaurant performance, sales trends, menu intelligence, and revenue prediction for a food delivery platform.

The project combines:

* SQL for data cleaning and EDA
* Power BI for interactive dashboards
* Python for analytics and machine learning
* Streamlit for web application deployment
* Logistic Regression for predictive modeling

---

# 🎯 Business Problem

Food delivery businesses generate large volumes of transactional and customer data. However, without proper analytics, it becomes difficult to:

* Identify high-performing restaurants
* Understand customer ordering behavior
* Analyze cuisine and pricing trends
* Monitor revenue growth patterns
* Predict high revenue restaurant potential

This project solves these problems through data-driven dashboards and predictive analytics.

---

# 🛠️ Technology Stack

| Technology     | Purpose                          |
| -------------- | -------------------------------- |
| SQL Server     | Data Cleaning, EDA & KPI Queries |
| Power BI       | Dashboard Development            |
| Python         | Data Analysis & Machine Learning |
| Pandas & NumPy | Data Processing                  |
| Plotly         | Interactive Visualizations       |
| Scikit-Learn   | Predictive Modeling              |
| Streamlit      | Web Application Deployment       |
| GitHub         | Version Control                  |

---

# 🗂️ Dataset Overview

The project uses multiple relational datasets:

| Table      | Description                            |
| ---------- | -------------------------------------- |
| USERS      | Customer demographics and profile data |
| ORDERS     | Order transactions and sales data      |
| RESTAURANT | Restaurant details and ratings         |
| MENU       | Menu items, cuisine and pricing        |
| FOOD       | Food item details                      |

---

# 📊 SQL Work

The SQL phase included:

* Data Import into SQL Server
* Exploratory Data Analysis (EDA)
* Data Cleaning & Transformations
* KPI Definitions
* Outlier Detection
* Derived Columns Creation
* Business Query Analysis

### Example KPIs

* Total Revenue
* Total Orders
* Average Order Value
* Repeat Customers
* Weekend Orders Percentage
* Top Revenue Cities
* Top Revenue Restaurants
* Cuisine Revenue Contribution

---

# 📈 Power BI Dashboards

Three interactive dashboards were created:

## 1️⃣ Business & Sales Overview

* Revenue Trend Analysis
* Top Restaurants by Revenue
* Top Cities by Revenue
* Cuisine Revenue Contribution
* KPI Cards

## 2️⃣ Customer & Restaurant Performance

* Customer Age Distribution
* Occupation Analysis
* Top Restaurants by Orders
* Cuisine Preference by Gender
* Customer Segmentation

## 3️⃣ Menu & Pricing Intelligence

* Average Price by Cuisine
* Menu Variety Analysis
* Price Range Distribution
* Top Expensive Menu Items
* Cuisine-wise Menu Analysis

---

# 🤖 Predictive Modeling

A Logistic Regression model was developed to predict whether a restaurant has:

✅ High Revenue Potential
or
⚠️ Low Revenue Potential

## Features Used

* City
* Cuisine
* Restaurant Cost
* Average Menu Price
* Menu Variety
* Unique Cuisine Count

## Model Evaluation

| Metric        |  Score |
| ------------- | -----: |
| Accuracy      | 59.09% |
| Precision     | 68.16% |
| Recall        | 34.51% |
| F1 Score      | 45.82% |
| ROC AUC Score | 64.10% |

---

# 🌐 Streamlit Web Application

The project includes a fully interactive Streamlit web application with:

* Login Authentication
* KPI Dashboard
* Interactive Filters
* Visual Analytics
* Predictive Model Integration
* Downloadable Filtered Data
* Business Insights & Recommendations

### Login Credentials

```txt
User ID: admin
Password: admin123
```

---

# 📌 Key Insights

* A small group of restaurants contributes significantly to overall revenue.
* Certain cuisines dominate sales and menu presence.
* Repeat customer percentage indicates strong customer retention.
* Weekend orders differ significantly from weekday trends.
* Premium cuisines have higher average menu prices.
* Menu diversity positively impacts restaurant revenue potential.

---

# 📚 Business Recommendations

* Expand operations in high-performing cities.
* Improve menu diversity for low-performing restaurants.
* Optimize pricing strategies for better profitability.
* Focus marketing campaigns on repeat customers.
* Promote high-demand cuisines strategically.

---

# ⚠️ Challenges Faced

* Large dataset handling in Streamlit Cloud
* Merge conflict cleanup during deployment
* Memory optimization for live deployment
* Data consistency handling across multiple tables

---

# 🎓 Learning Outcomes

Through this project, the following skills were developed:

* SQL-based data analytics
* Data cleaning & transformation
* Dashboard design principles
* Business intelligence reporting
* Machine learning model deployment
* Streamlit web application development
* GitHub version control & deployment workflows

---

# 📂 Project Structure

```txt
FoodDelivery_WebApp/
│
├── FoodDelivery_WebApp.py
├── requirements.txt
├── runtime.txt
├── logistic_high_revenue_model.pkl
├── scaler.pkl
├── model_features.pkl
├── top_cities.pkl
├── top_cuisines.pkl
├── SQL Files
├── Power BI Dashboards
├── Presentation
└── README.md
```

---

# 🔗 Project Links

## GitHub Repository

[https://github.com/yatesh622/FoodDelivery_WebApp.git](https://github.com/yatesh622/FoodDelivery_WebApp.git)

## Streamlit Web Application

[https://food-delivery-webapp.streamlit.app/](https://food-delivery-webapp.streamlit.app/)

---

# 👨‍💻 Developed By

Yatesh Kumar
[yateshkumar622@gmail.com](mailto:yateshkumar622@gmail.com)
Food Delivery Customer & Restaurant Analytics System
Business Intelligence | Data Analytics | Machine Learning
