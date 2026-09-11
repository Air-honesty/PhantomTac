# PhantomTac project website

The website entry point is `index.html`. It follows the original single-page layout, with inline CSS and the original
Tailwind CDN dependency. No package installation or build step is required.
Author information appears below the title; the Citation section follows
the source-code section.

## Preview locally

From the repository root:

```sh
python3 -m http.server 8000
```

Open `http://localhost:8000/`. The page also supports hosting beneath the
`/PhantomTac/` path. All resource downloads use relative URLs.

## Publish with GitHub Pages

The project is intended to be available at `https://phantomtac.org/` once the
GitHub Pages custom-domain configuration and DNS records are active.

The repository is published through GitHub Actions. The workflow in
`.github/workflows/deploy-pages.yml` deploys the repository contents after
each push to `main`.

## Content and assets

- `src/` contains the four source files linked by the website.
- `figures/` contains the three images displayed by the website.
- `assets/media/` contains H.264/AAC MP4 videos for browser playback, with
  the MP4 index at the beginning of each file for streaming.
- `assets/downloads/` contains the BibTeX citation.
- The original navigation, section order, figure layout, six-video grid,
  FAQ disclosures, and individual resource cards are retained.
- A small inline script adds citation copying; the `.bib` download remains
  available independently of clipboard access.

Author names, affiliations, contact addresses, the abstract, conference metadata,
DOI, and the citation are based on the camera-ready title-page image supplied
by the authors. `assets/downloads/phantomtac.bib` provides a downloadable citation.
A full paper PDF has not been provided, so no PDF download is advertised.
If the domain changes, update the canonical URL and Open Graph URL/image in
`index.html`.
