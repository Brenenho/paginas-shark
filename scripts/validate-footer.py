"""Exercise the portable footer without sending tracker/conversion requests."""
import argparse
import json
from pathlib import Path
import re
from playwright.sync_api import sync_playwright

parser = argparse.ArgumentParser()
parser.add_argument('--chrome', default='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
args = parser.parse_args()
skill = Path(__file__).resolve().parents[1]
template = (skill / 'assets/footer-universal.html').read_text()
config = json.loads((skill / 'assets/footer-oilbase20.config.json').read_text())
configured = re.sub(r'(<script type="application/json" id="shark-footer-config">).*?(</script>)', lambda m: m[1] + json.dumps(config) + m[2], template, flags=re.S)
cases = [
    ('getoilbase20.com', '', 'buygoods'),
    ('oilbase20.com', '', 'clickbank'),
    ('unknown.example', '', ''),
    ('oilbase20.com', 'buygoods', 'buygoods'),
    ('getoilbase20.com', 'stripe', 'stripe'),
]
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path=args.chrome)
    for host, server_merchant, expected in cases:
        context = browser.new_context()
        page = context.new_page()
        requests = []
        body = configured
        if server_merchant:
            body = body.replace('{{ request.merchant_code }}', server_merchant).replace('{{ var.offer_name }}', 'Oilbase-20')
        else:
            body = re.sub(r' data-elastic-(merchant|brand)="[^"]*"', '', body)
        markup = '<!doctype html><html lang="en"><head><meta charset="utf-8"></head><body style="font-family:serif"><main>Test content</main>' + body + '</body></html>'
        url = 'https://' + host + '/footer-test?merchant=clickbank'
        def route(request):
            if request.request.url == url:
                request.fulfill(status=200, content_type='text/html', body=markup)
            else:
                requests.append(request.request.url)
                request.abort()
        page.route('**/*', route)
        page.goto(url, wait_until='domcontentloaded')
        page.wait_for_timeout(1100)
        def state():
            return page.evaluate('''() => ({merchant:document.querySelector('#shark-footer').dataset.merchant, blocks:document.querySelectorAll('#shark-footer .shark-footer-merchant:not([hidden])').length, copy:document.querySelector('.shark-footer-disclaimer').textContent, brand:document.querySelector('[data-shark-brand]').textContent, fonts:getComputedStyle(document.querySelector('main')).fontFamily, footers:document.querySelectorAll('#shark-footer').length, scripts:[...document.scripts].filter(s=>s.src).map(s=>s.src),frames:document.querySelectorAll('iframe').length})''')
        result = state()
        assert result['merchant'] == expected, result
        assert result['blocks'] == (1 if expected in ['buygoods', 'clickbank'] else 0), result
        assert result['brand'] == 'Oilbase-20' and result['fonts'] == 'serif' and result['footers'] == 1, result
        if expected == 'buygoods':
            assert 'BuyGoods is the retailer' in result['copy'] and 'ClickBank is the retailer' not in result['copy']
            assert any('tracking.buygoods.com' in u for u in requests)
            assert not any('scripts.clickbank.net' in u for u in requests)
            assert result['frames'] == 1
        elif expected == 'clickbank':
            assert 'ClickBank is the retailer' in result['copy'] and 'BuyGoods is the retailer' not in result['copy']
            assert any('scripts.clickbank.net' in u for u in requests)
            assert not any('tracking.buygoods.com' in u for u in requests)
        else:
            assert not result['scripts'] and not result['frames'], result
        page.evaluate("SharkFooter.setMerchant('clickbank'); SharkFooter.setMerchant('clickbank'); SharkFooter.refresh();")
        updated = state()
        assert updated['merchant'] == 'clickbank'
        assert len([u for u in updated['scripts'] if 'scripts.clickbank.net' in u]) == 1
        page.evaluate('SharkFooter.clearMerchant()')
        assert state()['merchant'] == expected
        print(json.dumps({'host':host,'serverMerchant':server_merchant,'resolved':expected,'result':'PASS','tracking_requests_intercepted':True,'no_global_font_change':True,'no_duplicate_scripts':True}))
        context.close()
    # A second brand must not inherit Oilbase's account/vendor/domain settings.
    alternate = dict(config, brandName='Example Brand', domains={'example-brand.test': {'merchant':'clickbank'}}, merchants={'clickbank':{'vendor':'example-vendor'}}, trackConversion=False)
    alt = re.sub(r'(<script type="application/json" id="shark-footer-config">).*?(</script>)', lambda m:m[1]+json.dumps(alternate)+m[2], template, flags=re.S)
    alt = re.sub(r' data-elastic-(merchant|brand)="[^"]*"','',alt)
    page=browser.new_page()
    page.route('**/*',lambda r:r.fulfill(status=200,content_type='text/html',body='<html><body>'+alt+'</body></html>') if r.request.url=='https://example-brand.test/' else r.abort())
    page.goto('https://example-brand.test/',wait_until='domcontentloaded')
    assert page.evaluate('window.clickbank.vendor')=='example-vendor'
    assert page.locator('[data-shark-brand]').inner_text()=='Example Brand'
    print('Second brand: PASS; vendor/brand replaced independently')
    browser.close()
