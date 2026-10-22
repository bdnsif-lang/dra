# Vendored files for the official forms

Embedded into `Paie_Slovaquie_2026.html` by `tools/embed_forms.py`, so the page fills the official PDFs offline.

| File | What | License |
|---|---|---|
| `pdf-lib-1.17.1.min.js` | pdf-lib 1.17.1 (npm `pdf-lib`, `dist/pdf-lib.min.js`) | MIT (`pdf-lib.LICENSE.md`) |
| `fontkit-1.1.1.umd.min.js` | @pdf-lib/fontkit 1.1.1 (`dist/fontkit.umd.min.js`), lets pdf-lib embed a TrueType font | MIT |
| `LiberationSans-subset.ttf` | Liberation Sans Regular, subset to Latin, Latin-1 and Latin Extended-A (all Slovak letters) with `pyftsubset` | SIL Open Font License 1.1 |
