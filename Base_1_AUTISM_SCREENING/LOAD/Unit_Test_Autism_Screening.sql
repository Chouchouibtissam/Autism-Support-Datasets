-- ************************************************TEST UNITAIRE ********************************
SET SERVEROUTPUT ON;
DECLARE
  -- Variables pour stocker les valeurs de test
  v_test_id NUMBER;
  v_A1_Score NUMBER(1) := 1;
  v_A2_Score NUMBER(1) := 0;
  v_A3_Score NUMBER(1) := 0;
  v_A4_Score NUMBER(1) := 1;
  v_A5_Score NUMBER(1) := 0;
  v_A6_Score NUMBER(1) := 1;
  v_A7_Score NUMBER(1) := 1;
  v_A8_Score NUMBER(1) := 0;
  v_A9_Score NUMBER(1) := 0;
  v_A10_Score NUMBER(1) := 1;
  v_age NUMBER := 21;
  v_gender CHAR(1) := 'f';
  v_ethnicity VARCHAR2(50) := 'test ethnicity';
  v_jaundice VARCHAR2(3) := 'no';
  v_autism VARCHAR2(3) := 'no';
  v_country VARCHAR2(200) := 'france';  
  v_result NUMBER := 5; 
  v_relation VARCHAR2(50) := 'self';
  v_age_group VARCHAR2(20) := 'adult'; 
  v_Class_ASD NUMBER(1) := 0;  
BEGIN
  -- Insertion de données de test
  INSERT INTO autism_screening (A1_Score, A2_Score, A3_Score, A4_Score, A5_Score, A6_Score, A7_Score, A8_Score, A9_Score, A10_Score, age, gender, ethnicity, jaundice, autism, country, result, relation, age_group, Class_ASD)
  VALUES (v_A1_Score, v_A2_Score, v_A3_Score, v_A4_Score, v_A5_Score, v_A6_Score, v_A7_Score, v_A8_Score, v_A9_Score, v_A10_Score, v_age, v_gender, v_ethnicity, v_jaundice, v_autism, v_country, v_result, v_relation, v_age_group, v_Class_ASD)
  RETURNING id INTO v_test_id;
  DBMS_OUTPUT.PUT_LINE('Insertion réussie. ID de test: ' || v_test_id);
  -- Tentative d'insertion de données dupliquées pour tester le trigger
  BEGIN
    INSERT INTO autism_screening (A1_Score, A2_Score, A3_Score, A4_Score, A5_Score, A6_Score, A7_Score, A8_Score, A9_Score, A10_Score, age, gender, ethnicity, jaundice, autism, country, result, relation, age_group, Class_ASD)
    VALUES (v_A1_Score, v_A2_Score, v_A3_Score, v_A4_Score, v_A5_Score, v_A6_Score, v_A7_Score, v_A8_Score, v_A9_Score, v_A10_Score, v_age, v_gender, v_ethnicity, v_jaundice, v_autism, v_country, v_result, v_relation, v_age_group, v_Class_ASD);
    DBMS_OUTPUT.PUT_LINE('✗ TEST FAILED: Duplicate insertion succeeded');
  EXCEPTION
    WHEN OTHERS THEN
      DBMS_OUTPUT.PUT_LINE('✓ TEST PASSED: Duplicate insertion prevented as expected');
  END;
 -- Cleanup Suppression des données de test insérées
  DELETE FROM autism_screening WHERE id = v_test_id;
  DBMS_OUTPUT.PUT_LINE('✓ Cleanup successful. Test data deleted.');
EXCEPTION
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('✗ Error during test execution: ' || SQLERRM);
END;
/
-- Test table existence ******************************************************************************************
SELECT table_name FROM user_tables WHERE table_name IN ('AUTISM_SCREENING');
-- Test des Colonnes et Types **********************************************************************************
SELECT column_name, data_type FROM user_tab_columns WHERE table_name = 'AUTISM_SCREENING';