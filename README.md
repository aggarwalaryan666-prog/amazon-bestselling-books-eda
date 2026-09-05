# 📚 Amazon Bestselling Books — Data Analysis

## 📌 Project Overview

This project performs exploratory data analysis (EDA) on Amazon bestselling books using Python.

The analysis explores book ratings, reviews, prices, genres, authors, and yearly trends to identify useful patterns and insights from the dataset.

## 🎯 Objectives

- Analyze bestselling books by genre
- Study user ratings and reviews
- Analyze book price distribution
- Identify the most reviewed books
- Compare Fiction and Non-Fiction books
- Study relationships between price, reviews, and ratings
- Visualize important patterns using charts

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

## 📊 Analysis Performed

### 1. Data Understanding
- Dataset structure
- Number of rows and columns
- Data types
- Missing values
- Statistical summary

### 2. Exploratory Data Analysis

The project includes visualizations for:

- Book price distribution
- Genre distribution
- Average rating by genre
- Average price by genre
- Average reviews by genre
- Top reviewed books
- Reviews vs User Rating
- Price vs User Rating
- Correlation analysis

## 🔍 Key Findings

- Fiction books have a slightly higher average rating than Non-Fiction books.
- Non-Fiction books have a higher average price than Fiction books.
- Fiction books receive more reviews on average in this dataset.
- "Where the Crawdads Sing" by Delia Owens is among the most reviewed books in the dataset.
- Price and user rating show a very weak linear relationship.

## 📁 Project Structure

```text
amazon-bestselling-books/
│
├── books.csv
├── amazon-bestselling-books-eda.ipynb
├── requirements.txt
├── README.md
│
└── graphs/
    ├── book_price_distribution.png
    ├── genre_distribution.png
    ├── average_rating_by_genre.png
    ├── average_price_by_genre.png
    ├── average_reviews_by_genre.png
    ├── reviews_vs_rating.png
    └── price_vs_rating.png