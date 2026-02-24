# CAS502 - Spring 2026
## Team
John Moore, Nicole Silvers
# Project Overview
## Description
Course project for CAS 502. A Measles Model will be transferred 
from Jupyter Notebooks to Python so a GUI and further 
functionality can be integrated.
## Challenges
Proficiency using Git and GitHub, which is new to one of us and 
the other is a non-expert. Time zone differences and other time 
commitments in the form of work, life and courseload will pose 
other challenges. Outside events, beyond the control of either 
participants. Unequal coding proficiency and experience will 
challenge participants.
## Communications Plan
Asynchronous work in parallel, using slack, canvas and in code 
comments to notify other of status and challenges. Honesty and 
transparency in communications to offset experience and anxiety 
impacts. Mutually understood goal to continue working towards 
full program functionality regardless of challenge or 
communication status.
## Git branching
All team members have committed to a single branch thus far. For 
the further development of the project we will use feature 
branches. We will each develop locally on feature branches for 
our assigned features. When the feature coding is completed, we 
will open pull requests (PRs). When each PR is tested and 
approved, it will be merged with the main branch.
## Setup and Usage
Project requires Python 3.13.
### Setup
```bash
python -m venv venv 
source venv/Scripts/activate
pip install -r requirements.txt
```
### Usage
1. Clone [repository](https://github.com/SilverSeptember/CAS502)
2. Create virtual environment
3. Install dependencies
4. Run the main simulation script
## Notes
On Windows, Python requires Tcl/Tk support enabled. If Tcl/Tk 
unavailable or not working properly utilize the following:
```bash
MPLBACKEND=Agg python Epidemiology_Final_with_Migration_Final.py
```
Figures will not output in current configuration. 

