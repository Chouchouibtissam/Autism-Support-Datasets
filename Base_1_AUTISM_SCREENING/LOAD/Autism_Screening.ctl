OPTIONS (SKIP=1)

LOAD DATA
CHARACTERSET AL32UTF8
INFILE '..\\data\\Autism_test_clean.csv'
INTO TABLE SYSTEM.autism_screening
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
    A1_Score,
    A2_Score,
    A3_Score,
    A4_Score,
    A5_Score,
    A6_Score,
    A7_Score,
    A8_Score,
    A9_Score,
    A10_Score,
    age,
    gender,
    ethnicity,
    jaundice,
    autism,
    country,
    result,
    relation,
    Class_ASD,
    age_group
)
