CREATE DATABASE ViralVerse;
USE ViralVerse;

CREATE TABLE Platform (
    platform_id INT PRIMARY KEY IDENTITY(1,1),
    platform_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE Content_Type (
    content_type_id INT PRIMARY KEY IDENTITY(1,1),
    content_type_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE Topic (
    topic_id INT PRIMARY KEY IDENTITY(1,1),
    topic_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE Location (
    location_id INT PRIMARY KEY IDENTITY(1,1),
    language VARCHAR(50),
    region VARCHAR(50),
    UNIQUE(language, region)
);

CREATE TABLE Hashtag (
    hashtag_id INT PRIMARY KEY IDENTITY(1,1),
    hashtag_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE Post (
    post_id VARCHAR(30) PRIMARY KEY,
    platform_id INT,
    content_type_id INT,
    topic_id INT,
    location_id INT,
    post_datetime DATETIME,
    views BIGINT,
    likes BIGINT,
    comments BIGINT,
    shares BIGINT,
    engagement_rate DECIMAL(10,6),
    sentiment_score DECIMAL(10,6),
    is_viral BIT,

    FOREIGN KEY (platform_id) REFERENCES Platform(platform_id),
    FOREIGN KEY (content_type_id) REFERENCES Content_Type(content_type_id),
    FOREIGN KEY (topic_id) REFERENCES Topic(topic_id),
    FOREIGN KEY (location_id) REFERENCES Location(location_id)
);

CREATE TABLE Post_Hashtag (
    post_id VARCHAR(30),
    hashtag_id INT,

    PRIMARY KEY (post_id, hashtag_id),

    FOREIGN KEY (post_id) REFERENCES Post(post_id),
    FOREIGN KEY (hashtag_id) REFERENCES Hashtag(hashtag_id)
);

USE ViralVerse;

CREATE TABLE Raw_SocialMedia (
    post_id VARCHAR(30),
    platform VARCHAR(50),
    content_type VARCHAR(50),
    topic VARCHAR(50),
    language VARCHAR(20),
    region VARCHAR(50),
    post_datetime DATETIME,
    hashtags VARCHAR(1000),
    views BIGINT,
    likes BIGINT,
    comments BIGINT,
    shares BIGINT,
    engagement_rate DECIMAL(10,6),
    sentiment_score DECIMAL(10,6),
    is_viral BIT
);

USE ViralVerse;

BULK INSERT Raw_SocialMedia
FROM 'C:\Users\Admin\Desktop\coding\DATA ANALYSIS BOOTCAMP\social_media_viral_content_dataset.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    TABLOCK
);

ALTER TABLE Raw_SocialMedia
ALTER COLUMN post_datetime VARCHAR(50);

TRUNCATE TABLE Raw_SocialMedia;


SELECT COUNT(*) AS Total_Rows
FROM Raw_SocialMedia;

-- 1. Check sample records
SELECT TOP 10 *
FROM Raw_SocialMedia;

-- 2. Check platforms
SELECT platform, COUNT(*) AS post_count
FROM Raw_SocialMedia
GROUP BY platform;

-- 3. Check viral vs non-viral
SELECT is_viral, COUNT(*) AS post_count
FROM Raw_SocialMedia
GROUP BY is_viral;

USE ViralVerse;

-- 1. Platforms
INSERT INTO Platform (platform_name)
SELECT DISTINCT platform
FROM Raw_SocialMedia;


-- 2. Content Types
INSERT INTO Content_Type (content_type_name)
SELECT DISTINCT content_type
FROM Raw_SocialMedia;


-- 3. Topics
INSERT INTO Topic (topic_name)
SELECT DISTINCT topic
FROM Raw_SocialMedia;


-- 4. Language + Region
INSERT INTO Location (language, region)
SELECT DISTINCT language, region
FROM Raw_SocialMedia;


-- 5. Hashtags
INSERT INTO Hashtag (hashtag_name)
SELECT DISTINCT LTRIM(RTRIM(value))
FROM Raw_SocialMedia
CROSS APPLY STRING_SPLIT(hashtags, ' ')
WHERE LTRIM(RTRIM(value)) <> '';

USE ViralVerse;

INSERT INTO Post (
    post_id,
    platform_id,
    content_type_id,
    topic_id,
    location_id,
    post_datetime,
    views,
    likes,
    comments,
    shares,
    engagement_rate,
    sentiment_score,
    is_viral
)
SELECT
    r.post_id,
    p.platform_id,
    ct.content_type_id,
    t.topic_id,
    l.location_id,
    TRY_CONVERT(DATETIME, r.post_datetime, 105),
    r.views,
    r.likes,
    r.comments,
    r.shares,
    r.engagement_rate,
    r.sentiment_score,
    r.is_viral
FROM Raw_SocialMedia r
JOIN Platform p
    ON r.platform = p.platform_name
JOIN Content_Type ct
    ON r.content_type = ct.content_type_name
JOIN Topic t
    ON r.topic = t.topic_name
JOIN Location l
    ON r.language = l.language
    AND r.region = l.region;

    SELECT TOP 10 *
FROM Post;


USE ViralVerse;

INSERT INTO Post_Hashtag (post_id, hashtag_id)
SELECT DISTINCT
    r.post_id,
    h.hashtag_id
FROM Raw_SocialMedia r
CROSS APPLY STRING_SPLIT(r.hashtags, ' ') s
JOIN Hashtag h
    ON h.hashtag_name = LTRIM(RTRIM(s.value));


    SELECT TOP 20
    p.post_id,
    pl.platform_name,
    ct.content_type_name,
    t.topic_name,
    l.language,
    l.region,
    p.views,
    p.likes,
    p.comments,
    p.shares,
    p.engagement_rate,
    p.is_viral
FROM Post p
JOIN Platform pl
    ON p.platform_id = pl.platform_id
JOIN Content_Type ct
    ON p.content_type_id = ct.content_type_id
JOIN Topic t
    ON p.topic_id = t.topic_id
JOIN Location l
    ON p.location_id = l.location_id;


--Display all posts from Instagram
SELECT p.post_id, p.views, p.likes, p.comments
FROM Post p
JOIN Platform pl ON p.platform_id = pl.platform_id
WHERE pl.platform_name = 'Instagram';

--Find viral posts
SELECT post_id, views, likes, comments, shares
FROM Post
WHERE is_viral = 1;

--Top 10 posts by views
SELECT TOP 10 post_id, views, likes, shares
FROM Post
ORDER BY views DESC;

--Platform-wise number of posts
SELECT pl.platform_name,
       COUNT(*) AS total_posts
FROM Post p
JOIN Platform pl ON p.platform_id = pl.platform_id
GROUP BY pl.platform_name
ORDER BY total_posts DESC;

--Platform-wise average engagement
SELECT pl.platform_name,
       ROUND(AVG(p.engagement_rate), 4) AS avg_engagement
FROM Post p
JOIN Platform pl ON p.platform_id = pl.platform_id
GROUP BY pl.platform_name
ORDER BY avg_engagement DESC;

--Topic-wise average views
SELECT t.topic_name,
       AVG(p.views) AS avg_views
FROM Post p
JOIN Topic t ON p.topic_id = t.topic_id
GROUP BY t.topic_name
ORDER BY avg_views DESC;

--Count viral posts by platform
SELECT pl.platform_name,
       COUNT(*) AS viral_posts
FROM Post p
JOIN Platform pl ON p.platform_id = pl.platform_id
WHERE p.is_viral = 1
GROUP BY pl.platform_name
ORDER BY viral_posts DESC;

--Most-used hashtags
SELECT h.hashtag_name,
       COUNT(*) AS usage_count
FROM Post_Hashtag ph
JOIN Hashtag h ON ph.hashtag_id = h.hashtag_id
GROUP BY h.hashtag_name
ORDER BY usage_count DESC;

--Viral posts by topic
SELECT t.topic_name,
       COUNT(*) AS viral_posts
FROM Post p
JOIN Topic t ON p.topic_id = t.topic_id
WHERE p.is_viral = 1
GROUP BY t.topic_name
ORDER BY viral_posts DESC;

--Average engagement of viral vs non-viral posts
SELECT
    CASE
        WHEN is_viral = 1 THEN 'Viral'
        ELSE 'Not Viral'
    END AS post_category,
    ROUND(AVG(engagement_rate), 4) AS avg_engagement
FROM Post
GROUP BY is_viral;

--Platform with the highest average engagement
SELECT TOP 1
    pl.platform_name,
    ROUND(AVG(p.engagement_rate) * 100, 2) AS avg_engagement_percent
FROM Post p
JOIN Platform pl
    ON p.platform_id = pl.platform_id
GROUP BY pl.platform_name
ORDER BY avg_engagement_percent DESC;

--Topics with more than 100 viral posts
SELECT
    t.topic_name,
    COUNT(*) AS viral_posts
FROM Post p
JOIN Topic t
    ON p.topic_id = t.topic_id
WHERE p.is_viral = 1
GROUP BY t.topic_name
HAVING COUNT(*) > 100
ORDER BY viral_posts DESC;

--Countries/regions with the most viral posts
SELECT
    l.region,
    COUNT(*) AS viral_posts
FROM Post p
JOIN Location l
    ON p.location_id = l.location_id
WHERE p.is_viral = 1
GROUP BY l.region
ORDER BY viral_posts DESC;

--Content type with highest average views
SELECT
    ct.content_type_name,
    ROUND(AVG(p.views), 0) AS avg_views
FROM Post p
JOIN Content_Type ct
    ON p.content_type_id = ct.content_type_id
GROUP BY ct.content_type_name
ORDER BY avg_views DESC;

--Viral posts with engagement above the overall average
SELECT
    p.post_id,
    p.views,
    p.engagement_rate
FROM Post p
WHERE p.is_viral = 1
AND p.engagement_rate >
    (SELECT AVG(engagement_rate)
     FROM Post)
ORDER BY p.engagement_rate DESC;

--Most popular hashtags in viral posts
SELECT
    h.hashtag_name,
    COUNT(*) AS viral_post_count
FROM Post_Hashtag ph
JOIN Post p
    ON ph.post_id = p.post_id
JOIN Hashtag h
    ON ph.hashtag_id = h.hashtag_id
WHERE p.is_viral = 1
GROUP BY h.hashtag_name
ORDER BY viral_post_count DESC;

--Platform + topic analysis
SELECT
    pl.platform_name,
    t.topic_name,
    COUNT(*) AS total_posts,
    SUM(CASE WHEN p.is_viral = 1 THEN 1 ELSE 0 END) AS viral_posts
FROM Post p
JOIN Platform pl
    ON p.platform_id = pl.platform_id
JOIN Topic t
    ON p.topic_id = t.topic_id
GROUP BY pl.platform_name, t.topic_name
ORDER BY pl.platform_name, viral_posts DESC;

--Highest-viewed viral post for each platform
SELECT
    pl.platform_name,
    MAX(p.views) AS highest_views
FROM Post p
JOIN Platform pl
    ON p.platform_id = pl.platform_id
WHERE p.is_viral = 1
GROUP BY pl.platform_name
ORDER BY highest_views DESC;

--Average sentiment of viral vs non-viral
SELECT
    CASE
        WHEN is_viral = 1 THEN 'Viral'
        ELSE 'Not Viral'
    END AS category,
    ROUND(AVG(sentiment_score), 3) AS avg_sentiment
FROM Post
GROUP BY is_viral;

--Platform-wise viral percentage
SELECT
    pl.platform_name,
    COUNT(*) AS total_posts,
    SUM(CASE WHEN p.is_viral = 1 THEN 1 ELSE 0 END) AS viral_posts,
    ROUND(
        100.0 * SUM(CASE WHEN p.is_viral = 1 THEN 1 ELSE 0 END)
        / COUNT(*), 2
    ) AS viral_percentage
FROM Post p
JOIN Platform pl
    ON p.platform_id = pl.platform_id
GROUP BY pl.platform_name
ORDER BY viral_percentage DESC;