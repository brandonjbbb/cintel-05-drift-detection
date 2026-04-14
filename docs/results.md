# Results

## Output artifacts

After running the pipeline, the project generates:

- `artifacts/drift_summary_brandon.csv`
- `artifacts/drift_summary_long_brandon.csv`

## What the results show

The results compare the reference period to the current period and report:

- average requests
- average errors
- average latency
- error rate
- differences between periods
- drift flags for each metric

## Observation

The long-form summary artifact is easier to read because it places one field on each row rather than using a single wide row.

## Why this matters

This kind of workflow helps analysts monitor systems over time, document changes, and identify when current behavior may no longer match an expected baseline.
