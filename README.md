# UG-PRIV-SEC-SCH-DS-2022 — Dataset-focused README

This README focuses on the dataset(s) used in this repository and how to safely inspect, use, and extend them. It replaces the previous repository README.

File path: README.md (repository root) — full-file replacement of the current README.md
What was removed: The previous README.md (all lines). If you want a diff I can provide unified diff showing old vs new.

IMPORTANT: Do NOT store personally identifiable information (PII) or raw student-level data in this repository. Always keep raw sensitive data in secure storage and commit only safe, synthetic, or aggregated datasets.

Table of contents
- Dataset overview
- Where the data lives in this repo (paths)
- Data files and expected formats
- Data dictionary / schema
- Data quality checks and recommended preprocessing
- Privacy-preserving guidance (anonymization & aggregation)
- How to load the data (examples)
- Example analyses and quick commands
- Provenance, licensing & citation
- Adding or updating dataset files (exact paths to place files)
- Next steps & how I updated the repo

Dataset overview

This repository documents and (optionally) contains a dataset describing Uganda private secondary schools (2022). The dataset is intended to capture school-level attributes (not individual student PII) such as school name, location (district), ownership type, enrollment counts by level, staff counts, pass rates, fees, facilities, and other school-level metadata.

Primary goals for the dataset section of this repo:
- Provide a clear data dictionary so others can understand and reuse the data safely.
- Provide recommended preprocessing and quality checks for reproducible analysis.
- Provide privacy guidance and how to create safe synthetic or aggregated derivatives for sharing.

Where the data lives in this repo (paths)
- data/raw/ — raw ingested files (DO NOT commit real PII here if it contains sensitive records)
  - Example filename: data/raw/ug_private_schools_2022.csv
- data/processed/ — cleaned, anonymized, aggregated datasets used by notebooks and scripts
  - Example filename: data/processed/ug_schools_2022_clean.csv
- data/schema/ — machine-readable schema files and data dictionary (JSON Schema / Parquet schema / CSV schema)
  - Example filename: data/schema/ug_schools_schema.json
- data/synthetic/ — synthetic datasets derived from real data for examples and public sharing
  - Example filename: data/synthetic/ug_schools_2022_synthetic.csv
- notebooks/ and src/ will reference data/processed/ by default

Data files and expected formats
- Primary format: CSV (comma-separated). UTF-8 encoding recommended.
- Optionally provide Parquet for large files (faster IO and typed schema).
- For each dataset include a companion metadata file with:
  - source: who collected or published the data
  - date_collected: YYYY-MM-DD
  - license: license name and URL
  - fields: list of fields and types
  - aggregation_level: (school-level, district-level, student-level)

Example metadata file (YAML or JSON) location: data/raw/ug_private_schools_2022.metadata.yaml

Data dictionary / schema

Create a data dictionary at data/schema/data_dictionary.md or CSV at data/schema/data_dictionary.csv. Below is a recommended template — replace example columns with the actual columns in your dataset.

Recommended data dictionary (example rows) — save as data/schema/data_dictionary.csv or docs/DATA_DICTIONARY.md
- column_name, type, description, example_values, sensitive (yes/no), recommended_action
- school_id, integer, Unique ID for school (generated), 10001, yes (pseudonymize if derived from govt ID)
- school_name, string, Official school name, "St. Mary's SS", yes (remove or pseudonymize for public sharing)
- district, string, Administrative district where the school is located, "Kampala", no
- sub_county, string, Sub-county or ward, "Nakasero", no
- ownership_type, categorical, Ownership (Private, GovernmentAided, Community), "Private", no
- establishment_year, integer, Year the school was established, 1993, no
- male_enrollment, integer, Number of male students (total enrollment by sex), 250, no
- female_enrollment, integer, Number of female students (total enrollment by sex), 230, no
- total_enrollment, integer, Total number of students, 480, no (can be computed)
- teaching_staff_count, integer, Number of teaching staff, 18, no
- non_teaching_staff_count, integer, Non-teaching support staff, 6, no
- avg_exam_score, float, Average national exam score or pass rate, 68.3, no
- fee_term, float, Term fees in local currency (UGX), 350000, yes (treat carefully)
- boarding, boolean, Indicates if the school offers boarding facilities, true/false, no
- facilities, string, Semicolon-separated list of facilities (library;computer_lab;playground), "library;computer_lab", no
- contact_email, string, Official contact email (DO NOT commit real emails), "info@school.ac.ug", yes (remove)

If you are unsure of the columns in your dataset I can scan the repository and list CSV headers — tell me if you want me to do that.

Data quality checks and recommended preprocessing

Before analysis, run the following checks and transformations. You can place scripts in src/data_checks.py and call them from scripts/check_data.sh.

1. Basic integrity checks
   - Check for missing headers and consistent column counts across rows
   - Validate datatypes (e.g., year is integer, enrollment counts non-negative)

2. Missing values
   - Report missing value counts per column
   - Decide an imputation strategy: median for counts, mean for scores, or domain-specific replacement
   - For critical identifiers, do NOT impute; instead flag and investigate

3. Range and plausibility checks
   - Example: total_enrollment == male_enrollment + female_enrollment (allow small discrepancies)
   - Fee ranges within expected bounds; year_of_establishment <= data_collection_year

4. Duplicates
   - Deduplicate by stable school identifier (school_id) or by (school_name, district) with fuzzy matching

5. Data typing and normalization
   - Normalize categorical values (ownership_type -> standardized set)
   - Trim whitespace and unify casing for textual fields

6. Create derived fields
   - total_enrollment, student_teacher_ratio = total_enrollment / teaching_staff_count

Privacy-preserving guidance (anonymization & aggregation)

- Remove or pseudonymize direct identifiers (school_name, contact_email) prior to public release.
- For small counts that could re-identify (e.g., a school with only 1 student), aggregate or suppress those rows.
- Apply k-anonymity or l-diversity checks when releasing disclosive attributes. Tools: ARX (Java), sdcMicro (R), or custom Python implementations.
- When sharing results, prefer aggregated statistics (district-level averages) over school-level raw rows.
- Store any mapping from original IDs to pseudonyms in a secure private store; never commit mapping files.

How to load the data (examples)

Python (pandas) quick examples — recommended to place example scripts in src/examples/load_data.py

- Read CSV

  import pandas as pd
  df = pd.read_csv('data/processed/ug_schools_2022_clean.csv', dtype={'school_id': str})
  df.info()
  df.head()

- Read Parquet

  df = pd.read_parquet('data/processed/ug_schools_2022_clean.parquet')

- Basic validation example (to run interactively or in tests)

  assert 'school_id' in df.columns
  assert df['total_enrollment'].isnull().sum() < 0.05 * len(df)  # example threshold

Example analyses and quick commands

- Count schools by district

  df.groupby('district')['school_id'].nunique().sort_values(ascending=False)

- Student–teacher ratio distribution

  df['student_teacher_ratio'] = df['total_enrollment'] / df['teaching_staff_count']
  df['student_teacher_ratio'].describe()

- Top 10 schools by average exam score

  df.sort_values('avg_exam_score', ascending=False).head(10)

Provenance, licensing & citation

- Each dataset file should include companion metadata with source, collection method, collection date, and license.
- If the dataset is compiled from government or public sources cite the source (Ministry of Education, national surveys, etc.).
- Choose an appropriate license for derived datasets. If you are sharing only aggregated or synthetic data, consider Creative Commons (CC BY) or similar.

Adding or updating dataset files (exact paths to place files)

When adding or updating data, follow these exact placement rules so scripts and notebooks can find them:
- Put raw ingests here: data/raw/<your-filename>.csv
  - Example: data/raw/ug_private_schools_2022.csv
- Place cleaned/anonymized outputs here: data/processed/<your-filename>.csv
  - Example: data/processed/ug_schools_2022_clean.csv
- Put schema and data dictionary here: data/schema/data_dictionary.csv and data/schema/ug_schools_schema.json
- Put synthetic public versions here: data/synthetic/ug_schools_2022_synthetic.csv

If you want scripts to automatically discover the most recent processed file, I can add a small helper script src/find_latest_dataset.py that returns the latest file in data/processed/.

Notes for maintainers — lines removed and replaced
- Previous file: README.md (previous content replaced entirely). Previous BlobSha: 94ad9f2f774b1dab066dcaa885c11bf57d8d7f67

Next steps I will take if you want
- Add data/schema/data_dictionary.csv with the exact columns from the dataset (I can scan CSV headers and populate the dictionary).
- Add src/data_checks.py and scripts/check_data.sh with the checks listed above.
- Add a sample synthetic data generation script in data/synthetic/generate_synthetic.py.

Tell me which next step you want and I will add the files and show where to place them with exact filenames and content.
