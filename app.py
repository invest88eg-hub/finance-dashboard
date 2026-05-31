from flask import Flask, request, jsonify, send_file
from playwright.sync_api import sync_playwright
import json
import os
import tempfile

app = Flask(__name__)

@app.route('/screenshot', methods=['POST'])
def screenshot():
    data = request.json
    html_content = data.get('html', '')
    
    with tempfile.NamedTemporaryFile(suffix='.html', mode='w', delete=False) as f:
        f.write(html_content)
        html_file = f.name
    
    output_file = tempfile.mktemp(suffix='.png')
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 800, 'height': 1200})
        page.goto(f'file://{html_file}')
        page.wait_for_timeout(500)
        page.screenshot(path=output_file, full_page=True)
        browser.close()
    
    os.unlink(html_file)
    return send_file(output_file, mimetype='image/png')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
