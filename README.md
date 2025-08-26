## Overview

This project merges data from three primary sources:
- **Anthropic Economic Index (AEI)** task conversation data
- **Bureau of Labor Statistics (BLS)** Occupational Employment and Wage Statistics (OEWS)
- **Occupational Information Network (O*NET)**

The result is a unified dataset that links occupational tasks percent appearing in Claude conversations to wage, employment, and importance/frequency/relevance ratings for 2015 and 2025. We then use this data for analysis with charts stored in charts folder and script for generating these in scripts folder. 



## Repository Structure (WIP)
charts\
extra_data: all data sets used for merging and analysis.\
original_data: all original data Anthropic used for their analysis.\
scripts: all scripts used for merging and chart creation.



## Data Sources
- **AEI Data**: [Task Mappings 2/10/2025 Release](https://huggingface.co/datasets/Anthropic/EconomicIndex/blob/main/release_2025_02_10/onet_task_mappings.csv) 
- **BLS OEWS**: [All OEWS National and State 2024 and 2015](https://www.bls.gov/oes/tables.htm)
- **O\*NET Task Statements & Ratings**: [Statements Oct 2015](https://www.onetcenter.org/dictionary/20.1/excel/task_statements.html), [Ratings Oct 2015](https://www.onetcenter.org/dictionary/20.1/excel/task_ratings.html), [Ratings May 2025](https://www.onetcenter.org/dictionary/29.3/excel/task_ratings.html)
- **Additional**: [SOC Structure 2019](https://www.onetcenter.org/taxonomy/2019/structure.html), [SOC Code Crossswalk](https://www.onetcenter.org/taxonomy/2019/walk.html), [O*NET Scraped Wages](https://github.com/adamkq/onet-dataviz/blob/master/jobData.csv), [SOC Structure 2019](https://www.onetcenter.org/taxonomy/2019/structure.html)  

 


## Data Merging Steps
The merging pipeline follows these main steps. The script also organizes the steps in this way and has comments through out:
1. Map Anthropic Task %s to O*NET v20.1 Task Statements
2. Add SOC Major Occupational Category  
3. Add 2024 Wage and Employment Data 
4. Add 2015 Wage and Employment Data  
5. Adjust Employment Columns 
6. Add Task Rating Data 
7. Final Cleanup    

Full details on this process can be found here [here](https://docs.google.com/document/d/14HfdnTBviQ97DyKEBPYV6MVJ6uuteOk9lDPbGqdi1Z0/edit?usp=sharing).



## Reproducing

### Merging
1. Clone the repository:
```bash
git clone https://github.com/theodorewright11/aei_data_analysis/tree/main
cd aei_data_analysis
```
2. Create virtual environment (recommended):
```bash
python -m venv venv
venv\Scripts\activate  # On Mac/Linux: source venv/bin/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run file:
```bash
jupyter notebook scripts/data_merge.ipynb
```
Result is saved to ``` extra_data/tasks_final.csv```
- Optional: Under the "Imports" → "Parameter Adjustment" section in ```scripts/data_merge.ipynb``` frequency weights, inflation factors, and a variable toggle to save each steps' data frame into a csv are available for adjustment.

### Analysis
1. WIP

## Outputs
- Dataset  ``` extra_data/tasks_final.csv``` that links occupational tasks percent appearing in Claude conversations to wage, employment, and importance/frequency/relevance ratings for 2015 and 2025
- Charts ```charts/WIP```
