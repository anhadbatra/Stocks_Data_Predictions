{{ config(materialized='table', schema='final_dm') }}

WITH stock_dm AS (
    SELECT
        date_key,
        open,
        high,
        low,
        close,
        volume,
        polarity,
        compound,
        pos,
        neu,
        neg,
        positive_keywords,
        negative_keywords
    FROM {{ source('stock_facttable', 'fact_stock') }}
),

stock_dw AS (
    SELECT
        stock_dm.date_key,
        stock_dm.open,
        stock_dm.high,
        stock_dm.low,
        stock_dm.close,
        stock_dm.volume,
        stock_dm.polarity,
        stock_dm.compound,
        stock_dm.pos,
        stock_dm.neu,
        stock_dm.neg,
        stock_dm.positive_keywords,
        stock_dm.negative_keywords
    FROM stock_dm
    WHERE
        stock_dm.date_key IS NOT NULL AND
        stock_dm.open IS NOT NULL AND
        stock_dm.high IS NOT NULL AND
        stock_dm.low IS NOT NULL AND
        stock_dm.close IS NOT NULL AND
        stock_dm.volume IS NOT NULL AND
        stock_dm.polarity IS NOT NULL AND
        stock_dm.compound IS NOT NULL AND
        stock_dm.pos IS NOT NULL AND
        stock_dm.neu IS NOT NULL AND
        stock_dm.neg IS NOT NULL AND
        stock_dm.positive_keywords IS NOT NULL AND
        stock_dm.negative_keywords IS NOT NULL
)

SELECT * FROM stock_dw
