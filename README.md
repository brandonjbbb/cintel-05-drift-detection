# cintel-05-drift-detection

[![Python 3.14+](https://img.shields.io/badge/python-3.14%2B-blue?logo=python)](#)
[![MIT](https://img.shields.io/badge/license-see%20LICENSE-yellow.svg)](./LICENSE)

> Professional Python project for continuous intelligence and drift detection.

Continuous intelligence systems monitor data streams, detect change, and support informed decisions in real time. This project applies those ideas through a professional Python workflow using baseline comparison and drift detection.

In the age of generative AI, durable skills are grounded in real work: setting up a professional environment, reading and running code, understanding project logic, modifying code, documenting results, and pushing work to a shared repository. This project follows the structure of a professional Python analytics project and helps build those habits through hands-on practice.

## This Project

This project focuses on **drift detection**.

Drift detection often begins with **baseline comparison**, comparing **current** system behavior to an earlier **reference period**. The goal is to identify meaningful changes in system behavior by comparing summary statistics across two time periods.

This project reads system metrics from input CSV files, calculates average values for each period, measures the difference between them, and flags potential drift when the change exceeds a chosen threshold.

The project helps demonstrate:

- how average metrics are compared across time periods
- how baseline differences can indicate system change
- how drift flags can be used to highlight meaningful change
- how project outputs can be saved as artifacts for review

## My Custom Project

I modified the example project by adding a new derived metric called **error rate**.

Error rate is calculated as total errors divided by total requests. I made this change because error rate gives a more meaningful measure of reliability than raw error counts alone. A system may have more total errors simply because it handled more traffic, but error rate helps show whether reliability itself changed.

After running the modified project, the output includes:

- reference and current error rate
- error rate difference
- error rate drift flag

This made the project more useful for understanding changes in service quality as well as changes in workload.

## Data

My custom pipeline reads system metrics from:

- `data/reference_metrics_brandon.csv`
- `data/current_metrics_brandon.csv`

Each row represents one observation of system behavior.

The datasets include these fields:

- `requests` - number of requests handled
- `errors` - number of failed requests
- `total_latency_ms` - total response time in milliseconds

The pipeline compares the reference and current datasets, summarizes the metrics, calculates differences, and saves the drift results as artifacts.

## Output Artifacts

After running the project, the following output files are created in `artifacts/`:

- `artifacts/drift_summary_brandon.csv`
- `artifacts/drift_summary_long_brandon.csv`

The first file saves the summary results in a wide one-row format.
The second file saves the same results in a long format with one field per row, which is easier to read.

## Working Files

The main parts of this project are:

- **data/** - input datasets
- **docs/** - project documentation
- **src/cintel/** - Python pipeline code
- **artifacts/** - generated output files
- **pyproject.toml** - project metadata and dependencies
- **zensical.toml** - documentation site configuration

## Setup

### Clone the repository

In a machine terminal, open your `Repos` folder and run:

```shell
git clone https://github.com/brandonjbbb/cintel-05-drift-detection.git
cd cintel-05-drift-detection
code .
