# Predicting Customer Purchase Behavior  
### Instacart Market Basket Analysis

This project uses the **Instacart Market Basket Analysis** dataset to predict which products a customer is likely to purchase in their **next order**. It includes data preparation, exploratory analysis, feature engineering, and machine learning models for next-product recommendation.

---

## 📌 Project Objective
To build a model that recommends **top products** a customer will likely buy next based on:
- Past purchase history  
- User–product interaction patterns  
- Product popularity and reorder behavior  

This reflects real-world systems used by e-commerce platforms to personalize shopping experiences.

---

## 📂 Dataset Overview
The project uses the public **Instacart** dataset from Kaggle, consisting of over 3 million grocery orders.

Main files include:
- `orders.csv` – customer orders  
- `order_products__prior.csv` – items from previous orders  
- `order_products__train.csv` – items used as target labels  
- `products.csv` – product details  
- `aisles.csv`, `departments.csv` – metadata  

---

## 🔍 Exploratory Data Analysis (EDA)
The EDA explores:
- Ordering frequency per user  
- Basket size distribution  
- Hour/day purchasing patterns  
- Top products and reorder rates  
- Product co-occurrence behavior  
- User purchase habits over time  

Insights from EDA help shape useful features for modeling.

---

## 🛠️ Feature Engineering

### User-Level Features
- Number of orders  
- Average basket size  
- Days since prior order  
- Most active shopping times  

### Product-Level Features
- Total purchases  
- Reorder probability  
- Product popularity score  

### User–Product Interaction Features
- Total times user bought the product  
- Recency of last purchase  
- User-level reorder ratio  
- Orders since last purchase  

These features form the training data for machine learning models.

---

## 🤖 Modeling Approach

### Baseline Methods
- Most popular products  
- User's frequently purchased items  
- Items from last basket  

### Machine Learning Models


---

## 📈 Evaluation Metrics
  


---

## 📁 Project Structure


