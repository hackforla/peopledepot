# MkDocs

We are using MkDocs to generate our documentation. See [Docker-mkdocs repo](https://hackforla.github.io/docker-mkdocs/) for information about MkDocs and the image we're using.

## Work on docs locally

!!! note "The first time starting the container may take longer due to downloading the ~40MB docker image"

1. Run the mkdocs container.

    ```bash
    docker-compose up mkdocs # (1)!
    ```

    1. Optionally use the `-d` flag to run the container in the background

1. Open a browser to [`http://localhost:8005/`](https://localhost:8005/) to view the documentation locally.

1. Modify the files in the `docs` directory. The site will auto-update when the files are saved.

1. ++ctrl+c++ to quit the local server and stop the container

## Auto-generated docs

We have a [GitHub Action](https://github.com/hackforla/peopledepot/blob/main/.github/workflows/deploy-docs.yml) set up to generate and host the documentation on a [GitHub Pages site](https://hackforla.github.io/peopledepot/)

## MkDocs syntax

We're using Material for MkDocs. Aside from standard markdown syntax, there are some MkDocs and Material-specific syntax which can help more effective documentation. See the [Material reference docs](https://squidfunk.github.io/mkdocs-material/reference/) for the complete set of syntax.

Here's a list of commonly used MkDocs syntax for quick reference.

### [Code Blocks](https://squidfunk.github.io/mkdocs-material/reference/code-blocks/)

=== "Example"
    ```python title="Code Block"
    @admin.register(RecurringEvent)
    class RecurringEventAdmin(admin.ModelAdmin):
        list_display = (
            "name",
            "start_time",
            "duration_in_min",
        )
    ```

    ```python title="Numbered Lines" linenums="1"
    @admin.register(RecurringEvent)
    class RecurringEventAdmin(admin.ModelAdmin):
        list_display = (
            "name",
            "start_time",
            "duration_in_min",
        )
    ```

    ```python title="Highlighted Lines" hl_lines="1 3 5"
    @admin.register(RecurringEvent)
    class RecurringEventAdmin(admin.ModelAdmin):
        list_display = (
            "name",
            "start_time",
            "duration_in_min",
        )
    ```

=== "Code"
    ````
    ```python title="Code Block"
    @admin.register(RecurringEvent)
    class RecurringEventAdmin(admin.ModelAdmin):
        list_display = (
            "name",
            "start_time",
            "duration_in_min",
        )
    ```

    ```python title="Numbered Lines" linenums="1"
    @admin.register(RecurringEvent)
    class RecurringEventAdmin(admin.ModelAdmin):
        list_display = (
            "name",
            "start_time",
            "duration_in_min",
        )
    ```

    ```python title="Highlighted Lines" hl_lines="1 3 5"
    @admin.register(RecurringEvent)
    class RecurringEventAdmin(admin.ModelAdmin):
        list_display = (
            "name",
            "start_time",
            "duration_in_min",
        )
    ```
    ````

### [Code Annotations](https://squidfunk.github.io/mkdocs-material/reference/annotations/)

=== "Example"
    ```bash
    Click the plus sign --> # (1)!
    ```

    1. This is an explanation text

=== "Code"
    ````
    ``` bash
    Click the plus sign --> # (1)!
    ```

    1. This is an explanation text
    ````

### [Text blocks](https://facelessuser.github.io/pymdown-extensions/extensions/blocks/plugins/details/)

=== "Example"
    !!! example "Simple Block"

    !!! example
        Content Block Text

    ??? example "Expandable Block"
        Content

    ???+ example "Opened Expandable Block"
        Content

=== "Code"
    ```
    !!! example "Simple Block"

    !!! example
        Content Block Text

    ??? example "Expandable Block"
        Content

    ???+ example "Opened Expandable Block"
        Content
    ```

### [Tabbed content](https://facelessuser.github.io/pymdown-extensions/extensions/tabbed/)

=== "Example"
    === "Linux"
        linux-specific content

    === "Mac"
        mac-specific content

=== "Code"
    ```
    === "Linux"

        linux-specific content

    === "Mac"

        mac-specific content
    ```

### [Buttons](https://squidfunk.github.io/mkdocs-material/reference/buttons/)

=== "Example"
    1. ++ctrl+c++ to quit the local server and stop the container

=== "Code"
    ```
    1. ++ctrl+c++ to quit the local server and stop the container
    ```
