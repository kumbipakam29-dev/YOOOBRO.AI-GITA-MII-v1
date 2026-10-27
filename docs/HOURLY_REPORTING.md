# Hourly Reporting

The GitHub Actions workflow is scheduled for minute 17 of each hour and can also be run manually from the Actions tab.

The workflow currently creates a status snapshot from the repository and current run metadata. It does not continuously train a model, watch arbitrary external servers, or guarantee that every scheduled run executes on time.

GitHub may delay scheduled workflows. The first run should be checked in the Actions tab after the repository has received the workflow commit.

Report labels:
- Actual training: only when a training command has executed and emitted evidence.
- Simulation: synthetic assumptions only; never physical hardware metrics.
- Planned: not yet executed.
- Unverified: no independent confirmation is recorded.
