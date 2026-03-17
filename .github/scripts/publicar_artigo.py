import json
import os
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

if dst.exists():
    print(f"Artigo ja publicado: {artigo_slug}")
else:
    shutil.copy2(src, dst)
    print(f"Artigo publicado: {artigo_slug}.html")

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
lead_short = lead[:120] + "..." if len(lead) > 120 else lead

novo_card = f"""
      <article class="card">
        <div class="card-thumb"><img src="{img_url}" alt="{titulo}" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
        <div class="card-body">
          <span class="card-cat">{categoria}</span>
          <h2><a href="artigos/{artigo_slug}.html">{titulo}</a></h2>
          <p>{lead_short}</p>
          <a href="artigos/{artigo_slug}.html" class="card-link">Ler artigo →</a>
        </div>
      </article>"""

marker = '<article class="card featured">'
if marker in content:
    content = content.replace(marker, novo_card + "\n\n      " + marker, 1)
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"index.html atualizado com card: {titulo}")
else:
    print("Marcador nao encontrado.")
