"""Embed the official blank forms, the font and pdf-lib into Paie_Slovaquie_2026.html (between the FORMS markers),
so the page can fill the forms with the payroll data offline.
The forms' own input fields are removed: the page draws the values at the fields' places.
Run after changing a form or a vendored file:  python3 tools/embed_forms.py   (needs pypdf)"""
import base64, io, pathlib, re
from pypdf import PdfReader, PdfWriter

root = pathlib.Path(__file__).resolve().parent.parent
src, vendor = root / 'paie' / 'formulaires_officiels', root / 'tools' / 'vendor'
FORMS = {                                    # key used by the page: file in paie/formulaires_officiels
    'PREHLAD': 'PREHLADv26.pdf',
    'HLASENIE': 'HLASENIEv23.pdf',
    'HLASENIE_IV': 'HLASENIEv23_cast_IV.pdf',
    'HLASENIE_V': 'HLASENIEv23_cast_V.pdf',
    'POT': 'POT395v26.pdf',
    'RZ': 'Rocne_zuctovanie_2025.pdf',
    'VYH': 'VYH36v25_1_Vyhlasenie_NCZD_bonus.pdf',
    'ZIA': 'ZIA38v25_Ziadost_rocne_zuctovanie.pdf',
}

def blank(path):
    r, w = PdfReader(path), PdfWriter()
    for p in r.pages:
        if '/Annots' in p: del p['/Annots']
        w.add_page(p)
    for p in w.pages: p.compress_content_streams()
    w.compress_identical_objects(remove_duplicates=True, remove_unreferenced=True)
    out = io.BytesIO(); w.write(out); return out.getvalue()

def plain(id_, data): return f'<script type="text/plain" id="{id_}">{base64.b64encode(data).decode()}</script>'

parts, total = [], 0
for key, name in FORMS.items():
    data = blank(src / name); total += len(data)
    parts.append(plain('of-' + key, data))
parts.append(plain('of-font', (vendor / 'LiberationSans-subset.ttf').read_bytes()))
for js in ('pdf-lib-1.17.1.min.js', 'fontkit-1.1.1.umd.min.js'):
    parts.append('<script>' + (vendor / js).read_text(encoding='utf-8').replace('</script', '<\\/script') + '</script>')

app = root / 'Paie_Slovaquie_2026.html'
s = app.read_text(encoding='utf-8')
s, n = re.subn(r'<!--FORMS-->.*?<!--/FORMS-->', lambda m: '<!--FORMS-->' + '\n'.join(parts) + '<!--/FORMS-->', s, flags=re.S)
if n != 1: raise SystemExit('FORMS markers not found')
app.write_text(s, encoding='utf-8')
print('embedded', len(FORMS), 'forms,', total, 'bytes of PDF')
