
# CI/CD Pipeline Project
[![CI Pipeline](https://github.com/SangaviKS/cicd-pipeline-project/actions/workflows/ci.yml/badge.svg)](https://github.com/SangaviKS/cicd-pipeline-project/actions/workflows/ci.yml)

[![Build Status](https://dev.azure.com/sangavi-devops/cicd-pipeline-project/_apis/build/status%2FSangaviKS.cicd-pipeline-project?branchName=main)](https://dev.azure.com/sangavi-devops/cicd-pipeline-project/_build/latest?definitionId=1&branchName=main)

Automated CI/CD pipeline demonstrating Python testing, coverage reporting,
and multi-platform pipeline configuration using both GitHub Actions and
Azure DevOps.

## Overview

This project takes sensor simulation logic (reused from my [IoT Telemetry
Pipeline project](https://github.com/yourusername/azure-aws-iot-telemetry-pipeline))
and wraps it in a complete CI/CD workflow — automated testing, multi-version
compatibility checks, code coverage reporting, and branch-based deployment
gates.

## Features
- 14 pytest unit tests covering sensor data generation, anomaly detection, and validation logic
- Multi-version testing (Python 3.11 and 3.12) on every push
- Dual pipeline implementation: GitHub Actions (fully verified) and Azure DevOps (configured, pending hosted agent parallelism approval for personal-tier organizations)
- Code coverage reporting (target: 90%+)
- Branch-based workflow with PR-gated merges to main
- Test results and coverage published as pipeline artifacts

## Tech Stack
- **Language:** Python 3.11 / 3.12
- **Testing:** pytest, pytest-cov
- **CI/CD:** GitHub Actions, Azure DevOps Pipelines

## Project Structure
```text
cicd-pipeline-project/
├── core/
│   └── sensor.py              # Sensor logic, anomaly detection, validation
├── tests/
│   └── test_sensor.py         # 14 pytest unit tests
├── .github/workflows/
│   └── ci.yml                 # GitHub Actions pipeline
├── azure-pipelines.yml        # Azure DevOps pipeline (work in progress)
└── requirements.txt
```

## How to Run Locally
```bash
git clone https://github.com/yourusername/cicd-pipeline-project.git
cd cicd-pipeline-project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest tests/ --cov=core --cov-report=term-missing -v
```

## CI/CD Workflow
1. Push to `dev` branch triggers both pipelines
2. Tests run across Python 3.11 and 3.12 in parallel
3. Coverage report generated and published
4. Pull request to `main` re-runs all checks as required status checks
5. Merge only allowed after checks pass

## Setup Notes

### GitHub Actions Node.js Deprecation
GitHub Actions runners are migrating from Node.js 20 to Node.js 24.
Initial workflow using `actions/upload-artifact@v5` still triggered
deprecation warnings despite being a "recent" version, because v5 only
had preliminary Node 24 support and still defaulted to Node 20 internally.
Resolved by upgrading to `actions/upload-artifact@v6`, which explicitly
declares Node 24 as its runtime.

### Azure DevOps: From Hosted Agents to a Self-Hosted Mac Agent
Azure DevOps organizations created on personal/free-tier Microsoft accounts
require a manual parallelism grant request before hosted agents become
available, even for projects within documented free tier limits. Public
projects receive this automatically, but Microsoft has restricted public
project creation on certain personal accounts, requiring private project
parallelism requests instead (typical turnaround: 2-3 business days).

Rather than wait on approval, the pipeline was reconfigured to run on a
**self-hosted agent** installed locally instead of Microsoft's hosted pool.
This involved resolving several platform-specific issues along the way:

- **macOS Gatekeeper** blocked the unsigned agent binary
  (`Agent.Listener`) from running; resolved by clearing the quarantine
  attribute (`xattr -dr com.apple.quarantine`) on the agent directory.
- **Background service registration** via `svc.sh install` reported as
  configured but didn't reliably stay running; resolved by running the
  agent in foreground mode (`./run.sh`) instead, sufficient for a
  portfolio/demo use case that doesn't require 24/7 uptime.
- **Pipeline pool reference syntax**: `vmImage` is reserved for
  Microsoft-hosted images and silently fails to resolve a self-hosted
  pool name. Fixed by using `pool: name:` instead of `pool: vmImage:`.
- **`UsePythonVersion@0`** attempted to download a fresh Python build
  from GitHub on every run rather than using Python already installed
  locally, causing multi-minute hangs and anonymous GitHub rate-limit
  warnings. Resolved by referencing local Homebrew Python interpreters
  directly in the pipeline script steps instead of relying on the
  hosted-agent-oriented version-management task.
- **Disk space warnings** during pipeline runs initially looked like a
  false positive from a synthetic volume, but `df -h` across all mounted
  volumes confirmed the real data volume was genuinely at 96% capacity.
  Resolved by clearing unused disk image mounts, Homebrew cache, and
  Xcode derived data, freeing roughly 20GB.
- **`PublishCodeCoverageResults@2`** produced a cosmetic localization
  warning (`Can't find loc string for key: InstallDotNetCoreForPublishing`)
  while attempting to provision .NET on the self-hosted agent. Resolved
  by pre-installing .NET (`brew install dotnet`) so the task could detect
  it rather than attempting its own installation.
- **Private project badge visibility**: Azure DevOps blocks anonymous
  access to pipeline status badges on private projects by default, so the
  badge would not render for external viewers on a public GitHub README.
  Resolved by enabling anonymous badge access under
  Project Settings → Pipelines → Settings.

Both pipelines now run successfully with zero warnings across Python 3.11
and 3.12.

## What I Learned
- Writing meaningful unit tests beyond "does it run" — testing boundary conditions, type validation, and business logic (anomaly thresholds)
- Configuring matrix builds to test multiple Python versions in parallel
- Differences between GitHub Actions and Azure DevOps YAML syntax for equivalent pipeline stages
- Branch-based workflow with PR gates as a deployment safety mechanism
- Code coverage reporting and using it to identify untested code paths
- Diagnosing platform-specific infrastructure constraints (Node.js runtime versioning, Azure DevOps free-tier agent provisioning) rather than just writing pipeline YAML
- Standing up and troubleshooting a self-hosted Azure DevOps agent on macOS, including Gatekeeper security restrictions, launchd service quirks, and pool/runtime configuration differences from hosted agents
- Diagnosing real disk space constraints across macOS's layered APFS volume structure rather than assuming a misleading warning was a false positive
- Making a pragmatic infrastructure decision under an external approval bottleneck (self-hosted agent vs. waiting) rather than blocking progress