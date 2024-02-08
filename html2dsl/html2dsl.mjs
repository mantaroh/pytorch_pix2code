/**
 * Usage:
 *   node html2dsl.js <html-file>
 */
import fs from 'fs';
import path from 'path';
import parse from 'html-dom-parser';
import puppeteer from 'puppeteer';
import crypto from 'crypto';


const html2dsl = async (html) => {
    const browser = await puppeteer.launch({
        headless: 'new',
    });

    try {
        // Load content to puppeteer (chromium)
        const page = await browser.newPage();
        await page.setViewport({width: 1920, height: 1081});
        await page.setContent(html);

        // generate hash file name from input html string
        const hashFileName = crypto.createHash('md5').update(html).digest('hex');

        // Inject Getting component script
        await page.addScriptTag({path: 'generate-dsl-injecter.js'});
        await page.screenshot({ path: `screen/${hashFileName}.png` });
        const dsl = await page.evaluate(() => {
            const dsl = generateDSL();
            return dsl;
        });
        console.log(dsl);

        await page.close();

    } catch (error) {
        console.error(error.message);
        process.exit(1);
    } finally {
        await browser.close();
    }
};

const main = async () => {
    const htmlFile = process.argv[2];
    if (!htmlFile) {
        console.error('Usage: node html2dsl.js <html-file>');
        process.exit(1);
    }
    
    const htmlData = fs.readFileSync(htmlFile, 'utf8');
    const html = htmlData.toString();
    console.log(html);
    const dsl = await html2dsl(html);
    // console.log(dsl);
};

main();