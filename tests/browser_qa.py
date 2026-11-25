"""Optional browser QA: Python playwright plus a Chromium executable. Run from repo root."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import subprocess, os, time, json, shutil
root=Path.cwd(); port=8765
server=subprocess.Popen(['node','scripts/serve.mjs'],env={**os.environ,'PORT':str(port)},stdout=subprocess.DEVNULL)
base=f'http://127.0.0.1:{port}'
paths=['/']+[f'/sites/variant-{i}/' for i in range(1,5)]+['/dist/production/','/dist/review/']+[f'/dist/portfolio/sites/commission-calculator/variant-{i}/' for i in range(1,5)]
records=[]
try:
 time.sleep(.5)
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path=os.getenv('CHROMIUM_PATH') or shutil.which('chromium'),args=['--no-sandbox'])
  for route in paths:
   page=browser.new_page(viewport={'width':1440,'height':1000},accept_downloads=True); errors=[]; bad=[]
   page.on('pageerror',lambda e:errors.append(str(e)));page.on('response',lambda r:bad.append(f'{r.status} {r.url}') if r.status>=400 else None)
   page.goto(base+route);page.wait_for_selector('body[data-calculated=true]');assert page.locator('#monthly').inner_text()=='$15,000',route
   assert page.locator('#three').inner_text()=='$540,000',route
   if route.startswith('/sites/variant-'):
    name=route.split('/')[2];page.screenshot(path=str(root/'previews'/f'{name}-desktop.png'))
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
    if width==390 and route.startswith('/sites/variant-'):page.screenshot(path=str(root/'previews'/f'{name}-mobile.png'))
   assert not errors,(route,errors);assert not bad,(route,bad);records.append({'route':route,'baseline':'pass','interactions':'pass','exports':'pass','320px_390px_no_overflow':'pass','page_errors':errors,'failed_responses':bad});print('PASS',route,flush=True);page.close()
  browser.close()
finally:
 server.terminate();server.wait()
(root/'docs/browser-qa.json').write_text(json.dumps(records,indent=2)+'\n')
