# CAS 502 - Spring 2026

## Team
Nicole Silvers, John Moore

# Project Overview

## Description
Project implements a measles epidemic model. Reconfigured from a 
Jupyter Notebook into a structured Python package Course project
with:
 - Tkinter based GUI
 - Editable epidemiological parameters
 - Independent X-axis control
 - Script based execution for reproducibility
 - Automated testing through pytest
 - Version pinned dependencies 


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

### System Requirements
- Python 3.13
- pip
- Tkinter 

Note: Tkinter is usually bundled with Python on macOS and Windows. On some Linux distros, it isn't included by default and has to be installed separately via the package manager.
Example: Ubuntu may require: 
```bash
sudo apt install python3-tk 
```


### Setup
```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

### Dependencies
numpy==2.4.*
scipy==1.17.*
matplotlib==3.10.*
pytest==9.*


## Usage
1. Clone [repository](https://github.com/SilverSeptember/CAS502)
2. Create virtual environment
3. Install dependencies
4. Launch the GUI (primary interface):
```bash
python scripts/run_model.py
```

### GUI Usage

#### Interface Guide
- Click **Run Simulation** to compute all three models (SIR, SIRS, extended SIRS with demography).
- Four tabbed plots appear on the left:
  1. **SIR vs SIRS** — proportion infected over time for both models.
  2. **SIRS Proportion** — I/N from the extended model with seasonality and vaccination.
  3. **Infected Count** — absolute infected count with demography, mortality, and importation.
  4. **Coverage Sweep** — peak infection vs vaccination coverage (80%–98%).
- The **Model Narrative** panel on the right displays all parameter values, computed quantities, and key epidemiological relationships.
- Use **X-axis max (weeks)** + **Apply** to zoom the time-series plots (tabs 1–3).

### Legacy Script
The original script ported from Jupyter can still be run directly:
```bash
python3 Epidemiology_Final_with_Migration_Final.py
```

### Output
Plots are generated using matplotlib embedded in the Tkinter GUI.
* Time-series plots of susceptible, infected, and recovered populations.
* Comparative visualizations of vaccination scenarios.

### Notes
On Windows, Python requires Tcl/Tk support enabled. If Tcl/Tk is
unavailable or not working properly, use the legacy python script like this:

```bash
MPLBACKEND=Agg python Epidemiology_Final_with_Migration_Final.py
```

## Bug Reports & Feature Requests
If you encounter a bug or would like to request a new feature, please open an Issue on this repository. 
Please include:
1. Clear description of the issue
2. Steps to reproduce the problem
3. Expected behavior
4. Your operating system and Python version

## Contributions
We welcome contributions to improve the model or extend its functionality.
All contributions should maintain readability, include appropriate comments and follow the existing project structure. 
To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes with clear documentation and comments
4. Submit a Pull Request

