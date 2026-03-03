# Semantic Model Complexity for Event Graph Discrete-Event Simulation Models via Abstract State Machines

Reproducible companion repository for the paper *"Semantic Model Complexity for Event Graph Discrete-Event Simulation Models via Abstract State Machines."*.

This repository allows readers to reproduce all results from the paper, including complexity metric calculation, runtime measurement, log-log regression analysis, and figure generation.

## Quick Start

```bash
pip install -r requirements.txt
```

Then run the notebooks in order:

| Notebook | Description |
|----------|-------------|
| `00_simasm_pipeline.ipynb` | Walk through the SimASM pipeline: event graph to assembly to simulation to complexity analysis |
| `01_complexity_metrics.ipynb` | Calculate SMC, CC, LOC, KC for all 47 models and verify against pre-computed values |
| `02_runtime_measurement.ipynb` | Run O2DES simulations (or load pre-computed results) |
| `03_regression_analysis.ipynb` | Log-log regression, out-of-sample prediction, Diebold-Mariano tests |
| `04_figures.ipynb` | Generate all paper figures |

Pre-computed results are included in `data/results/`, so you can reproduce the analysis without re-running simulations. Set `RERUN = True` in notebook 02 to regenerate runtime measurements from scratch.

## Repository Structure

```
simasm-complexity-project/
├── README.md
├── LICENSE                           # MIT
├── requirements.txt
│
├── notebooks/
│   ├── 00_simasm_pipeline.ipynb      # SimASM pipeline walkthrough
│   ├── 01_complexity_metrics.ipynb   # Calculate SMC, CC, LOC, KC
│   ├── 02_runtime_measurement.ipynb  # Run O2DES simulations (or load pre-computed)
│   ├── 03_regression_analysis.ipynb  # Log-log regression, OOS, DM tests
│   └── 04_figures.ipynb              # Generate all paper figures
│
├── src/
│   ├── __init__.py
│   ├── utils.py                      # Shared helpers (metrics, regression, DM test)
│   ├── o2despy/                      # Bundled O2DES.py framework
│   └── models/                       # Generated O2DES queue models (Python)
│
├── data/
│   ├── models/                       # JSON event graph specifications (47 models)
│   ├── simasm/                       # SimASM source files (for HET analysis)
│   └── results/                      # Pre-computed results
│       ├── all_metrics.json          # Combined metrics for all models
│       ├── hybrid_runtime.json       # Runtime data (47 models x 30 replications)
│       ├── runtime_measurements.csv  # Conference paper runtime data
│       └── runtime_summary.csv       # Aggregated with 95% CI
│
└── output/                           # Generated figures and tables (via notebooks)
```

## Models

The study uses 47 queueing network models across four topologies:

| Topology   | Development Set | OOS Set | Total |
|------------|-----------------|---------|-------|
| Tandem     | 9 (n=1..20)     |         | 9     |
| Fork-Join  | 9 (n=1..20)     |         | 9     |
| Feedback   | 9 (n=1..20)     |         | 9     |
| Hybrid     |                 | 9       | 9     |
| **Total**  | **27**          | **9**   | **36** |

The development set (27 models) is used for log-log regression fitting. The out-of-sample set consists of 9 hybrid models in a 3x3 factorial design (N in {2,3,4}, M in {2,3,4}).

## Complexity Metrics

| Metric | Source | Method |
|--------|--------|--------|
| **SMC** (SimASM Model Complexity) | `.simasm` files | HET analysis via `simasm` |
| **CC** (Cyclomatic Number) | `.json` event graph specs | M = E - V + 2P |
| **LOC** (Lines of Code) | `.simasm` files | Non-blank, non-comment lines |
| **KC** (Kolmogorov Complexity) | `.simasm` files | log2(zlib compressed size) |

## The SimASM Pipeline

Notebook 00 walks through the full SimASM pipeline for a single model:

```
Event Graph (JSON)  --simasm.convert_model()-->  SimASM Assembly (.simasm)
                                                        |
                                     +------------------+------------------+
                                     |                  |                  |
                              run_experiment()    analyze_simasm()    register_model()
                                     |                  |                  |
                              Simulation          SMC / HET         Model Registry
                              Results             Metrics           (reuse in expts)
```

SimASM's assembly code is a formal intermediate representation that captures the full operational semantics of each simulation model. Its structured complexity (SMC) captures model difficulty that surface-level metrics (LOC, cyclomatic number) miss.

## Dependencies

- [`simasm`](https://pypi.org/project/simasm/) - SimASM compiler, runtime, and HET complexity analyzer
- `numpy`, `scipy` - numerical computation and statistics
- `matplotlib` - figure generation
- `pandas` - data handling (used by O2DES.py)
- `sortedcontainers` - required by O2DES.py
- `jupyter` - notebook execution

## License

MIT
