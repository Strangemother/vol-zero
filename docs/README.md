# VOL Zero GitHub Pages

This folder contains the static GitHub Pages site for VOL Zero.

The page is intentionally plain HTML and CSS. It does not deploy through a
GitHub Actions workflow. Publish it manually when you want the public site to
change.

## GitHub Pages setup

In the repository settings, configure GitHub Pages to deploy from:

- Source: `Deploy from a branch`
- Branch: `gh-pages`
- Folder: `/ (root)`

## Publish

From the repository root, publish this folder to the `gh-pages` branch:

```sh
git subtree push --prefix github-pages origin gh-pages
```

That command is the only deploy step. Changes in this folder will not update
the public page until you run it.

## Local preview

Open `index.html` in a browser, or serve the folder with any static file server.
