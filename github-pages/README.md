# VOL Zero GitHub Pages

This folder contains the static GitHub Pages site for VOL Zero.

The page is intentionally plain HTML and CSS. It does not use a repository
GitHub Actions workflow.

## GitHub Pages setup

In the repository settings, configure GitHub Pages to deploy from:

- Source: `Deploy from a branch`
- Branch: `gh-pages`
- Folder: `/ (root)`

## Publish

Render the Flask documentation site as static files:

```sh
tool site run
tool site export
```

The compatibility command `python convert.py` delegates to the same exporter.

Publish the generated files to the `gh-pages` branch when you want the public
page to update:

```sh
tool site deploy
```

The public site is served at <https://strangemother.github.io/vol-zero/>.

## Local preview

Open `index.html` in a browser, or serve the folder with any static file server.
