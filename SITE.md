# PhantomTac project website

The website entry point is `index.html`. It follows the original single-page layout, with inline CSS and the original
Tailwind CDN dependency. No package installation or build step is required.
Author information appears below the title; the Citation section follows
the original datasets section. The earlier `assets/site.css` and
`assets/site.js` redesign files are not loaded by this page.

## Preview locally

From the repository root:

```sh
python3 -m http.server 8000
```

Open `http://localhost:8000/`. The page also supports hosting beneath the
`/PhantomTac/` path. All resource downloads use relative URLs.

## Publish with GitHub Pages

The intended project URL is `https://air-honesty.github.io/PhantomTac/`.

A repository owner or maintainer must enable Pages in **Settings → Pages**:

1. Under **Build and deployment**, choose **Deploy from a branch**.
2. Select **main** and **/ (root)**, then save.
3. Wait for the Pages deployment to finish, then open the published URL.

The `.nojekyll` file allows the static assets to be served without Jekyll
processing. Subsequent pushes to `main` update the website automatically.

GitHub Free supports Pages for public repositories. Publishing from this
private personal repository requires an eligible plan such as GitHub Pro.
The repository visibility is not changed by the website files. See the
[GitHub Pages publishing documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

## Content and assets

- `src/`, `data/`, `figures/`, and `videos/` retain their original files.
- `assets/media/` contains additional H.264/AAC MP4 copies for web playback,
  with the MP4 index at the beginning of each file for streaming.
- `assets/posters/` contains still frames from the demonstration videos.
- `assets/downloads/` contains ZIP archives of the original datasets and
  source files. Regenerate these archives if the originals change later.
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
