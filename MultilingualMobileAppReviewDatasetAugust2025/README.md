# **Multilingual Mobile App Review Analysis**

This project presents a comprehensive analysis of the "Multilingual Mobile App Reviews Dataset 2025" from Kaggle. The primary goal was to perform a full-cycle data analysis project: from cleaning and preprocessing a messy, realistic
dataset to uncovering insights through exploratory data analysis (EDA) and statistical testing, and finally, deploying
The findings are in an interactive web application.

## **🚀 Live Demo**

You can explore the findings and interact with the data through the live Streamlit dashboard:

[**➡️ View the Interactive Dashboard**](https://multilingual-mobile-app-reviews.streamlit.app/)

![alt text](https://github.com/SandyCompetent/Kaggle-Analysis-Showcase/blob/main/MultilingualMobileAppReviewDatasetAugust2025/Output/streamlit_output_01.jpg)


## **📊 The Dataset**

The project utilises a synthetic dataset containing over 2,500 mobile app reviews across 40+ popular applications and 24
different languages. It was intentionally designed with data quality issues like missing values and mixed data types to
provide a practical data cleaning challenge.

* Dataset: [Multilingual Mobile App Reviews Dataset 2025 on Kaggle](https://www.kaggle.com/datasets/pratyushpuri/multilingual-mobile-app-reviews-dataset-2025/data)

## **🔑 Key Findings & Visualizations**

The analysis, conducted in a Jupyter Notebook, revealed several interesting patterns in the data.

### **Analysis Overview**

The general distribution of ratings is fairly balanced, with a mean rating of **3.02**. When categorized, 'Average'
And 'Poor' reviews are the most frequent, suggesting users are more vocal when an experience isn't perfect.

![alt text](https://github.com/SandyCompetent/Kaggle-Analysis-Showcase/blob/main/MultilingualMobileAppReviewDatasetAugust2025/Output/output_01.png)

### **Correlations and Demographics**

Surprisingly, the analysis showed no significant correlation between a user's age or the length of their review and the
final rating they gave. An ANOVA test further confirmed that there were no statistically significant differences in
average ratings across the 18 different app categories (p-value \> 0.05).

![alt text](https://github.com/SandyCompetent/Kaggle-Analysis-Showcase/blob/main/MultilingualMobileAppReviewDatasetAugust2025/Output/output_02.png)

## **🛠️ Technical Stack**

* **Language:** Python
* **Libraries:**
    * Data Manipulation: Pandas, NumPy
    * Data Visualisation: Matplotlib, Seaborn, Plotly
    * Statistical Analysis: SciPy
    * Web App Framework: Streamlit

## **📂 Project Links**

* Interactive App:
  [https://multilingual-mobile-app-reviews.streamlit.app/](https://multilingual-mobile-app-reviews.streamlit.app/)
* Kaggle Notebook:
  [View the full analysis on Kaggle](https://www.kaggle.com/code/sandeepmalviya/multilingual-app-review-analysis)
* Dataset Source:
  [Kaggle Dataset Page](https://www.kaggle.com/datasets/pratyushpuri/multilingual-mobile-app-reviews-dataset-2025/data)
* GitHub Repository:
  [https://github.com/SandyCompetent/Kaggle-Analysis-Showcase](https://github.com/SandyCompetent/Kaggle-Analysis-Showcase)

## **⚙️ How to Run Locally**

To run the Streamlit application on your local machine, follow these steps:

1. **Clone the repository:**  
```
   git clone https://github.com/SandyCompetent/Kaggle-Analysis-Showcase.git  
   cd Kaggle-Analysis-Showcase/MultilingualMobileAppReviewDatasetAugust2025
```
2. **Install the required dependencies:**
```
   pip install -r requirements.txt
```
3. **Run the Streamlit app:**
```
   streamlit run streamlit_app.py
```
