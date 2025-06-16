{{ config(materialized='table') }}

WITH stock AS (
    SELECT
        timestamp,
        open,
        high,
        low,
        close,
        volume
    FROM {{ source('stock_dm', 'stock_dm') }}
),

sentiment AS (
    SELECT
        date,
        polarity,
        compound,
        pos,
        neu,
        neg,
        positive_keywords,
        negative_keywords
    FROM {{ source('sentiment_dm', 'sentiment_analysis') }}
),

combined AS (
    SELECT
        COALESCE(stock.timestamp, sentiment.date) AS date_key,
        stock.open,
        stock.high,
        stock.low,
        stock.close,
        stock.volume,
        sentiment.polarity,
        sentiment.compound,
        sentiment.pos,
        sentiment.neu,
        sentiment.neg,
        sentiment.positive_keywords,
        sentiment.negative_keywords
    FROM stock
    FULL OUTER JOIN sentiment
        ON stock.timestamp = sentiment.date
)

SELECT * FROM combined
