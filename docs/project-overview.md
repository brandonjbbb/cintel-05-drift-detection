# Project Overview

## Problem

System behavior can change over time. A process that once behaved normally may begin to show differences in volume, reliability, or latency.

## Approach

This project uses a simple drift detection pipeline:

1. Read reference and current metrics from CSV files
2. Calculate average values for each period
3. Compute the difference between current and reference values
4. Flag drift when the difference exceeds a threshold
5. Save results as artifact files

## Metrics used

The project compares:

- requests
- errors
- total latency in milliseconds
- error rate

## Why error rate matters

Raw error counts can increase just because traffic increases. Error rate gives a more meaningful measure of reliability because it puts errors in context relative to requests.
