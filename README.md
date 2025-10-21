# *WIP
# Overview

This project merges data from three primary sources:
- Anthropic Economic Index (AEI) task conversation data
- Bureau of Labor Statistics (BLS) Occupational Employment and Wage Statistics (OEWS)
- Occupational Information Network (O*NET)

The result is a unified dataset that links occupational tasks percent appearing in Claude conversations to wage, employment, and importance/frequency/relevance ratings for 2015 and 2025. We then use this data for analysis with charts stored in the outputs folder and scripts for generating these in the scripts folder. 



## Repository Structure
outputs/exploratory_charts: 100+ charts made from looping over different parameters and data variations covering various categories and granularities.\
outputs/charts_for_sharing: A few handpicked charts that give real insights and can be shared to others. READ.me included for interpretation \
data: all data sets used for merging as well as those created that are used for analysis.\
scripts: all scripts used for merging and chart creation.


# Merging 

## Data Sources
- AEI Data
  - [Task Mappings v1 2/10/2025 Release](https://huggingface.co/datasets/Anthropic/EconomicIndex/blob/main/release_2025_02_10/onet_task_mappings.csv) 
  -  [Task Mappings v2 3/27/2025 Release](https://huggingface.co/datasets/Anthropic/EconomicIndex/blob/main/release_2025_03_27/task_pct_v2.csv) 
- BLS OEWS
  - [All OEWS National and State 2024 and 2015](https://www.bls.gov/oes/tables.htm)
- O\*NET Task Statements & Ratings
  - [Statements Oct 2015](https://www.onetcenter.org/dictionary/20.1/excel/task_statements.html)
  - [Ratings Oct 2015](https://www.onetcenter.org/dictionary/20.1/excel/task_ratings.html)
  - [Ratings May 2025](https://www.onetcenter.org/dictionary/29.3/excel/task_ratings.html)
- Additional
  - [SOC Structure 2019](https://www.onetcenter.org/taxonomy/2019/structure.html)
  - [SOC Code Crossswalk](https://www.onetcenter.org/taxonomy/2019/walk.html)
  - [O*NET Scraped Wages](https://github.com/adamkq/onet-dataviz/blob/master/jobData.csv)
  - [SOC Structure 2019](https://www.onetcenter.org/taxonomy/2019/structure.html)  



## Steps
The merging pipeline follows these main steps. The script also organizes the steps in this way and has comments through out:
1. Map Anthropic Task %s to O*NET v20.1 Task Statements
2. Add SOC Major Occupational Category  
3. Add 2024 Wage and Employment Data 
4. Add 2015 Wage and Employment Data  
5. Adjust Employment Columns 
6. Add Task Rating Data 
7. Final Cleanup On Main Data
8. Create Economy Task Frequency Data
9. Create Task Automation Data



Full details on this process can be found [here](https://docs.google.com/document/d/14HfdnTBviQ97DyKEBPYV6MVJ6uuteOk9lDPbGqdi1Z0/edit?usp=sharing).



## Reproducing
1. Clone the repository:
```bash
git clone https://github.com/theodorewright11/aei_data_analysis
cd aei_data_analysis
```
1. Create virtual environment (recommended):
```bash
python -m venv venv
.\venv\Scripts\activate.ps1 
```
1. Install dependencies:
```bash
pip install -r requirements.txt
```
1. Run file:
```bash
jupyter notebook scripts/data_merge.ipynb
```
Datasets used are saved to the data folder namely: ``` data/tasks_final.csv```
- Optional: Under the "Imports" → "Parameter Adjustment" section in ```scripts/data_merge.ipynb```, frequency weights, inflation factors, and a variable toggle to save each steps' data frame into a csv are available for adjustment.



# Analysis

## Data Sources
- ``` data/tasks_final.csv``` created from merging.
- ``` data/ratings_eco_2015.csv``` created from merging.
- ``` data/ratings_eco_2025.csv``` created from merging.
- ``` data/automation_tasks_imputed.csv``` created from merging.
- ``` data/automation_tasks_matched_2015.csv``` created from merging.
- ``` data/automation_tasks_matched_2025.csv``` created from merging.



## Steps
WIP



## Reproducing
WIP



# Outputs
## Datasets
- ``` data/tasks_final.csv```:  links occupational tasks percent appearing in Claude conversations (v1) to wage, employment, and importance/frequency/relevance ratings for 2015 and 2025.
- ``` data/tasks_final_v2.csv```:  links occupational tasks percent appearing in Claude conversations (v2) to wage, employment, and importance/frequency/relevance ratings for 2015 and 2025.
- `data/ratings_eco_2015.csv`: O*NET task ratings (frequency, importance, relevance) merged with 2015 BLS employment and wage data at task level.
- `data/ratings_eco_2025.csv`: O*NET 2025 task ratings merged with 2024 BLS employment and wage data at task level.
- `data/automation_tasks_imputed.csv`: Primary analysis dataset linking AI-automatable tasks (from AEI) to baseline task completions with SOC code transitions and imputed employment values.
- `data/automation_tasks_matched_2015.csv`: AI tasks matched directly to 2015 baseline without imputation.
- `data/automation_tasks_matched_2025.csv`: AI tasks matched directly to 2025 baseline without imputation (excludes unmatched tasks from AEI data, ~15% task coverage data loss).
## Charts
- ```charts/exploratory```: WIP
- ```charts/report```: see ```charts/report/README.md``` for an explanation of these charts.
