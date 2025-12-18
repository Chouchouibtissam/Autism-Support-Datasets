"""
Transform.py
Data cleaning and transformation pipeline for Autism Screening datasets
"""

import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import os


def load_data():
    """Load the three autism screening datasets"""
    print("Loading data...")
    
    child_df = pd.read_csv('data/Autism-Child-Data.csv', na_values=['?'])
    adolescent_df = pd.read_csv('data/Autism-Adolescent-Data.csv', na_values=['?'])
    adult_df = pd.read_csv('data/Autism-Adult-Data.csv', na_values=['?'])
    
    print(f"Child dataset loaded: {child_df.shape}")
    print(f"Adolescent dataset loaded: {adolescent_df.shape}")
    print(f"Adult dataset loaded: {adult_df.shape}")
    
    return child_df, adolescent_df, adult_df


def standardize_columns(df):
    """Standardize column names: lowercase, replace spaces/hyphens with underscores"""
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_').str.replace('/', '_')
    # Rename contry_of_res to country 
    if 'contry_of_res' in df.columns:
        df = df.rename(columns={'contry_of_res': 'country'})
    return df


def drop_unnecessary_columns(df, columns_to_drop):
    """Drop specified columns if they exist"""
    existing_cols = [col for col in columns_to_drop if col in df.columns]
    if existing_cols:
        df = df.drop(columns=existing_cols)
    return df


def clean_dataset(df, dataset_name):
    """Clean individual dataset"""
    print(f"\nCleaning {dataset_name} dataset...")
    
    df = df.copy()
    initial_rows = len(df)
    
    # Fix column name typos
    df = df.rename(columns={
        'jundice': 'jaundice',
        'austim': 'autism'
    })
    print(f"Column names corrected")
    
    # Remove duplicates
    df = df.drop_duplicates()
    duplicates_removed = initial_rows - len(df)
    print(f"Duplicates removed: {duplicates_removed}")
    
    # Clean string values (strip whitespace, lowercase)
    string_cols = df.select_dtypes(include=['object']).columns
    for col in string_cols:
        df[col] = df[col].apply(lambda x: x.strip().lower() if pd.notna(x) else x)
    print(f"String values cleaned")
    
    # Standardize country names
    if 'country' in df.columns:
        df['country'] = df['country'].replace({
            'americansamoa': 'american samoa',
            'viet nam': 'vietnam',
            'u.s. outlying islands': 'united states'
        })
    print(f"Country names standardized")
    
    # Add age_group identifier
    df['age_group'] = dataset_name.lower()
    print(f"Added age_group column: {dataset_name.lower()}")
    print(f"Final rows: {len(df)}")
    
    return df


def handle_missing_values(df, dataset_name):
    """Remove rows with missing values"""
    print(f"\nHandling missing values for {dataset_name}...")
    
    df = df.copy()
    initial_rows = len(df)
    initial_missing = df.isnull().sum().sum()
    
    print(f"Initial missing values: {initial_missing}")
    
    # Drop rows with any missing values
    df = df.dropna()
    
    rows_removed = initial_rows - len(df)
    print(f"Rows removed: {rows_removed}")
    print(f"Final rows: {len(df)}")
    
    return df


def convert_data_types(df, dataset_name):
    """Convert columns to appropriate data types"""
    print(f"\nConverting data types for {dataset_name}...")
    
    df = df.copy()
    
    # Convert screening question columns (A1-A10) to integer
    score_cols = [col for col in df.columns if col.startswith('a') and '_score' in col]
    for col in score_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    print(f"Converted {len(score_cols)} score columns to int")
    
    # Convert result to integer
    if 'result' in df.columns:
        df['result'] = pd.to_numeric(df['result'], errors='coerce').fillna(0).astype(int)
        print(f"result converted to int")
    
    # Convert age to integer
    if 'age' in df.columns:
        initial_rows = len(df)
        df['age'] = pd.to_numeric(df['age'], errors='coerce').astype(int)
        print(f"age converted to int")
        # Remove rows where age is greater than 150
        df = df[df['age'] <= 150].copy()
        rows_removed = initial_rows - len(df)
        if rows_removed > 0:
            print(f"Rows with age > 150 removed: {rows_removed}")
    
    # Convert target variable (Class/ASD) to binary integer (0/1)
    target_col = [col for col in df.columns if 'class' in col or 'asd' in col]
    if target_col:
        col = target_col[0]
        df[col] = df[col].map({'yes': 1, 'no': 0})
        df[col] = df[col].fillna(0).astype(int)
        print(f"{col} converted to binary int (0=No, 1=Yes)")
    
    return df


def merge_datasets(child_df, adolescent_df, adult_df):
    """Merge all three datasets"""
    print("\nMerging datasets...")
    
    merged_df = pd.concat([child_df, adolescent_df, adult_df], ignore_index=True)
    
    print(f"Datasets merged successfully")
    print(f"Total rows: {merged_df.shape[0]}")
    print(f"Total columns: {merged_df.shape[1]}")
    
    return merged_df


def validate_dataset(df):
    """Validate the final dataset"""
    print("\nValidating dataset...")
    
    missing_total = df.isnull().sum().sum()
    duplicates = df.duplicated().sum()
    
    # Check target variable distribution
    target_col = [col for col in df.columns if 'class' in col or 'asd' in col][0]
    print(f"Target variable ({target_col}) distribution:")
    print(df[target_col].value_counts())

    if 'country' in df.columns:
        print(f"Unique countries: {df['country'].nunique()}")
    
    is_valid = (missing_total == 0 and duplicates == 0)
    
    if is_valid:
        print("\n✅ Dataset is VALID")
    else:
        print("\n⚠️ Dataset has issues")
    
    return is_valid


def save_dataset(df, output_path):
    """Save the cleaned dataset"""
    print("\nSaving dataset...")
    
    df.to_csv(output_path, index=False)
    
    print(f"File saved: {output_path}")


def main():
    """Main transformation pipeline"""
    print("\nAUTISM SCREENING DATA - TRANSFORMATION PIPELINE\n")
    
    # 1. Load data
    child_df, adolescent_df, adult_df = load_data()
    
    # 2. Standardize column names
    print("\nStandardizing columns...")
    child_df = standardize_columns(child_df)
    adolescent_df = standardize_columns(adolescent_df)
    adult_df = standardize_columns(adult_df)
    print("Column names standardized")
    
    # 3. Drop unnecessary columns
    columns_to_drop = ['unnamed:_0', 'used_app_before', 'age_desc']
    child_df = drop_unnecessary_columns(child_df, columns_to_drop)
    adolescent_df = drop_unnecessary_columns(adolescent_df, columns_to_drop)
    adult_df = drop_unnecessary_columns(adult_df, columns_to_drop)
    print("Unnecessary columns dropped")
    
    # 4. Clean datasets
    child_clean = clean_dataset(child_df, 'Child')
    adolescent_clean = clean_dataset(adolescent_df, 'Adolescent')
    adult_clean = clean_dataset(adult_df, 'Adult')
    
    # 5. Handle missing values
    child_clean = handle_missing_values(child_clean, 'Child')
    adolescent_clean = handle_missing_values(adolescent_clean, 'Adolescent')
    adult_clean = handle_missing_values(adult_clean, 'Adult')
    
    # 6. Convert data types
    child_clean = convert_data_types(child_clean, 'Child')
    adolescent_clean = convert_data_types(adolescent_clean, 'Adolescent')
    adult_clean = convert_data_types(adult_clean, 'Adult')
    
    # 7. Merge datasets
    merged_df = merge_datasets(child_clean, adolescent_clean, adult_clean)
    
    # 8. Validate dataset
    is_valid = validate_dataset(merged_df)
    
    # 9. Save cleaned dataset
    output_path = 'data/Autism_test_clean.csv'
    save_dataset(merged_df, output_path)
    
    # 10. Final summary
    print("\n✅ Transformation completed successfully")
    print(f"Final dataset: {merged_df.shape[0]} rows, {merged_df.shape[1]} columns")
    print(f"Output file: {output_path}\n")


if __name__ == "__main__":
    main()