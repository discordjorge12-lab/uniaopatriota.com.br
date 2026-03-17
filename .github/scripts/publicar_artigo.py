import json
import shutil
from datetime import date
from pathlib import Path
import re

START_DATE = date(2026, 3, 17)

today = date.today()
day_index = (today - START_DATE).days

print(f"Hoje: {today} | Dia #{day_index}")

schedule_path = Path("artigos/agendados/schedule.json")
if not schedule_path.exists():
    print("schedule.json nao encontrado. Nada a fazer.")
    exit(0)

with open(schedule_path) as f:
    schedule = json.load(f)

artigo_slug = None
for slug, idx in schedule.items():
    if idx == day_index:
        artigo_slug = slug
        break

if artigo_slug is None:
    print(f"Nenhum artigo agendado para o dia {day_index}. Nada a fazer.")
    exit(0)

src = Path(f"artigos/agendados/{artigo_slug}.html")
dst = Path(f"artigos/{artigo_slug}.html")

if not src.exists():
    print(f"Arquivo fonte nao encontrado: {src}")
    exit(1)

if not dst.exists():
    shutil.copy2(src, dst)
    print(f"Artigo publicado: {artigo_slug}.html")
else:
    print(f"Artigo ja publicado: {artigo_slug}")

index_path = Path("index.html")
with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

if artigo_slug in content:
    print("Card ja existe no index.html.")
    exit(0)

with open(dst, "r", encoding="utf-8") as f:
    artigo_html = f.read()

titulo_match = re.search(r'<h1 class="article-title">(.*?)</h1>', artigo_html)
cat_match = re.search(r'<span class="article-cat">(.*?)</span>', artigo_html)
img_match = re.search(r'<img src="(https://picsum[^"]+)" alt', artigo_html)
lead_match = re.search(r'<p class="article-lead">(.*?)</p>', artigo_html)

titulo = titulo_match.group(1) if titulo_match else artigo_slug
categoria = cat_match.group(1) if cat_match else "Produtividade"
img_url = img_match.group(1) if img_match else "https://picsum.photos/id/1/600/400"
lead = lead_match.group(1) if lead_match else ""
lead_short = lead[:150] + "..." if len(lead) > 150 else lead

# Novo artigo entra como featured
novo_featured = f"""      <article class="card featured">
        <div class="card-thumb"><img src="{img_url}" alt="{titulo}" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
        <div class="card-body">
          <span class="card-cat">{categoria}</span>
          <h2><a href="artigos/{artigo_slug}.html">{titulo}</a></h2>
          <p>{lead_short}</p>
          <a href="artigos/{artigo_slug}.html" class="card-link">Ler artigo →</a>
        </div>
      </article>"""

# Artigo featured atual vira card normal
content = re.sub(
    r'<article class="card featured">',
    '<article class="card">',
    content,
    count=1
)

# Insere novo featured no topo da grade
marker = '<div class="articles-grid">'
if marker in content:
    content = content.replace(marker, marker + "\n\n" + novo_featured + "\n", 1)
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"index.html atualizado: {titulo} entrou como destaque")
else:
    print("Marcador articles-grid nao encontrado.")
