"""Copy Fiche_Employe.html into Paie_Slovaquie_2026.html (base64 block between the FICHE markers).
Run after any change to the form:  python3 tools/embed_fiche.py"""
import base64, pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
form = (root / 'Fiche_Employe.html').read_bytes()
app = root / 'Paie_Slovaquie_2026.html'
s = app.read_text(encoding='utf-8')
block = '<script type="text/plain" id="ficheTpl">' + base64.b64encode(form).decode() + '</script>'
s, n = re.subn(r'<!--FICHE-->.*?<!--/FICHE-->', lambda m: '<!--FICHE-->' + block + '<!--/FICHE-->', s, flags=re.S)
if n != 1: raise SystemExit('FICHE markers not found')
app.write_text(s, encoding='utf-8')
print('embedded', len(form), 'bytes')
