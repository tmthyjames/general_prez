%%sql DB=econ MAKE_GLOBAL=df NOTIFY=3
SELECT *,
    CASE
        WHEN num_of_sb > 0 THEN TRUE
        ELSE FALSE
    END AS has_starbucks
FROM ( 
        SELECT DISTINCT 
            ST_Area(postal.geom::geography) / 1609.34^2 AS sq_miles,
            "HC03_VC96",
            "HC01_VC03",
            "HC01_VC103",
            "HC03_VC67",
            "HC03_VC68",
            "HC03_VC88",
            "HC03_VC49",
            "HC01_VC88",
            "HC03_VC135",
            "HC03_VC136",
            "HC03_VC92",
            z."HC03_VC12",
            z."HC03_VC41",
            "HC03_VC43",
            "HC03_VC161",
            "HC01_VC118",
            z."HC03_VC171",
            "HC03_VC87",
            zn.*,
            z.starbucks_count,
            sqrt("HC01_VC03") AS "HC01_VC03_sqrt",
            count(sb."zipcode") OVER ( PARTITION BY sb.zipcode ) AS num_of_sb,
            sb."City",
            sb."State",
            sb."Latitude",
            sb."Longitude",
            ST_AsGeoJSON(postal.geom) AS the_geom
        FROM zip_data_sb z
        JOIN zip_data2 z2 ON z2."Id" = z."Id"
        JOIN zip_data3 z3 ON z3."Id" = z."Id"
        LEFT JOIN sb_stores sb ON z."Id2" = sb."zipcode"
        JOIN cb_2015_us_zcta510_500k postal ON postal.geoid10::bigint = z."Id2"
        JOIN cb_2016_us_state_500k state ON ST_Touches(state.geom, postal.geom) 
            OR ST_Contains(state.geom, postal.geom)
        JOIN ( 
            SELECT zip,
                sum(CASE
                      WHEN naics ~ '^445' THEN est
                  END)::bigint AS "grocery_stores",
                sum(CASE
                      WHEN naics ~ '^722' THEN est
                  END)::bigint AS "restaurants",
                sum(CASE
                      WHEN naics ~ '^311' THEN est
                  END)::bigint AS "manufacturing",
                sum(CASE
                      WHEN naics ~ '^54171'
                           OR naics = '518210' THEN est
                  END)::bigint AS "tech",
                sum(CASE
                      WHEN naics ~ '^611' THEN est
                  END)::bigint AS "colleges",
                sum(CASE
                      WHEN naics = '------' THEN est
                  END)::bigint AS "total",
                sum(CASE
                      WHEN naics = '531120' THEN est
                  END)::bigint AS "shopping_centers",
                sum(CASE
                      WHEN naics ~ '^23611' THEN est
                  END)::bigint AS "new_homes",
                sum(CASE
                      WHEN naics ~ '^5311' THEN est
                  END)::bigint AS "hotels",
                sum(CASE
                      WHEN naics ~ '^4411' THEN est
                  END)::bigint AS "car_dealers",
                sum(CASE
                      WHEN naics ~ '^4853' THEN est
                  END)::bigint AS "taxis",
                sum(CASE
                      WHEN naics = '481111'
                           OR naics IN ('485999', '488119', '488190') THEN est
                  END)::bigint AS "airport_related"
            FROM zip_to_naics
            GROUP BY zip 
        ) zn ON zn.zip = z."Id2"
        WHERE state.stusps = 'TN'
        ORDER BY num_of_sb DESC
) sub_query