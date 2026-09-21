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

Commit changes to this folder on `main`, then publish them to the `gh-pages`
branch when you want the public page to update:

```sh
git subtree push --prefix github-pages origin gh-pages
```

The public site is served at <https://strangemother.github.io/vol-zero/>.

## Local preview

Open `index.html` in a browser, or serve the folder with any static file server.
