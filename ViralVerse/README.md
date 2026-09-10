# ViralVerse 📱🔥

### A Relational Database for Understanding Social Media Virality

ViralVerse is an RDBMS project built using Microsoft SQL Server to analyze social media content, engagement, hashtags, platforms, topics, languages, and regions.

## 🎯 Objective

The objective of this project is to design a normalized relational database and use SQL queries to identify patterns associated with viral social media content.

## 📊 Dataset

The project uses the **Social Media Viral Content & Engagement Metrics** dataset from Kaggle.

The dataset contains 2,000 social media posts and 15 attributes including:

- Platform
- Content Type
- Topic
- Language
- Region
- Post Date/Time
- Hashtags
- Views
- Likes
- Comments
- Shares
- Engagement Rate
- Sentiment Score
- Viral Status

## 🛠️ Technology

- Microsoft SQL Server
- SQL
- Kaggle Dataset
- GitHub

## 🗄️ Database Design

The database contains the following normalized tables:

- Platform
- Content_Type
- Topic
- Location
- Post
- Hashtag
- Post_Hashtag

The `Post_Hashtag` table represents the many-to-many relationship between posts and hashtags.

## 🔑 RDBMS Concepts Demonstrated

- Primary Keys
- Foreign Keys
- Normalization
- 1NF
- 2NF
- 3NF
- One-to-Many Relationships
- Many-to-Many Relationships
- JOIN
- GROUP BY
- HAVING
- Aggregate Functions
- Subqueries
- Conditional Expressions

## 🔍 Example Analysis

The database can answer questions such as:

- Which platform has the highest average engagement?
- Which topics produce the most viral posts?
- Which hashtags are most frequently associated with viral content?
- Which regions have the most viral posts?
- Which content types receive the highest average views?
- What percentage of posts are viral on each platform?
- How does sentiment differ between viral and non-viral posts?

## 📐 ER Diagram

![ViralVerse ER Diagram](ER_Diagram.png)

## 📁 Project Structure

```text
ViralVerse/
│
├── ViralVerse_Complete.sql
├── ER_Diagram.png
└── README.md
