"""Verify rendered glyph fonts, not only CSS declarations, without firing known vendor pixels."""
import argparse
import json
import os
from playwright.sync_api import sync_playwright

parser = argparse.ArgumentParser()
parser.add_argument('--url', default=os.environ.get('SHARK_FONT_CHECK_URL'))
parser.add_argument('--font', default='Barlow')
parser.add_argument('--selector', action='append', required=True)
parser.add_argument('--chrome', default='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
args = parser.parse_args()
if not args.url:
    parser.error('Provide --url or SHARK_FONT_CHECK_URL; preview secrets need not appear in commands/output.')
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path=args.chrome)
    page = browser.new_page(viewport={'width':390, 'height':844})
    blocked = ['tracking.buygoods.com', 'buygoods.com/affiliates/go/conversion/', 'scripts.clickbank.net']
    page.route('**/*', lambda r:r.abort() if any(host in r.request.url for host in blocked) else r.continue_())
    response = page.goto(args.url, wait_until='domcontentloaded', timeout=60000)
    assert response.status == 200, 'Page did not render successfully'
    page.wait_for_function('(font)=>[...document.fonts].some(f=>f.family===font)', arg=args.font, timeout=30000)
    page.evaluate('document.fonts.ready')
    cdp = page.context.new_cdp_session(page)
    cdp.send('DOM.enable'); cdp.send('CSS.enable')
    doc = cdp.send('DOM.getDocument')
    for selector in args.selector:
        element = page.locator(selector).first
        assert element.count() == 1, 'Missing selector: ' + selector
        element.scroll_into_view_if_needed()
        node = cdp.send('DOM.querySelector', {'nodeId':doc['root']['nodeId'], 'selector':selector})
        fonts = cdp.send('CSS.getPlatformFontsForNode', {'nodeId':node['nodeId']})['fonts']
        declared = element.evaluate('(e)=>getComputedStyle(e).fontFamily')
        assert args.font in declared, 'Unexpected CSS font on ' + selector + ': ' + declared
        assert any(f['familyName'].startswith(args.font) and f['isCustomFont'] and f['glyphCount'] > 0 for f in fonts), 'Fallback glyphs on ' + selector
        print(json.dumps({'selector':selector, 'declared':declared, 'renderedFonts':fonts, 'result':'PASS'}))
    browser.close()
