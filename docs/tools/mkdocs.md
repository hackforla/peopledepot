# MkDocs

We are using MkDocs to generate our documentation. See [Docker-mkdocs repo](https://hackforla.github.io/docker-mkdocs/) for information about MkDocs and the image we're using.

#### Work on docs locally

!!! note "The first time starting the container may take longer due to downloading the ~40MB docker image"

1. Run the mkdocs container.

    ```bash
    docker-compose up mkdocs # (1)!
    ```

    1. Optionally use the `-d` flag to run the container in the background

1. Open a browser to [`http://localhost:8005/`](https://localhost:8005/) to view the documentation locally.

1. Modify the files in the `docs` directory. The site will auto-update when the files are saved.

1. ++ctrl+c++ to quit the local server and stop the container

#### Auto-generated docs

We have a [GitHub Action](https://github.com/hackforla/peopledepot/blob/main/.github/workflows/deploy-docs.yml) set up to generate and host the documentation on a [GitHub Pages site](https://hackforla.github.io/peopledepot/)
