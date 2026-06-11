---
tags:
  - AWS
  - deployment
---

# AWS Deployment Resources

## Development Deployment

The development environment (`peopledepot-dev.vrms.io`) is automatically deployed whenever code is pushed to the `main` branch. It's used for testing features and validating infrastructure changes before production.

**Live Site:** [peopledepot-dev.vrms.io](https://peopledepot-dev.vrms.io/)

### AWS Resources

!!! note "Requires incubator account access from #ops"

| Resource                                                                                                                                                                  | Purpose                       |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| [Logs](https://us-west-2.console.aws.amazon.com/cloudwatch/home?region=us-west-2#logsV2:log-groups/log-group/$252Fecs$252Fpeople-depot-backend-dev)                       | Monitor app output and errors |
| [Database Credentials](https://us-west-2.console.aws.amazon.com/systems-manager/parameters/?region=us-west-2&tab=Table#list_parameter_filters=Name:Contains:people-depot) | View credentials              |
| [Deployment Status](https://github.com/hackforla/peopledepot/actions/workflows/deploy-dev.yml)                                                                            | Check latest deployment run   |

### How Deployment Works

1. Code is pushed to the `main` branch
1. GitHub Actions automatically triggers the [deploy-dev workflow](https://github.com/hackforla/peopledepot/blob/main/.github/workflows/deploy-dev.yml)
1. The workflow builds the Docker image using [Dockerfile-aws](https://github.com/hackforla/peopledepot/blob/main/app/Dockerfile-aws)
1. The updated image is pushed to the incubator account on AWS
1. Terraform starts the Docker container, which runs [entrypoint-aws.sh](https://github.com/hackforla/peopledepot/blob/main/app/entrypoint-aws.sh) to execute database migrations, then launches the app via gunicorn (WSGI server); static files are served by whitenoise

### Configuration & Infrastructure

**Docker & App Startup**

- [Dockerfile](https://github.com/hackforla/peopledepot/blob/main/app/Dockerfile-aws) — Defines the container image; multi-stage build using production dependencies and gunicorn
- [Entrypoint Script](https://github.com/hackforla/peopledepot/blob/main/app/entrypoint-aws.sh) — Runs database migrations then starts gunicorn; whitenoise serves static files
- [Production Settings](https://github.com/hackforla/peopledepot/blob/main/app/peopledepot/settings_aws.py) — Django settings for AWS; inherits base settings and strips dev-only apps

**Infrastructure as Code (Terraform)**

- [Terraform Project Directory](https://github.com/hackforla/incubator/tree/main/terraform/projects/people-depot) — All AWS resource definitions
- [Dev Environment Variables](https://github.com/hackforla/incubator/blob/main/terraform/projects/people-depot/environment-dev.tf) — Dev-specific config

### Troubleshooting & References

- [Deployment Issue #330](https://github.com/hackforla/peopledepot/issues/330#issuecomment-2645969180) — Historical context
