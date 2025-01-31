# Markdown Cheatsheet

There are basic markdown features recommended for use in Pulp.

### Internal links

Adding absolute links is enabled by `mkdocs-site-urls`
(learn more [here](https://github.com/octoprint/mkdocs-site-urls)).
This is preferred over *relative* links because of our complex structure. See tradeoffs [here](https://github.com/pulp/pulp-docs/issues/2)

```markdown
# Template
[My Link](site:{repo-name}/docs/{persona}/{content-type}/some-page.md).

# Example
[My Link](site:pulp-docs/docs/dev/reference/markdown-cheatsheet.md).

# Rendered
[My Link](http://127.0.0.1:8000/pulp-docs/docs/dev/reference/markdown-cheatsheet/).
```

### Tabbed content

Having tabs for alternative content is enabled by mkdocs-material
(learn more [here](https://squidfunk.github.io/mkdocs-material/reference/content-tabs/#usage)).
It looks like this:

!!! example

    === "Run"

        ```bash
        cat myfile.txt
        ```

    === "Output"

        ```bash
        line1
        line2
        line3
        ```

The basic syntax is:

- Each tab title must be in quotes
- Each tab block must have 4 spaces of indent
- Put space around `=== "Title"`

```` title="sample-tabbed-content.md"
=== "Run"

    ```bash
    cat myfile.txt
    ```

=== "Output"

    ```bash
    line1
    line2
    line3
    ```
````


### Ordering Files

Ordering is enabled by `mkdocs-literate-nav`
(learn more [here](https://oprypin.github.io/mkdocs-literate-nav/reference.html)).

The basic setup is having a file in `{repo}/docs/{persona}/{doc_type}/_SUMMARY.md`.
In this file you should use the following syntax:

```markdown title="pulp_plugin/docs/user/guides/_SUMMARY.md"
# Basic
* [First list item](z-page.md)
* [Second list item](m-page.md)
* [Third list item](a-page.md)

# Subdirs
* [First list item](some-page.md)
* Subsection title
    * [Foo](subdirectory/foo.md)
    * [Bar](subdirectory/bar.md)

# Recursive Globs
* [I want this first](some-page.md)
* *.md
* [This last and recurse this dir](other/)
```

### Codeblocks

Mkdocs-material comes with builtin support for syntax highlighting in codeblocks.
You may use `python`, `bash`, `yaml`, `json`, `yaml` and most popular programming languages.

!!! example

    ```python
    serializer = mymodelserializer(data=data)
    serializer.is_valid(raise_exception=true)
    instance = serializer.create(serializer.validated_data)
    print(instance)
    ```

Markdown syntax:

````
```python
serializer = mymodelserializer(data=data)
serializer.is_valid(raise_exception=true)
instance = serializer.create(serializer.validated_data)
print(instance)
```
````

The codeblock can also have a title, which is useful if its a file:

!!! example

    ```bash title="sample-title-here.sh"
    pulp file repository update --name myrepo --retained-versions 1
    ```

Markdown syntax:

````
```bash title="sample-title-here.sh"
pulp file repository update --name myrepo --retained-versions 1
```
````

### Images

The image paths can be relative or absolute:

Simple:

```markdown
# Relative path. Image is in the same folder
![OperatorHub tab](1.png "Pulp on OperatorHub tab")

# Absolute path. Specify the path with 'site:'
![Pulp 101](site:pulpcore/docs/assets/images/pulp-101.png)
```

With subtitle:

```markdown
# Subtitle on top
<figure markdown="span">
  <figcaption>Find Pulp  at `OperatorHub > Integration & Delivery`.</figcaption>
  ![OperatorHub tab](1.png "Pulp on OperatorHub tab")
</figure>

# Subtitle at bottom
<figure markdown="span">
  <figcaption>Find Pulp  at `OperatorHub > Integration & Delivery`.</figcaption>
  ![OperatorHub tab](1.png "Pulp on OperatorHub tab")
</figure>
```

### Admonitions

[See mkdocs-material](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#supported-types)

Use them wisely.

