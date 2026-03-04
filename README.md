# CAS 502 - Spring 2026

## Team
Nicole Silvers, John Moore

## Project Overview

### Description
This project implements a measles epidemic model that explores how vaccination coverage, waning immunity, seasonality, and migration affect disease outbreaks in a population. It was originally developed as a Jupyter Notebook and has been refactored into a structured Python package.

The model progresses through three levels of complexity: a basic SIR (Susceptible-Infected-Recovered) model, an SIRS model that adds waning immunity and vaccination, and a full extended SIRS model with demography, disease mortality, seasonal forcing, importation of infections, and migration. This allows users to see how each added layer of realism changes the epidemic dynamics.

### Features
 - Tkinter based GUI for interactive exploration
 - Editable epidemiological parameters (R0, gamma, mu, nu)
 - Independent X-axis control for zooming time-series plots
 - Script based execution for reproducibility
 - Automated testing through pytest  
 - Version pinned dependencies

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

### Dependencies
```text
numpy==2.4.*
scipy==1.17.*
matplotlib==3.10.*
pytest==9.*
```

### Setup
```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows
pip install -r requirements.txt # Install dependencies
```

## Usage

### Steps
1. Clone the [repository](https://github.com/SilverSeptember/CAS502)
2. Create a virtual environment
3. Install dependencies
4. Launch the GUI (primary interface):
```bash
python scripts/run_model.py
```
### GUI Guide
- Click **Run Simulation** to compute all three models (SIR, SIRS, and extended SIRS with demography and migration).
- Four tabbed plots appear on the left:
  1. **SIR vs SIRS** — Shows the proportion of the population infected
     over time for both models side by side. The SIR curve will always
     show a single epidemic wave that dies out permanently. The SIRS
     curve shows recurring waves because waning immunity and seasonality
     allow the disease to come back. Comparing the two illustrates why
     waning immunity matters for a disease like measles.
  2. **SIRS Proportion** — Shows I/N (infected as a fraction of total
     population) from the extended model that includes seasonality and
     vaccination. This plot reveals the long-term oscillating pattern
     of endemic measles — the disease never fully disappears but rises
     and falls with seasonal cycles.
  3. **Infected Count** — Shows the absolute number of infected
     individuals over time from the full model with demography,
     mortality, and importation. Unlike the proportion plots, this
     shows raw numbers so you can see the actual scale of outbreaks.
     Spikes may appear at importation pulse times (weeks 130 and 390
     by default) when external infections are introduced.
  4. **Coverage Sweep** — Shows how peak infection changes as
     vaccination coverage increases from 80% to 98%. The downward
     trend demonstrates that higher coverage reduces outbreak severity.
     The shape of this curve shows how close the population is to
     herd immunity — a steep drop indicates the threshold where
     vaccination becomes effective enough to suppress major outbreaks.
- The **Model Narrative** panel on the right displays all parameter values, derived epidemiological quantities, and key parameter relationships.
- Use **X-axis max (weeks)** + **Apply** to zoom the time-series plots (tabs 1–3).



### Editable Parameters
The toolbar lets you modify four parameters before running a simulation:
- **R0** — Basic reproduction number. For measles, typically 12–18. Higher values mean more transmissible. Default: 15.
- **gamma** — Recovery rate in 1/weeks. A value of 1.0 means an average infectious period of 1 week. Default: 1.0.
- **mu** - Natural death rate in 1/weeks. Default corresponds to a ~70-year lifespan.
- **nu** — Catch-up vaccination rate in 1/weeks. The rate at which susceptible individuals get vaccinated. Default: 0.005.

### Legacy Script
The original script ported from Jupyter can still be run directly:
```bash
python3 Epidemiology_Final_with_Migration_Final.py
```

On Windows, if Tcl/Tk is unavailable or not working properly:
```bash
MPLBACKEND=Agg python Epidemiology_Final_with_Migration_Final.py
```

## Testing
Run the full test suite:
```bash
python -m pytest -v
```

The test suite includes three levels:
- **Unit tests** — test individual functions in isolation with known inputs and expected outputs (for now it includes tests for beta_t and sir_rhs functions in model.py)
- **Integration tests** — run the full simulation pipeline and verify properties of the combined output (conservation, peak behavior, coverage sweep)
- **System tests** — verify that modules import correctly, scripts parse without errors, and the narrative builder produces valid output

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

We chose MIT because it is simple, permissive, and widely used in academic
and open source projects. It allows anyone to use, modify, and distribute
the code with minimal restrictions, which fits the educational and
collaborative nature of this project.

## Citation
This repository includes a `CITATION.cff` for software citation metadata.

Zenodo DOI: 10.5281/zenodo.18856455

## Bug Reports & Feature Requests
If you encounter a bug or would like to request a new feature, please open an Issue on this repository.
Please include:
1. A clear description of the issue
2. Steps to reproduce the problem
3. Expected behavior
4. Your operating system and Python version

## Contributions
We welcome contributions to improve the model or extend its functionality.
All contributions should maintain readability, include appropriate comments, and follow the existing project structure.
To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes with clear documentation and comments
4. Submit a Pull Request

## Development & Planning
### Challenges
Proficiency using Git and GitHub, which is new to one of us and 
the other is a non-expert. Time zone differences and other time 
commitments in the form of work, life and courseload will pose 
other challenges. Outside events, beyond the control of either 
participants. Unequal coding proficiency and experience will 
challenge participants.

### Communications Plan
Asynchronous work in parallel, using slack, canvas and in code 
comments to notify other of status and challenges. Honesty and 
transparency in communications to offset experience and anxiety 
impacts. Mutually understood goal to continue working towards 
full program functionality regardless of challenge or 
communication status.

### Git branching
All team members have committed to a single branch thus far. For 
the further development of the project we will use feature 
branches. We will each develop locally on feature branches for 
our assigned features. When the feature coding is completed, we 
will open pull requests (PRs). When each PR is tested and 
approved, it will be merged with the main branch.
