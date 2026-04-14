# Continuous Intelligence

This site provides documentation for this project.
Use the navigation to explore module-specific materials.

## How-To Guide

Many instructions are common to all our projects.

See
[⭐ **Workflow: Apply Example**](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/)
to get these projects running on your machine.

## Project Documentation Pages (docs/)

- **Home** - this documentation landing page
- **Project Instructions** - instructions specific to this module
- **Your Files** - how to copy the example and create your version
- **Glossary** - project terms and concepts

## Additional Resources

- [Suggested Datasets](https://denisecase.github.io/pro-analytics-02/reference/datasets/cintel/)

## Custom Project

### Dataset
I used two CSV datasets containing system performance metrics collected during two different periods: a reference period and a current period. The datasets include requests, errors, and total latency in milliseconds, which let me compare expected system behavior to more recent behavior.

### Signals
The main signals used in this project were average requests, average errors, average total latency, and a derived error rate signal. I also created difference signals and drift flags to show when the current system behavior changed enough from the reference baseline to be considered meaningful.

### Experiments
My main modification experiment was adding error rate as a new derived metric and drift signal. I wanted to test whether comparing errors relative to requests would provide a more useful reliability measure than raw error counts alone.

### Results
After running the project, the output artifacts showed the reference and current summaries, the differences between them, and drift flags for each signal. The added error rate metric gave me another way to detect whether system reliability had changed between the two periods.

### Interpretation
This means the system can now be monitored not only for changes in traffic and latency, but also for changes in reliability relative to workload. From a business intelligence perspective, this helps identify whether performance issues are simply caused by higher demand or whether service quality itself is drifting in a concerning way.
