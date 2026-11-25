"""Offline UI fixture tests. Resolves actual local HTML/CSS/JS paths, inlines source
for browser rendering without navigation. Does not replace real HTTP smoke testing."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import re, json, shutil, os
root=Path.cwd()
paths=[root/'index.html']+[root/f'sites/variant-{i}/index.html' for i in range(1,5)]+[root/'dist/production/index.html',root/'dist/review/index.html']+[root/f'dist/portfolio/sites/commission-calculator/variant-{i}/index.html' for i in range(1,5)]

def fixture(path):
 html=path.read_text(); seen=set(); scripts=[]
 def bundle(p):
  p=p.resolve()
  if p in seen:return
  seen.add(p);s=p.read_text()
  for m in re.finditer(r"^import\s+.*?\s+from\s+['\"]([^'\"]+)['\"];?",s,re.M):bundle(p.parent/m.group(1))
  s=re.sub(r"^import\s+.*?\s+from\s+['\"][^'\"]+['\"];?\s*",'',s,flags=re.M)
  s=re.sub(r'\bexport\s+(?=(?:const|function|class|let)\b)','',s)
  scripts.append(s)
 def style(m):return '<style>'+(path.parent/m.group(1)).read_text()+'</style>'
 html=re.sub(r'<link rel="stylesheet" href="([^"]+)">',style,html)
 # Verify the favicon exists, then remove URL reference in fixture.
 for ref in re.findall(r'<link rel="icon" href="([^"]+)"',html):assert (path.parent/ref).is_file()
 html=re.sub(r'<link rel="icon"[^>]+>','',html)
 for src in re.findall(r'<script type="module" src="([^"]+)"',html):bundle(path.parent/src)
 # Avoid declaration collisions across ES module scopes by removing duplicate local declarations.
 # Only reporting imports calculate/compare/config and exports functions; no conflicting locals.
 return re.sub(r'<script type="module" src="[^"]+"></script>','<script>'+lambda_placeholder+'</script>',html).replace(lambda_placeholder,'\n'.join(scripts))
lambda_placeholder='__FIXTURE_SCRIPT__'
records=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=os.getenv('CHROMIUM_PATH') or shutil.which('chromium'),args=['--no-sandbox'])
 for path in paths:
  route=str(path.relative_to(root));page=browser.new_page(viewport={'width':1440,'height':1000},accept_downloads=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(fixture(path));page.wait_for_selector('body[data-calculated=true]',timeout=5000)
  assert page.locator('#monthly').inner_text()=='$15,000',route
  assert page.locator('#three').inner_text()=='$540,000',route
  source=route.startswith('sites/variant-')
  if source:
   name=path.parent.name;page.screenshot(path=str(root/'previews'/f'{name}-desktop.png'))
  page.locator('#deals').fill('20');assert page.locator('#monthly').inner_text()=='$30,000',route
  page.locator('#scenario').select_option('conservative');assert page.locator('#monthly').inner_text()=='$18,000',route
  page.locator('#deals').fill('0');assert page.locator('#monthly').inner_text()=='$0',route
  page.locator('#deals').fill('-1');assert page.locator('#errors').inner_text() and page.locator('#csv').is_disabled(),route
  page.locator('#reset').click();assert page.locator('#monthly').inner_text()=='$15,000',route
  page.locator('[data-allocation=business]').fill('50');assert '100%' in page.locator('#errors').inner_text(),route
  page.locator('#equal').click();assert page.locator('#monthly').inner_text()=='$15,000',route
  with page.expect_download() as dl:page.locator('#csv').click()
  assert '"36 months","540000"' in Path(dl.value.path()).read_text(),route
  with page.expect_download() as dl:page.locator('#download').click()
  assert json.loads(Path(dl.value.path()).read_text())['results']['threeYear']==540000,route
  for width in (390,320):
   page.set_viewport_size({'width':width,'height':844});page.evaluate('window.scrollTo(0,0)');page.wait_for_timeout(100)
   actual=page.evaluate('document.documentElement.scrollWidth');assert actual<=width+1,(route,width,actual)
   if source and width==390:page.screenshot(path=str(root/'previews'/f'{name}-mobile.png'))
  assert not errors,(route,errors);records.append({'file':route,'baseline':'pass','interactions':'pass','exports':'pass','320px_390px_no_overflow':'pass','local_imports':'pass','page_errors':errors});print('PASS',route,flush=True);page.close()
 browser.close()
(root/'docs/browser-qa.json').write_text(json.dumps({'mode':'offline local HTML/CSS/JS fixture; actual HTTP navigation blocked by administrator','results':records},indent=2)+'\n')
