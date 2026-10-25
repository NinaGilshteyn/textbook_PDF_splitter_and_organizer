"""Split a verified bookmarked textbook, prepare per-chapter video prompts and index.
Inspect the resulting manifest/opening-page text before uploading externally.
"""
from pathlib import Path
import argparse,base64,hashlib,html,json,re
from urllib.parse import quote
import pymupdf as fitz

def main():
 p=argparse.ArgumentParser()
 for name in ('source','output','book','edition','authors','year'):p.add_argument('--'+name,required=True)
 p.add_argument('--notebook',required=True);p.add_argument('--research-lens',default='Relate supported chapter concepts to cell identity, gene regulation and experimental reasoning; do not invent external paper findings.')
 p.add_argument('--prompt-template',type=Path,default=Path(__file__).resolve().parents[1]/'assets/video_prompt.txt')
 a=p.parse_args();source=Path(a.source).resolve();out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=True)
 if (out/'manifest.json').exists():raise SystemExit('Existing manifest: inspect/resume it instead of overwriting the batch.')
 original_hash=hashlib.sha256(source.read_bytes()).hexdigest();d=fitz.open(source);toc=d.get_toc();top=[x for x in toc if x[0]==1];chapters=[]
 for level,title,page in top:
  match=re.match(r'^(\d+)\s+(.+)',title)
  if not match:continue
  stop=next((x[2]-1 for x in top if x[2]>page),len(d))
  chapters.append({'number':int(match[1]),'title':match[2].strip(),'start':page-1,'stop':stop})
 if not chapters or [x['number'] for x in chapters]!=list(range(1,len(chapters)+1)):raise SystemExit('Chapter bookmarks are absent/nonconsecutive: review boundaries manually.')
 template=a.prompt_template.read_text(encoding='utf-8');cards=[]
 for c in chapters:
  title=c['title'];stem=f'Chapter {c["number"]:02} - '+re.sub(r'[<>:"/\\|?*]',' - ',title);stem=re.sub(r'\s+',' ',stem).strip(' .')[:100].rstrip(' .');folder=out/f'Chapter {c["number"]:02}';folder.mkdir(exist_ok=True);pdf=folder/(stem+'.pdf')
  part=fitz.open();part.insert_pdf(d,from_page=c['start'],to_page=c['stop']-1)
  subset=[[level-1,t,page-c['start']] for level,t,page in toc if level>=2 and c['start']<page<=c['stop']]
  if subset:
   base=subset[0][0]-1;subset=[[max(1,l-base),t,n] for l,t,n in subset];part.set_toc(subset)
  part.set_metadata({'title':f'Chapter {c["number"]}: {title}','author':a.authors,'subject':f'{a.book}, {a.edition} ({a.year}); unmodified source-page chapter extract'})
  part.save(pdf,garbage=3,deflate=True);part.close();check=fitz.open(pdf)
  assert len(check)==c['stop']-c['start']
  for j in (0,len(check)-1):
   assert check[j].get_pixmap(matrix=fitz.Matrix(.5,.5)).samples==d[c['start']+j].get_pixmap(matrix=fitz.Matrix(.5,.5)).samples
  prompt=template.format(number=c['number'],title=title,filename=pdf.name,book=a.book,edition=a.edition,authors=a.authors,year=a.year,research_lens=a.research_lens)
  if len(prompt)>5000:raise SystemExit(f'Chapter {c["number"]} prompt exceeds 5000 characters; adapt before uploading.')
  promptfile=folder/f'Chapter {c["number"]:02} - Video Prompt.txt';promptfile.write_text(prompt,encoding='utf-8')
  c.update(pdf=str(pdf.relative_to(out)),filename=pdf.name,prompt_file=str(promptfile.relative_to(out)),prompt=prompt,opening_text=check[0].get_text(),pages=len(check),status='not-submitted',format='Explainer',style='Kawaii')
  check.close();cards.append(f'<li><h2>Chapter {c["number"]:02} — {html.escape(title)}</h2><p>{c["pages"]} source pages</p><a href="{quote(c["pdf"].replace(chr(92),"/"))}">Chapter PDF</a> · <a href="{quote(c["prompt_file"].replace(chr(92),"/"))}">Video prompt</a></li>')
 assert hashlib.sha256(source.read_bytes()).hexdigest()==original_hash
 manifest={'source':str(source),'source_sha256':original_hash,'book':a.book,'edition':a.edition,'authors':a.authors,'year':a.year,'notebook':a.notebook,'chapters':chapters,'verification':'First/last rendered pages match source; chapter boundaries require source-opening review before upload.'}
 (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 index='<!doctype html><html><head><meta charset="utf-8"><title>'+html.escape(a.book)+' — Chapter videos</title><style>body{max-width:1000px;margin:40px auto;padding:0 24px;font:16px/1.6 system-ui;background:#faf5ff;color:#292139}li{background:white;padding:18px;margin:15px 0;border:1px solid #d9ccec;border-radius:12px;list-style:none}ul{padding:0}h2{font-size:19px}a{color:#604090}</style></head><body><h1>'+html.escape(a.book)+' — Chapter videos</h1><p>'+html.escape(a.edition)+' · '+html.escape(a.year)+' · <a href="'+html.escape(a.notebook,quote=True)+'">Open Gemini notebook</a></p><p>One chapter per source. Video settings: Explainer, English, Kawaii. Prompts are prepared; generation status is recorded in manifest.json.</p><ul>'+''.join(cards)+'</ul></body></html>'
 (out/'Start Here.html').write_text(index,encoding='utf-8');print(f'Prepared {len(chapters)} chapters; original unchanged. Manifest: {out/"manifest.json"}')
if __name__=='__main__':main()
