from flask import Flask, render_template_string, request, session, redirect, url_for
from pathlib import Path
import os, secrets

def get_or_create_secret_key(filename=None):
    env = os.environ.get("SECRET_KEY")
    if env:
        return env

    if filename is None:
        filename = Path.home() / ".text_navigator" / "secret_key"

    try:
        filename.parent.mkdir(parents=True, exist_ok=True)
        if filename.exists():
            return filename.read_text(encoding="utf-8").strip()
        key = secrets.token_urlsafe(32)
        filename.write_text(key, encoding="utf-8")
        try:
            filename.chmod(0o600)
        except Exception:
            pass
        return key
    except Exception:
        return secrets.token_urlsafe(32)

app = Flask(__name__)
app.config["SECRET_KEY"] = get_or_create_secret_key()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>pyCardShuffle</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #e8f4f2 0%, #b8dbd6 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            width: 100%;
            max-width: 1000px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
            padding: 0 20px;
        }
        
        .insert-btn {
            background: linear-gradient(135deg, #20b2aa 0%, #48d1cc 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 500;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transition: all 0.3s ease;
        }
        
        .insert-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.2);
            background: linear-gradient(135deg, #1a9a92 0%, #40c4b9 100%);
        }
        
        .insert-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        
        .modal-content {
            background: white;
            padding: 30px;
            border-radius: 12px;
            width: 90%;
            max-width: 600px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .modal-textarea {
            width: 100%;
            height: 300px;
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            padding: 15px;
            font-size: 14px;
            font-family: monospace;
            resize: vertical;
            margin-bottom: 20px;
        }
        
        .modal-textarea:focus {
            outline: none;
            border-color: #20b2aa;
        }
        
        .modal-textarea::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        .modal-textarea::-webkit-scrollbar-track {
            background: #e8f4f2;
            border-radius: 4px;
        }
        
        .modal-textarea::-webkit-scrollbar-thumb {
            background: #20b2aa;
            border-radius: 4px;
        }
        
        .modal-textarea::-webkit-scrollbar-thumb:hover {
            background: #1a9a92;
        }
        
        .modal-textarea::-webkit-scrollbar-corner {
            background: #e8f4f2;
        }
        
        .modal-textarea {
            scrollbar-width: thin;
            scrollbar-color: #20b2aa #e8f4f2;
        }
        
        .modal-buttons {
            display: flex;
            gap: 10px;
            justify-content: flex-end;
        }
        
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #20b2aa 0%, #48d1cc 100%);
            color: white;
        }
        
        .btn-primary:hover {
            background: linear-gradient(135deg, #1a9a92 0%, #40c4b9 100%);
        }
        
        .btn-secondary {
            background: #f8f9fa;
            color: #6c757d;
            border: 1px solid #dee2e6;
        }
        
        .btn-clear {
            background: #c9d6d3;
            color: #5a6b68;
            border: 1px solid #b0c2be;
        }
        
        .btn-clear:hover {
            background: #bcc8c5;
            border-color: #9fb3af;
        }
        
        .btn:hover {
            transform: translateY(-1px);
        }
        
        .page-counter {
            font-size: 18px;
            font-weight: 600;
            color: #495057;
            margin-bottom: 10px;
        }
        
        .text-box {
            background: rgba(255, 255, 255, 0.9);
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 100%;
            max-height: 60vh;
            min-height: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            font-size: 16px;
            line-height: 1.6;
            color: #495057;
            white-space: pre-wrap;
            transition: background 0.2s ease;
            position: relative;
            overflow: auto;
            word-wrap: break-word;
            overflow-wrap: break-word;
            /* Make text selectable */
            -webkit-user-select: text;
            -moz-user-select: text;
            -ms-user-select: text;
            user-select: text;
        }
        
        .text-box:hover {
            background: rgba(255, 255, 255, 0.95);
        }
        
        .text-box::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        .text-box::-webkit-scrollbar-track {
            background: #e8f4f2;
            border-radius: 4px;
        }
        
        .text-box::-webkit-scrollbar-thumb {
            background: #20b2aa;
            border-radius: 4px;
        }
        
        .text-box::-webkit-scrollbar-thumb:hover {
            background: #1a9a92;
        }
        
        .text-box::-webkit-scrollbar-corner {
            background: #e8f4f2;
        }
        
        /* Firefox scrollbar styling */
        .text-box {
            scrollbar-width: thin;
            scrollbar-color: #20b2aa #e8f4f2;
        }
        
        .text-box.empty-state-container {
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        
        .navigation {
            display: flex;
            gap: 15px;
        }
        
        .nav-btn {
            background: linear-gradient(135deg, #20b2aa 0%, #48d1cc 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 500;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transition: all 0.3s ease;
            min-width: 100px;
        }
        
        .nav-btn:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.2);
            background: linear-gradient(135deg, #1a9a92 0%, #40c4b9 100%);
        }
        
        .nav-btn:disabled {
            background: #e9ecef;
            color: #adb5bd;
            cursor: not-allowed;
            box-shadow: none;
            transform: none;
        }
        
        .empty-state {
            font-style: italic;
            color: #6c757d;
        }
        
        .copy-indicator {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #20b2aa;
            color: white;
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
            opacity: 0;
            transform: translateY(-10px);
            transition: all 0.3s ease;
            z-index: 1001;
        }
        
        .copy-indicator.show {
            opacity: 1;
            transform: translateY(0);
        }
        
        .copy-button {
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(32, 178, 170, 0.8);
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 500;
            opacity: 0;
            transition: opacity 0.2s ease;
        }
        
        .text-box:hover .copy-button {
            opacity: 1;
        }
        
        .copy-button:hover {
            background: rgba(26, 154, 146, 0.9);
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .container {
                padding: 0 10px;
            }
            
            .text-box {
                padding: 20px;
                max-height: 50vh;
                font-size: 14px;
            }
            
            .modal-content {
                padding: 20px;
                width: 95%;
            }
            
            .navigation {
                flex-direction: column;
                gap: 10px;
            }
            
            .nav-btn {
                min-width: 200px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <button class="insert-btn" onclick="openModal()">Insert</button>
        
        {% if pages %}
            <div class="page-counter">{{ current_page }}/{{ total_pages }}</div>
            <div class="text-box">
                <button class="copy-button" onclick="copyCurrentText(event)">Copy All</button>
                {{- current_text|trim -}}
            </div>
        {% else %}
            <div class="text-box empty-state-container">
                <div class="empty-state">No pages yet. Click "Insert" to add some text!</div>
            </div>
        {% endif %}
        
        <div class="navigation">
            <form method="POST" action="{{ url_for('navigate') }}" style="display: inline;">
                <input type="hidden" name="direction" value="prev">
                <button type="submit" class="nav-btn" {% if not pages or current_page <= 1 %}disabled{% endif %}>
                    ← Previous
                </button>
            </form>
            
            <form method="POST" action="{{ url_for('navigate') }}" style="display: inline;">
                <input type="hidden" name="direction" value="next">
                <button type="submit" class="nav-btn" {% if not pages or current_page >= total_pages %}disabled{% endif %}>
                    Next →
                </button>
            </form>
        </div>
    </div>
    
    <div class="copy-indicator" id="copyIndicator">Copied!</div>
    
    <div class="insert-modal" id="insertModal">
        <div class="modal-content">
            <h3 style="margin-bottom: 20px; color: #495057;">Insert Text</h3>
            <form method="POST" action="{{ url_for('insert_text') }}">
                <textarea class="modal-textarea" name="text_input" placeholder="Paste your text here. Use --- to separate pages...">{{ saved_text }}</textarea>
                <div class="modal-buttons">
                    <button type="button" class="btn btn-clear" onclick="clearTextarea()">Clear</button>
                    <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
                    <button type="submit" class="btn btn-primary">Insert</button>
                </div>
            </form>
        </div>
    </div>
    
    <script>
        function openModal() {
            document.getElementById('insertModal').style.display = 'flex';
        }
        
        function closeModal() {
            document.getElementById('insertModal').style.display = 'none';
        }
        
        function clearTextarea() {
            document.querySelector('.modal-textarea').value = '';
        }
        
        function copyCurrentText(event) {
            event.stopPropagation();
            
            const textBox = document.querySelector('.text-box');
            if (!textBox) return;
            
            const copyButton = textBox.querySelector('.copy-button');
            let text = '';
            
            const clone = textBox.cloneNode(true);
            const cloneButton = clone.querySelector('.copy-button');
            if (cloneButton) {
                cloneButton.remove();
            }
            text = clone.textContent.trim();
            
            if (!text) return;
            
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(text).then(function() {
                    showCopyIndicator();
                }).catch(function(err) {
                    console.log('Clipboard API failed, using fallback');
                    fallbackCopyText(text);
                });
            } else {
                fallbackCopyText(text);
            }
        }
        
        function fallbackCopyText(text) {
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.left = '-9999px';
            textArea.style.top = '-9999px';
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            
            try {
                const successful = document.execCommand('copy');
                if (successful) {
                    showCopyIndicator();
                }
            } catch (err) {
                console.log('Fallback copy failed');
            }
            
            document.body.removeChild(textArea);
        }
        
        function showCopyIndicator() {
            const indicator = document.getElementById('copyIndicator');
            indicator.classList.add('show');
            setTimeout(() => {
                indicator.classList.remove('show');
            }, 2000);
        }
        
        document.getElementById('insertModal').addEventListener('click', function(e) {
            if (e.target === this) {
                closeModal();
            }
        });
        
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeModal();
            }
        });
        
        document.querySelector('.text-box').addEventListener('click', function(e) {
            if (window.getSelection().toString().length === 0 && !e.target.classList.contains('copy-button')) {
                // Allow normal text selection behavior
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    pages = session.get('pages', [])
    current_page = session.get('current_page', 1)
    saved_text = session.get('saved_text', '')
    
    if pages:
        current_text = pages[current_page - 1] if current_page <= len(pages) else ""
        total_pages = len(pages)
    else:
        current_text = ""
        total_pages = 0
        current_page = 0
    
    return render_template_string(HTML_TEMPLATE, 
                                pages=pages,
                                current_page=current_page,
                                total_pages=total_pages,
                                current_text=current_text,
                                saved_text=saved_text)

@app.route('/insert', methods=['POST'])
def insert_text():
    text_input = request.form.get('text_input', '')
    
    session['saved_text'] = text_input
    
    if text_input.strip():
        raw_pages = text_input.split('---')
        pages = []
        for page in raw_pages:
            stripped_page = page.strip()
            if stripped_page:
                pages.append(stripped_page)
        
        if pages:
            session['pages'] = pages
            session['current_page'] = 1
    
    return redirect(url_for('index'))

@app.route('/clear', methods=['POST'])
def clear_text():
    session['saved_text'] = ''
    return redirect(url_for('index'))

@app.route('/navigate', methods=['POST'])
def navigate():
    direction = request.form.get('direction')
    pages = session.get('pages', [])
    current_page = session.get('current_page', 1)
    
    if pages:
        if direction == 'prev' and current_page > 1:
            session['current_page'] = current_page - 1
        elif direction == 'next' and current_page < len(pages):
            session['current_page'] = current_page + 1
    
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8992, debug=False)