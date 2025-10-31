# AI Task Automation Analysis - Preliminary Report Oct 2025 Charts

## Overview

This folder contains publication-ready charts analyzing AI labor force impact potential across U.S. occupations using the Anthropic Economic Index (AEI), O*NET task data, and BLS wage and employment data.


## Automation By Task Completion
**Methodology:** Tasks from the O*NET occupational database are classified as "AI-automatable" if they appear in the Anthropic Economic Index, which tracks actual Claude usage patterns. Task frequency ratings from O*NET and employment data from BLS are used to calculate what percentage of each occupation's work could be automated based on task completions.

**Data Quality:** 
- Analysis excludes 7 occupations (0.8%) where methodology produced >100% automation values, indicating data quality issues in SOC code transitions with frequency measurements.
- Charts using Utah employment numbers include more imputations and are less reliable until futher notice proving the robustness of the imputations.

**Limitations:**

1. **Equal time assumption:** This analysis treats all tasks as taking equal time, which is a simplification. In reality, some tasks take minutes while others take hours or days. This means our automation percentages may overweight frequent simple tasks and underweight rare complex tasks.

2. **Automation vs. augmentation:** Tasks classified as "AI-automatable" represent a spectrum of AI involvement - from full automation to partial assistance to workflow modification. The analysis does not distinguish between tasks that AI can completely perform versus tasks where AI provides support. Many real-world applications involve augmentation rather than full replacement.

**Takeaways:** Given our limitations, these results should not be interpreted as predictions of job loss or definitive automation outcomes. They simply identify AI exposure hotspots in the labor force - occupations and sectors where AI tools, if used to the full extent on the tasks they can accomplish, are most likely to change workflows and task execution which may require workforce adaptation strategies.

---
### Tasks Automated

#### % Major Occupational Category Automated

**Description**
- Shows the percent of the tasks automated in the 23 major occupational categories as defined by the Bureau of Labor Statistics using national & Utah employment numbers.
- Each bar represents one major occupational category
- Percentages indicate what share of that major occupational categories total task completions are AI-automatable.

**Notable Results:**
- Top 3 categories are Educational Instruction and Library (53%), Legal (38.5%), and Office and Administrative Support (37%).
- Computer and Mathematical (33.4%) comes in at 5th place, contrary to Anthropics results, which had the majority by a wide margin of these occupations represented in their usage data. However one possible reason for this could be that their tasks take longer to complete, which would result in less coverage and therefore automation.
- Educational Instruction and Library has a significant margin above the next closest major occupational category
- Lowest occupations involve more physicality as would be expected.
---

#### Average % Occupation Automated By Major Occupational Category

**Description**
- Shows the average percent that an occupation's tasks are automated in the 23 major occupational categories as defined by the Bureau of Labor Statistics..
- Each bar represents one major occupational category
- Percentages indicate the average percent that an occupation's tasks are automated in that major occupational category.

**Notable Results:**
- WIP
---

#### Top 15 % Occupation Automated

**Description**
- Shows the 15 occupations with the highest percentage of their task completions classified as AI-automatable.
- Each bar represents one occupation with its major occupational category in brackets
- Percentages indicate what share of that occupation's total task completions are AI-automatable.

**Notable Results:**
- Educational occupations largely dominate the top positions (various Postsecondary Teachers)
- All top 15 occupations show above 80% automization.

---

### Workers Automated

#### Workers Automated by Major Occupational Category National

**Description**
- Assuming each task takes the same amount of time and that an AI-automatable task is completely automated by AI (all workers employ the use of AI for it completely), this shows the number of workers automated in each 23 major occupational categories as defined by the Bureau of Labor Statistics using national employment numbers. 
- Each bar represents one major occupational category
- Numbers indicate how many people in the major occupational category are AI-automatable. The percent of the maj occ cat tasks that are automatable is in parenthesis on the right.

**Notable Results:**
- WIP
---

#### Workers Automated by Major Occupational Category Utah

**Description**
- Assuming each task takes the same amount of time and that an AI-automatable task is completely automated by AI (all workers employ the use of AI for it completely), this shows the number of workers automated in each 23 major occupational categories as defined by the Bureau of Labor Statistics using utah employment numbers. 
- Each bar represents one major occupational category
- Numbers indicate how many people in the major occupational category are AI-automatable. The percent of the maj occ cat tasks that are automatable is in parenthesis on the right.

**Notable Results:**
- WIP
---

#### Top 15 Workers Automated by Occupation National

**Description**
- Assuming each task takes the same amount of time and that an AI-automatable task is completely automated by AI (all workers employ the use of AI for it completely), this shows the top 15 occupations with the highest number of workers automated using national employment data. 
- Each bar represents one occupation
- Numbers indicate how many people in the occupation are AI-automatable. The percent of the occupation's tasks that are automatable is in parenthesis on the right.

**Notable Results:**
- Office and Administrative Support show large presence
- Customer Service Representatives, Retail Salespersons, and Office Clerks are the top three by significant margins. 
- These results are partly skewed simply by occupations that have high employment.
- All occupations show above 80% automization.
---

#### Top 15 Workers Automated by Occupation Utah

**Description**
- Assuming each task takes the same amount of time and that an AI-automatable task is completely automated by AI (all workers employ the use of AI for it completely), this shows the top 15 occupations with the highest number of workers automated using Utah employment data. 
- Each bar represents one occupation
- Numbers indicate how many people in the occupation are AI-automatable. The percent of the occupation's tasks that are automatable is in parenthesis on the right.

**Notable Results:**
- WIP
---

### Economic Value of Automation

#### Economic Value Generated by Major Occupational Category National

**Description**
- Assuming each task completion has the same monetary value and that an automatable task is completely automated by AI (all workers employ the use of AI for it completely), this shows the economic value generated in each 23 major occupational categories as defined by the Bureau of Labor Statistics from automatable tasks using national employment and wage data.
- Each bar represents one major occupational category
- Numbers indicate how much monetary value is produced by automatable tasks. The percent of the maj occ cat tasks automatable is in parenthesis on the right.


**Notable Results:**
- WIP
---

#### Economic Value Generated by Major Occupational Category Utah

**Description**
- Assuming each task completion has the same monetary value and that an automatable task is completely automated by AI (all workers employ the use of AI for it completely), this shows the economic value generated in each 23 major occupational categories as defined by the Bureau of Labor Statistics from automatable tasks using Utah employment and wage data.
- Each bar represents one major occupational category
- Numbers indicate how much monetary value is produced by automatable tasks. The percent of the maj occ cat tasks automatable is in parenthesis on the right.


**Notable Results:**
- WIP
---

#### Top 15 Most Economic Value Generated by Occupation National

**Description**
- Assuming each task completion has the same monetary value and that an automatable task is completely automated by AI (all workers employ the use of AI for it completely), this shows the top 15 occupations with the most economic value generated from automatable tasks using national employment and wage data.
- Each bar represents one occupation
- Numbers indicate how much monetary value is produced by automatable tasks. The percent of the occupation's tasks that are automatable is in parenthesis on the right.

**Notable Results:**
- WIP
---

#### Top 15 Most Economic Value Generated by Occupation Utah

**Description**
- Assuming each task completion has the same monetary value and that an automatable task is completely automated by AI (all workers employ the use of AI for it completely), this shows the top 15 occupations with the most economic value generated from automatable tasks using Utah employment and wage data.
- Each bar represents one occupation
- Numbers indicate how much monetary value is produced by automatable tasks. The percent of the occupation's tasks that are automatable is in parenthesis on the right.

**Notable Results:**
- WIP
---

