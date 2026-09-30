// Renders the interface diagram HTML to PNG with the pre-installed Chromium.
// Usage: NODE_PATH=$(npm root -g) node render.js <in.html> <out.png>
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const [inFile, outFile] = process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium/chrome-linux/chrome' }).catch(async () => chromium.launch());
  const page = await browser.newPage({ viewport: { width: 2620, height: 2010 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(inFile), { waitUntil: 'load' });
  await page.waitForTimeout(300);
  await page.screenshot({ path: outFile, fullPage: true });
  await browser.close();
  console.log('wrote', outFile);
})();
