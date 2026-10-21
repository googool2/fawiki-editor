// Render an HTML file to PNG/JPEG with headless Chromium (Playwright).
// usage: node render.js page.html out.(png|jpg) width height [scale] [transparent]
const { chromium } = require('playwright');
(async () => {
  const [html, out, w, h, scale = '1', transparent = ''] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: +scale });
  await page.goto('file://' + require('path').resolve(html));
  await page.evaluate(() => document.fonts.ready);
  const type = out.endsWith('.jpg') ? 'jpeg' : 'png';
  await page.screenshot({ path: out, type, quality: type === 'jpeg' ? 86 : undefined,
                          omitBackground: transparent === 'transparent' });
  await browser.close();
})();
