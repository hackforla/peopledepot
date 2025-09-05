---
name: Security Check (supply-chain)
about: Check that the project's dependencies are secure.
title: Security check (supply-chain)
labels: 'complexity: small, feature: security, role: dev, s: PD team, size: 1pt'
assignees: ''

---

### Description

This issue is for performing a supply-chain security check on our project. The goal is to ensure that our dependencies, Docker images, and system packages are up-to-date and free from known vulnerabilities.

### Tasks

1. **Update Python dependency versions**
	- [ ] Update `requirements.in` to use the latest versions of Python dependencies.
	- [ ] Verify that all dependencies are updated correctly.
2. **Update pre-commit hook versions**
	- [ ] Update the pre-commit hook versions to the latest available.
	- [ ] Verify that the pre-commit hooks are working correctly.
3. **Update Black version**
	- [ ] Update the Black version manually in `blacken-docs`.
	- [ ] Verify that Black is working correctly.
4. **Update additional dependencies**
	- [ ] Update any additional dependencies manually.
	- [ ] Verify that all additional dependencies are updated correctly.
5. **Check Docker image for vulnerabilities**
	- [ ] Use a tool like `docker scan` or `trivy` to scan the Docker image for vulnerabilities.
	- [ ] Identify any vulnerabilities found.
6. **Resolve vulnerabilities**
	- [ ] Resolve any vulnerabilities found in the Docker image.
	- [ ] Verify that the vulnerabilities are resolved correctly.
7. **Update Python version in base image**
	- [ ] Update the Python version in the base image to the latest available.
	- [ ] Verify that the Python version is updated correctly.
8. **Update system dependencies**
	- [ ] Update any system dependencies (e.g. `*.apk` packages).
	- [ ] Verify that all system dependencies are updated correctly.
9. **Update UV version**
	- [ ] Update the UV version to the latest available.
	- [ ] Verify that the UV version is updated correctly.

### Acceptance Criteria

- [ ] All tasks are completed successfully.
- [ ] No known vulnerabilities are found in the Docker image or system dependencies.
- [ ] All dependencies are updated to the latest versions.
