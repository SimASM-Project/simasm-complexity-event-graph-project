"""Shared utility functions for complexity analysis and regression."""

import ast
import csv
import gzip
import json
import math
import os
import zlib
from pathlib import Path

import numpy as np
from scipy import stats


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_metrics(path):
    """Load metrics from JSON file. Returns list of dicts."""
    with open(path) as f:
        return json.load(f)


def load_runtime(path):
    """Load runtime data from JSON file. Returns list of dicts."""
    with open(path) as f:
        return json.load(f)


def load_runtime_csv(path):
    """Load runtime measurements CSV. Returns list of dicts."""
    with open(path) as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            for k in ("cpu_time", "wall_time", "departures", "throughput", "L", "L_q", "W"):
                if k in row:
                    row[k] = float(row[k])
            if "seed" in row:
                row["seed"] = int(row["seed"])
            rows.append(row)
        return rows


def merge_metrics_runtime(metrics, runtime):
    """Merge metrics and runtime data on model_name. Returns list of dicts."""
    rt_map = {r["model_name"]: r for r in runtime}
    merged = []
    for m in metrics:
        name = m["model_name"]
        if name in rt_map:
            entry = dict(m)
            entry["wall_time"] = rt_map[name]["wall_time"]
            entry["wall_time_std"] = rt_map[name].get("wall_time_std", None)
            entry["runtimes"] = rt_map[name].get("runtimes", [])
            merged.append(entry)
    return merged


# ---------------------------------------------------------------------------
# Complexity metrics
# ---------------------------------------------------------------------------

def compute_cc(filepath):
    """Compute cyclomatic complexity of a Python file using AST.

    CC = number of decision points + 1
    Decision points: if, elif, for, while, except, with, and, or,
                     assert, list/set/dict comprehension, ternary (IfExp)
    """
    with open(filepath) as f:
        source = f.read()
    tree = ast.parse(source)
    complexity = 1  # base
    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.IfExp)):
            complexity += 1
        elif isinstance(node, (ast.For, ast.While)):
            complexity += 1
        elif isinstance(node, ast.ExceptHandler):
            complexity += 1
        elif isinstance(node, ast.With):
            complexity += 1
        elif isinstance(node, ast.Assert):
            complexity += 1
        elif isinstance(node, ast.BoolOp):
            # each 'and'/'or' adds a branch
            complexity += len(node.values) - 1
        elif isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            complexity += len(node.generators)
    return complexity


def compute_loc(filepath, comment_prefix="//"):
    """Compute physical lines of code (non-blank, non-comment).

    For .simasm files, comments start with '//'.
    For .py files, pass comment_prefix='#'.
    """
    count = 0
    with open(filepath) as f:
        for line in f:
            stripped = line.strip()
            if stripped and not stripped.startswith(comment_prefix):
                count += 1
    return count


def compute_kc(filepath):
    """Approximate Kolmogorov complexity using zlib compression.

    Returns log2 of compressed size in bytes.
    Uses zlib.compress (deflate) at maximum compression level.
    """
    with open(filepath, "rb") as f:
        data = f.read()
    compressed = zlib.compress(data, 9)
    return math.log2(len(compressed))


def compute_cyclomatic_number(json_path):
    """Compute graph-theoretic cyclomatic number from event graph JSON.

    Cyclomatic number M = E - V + 2P
    where E = edges, V = vertices, P = connected components (1 for our models).
    """
    with open(json_path) as f:
        spec = json.load(f)
    v = len(spec.get("vertices", []))
    e = len(spec.get("scheduling_edges", [])) + len(spec.get("cancelling_edges", []))
    p = 1  # single connected component
    return e - v + 2 * p


# ---------------------------------------------------------------------------
# Regression helpers
# ---------------------------------------------------------------------------

def fit_loglog(x, y):
    """Fit log-log linear regression: log(y) = a + b*log(x).

    Returns dict with slope, intercept, r2, std_err, p_value.
    """
    log_x = np.log(np.array(x, dtype=float))
    log_y = np.log(np.array(y, dtype=float))
    slope, intercept, r_value, p_value, std_err = stats.linregress(log_x, log_y)
    return {
        "slope": slope,
        "intercept": intercept,
        "r2": r_value ** 2,
        "r_value": r_value,
        "p_value": p_value,
        "std_err": std_err,
    }


def predict_loglog(x, slope, intercept):
    """Predict y from log-log model: y = exp(intercept) * x^slope."""
    x = np.array(x, dtype=float)
    return np.exp(intercept) * x ** slope


def compute_r2(actual, predicted):
    """Compute R-squared (coefficient of determination)."""
    actual = np.array(actual, dtype=float)
    predicted = np.array(predicted, dtype=float)
    ss_res = np.sum((actual - predicted) ** 2)
    ss_tot = np.sum((actual - np.mean(actual)) ** 2)
    if ss_tot == 0:
        return 1.0
    return 1.0 - ss_res / ss_tot


def compute_r2_logspace(actual, predicted, train_y):
    """Compute OOS R² in log-space using training set mean as baseline.

    R² = 1 - SS_res(log) / SS_tot(log, train_mean)
    where SS_tot uses the mean of log(train_y) rather than the OOS mean.
    """
    log_actual = np.log(np.array(actual, dtype=float))
    log_predicted = np.log(np.array(predicted, dtype=float))
    log_train_mean = np.mean(np.log(np.array(train_y, dtype=float)))
    ss_res = np.sum((log_actual - log_predicted) ** 2)
    ss_tot = np.sum((log_actual - log_train_mean) ** 2)
    if ss_tot == 0:
        return 1.0
    return 1.0 - ss_res / ss_tot


def compute_mape(actual, predicted):
    """Compute Mean Absolute Percentage Error."""
    actual = np.array(actual, dtype=float)
    predicted = np.array(predicted, dtype=float)
    return np.mean(np.abs((actual - predicted) / actual)) * 100


def compute_rmse(actual, predicted):
    """Compute Root Mean Squared Error."""
    actual = np.array(actual, dtype=float)
    predicted = np.array(predicted, dtype=float)
    return np.sqrt(np.mean((actual - predicted) ** 2))


def diebold_mariano(e1, e2, h=1):
    """Diebold-Mariano test for equal predictive accuracy.

    Compares squared forecast errors e1^2 vs e2^2.
    Returns DM statistic and p-value.
    H0: both forecasts have equal accuracy.
    Negative DM => model 1 is better (smaller errors).
    """
    e1 = np.array(e1, dtype=float)
    e2 = np.array(e2, dtype=float)
    d = e1 ** 2 - e2 ** 2
    n = len(d)
    d_bar = np.mean(d)

    # Newey-West variance estimator
    gamma_0 = np.var(d, ddof=0)
    if h > 1:
        for k in range(1, h):
            gamma_k = np.mean((d[k:] - d_bar) * (d[:-k] - d_bar))
            gamma_0 += 2 * gamma_k

    if gamma_0 == 0:
        return 0.0, 1.0

    dm_stat = d_bar / np.sqrt(gamma_0 / n)
    p_value = 2 * (1 - stats.norm.cdf(abs(dm_stat)))
    return dm_stat, p_value


def spearman_rank(x, y):
    """Compute Spearman rank correlation."""
    rho, p = stats.spearmanr(x, y)
    return rho, p
