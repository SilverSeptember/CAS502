"""Tkinter GUI for the CAS502 measles SIRS simulation

Launch by running this in the termnal: ``python scripts/run_model.py`` or::

    from cas502.gui import MeaslesGUI
    MeaslesGUI().mainloop()
"""

import matplotlib
matplotlib.use("TkAgg")

import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from cas502.simulate import Parameters, SimulationResults, run_simulation


# Narrative builder (standalone, testable without GUI)

def build_narrative_text(params: Parameters, results: SimulationResults) -> str:
    """Return a multi-line narrative string summarising parameters and results."""
    herd_thresh = 1.0 - 1.0 / params.R0_target
    sections = []

    sections.append(
        "Disease Parameters:\n"
        f"  gamma (recovery rate): {params.gamma} /week\n"
        f"  R0 (basic reproduction number): {params.R0_target}\n"
        f"  beta0 (transmission rate): {params.beta0:.2f}\n"
        f"  Relationship: beta0 = R0 * gamma = {params.R0_target} * {params.gamma} = {params.beta0:.2f}"
    )

    sections.append(
        "Immunity & Vaccination:\n"
        f"  lam (waning rate): {params.lam:.5f} /week (~{1.0/params.lam/52.0:.1f}-year duration)\n"
        f"  coverage (birth vaccination): {params.coverage:.4f}\n"
        f"  nu (catch-up vaccination): {params.nu} /week"
    )

    sections.append(
        "Demography:\n"
        f"  mu (natural death rate): {params.mu:.6f} /week (~{1.0/params.mu/52.0:.0f}-year lifespan)\n"
        f"  delta (disease mortality): {params.delta} /week\n"
        f"  Lambda (birth rate): {params.Lambda:.2f} /week"
    )

    sections.append(
        "Seasonality:\n"
        f"  seasonal_amp: {params.seasonal_amp}\n"
        f"  seasonal_T: {params.seasonal_T} weeks"
    )

    sections.append(
        "Importation:\n"
        f"  eta_I (trickle): {params.eta_I} /week\n"
        f"  Pulse events: magnitude {params.pulse_mag} at weeks {params.pulse_times}"
    )

    sections.append(
        "Initial Conditions:\n"
        f"  S0 = {params.S0c:,.0f},  I0 = {params.I0c:,.0f},  R0 = {params.R0c:,.0f}\n"
        f"  N = {params.N_star:,.0f}\n"
        f"  Simulation duration: {params.t_max:.0f} weeks ({params.t_max/52.0:.1f} years)"
    )

    sections.append(
        "Simulation Results:\n"
        f"  R0 (baseline): {params.beta0 / params.gamma:.1f}\n"
        f"  Peak infected (count): {results.peak_I:,.0f} at week {results.t_peak:.1f}\n"
        f"  Final proportions: S={results.Sp[-1]:.4f}, I={results.Ip[-1]:.4f}, R={results.Rp[-1]:.4f}"
    )

    sections.append(
        "Key Relationships:\n"
        f"  R0 = beta0 / gamma = {params.beta0:.2f} / {params.gamma} = {params.beta0/params.gamma:.1f}\n"
        f"  Herd immunity threshold: 1 - 1/R0 = {herd_thresh:.4f} ({herd_thresh*100:.1f}%)\n"
        f"  Current coverage ({params.coverage:.4f}) vs threshold ({herd_thresh:.4f}): "
        + ("ABOVE" if params.coverage >= herd_thresh else "BELOW")
    )

    return "\n\n".join(sections) + "\n"


# GUI 

class MeaslesGUI(tk.Tk):
    """Main application window for the measles simulation."""

    def __init__(self):
        super().__init__()
        self.title("CAS502 — Measles SIRS Simulation")
        self.geometry("1400x800")
        self.minsize(1000, 600)

        self._params = Parameters()
        self._results: SimulationResults | None = None
        self._figures: dict[str, plt.Figure] = {}
        self._canvases: dict[str, FigureCanvasTkAgg] = {}

        self._build_toolbar()
        self._build_main_area()
        self._populate_narrative_intro()

    #toolbar

    def _build_toolbar(self):
        toolbar = ttk.Frame(self, padding=5)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self._run_btn = ttk.Button(toolbar, text="Run Simulation", command=self._on_run)
        self._run_btn.pack(side=tk.LEFT, padx=(0, 20))

        # GUI editable parameters
        self.r0_var = tk.StringVar(value=str(self._params.R0_target))
        self.gamma_var = tk.StringVar(value=str(self._params.gamma))
        self.mu_var = tk.StringVar(value=str(self._params.mu))
        self.nu_var = tk.StringVar(value=str(self._params.nu))
        self.tmax_var = tk.StringVar(value=str(self._params.t_max))

        ttk.Label(toolbar, text="R0:").pack(side=tk.LEFT)
        ttk.Entry(toolbar, textvariable=self.r0_var, width=6).pack(side=tk.LEFT, padx=(2, 10))

        ttk.Label(toolbar, text="gamma (/wk):").pack(side=tk.LEFT)
        ttk.Entry(toolbar, textvariable=self.gamma_var, width=8).pack(side=tk.LEFT, padx=(2, 10))

        ttk.Label(toolbar, text="mu (/wk):").pack(side=tk.LEFT)
        ttk.Entry(toolbar, textvariable=self.mu_var, width=12).pack(side=tk.LEFT, padx=(2, 10))

        ttk.Label(toolbar, text="nu (/wk):").pack(side=tk.LEFT)
        ttk.Entry(toolbar, textvariable=self.nu_var, width=8).pack(side=tk.LEFT, padx=(2, 10))

        ttk.Label(toolbar, text="X-axis max (weeks):").pack(side=tk.LEFT)
        self._xmax_var = tk.StringVar(value="520")
        self._xmax_entry = ttk.Entry(toolbar, textvariable=self._xmax_var, width=8)
        self._xmax_entry.pack(side=tk.LEFT, padx=5)

        self._apply_btn = ttk.Button(toolbar, text="Apply", command=self._on_apply_xaxis)
        self._apply_btn.pack(side=tk.LEFT)

    # main area

    def _build_main_area(self):
        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashwidth=6)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Left: tabbed plots
        self._notebook = ttk.Notebook(paned)
        tab_names = [
            ("SIR vs SIRS", "sir_vs_sirs"),
            ("SIRS Proportion", "sirs_proportion"),
            ("Infected Count", "infected_count"),
            ("Coverage Sweep", "coverage_sweep"),
        ]
        for label, key in tab_names:
            frame = ttk.Frame(self._notebook)
            self._notebook.add(frame, text=label)
            fig = plt.Figure(figsize=(8, 5), dpi=100)
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            self._figures[key] = fig
            self._canvases[key] = canvas


        paned.add(self._notebook, stretch="always")


        #Right: the narrative text
        narrative_frame = ttk.Frame(paned)
        ttk.Label(narrative_frame, text="Model Narrative", font=("TkDefaultFont", 12, "bold")).pack(
            anchor=tk.W, padx=5, pady=(5, 0)
        )
        self._narrative = tk.Text(narrative_frame, wrap=tk.WORD, width=40, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(narrative_frame, orient=tk.VERTICAL, command=self._narrative.yview)
        self._narrative.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._narrative.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        paned.add(narrative_frame, stretch="never")

    # actions

    def _on_run(self):

        from tkinter import messagebox

        self._run_btn.configure(state=tk.DISABLED)
        self.update_idletasks()
        try:
            try: # Validate GUI inputs
                r0_input = float(self.r0_var.get())
                gamma = float(self.gamma_var.get())
                mu = float(self.mu_var.get())
                nu = float(self.nu_var.get())
            except ValueError:
                messagebox.showerror("Invalid Input", "All parameter fields must be numeric")
                return
            
            if r0_input <= 0:
                messagebox.showerror("Invalid Input", "R0 must be greater than 0.")
                return
            if gamma <= 0:
                messagebox.showerror("Invalid input", "Gamma must be greater than 0.")
                return
            if mu < 0:
                messagebox.showerror("Invalid input", "Mu must be greater than or equal to 0.")
                return
            if nu < 0: 
                messagebox.showerror("Invalid input", "Nu must be greater than or equal to 0.")
                return
            
            self._params.R0_target = r0_input
            self._params.gamma = gamma
            self._params.mu = mu
            self._params.nu = nu

            self._results = run_simulation(self._params)
            self._draw_all_plots()
            self._update_narrative()
        finally:
            self._run_btn.configure(state=tk.NORMAL)

    def _on_apply_xaxis(self):
        if self._results is None:
            return
        try:
            x_max = float(self._xmax_var.get())
        except ValueError:
            return
        self._draw_all_plots(x_max=x_max)

    #  plotting

    def _draw_all_plots(self, x_max=None):
        self._plot_sir_vs_sirs(x_max)
        self._plot_sirs_proportion(x_max)
        self._plot_infected_count(x_max)
        self._plot_coverage_sweep()  # x-axis is coverage, not time

    def _plot_sir_vs_sirs(self, x_max=None):
        results = self._results
        figure = self._figures["sir_vs_sirs"]
        figure.clear()
        axis = figure.add_subplot(111)
        axis.plot(results.t, results.sol_sir[:, 1], label="I (SIR)")
        axis.plot(results.t, results.sol_sirs[:, 1], label="I (SIRS, seasonal)")
        axis.set_xlabel("Weeks")
        axis.set_ylabel("Proportion infected")
        axis.set_title("I(t): SIR vs SIRS")
        axis.legend()
        if x_max is not None:
            axis.set_xlim(0, x_max)
        figure.tight_layout()
        self._canvases["sir_vs_sirs"].draw()

    def _plot_sirs_proportion(self, x_max=None):
        results = self._results
        figure = self._figures["sirs_proportion"]
        figure.clear()
        axis = figure.add_subplot(111)
        axis.plot(results.t, results.Ip, label="I/N")
        axis.set_xlabel("Weeks")
        axis.set_ylabel("Proportion infected")
        axis.set_title("Expanded SIRS — measles-like seasonality & coverage")
        axis.legend()
        if x_max is not None:
            axis.set_xlim(0, x_max)
        figure.tight_layout()
        self._canvases["sirs_proportion"].draw()

    def _plot_infected_count(self, x_max=None):
        results = self._results
        figure = self._figures["infected_count"]
        figure.clear()
        axis = figure.add_subplot(111)
        axis.plot(results.t, results.I_c, label="Infected (count)")
        axis.set_xlabel("Weeks")
        axis.set_ylabel("Individuals")
        axis.set_title("Infected count with demography, mortality, importation")
        axis.legend()
        if x_max is not None:
            axis.set_xlim(0, x_max)
        figure.tight_layout()
        self._canvases["infected_count"].draw()

    def _plot_coverage_sweep(self):
        results = self._results
        figure = self._figures["coverage_sweep"]
        figure.clear()
        axis = figure.add_subplot(111)
        axis.plot(results.coverages, results.peaks, marker="o")
        axis.set_xlabel("Coverage (vaccinated at birth)")
        axis.set_ylabel("Peak I (approx, normalized)")
        axis.set_title("Peak infection vs vaccination coverage")
        figure.tight_layout()
        self._canvases["coverage_sweep"].draw()

    #narrative

    def _populate_narrative_intro(self):
        self._narrative.configure(state=tk.NORMAL)
        self._narrative.delete("1.0", tk.END)
        self._narrative.insert(tk.END,
            "Welcome to the CAS502 Measles Simulation.\n\n"
            "Click 'Run Simulation' to compute the SIR, SIRS, and extended "
            "SIRS models with measles-like parameters.\n\n"
            "After the simulation completes, this panel will display a "
            "detailed narrative of the model parameters and results.\n\n"
            "Use the 'X-axis max' control to zoom the time-series plots."
        )
        self._narrative.configure(state=tk.DISABLED)

    def _update_narrative(self):
        text = build_narrative_text(self._params, self._results)
        self._narrative.configure(state=tk.NORMAL)
        self._narrative.delete("1.0", tk.END)
        self._narrative.insert(tk.END, text)
        self._narrative.configure(state=tk.DISABLED)
