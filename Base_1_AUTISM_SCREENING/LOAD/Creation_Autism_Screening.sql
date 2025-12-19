-- Suppression des tables avec vérification de l'existence
BEGIN
   -- Tentative de suppression de la table autism_screening
   EXECUTE IMMEDIATE 'DROP TABLE autism_screening ';
EXCEPTION
   WHEN OTHERS THEN
      IF SQLCODE != -942 THEN
         RAISE;
      END IF;
END;
/

-- Drop sequences
DROP SEQUENCE autism_screening_seq;

--Create sequence for auto-increment
CREATE SEQUENCE autism_screening_seq START WITH 1 INCREMENT BY 1;

-- Create autism_screening table
CREATE TABLE autism_screening (
    id NUMBER PRIMARY KEY,
    A1_Score NUMBER(1) CONSTRAINT A1_Score_chk CHECK (A1_Score BETWEEN 0 AND 1) NOT NULL,
    A2_Score NUMBER(1) CONSTRAINT A2_Score_chk CHECK (A2_Score BETWEEN 0 AND 1) NOT NULL,
    A3_Score NUMBER(1) CONSTRAINT A3_Score_chk CHECK (A3_Score BETWEEN 0 AND 1) NOT NULL,
    A4_Score NUMBER(1) CONSTRAINT A4_Score_chk CHECK (A4_Score BETWEEN 0 AND 1) NOT NULL,
    A5_Score NUMBER(1) CONSTRAINT A5_Score_chk CHECK (A5_Score BETWEEN 0 AND 1) NOT NULL,
    A6_Score NUMBER(1) CONSTRAINT A6_Score_chk CHECK (A6_Score BETWEEN 0 AND 1) NOT NULL,
    A7_Score NUMBER(1) CONSTRAINT A7_Score_chk CHECK (A7_Score BETWEEN 0 AND 1) NOT NULL,
    A8_Score NUMBER(1) CONSTRAINT A8_Score_chk CHECK (A8_Score BETWEEN 0 AND 1) NOT NULL,
    A9_Score NUMBER(1) CONSTRAINT A9_Score_chk CHECK (A9_Score BETWEEN 0 AND 1) NOT NULL,
    A10_Score NUMBER(1) CONSTRAINT A10_Score_chk CHECK (A10_Score BETWEEN 0 AND 1) NOT NULL,
    age NUMBER CONSTRAINT age_chk CHECK (age > 0 AND age < 150) NOT NULL,
    gender CHAR(1) CONSTRAINT gender_chk CHECK (gender IN ('m', 'f')) NOT NULL,
    ethnicity VARCHAR2(50) NOT NULL,
    jaundice VARCHAR2(3) CONSTRAINT jaundice_chk CHECK (jaundice IN ('yes', 'no')) NOT NULL,
    autism VARCHAR2(3) CONSTRAINT autism_chk CHECK (autism IN ('yes', 'no')) NOT NULL,
    country VARCHAR2(200) NOT NULL,
    result NUMBER CONSTRAINT result_chk CHECK (result >= 0) NOT NULL,
    relation VARCHAR2(50) NOT NULL,
    Class_ASD NUMBER(1) CONSTRAINT Class_ASD_chk CHECK (Class_ASD IN (0, 1)) NOT NULL,
    age_group VARCHAR2(20) CONSTRAINT age_group_chk CHECK (age_group IN ('child', 'adolescent', 'adult')) NOT NULL
);
-- Trigger for auto-incrementing ID
CREATE OR REPLACE TRIGGER autism_screening_id 
BEFORE INSERT ON autism_screening 
FOR EACH ROW
BEGIN
  SELECT autism_screening_seq.NEXTVAL
  INTO   :new.id
  FROM   dual;
END;
/
-- Trigger to prevent duplicates
CREATE OR REPLACE TRIGGER trg_before_insert_autism_screening
BEFORE INSERT ON autism_screening
FOR EACH ROW
DECLARE
  v_exists NUMBER;
BEGIN
  -- Vérifie l'existence d'un enregistrement avec les mêmes valeurs pour toutes les colonnes
  SELECT COUNT(*)
  INTO v_exists
  FROM autism_screening
  WHERE A1_Score = :new.A1_Score
    AND A2_Score = :new.A2_Score
    AND A3_Score = :new.A3_Score
    AND A4_Score = :new.A4_Score
    AND A5_Score = :new.A5_Score
    AND A6_Score = :new.A6_Score
    AND A7_Score = :new.A7_Score
    AND A8_Score = :new.A8_Score
    AND A9_Score = :new.A9_Score
    AND A10_Score = :new.A10_Score
    AND age = :new.age
    AND LOWER(gender) = LOWER(:new.gender)
    AND LOWER(ethnicity) = LOWER(:new.ethnicity)
    AND LOWER(jaundice) = LOWER(:new.jaundice)
    AND LOWER(autism) = LOWER(:new.autism)
    AND LOWER(country) = LOWER(:new.country)
    AND result = :new.result
    AND LOWER(relation) = LOWER(:new.relation)
    AND class_asd = :new.class_asd
    AND LOWER(age_group) = LOWER(:new.age_group);

  IF v_exists > 0 THEN
    -- Annule l'insertion si un enregistrement similaire existe déjà
    RAISE_APPLICATION_ERROR(-20001, 'A similar record already exists in the table.');
  END IF;
END;
/

SELECT * FROM autism_screening;