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
## Installation
### Requirements
- Python 3.13
- pip
### Setup
```bash
python -m venv venv 
source venv/Scripts/activate
pip install -r requirements.txt
```
## Usage
1. Clone [repository](https://github.com/SilverSeptember/CAS502)
2. Create virtual environment
3. Install dependencies
4. Run the main simulation script
```bash
python Epidemiology_Final_with_Migration_Final.py
```
### Model Parameters
In the current configuration, model parameters are defined within the script and can be directly modified to explore different scenarios. 
### Output
Plots are generated using matplotlib. 
* Time-series plots of susceptible, infected and recovered populations.
* Comparative visualizations of vaccination scenarios.
Figures will not output in current configuration.
### Notes
On Windows, Python requires Tcl/Tk support enabled. If Tcl/Tk 
unavailable or not working properly utilize the following:
```bash
MPLBACKEND=Agg python Epidemiology_Final_with_Migration_Final.py
```

## Bug Reports & Feature Requests
If you encounter a bug or would like to request a new feature, please open an Issue on this repository. 
Please include:
- Clear description of the issue
- Steps to reproduce the problem
- Expected behavior
- Your operating system and Python version
## Contributions
We welcome contributions to improve the model or extend its functionality.
All contributions should maintain readability, include appropriate comments and follow the existing project structure. 
To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes with clear documentation and comments
4. Submit a Pull Request

