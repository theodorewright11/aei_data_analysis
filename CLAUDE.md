# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project merges and analyzes data from three primary sources to study occupational automation exposure:
- **Anthropic Economic Index (AEI)**: Task conversation data showing percent of tasks appearing in Claude conversations
- **Bureau of Labor Statistics (BLS) OEWS**: Occupational Employment and Wage Statistics
- **O*NET Database**: Occupational task statements and ratings (importance/frequency/relevance)

The final output is `data/tasks_final.csv`, which links occupational tasks to wage, employment, and task rating data for both 2015 and 2025, enabling analysis of automation exposure across different occupations.

## Development Environment

### Setup Commands
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Project

**Primary data merging pipeline:**
```bash
jupyter notebook scripts/data_merge.ipynb
```
Outputs:
- `data/tasks_final.csv` (main task-level dataset)
- `data/ratings_eco_2025.csv` and `data/ratings_eco_2015.csv` (economy-wide aggregations)

**Generate charts and visualizations:**
```bash
jupyter notebook scripts/charts.ipynb
```
Output: Chart files in `outputs/exploratory_charts/` subdirectories

**Other analysis notebooks:**
- `scripts/original_scripts/plots_original.ipynb` - Original plotting scripts
- `scripts/original_scripts/plots_edited_with_old.ipynb` - Edited plotting with historical data

## Repository Structure

```
aei_data_analysis/
├── data/                       # All datasets (source and intermediate)
│   ├── original_data/         # Original source data files
│   ├── merged_data_files/     # Intermediate merge outputs (optional saves)
│   ├── tasks_final.csv        # Main output: merged dataset
│   ├── task_pct_v1.csv        # AEI task percentages (version 1)
│   ├── task_pct_v2.csv        # AEI task percentages (version 2)
│   ├── oews_national_2024.csv # BLS national wage/employment 2024
│   ├── oews_national_2015.csv # BLS national wage/employment 2015
│   ├── oews_states_2024.csv   # BLS state wage/employment 2024
│   ├── oews_states_2015.csv   # BLS state wage/employment 2015
│   ├── task_ratings_may_2025.csv  # O*NET task ratings (2025)
│   ├── task_ratings_oct_2015.csv  # O*NET task ratings (2015)
│   ├── task_statements_v20.1.csv  # O*NET task descriptions
│   ├── ratings_eco_2025.csv       # Economy-wide task frequency (2025)
│   └── ratings_eco_2015.csv       # Economy-wide task frequency (2015)
├── outputs/                   # Generated outputs
│   ├── charts_for_sharing/    # Charts for reports and sharing
│   └── exploratory_charts/    # Exploratory visualizations
├── scripts/                   # Jupyter notebooks
│   ├── data_merge.ipynb      # Main merging pipeline
│   ├── charts.ipynb          # Chart generation
│   └── original_scripts/     # Original/legacy plotting scripts
│       ├── plots_original.ipynb
│       └── plots_edited_with_old.ipynb
└── exploratory/               # Exploratory analysis
    └── onet_data_exploration/ # O*NET data exploration notebooks
```

## Data Merging Pipeline Architecture

The `scripts/data_merge.ipynb` notebook follows an 8-step sequential pipeline:

### Step 1: Map Anthropic Task %s to O*NET v20.1 Task Statements
- Joins AEI task conversation percentages with O*NET task descriptions
- Creates base dataset linking Claude usage to occupational tasks

### Step 2: Add SOC Major Occupational Category
- Adds Standard Occupational Classification (SOC) major categories
- Enables aggregation by broad occupational groups

### Step 3: Add 2024 Wage and Employment Data
- Sub-steps:
  - 3.1: Update to 2019 SOC codes (from crosswalk)
  - 3.2: Add 2024 national wage data
  - 3.3: Add 2024 state-level wage data
  - 3.4: Add 2024 national employment data
  - 3.5: Add 2024 state-level employment data
  - 3.6: Merge all 2024 wage/employment into task data

### Step 4: Add 2015 Wage and Employment Data
- Parallel structure to Step 3 for historical comparison
- Sub-steps: 4.1-4.5 mirror 2024 process

### Step 5: Adjust Employment Columns
- Normalizes employment figures across time periods
- Calculates employment-weighted metrics

### Step 6: Add Task Rating Data
- Sub-steps:
  - 6.1: Load 2025 and 2015 task rating datasets
  - 6.2: Merge rating values (importance/frequency/relevance) into tasks
  - 6.3: Fill missing task rating values using imputation
  - 6.4: Combine 2015 and 2025 ratings into unified dataframe

### Step 7: Final Cleanup
- Removes temporary columns
- Standardizes column names and data types
- Outputs `data/tasks_final.csv`

### Step 8: Create Economy Task Frequency Data
- Aggregates task ratings and employment data to create economy-wide metrics
- Sub-steps:
  - 8.1: National ratings and employment data for 2025
  - 8.2: National ratings and employment data for 2015
  - 8.3: State ratings and employment data for 2025
  - 8.4: State ratings and employment data for 2015
  - 8.5: Add major occupational categories
- Outputs `data/ratings_eco_2025.csv` and `data/ratings_eco_2015.csv`

## Key Configuration Parameters

In `scripts/data_merge.ipynb` under "Imports → Parameter Adjustment" section:

- **Frequency weights**: Adjust how task frequency ratings are weighted
- **Inflation factors**: Control wage adjustment between 2015-2024
- **Save intermediate CSVs**: Toggle to save each step's dataframe to `data/merged_data_files/`

## Important Data Relationships

- **SOC codes**: Occupational classification system linking all datasets
  - 2010 SOC codes → 2019 SOC codes (via crosswalk in Step 3.1)
  - Different granularity levels: detailed (6-digit) vs major categories (2-digit)

- **O*NET versions**: Task statements from v20.1 (Oct 2015), ratings from both 2015 and 2025

- **State vs National data**:
  - National: Single wage/employment value per occupation
  - State: 50+ values per occupation, requires aggregation

- **Task ratings dimensions**: Each task has importance, frequency, and relevance scores

## Working with the Code

When modifying the data pipeline:
1. The pipeline is sequential - each step depends on previous steps
2. Intermediate dataframes are saved in `data/merged_data_files/` if enabled
3. Column naming conventions follow pattern: `{metric}_{year}_{geography}`
4. Missing data handling varies by step - check imputation logic in Step 6.3

When creating new visualizations:
1. Load `data/tasks_final.csv` as the primary data source
2. Exploratory charts go to `outputs/exploratory_charts/`
3. Charts for sharing/reports go to `outputs/charts_for_sharing/`
4. Follow existing plotting patterns in `scripts/charts.ipynb`
