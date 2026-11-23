// Print a live web page to PDF with the pre-installed Chromium
const { chromium } = require('playwright');
(async () => {
  const [url, out] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage();
  try { await p.goto(url, { waitUntil: 'networkidle', timeout: 90000 }); } catch (e) { console.log('goto warn:', e.message.split('\n')[0]); }
  await p.waitForTimeout(2000);
  console.log('title:', await p.title());
  await p.pdf({ path: out, format: 'A4', printBackground: true, margin: { top: '12mm', bottom: '12mm', left: '10mm', right: '10mm' } });
  await b.close();
})();
