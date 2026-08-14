---
tags:
  - scripts
  - GitHub Actions
---

# Pin GitHub Actions to specific SHAs

Source code: [scripts/pin-actions-to-shas.sh](https://github.com/hackforla/peopledepot/blob/main/docs/contributing/tools/scripts/pin-actions-to-shas.sh)

## What it does

This script will update all tag-referenced actions in the repository to their corresponding SHAs.

It will replace `uses: <owner>/<repo>@<tag>` with `uses: <owner>/<repo>@<sha>`.

This script is useful if you want to pin actions to specific SHAs in your repository.

## Requirements

- [GitHub CLI](https://cli.github.com/)
- [jq](https://jqlang.org/)

## Usage

Run it from the project root like this:

```bash
./scripts/pin-actions-to-shas.sh
```

Note: This script is idempotent. There's no harm in running it more than once. It will only update the actions that need to be updated.
