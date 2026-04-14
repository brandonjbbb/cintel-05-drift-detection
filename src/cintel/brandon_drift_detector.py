"""
brandon_drift_detector.py - Project script.

Author: Denise Case
Date: 2026-03

Modified by: Brandon Jean-Baptiste
Date: 2026-04
"""

# === DECLARE IMPORTS ===

import logging
from pathlib import Path
from typing import Final

import polars as pl
from datafun_toolkit.logger import get_logger, log_header, log_path

# === CONFIGURE LOGGER ===

LOG: logging.Logger = get_logger("P5", level="DEBUG")

# === DEFINE GLOBAL PATHS ===

ROOT_DIR: Final[Path] = Path.cwd()
DATA_DIR: Final[Path] = ROOT_DIR / "data"
ARTIFACTS_DIR: Final[Path] = ROOT_DIR / "artifacts"

REFERENCE_FILE: Final[Path] = DATA_DIR / "reference_metrics_brandon.csv"
CURRENT_FILE: Final[Path] = DATA_DIR / "current_metrics_brandon.csv"

OUTPUT_FILE: Final[Path] = ARTIFACTS_DIR / "drift_summary_brandon.csv"
SUMMARY_LONG_FILE: Final[Path] = ARTIFACTS_DIR / "drift_summary_long_brandon.csv"

# === DEFINE THRESHOLDS ===

REQUESTS_DRIFT_THRESHOLD: Final[float] = 20.0
ERRORS_DRIFT_THRESHOLD: Final[float] = 2.0
LATENCY_DRIFT_THRESHOLD: Final[float] = 1000.0
ERROR_RATE_DRIFT_THRESHOLD: Final[float] = 0.02

# === DEFINE THE MAIN FUNCTION ===


def main() -> None:
    """Run the drift detection pipeline."""
    log_header(LOG, "CINTEL")

    LOG.info("========================")
    LOG.info("START main()")
    LOG.info("========================")

    log_path(LOG, "ROOT_DIR", ROOT_DIR)
    log_path(LOG, "REFERENCE_FILE", REFERENCE_FILE)
    log_path(LOG, "CURRENT_FILE", CURRENT_FILE)
    log_path(LOG, "OUTPUT_FILE", OUTPUT_FILE)

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    log_path(LOG, "ARTIFACTS_DIR", ARTIFACTS_DIR)

    # ----------------------------------------------------
    # STEP 1: READ REFERENCE AND CURRENT CSV INTO DATAFRAMES
    # ----------------------------------------------------
    reference_df = pl.read_csv(REFERENCE_FILE)
    current_df = pl.read_csv(CURRENT_FILE)

    LOG.info(f"Loaded {reference_df.height} reference records")
    LOG.info(f"Loaded {current_df.height} current records")

    # ----------------------------------------------------
    # STEP 2: CALCULATE AVERAGE METRICS FOR EACH PERIOD
    # ----------------------------------------------------
    reference_summary_df = reference_df.select(
        [
            pl.col("requests").mean().alias("reference_avg_requests"),
            pl.col("errors").mean().alias("reference_avg_errors"),
            pl.col("total_latency_ms").mean().alias("reference_avg_latency_ms"),
            (pl.col("errors").sum() / pl.col("requests").sum())
            .round(4)
            .alias("reference_error_rate"),
        ]
    )

    current_summary_df = current_df.select(
        [
            pl.col("requests").mean().alias("current_avg_requests"),
            pl.col("errors").mean().alias("current_avg_errors"),
            pl.col("total_latency_ms").mean().alias("current_avg_latency_ms"),
            (pl.col("errors").sum() / pl.col("requests").sum())
            .round(4)
            .alias("current_error_rate"),
        ]
    )

    # ----------------------------------------------------
    # STEP 3: COMBINE THE TWO ONE-ROW SUMMARY TABLES
    # ----------------------------------------------------
    combined_df: pl.DataFrame = pl.concat(
        [reference_summary_df, current_summary_df],
        how="horizontal",
    )

    # ----------------------------------------------------
    # STEP 4: DEFINE DIFFERENCE RECIPES
    # ----------------------------------------------------
    requests_mean_difference_recipe: pl.Expr = (
        (pl.col("current_avg_requests") - pl.col("reference_avg_requests"))
        .round(2)
        .alias("requests_mean_difference")
    )

    errors_mean_difference_recipe: pl.Expr = (
        (pl.col("current_avg_errors") - pl.col("reference_avg_errors"))
        .round(2)
        .alias("errors_mean_difference")
    )

    latency_mean_difference_recipe: pl.Expr = (
        (pl.col("current_avg_latency_ms") - pl.col("reference_avg_latency_ms"))
        .round(2)
        .alias("latency_mean_difference_ms")
    )

    error_rate_difference_recipe: pl.Expr = (
        (pl.col("current_error_rate") - pl.col("reference_error_rate"))
        .round(4)
        .alias("error_rate_difference")
    )

    # ----------------------------------------------------
    # STEP 4.1: APPLY THE DIFFERENCE RECIPES TO EXPAND THE DATAFRAME
    # ----------------------------------------------------
    drift_df: pl.DataFrame = combined_df.with_columns(
        [
            requests_mean_difference_recipe,
            errors_mean_difference_recipe,
            latency_mean_difference_recipe,
            error_rate_difference_recipe,
        ]
    )

    # ----------------------------------------------------
    # STEP 5: DEFINE DRIFT FLAG RECIPES
    # ----------------------------------------------------
    requests_is_drifting_flag_recipe: pl.Expr = (
        pl.col("requests_mean_difference").abs() > REQUESTS_DRIFT_THRESHOLD
    ).alias("requests_is_drifting_flag")

    errors_is_drifting_flag_recipe: pl.Expr = (
        pl.col("errors_mean_difference").abs() > ERRORS_DRIFT_THRESHOLD
    ).alias("errors_is_drifting_flag")

    latency_is_drifting_flag_recipe: pl.Expr = (
        pl.col("latency_mean_difference_ms").abs() > LATENCY_DRIFT_THRESHOLD
    ).alias("latency_is_drifting_flag")

    error_rate_is_drifting_flag_recipe: pl.Expr = (
        pl.col("error_rate_difference").abs() > ERROR_RATE_DRIFT_THRESHOLD
    ).alias("error_rate_is_drifting_flag")

    # ----------------------------------------------------
    # STEP 5.1: APPLY THE DRIFT FLAG RECIPES TO EXPAND THE DATAFRAME
    # ----------------------------------------------------
    drift_df = drift_df.with_columns(
        [
            requests_is_drifting_flag_recipe,
            errors_is_drifting_flag_recipe,
            latency_is_drifting_flag_recipe,
            error_rate_is_drifting_flag_recipe,
        ]
    )

    LOG.info("Calculated summary differences and drift flags")

    # ----------------------------------------------------
    # STEP 6: SAVE THE FLAT DRIFT SUMMARY AS AN ARTIFACT
    # ----------------------------------------------------
    drift_df.write_csv(OUTPUT_FILE)
    LOG.info(f"Wrote drift summary file: {OUTPUT_FILE}")

    LOG.info("Drift summary dataframe:")
    LOG.info(drift_df)
    LOG.info("Let's make that a bit nicer to read...")
    LOG.info("All remaining steps are about creating a nicer display.")

    # ----------------------------------------------------
    # OPTIONAL STEP 6.1: LOG THE SUMMARY ONE FIELD PER LINE
    # ----------------------------------------------------
    drift_summary_dict = drift_df.to_dicts()[0]

    LOG.info("========================")
    LOG.info("Drift Detection Process:")
    LOG.info("========================")
    LOG.info("1. Summarize each period with means.")
    LOG.info("2. Compute difference of means.")
    LOG.info("3. Compute difference in error rate.")
    LOG.info("4. Flag drift if absolute difference exceeds a threshold.")
    LOG.info("========================")

    LOG.info("Drift summary (one field per line):")
    for field_name, field_value in drift_summary_dict.items():
        LOG.info(f"{field_name}: {field_value}")

    # ----------------------------------------------------
    # OPTIONAL STEP 7: CREATE A LONG-FORM ARTIFACT FOR DISPLAY
    # ----------------------------------------------------
    drift_summary_long_df = pl.DataFrame(
        {
            "field_name": list(drift_summary_dict.keys()),
            "field_value": [str(value) for value in drift_summary_dict.values()],
        }
    )

    # ----------------------------------------------------
    # OPTIONAL STEP 7.1: SAVE THE LONG-FORM DRIFT SUMMARY AS AN ARTIFACT
    # ----------------------------------------------------
    drift_summary_long_df.write_csv(SUMMARY_LONG_FILE)
    LOG.info(f"Wrote long summary file: {SUMMARY_LONG_FILE}")

    LOG.info("========================")
    LOG.info("Pipeline executed successfully!")
    LOG.info("========================")
    LOG.info("END main()")


# === CONDITIONAL EXECUTION GUARD ===

if __name__ == "__main__":
    main()
