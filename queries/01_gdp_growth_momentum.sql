-- GDP growth momentum by country, ranked within each year 
-- Source `bigquery-public-data.world_bank_wdi.indicators_data`
-- Indicator code: NY.GDP.MKTP.KD.ZG = "GDP growth (annual %)"


WITH gdp_growth AS (
    SELECT country_name, country_code, year, value AS gdp_growth_pct
    FROM `bigquery-public-data.world_bank_wdi.indicators_data`
    WHERE indicator_code = 'NY.GDP.MKTP.KD.ZG'
        AND country_code IN (
            'USA', 'CHN', 'IND', 'PAK', 'BRA')
        AND year >= 2015
        )

    ,growth_with_prior AS (
        SELECT country_name, country_code, year, gdp_growth_pct,
            LAG(gdp_growth_pct) OVER (PARTITION BY country_code ORDER BY year) AS prior_year_growth_pct
        FROM gdp_growth 
    )
    


SELECT 
    country_name
    ,country_code
    , year 
    , CONCAT((ROUND(gdp_growth_pct, 2)), '%') AS gdp_pct_display
    , CONCAT((ROUND(prior_year_growth_pct , 2)), '%') AS  prior_year_growth_display

FROM growth_with_prior
ORDER BY country_name, year;    