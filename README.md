# INTEGRATING-AI-MODELS-FOR-VOLTAGE-AND-CURRENT-MONITORING-IN-AUTONOMOUS-MOBILE-ROBOTS
# AI-Based Voltage and Current Anomaly Detection for Autonomous Mobile Robots (AMRs)

## Project Overview

This project presents an **AI-based predictive monitoring system** designed to detect voltage and current anomalies in **Autonomous Mobile Robots (AMRs)**. Electrical fluctuations such as voltage drops, spikes, or abnormal current consumption can damage robot components and disrupt industrial operations.

The proposed system uses **machine learning regression models** to analyze electrical parameters and predict abnormal conditions before hardware failures occur. A **Flask-based web application** provides an interactive interface for dataset upload, model evaluation, and real-time prediction.

---

## Problem Statement

Autonomous Mobile Robots used in industries rely heavily on stable electrical power for efficient operation. Traditional monitoring systems depend on fixed thresholds and react only after failures occur.

There is a need for a **data-driven predictive system** that continuously analyzes electrical parameters and detects anomalies early to prevent system damage and operational downtime.

---

## Objectives

* Develop an AI-based system to monitor electrical behavior in AMRs.
* Detect anomalies in voltage and current using machine learning models.
* Compare multiple ML algorithms using performance metrics.
* Implement a web interface for dataset upload, model selection, and prediction.
* Provide early warnings for abnormal electrical conditions.

---

## Technologies Used

### Programming Language

* Python

### Framework

* Flask

### Libraries

* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* Joblib

### Frontend

* HTML
* CSS
* JavaScript

### Database

* MySQL / SQL

---

## Machine Learning Models Used

The following regression algorithms were implemented and evaluated:

* Random Forest Regressor
* Extra Trees Regressor
* Decision Tree Regressor
* Gradient Boosting Regressor
* XGBoost Regressor
* K-Nearest Neighbors (KNN)

Models were evaluated using:

* Mean Squared Error (MSE)
* R² Score

The **Random Forest model** achieved the best performance with:

* **MSE = 0.0027**
* **R² Score = 0.9985**

---

## Dataset Description

The dataset used in this project is based on **electrical power consumption measurements**.

Main features used for prediction include:

* Global Reactive Power
* Voltage
* Global Intensity
* Sub Metering 1
* Sub Metering 2
* Sub Metering 3

These parameters represent electrical behavior and help identify abnormal energy consumption patterns.

---

## System Workflow

1. User registers and logs into the system.
2. User uploads a CSV dataset containing electrical parameters.
3. Data preprocessing is performed (cleaning, validation).
4. Machine learning models are evaluated.
5. The best model is selected for prediction.
6. Users input electrical parameters for real-time prediction.
7. The system predicts voltage behavior.
8. Z-score analysis determines whether the result is **Normal or Anomaly**.

---

## Anomaly Detection Method

The system uses **Z-score statistical analysis** to detect anomalies.

Formula:

Z = (X − μ) / σ

Where:

* X = Predicted voltage
* μ = Mean voltage
* σ = Standard deviation

If the Z-score exceeds the threshold, the system flags it as an **Anomaly**.

---
## Features

* User registration and login
* Dataset upload and visualization
* Multiple ML model evaluation
* Real-time prediction interface
* Z-score based anomaly detection
* Model performance comparison

---

## Future Scope

Future improvements for the system include:

* Integration with real-time IoT sensors in AMRs
* Implementation of deep learning models such as LSTM
* Cloud deployment for large-scale monitoring
* Mobile application for remote monitoring
* Integration with smart grid and industrial IoT systems

---

## Conclusion

This project demonstrates how **machine learning and predictive analytics** can improve the reliability of Autonomous Mobile Robots by detecting electrical anomalies before failures occur.

The proposed system provides an intelligent monitoring framework that enhances **operational safety, predictive maintenance, and energy efficiency** in industrial robotic environments.

