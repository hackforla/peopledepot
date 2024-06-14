# Github actions

These are the github actions used in the project.

## Files

```bash
.github/workflows/
└── deploy-docs.yml # (1)!
```

1. Deploy Documentation
    - triggered by commits to `main`
    - builds and deploys the mkdocs documentation to github pages.

## Actions page workflows

1. deploy-docs
    - see deploy-docs.yml above
1. pages-build-deployment
    - The github-pages bot runs this automatically for any project that publishes to github pages.
    - It does extra work that we don't need, but there's no way to disable it. See [here](https://stackoverflow.com/questions/72079903/do-i-need-the-pages-build-deployment-github-action-when-i-have-another-action-f).
