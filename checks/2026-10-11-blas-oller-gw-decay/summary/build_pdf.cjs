// Render the reader's summary to PDF with the pre-installed Chromium.
// Run from the repository root:
//   node checks/2026-10-11-blas-oller-gw-decay/summary/build_pdf.cjs
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const dir = __dirname;
  const html = path.join(dir, 'blas-oller-check-summary.html');
  const pdf = path.join(dir, 'blas-oller-check-summary.pdf');
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + html, { waitUntil: 'load' });
  await page.pdf({
    path: pdf,
    format: 'Letter',
    printBackground: true,
    margin: { top: '0.75in', bottom: '0.8in', left: '0.85in', right: '0.85in' },
    displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate:
      '<div style="width:100%;font-family:Inter,sans-serif;font-size:7.5px;color:#7a7975;padding:0 0.85in;display:flex;justify-content:space-between">' +
      '<span>Independent check of Blas &amp; Oller, arXiv:2607.24930</span>' +
      '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
  });
  await browser.close();
  console.log('wrote', pdf);
})();
