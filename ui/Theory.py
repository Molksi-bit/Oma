from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
import os
import json



class TheoryWindow(QMainWindow):
    def __init__(self, section_id=None):
        super().__init__()
        self.setWindowTitle("Theorie-Anzeige")
        self.webview = QWebEngineView()
        self.setCentralWidget(self.webview)

        
        html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "core", "theory.html"))
        json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "core", "theory.json"))
        with open(json_path, "r", encoding="utf-8") as f:
            theory_data = json.load(f)

        html = build_theory_html(section_id, theory_data)
        self.webview.setHtml(html, baseUrl=QUrl("https://example.com/"))
        self.webview.loadFinished.connect(self.inject_mathjax_trigger)

    def inject_mathjax_trigger(self):
        self.webview.page().runJavaScript("""
            if (window.MathJax && MathJax.typesetPromise) {
                MathJax.typesetPromise().then(() => {
                    console.log("MathJax fertig");
                });
            } else {
                console.error("MathJax nicht geladen");
            }
        """)

    def _inject_fragment_scroll_script(self, html, section_id):
        scroll_script = f"""
        <script>
            window.addEventListener('load', function () {{
                const target = document.getElementById("{section_id}");
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth' }});
                }}
            }});
        </script>
        """
        return html.replace("</body>", scroll_script + "</body>")
    


def build_theory_html(section_id, theory_data):
    if section_id not in theory_data or section_id == None:
        return "<h2>Here you can look up certain elements like magnets or variables for an overview description.</h2>"
    #anders auflösen

    entry = theory_data[section_id]
    html_parts = [f"<h2>{section_id}</h2>"]

    # Beschreibung
    for desc in entry.get("description", []):
        html_parts.append(f"<p>{desc}</p>")

    # Berechnungen (Formeln)
    for title, formula in entry.get("calculations", {}).items():
        html_parts.append(f"<p><strong>{title.capitalize()}:</strong> $$ {formula} $$</p>")

    # Verlinkte Themen
    links = entry.get("links", [])
    if links:
        html_parts.append("<h3>Verwandte Themen:</h3><ul>")
        for link in links:
            html_parts.append(f'<li><a href="#" onclick="window.scrollToTopic(\'{link}\')">{link}</a></li>')
        html_parts.append("</ul>")

    return wrap_in_mathjax_html("\n".join(html_parts), theory_data)

def wrap_in_mathjax_html(content, theory_data):
    # JS-Funktion zum dynamischen Umschalten der Themen über Buttons/Links
    topic_data = json.dumps(theory_data).replace("</", "<\\/")  # escape für </script>
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>
    window.MathJax = {{
        tex: {{
            inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
            displayMath: [['$$','$$'], ['\\\\[','\\\\]']]
        }},
        svg: {{ fontCache: 'global' }}
    }};
    </script>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
    <script>
    const topics = {topic_data};

    window.scrollToTopic = function(name) {{
        const entry = topics[name];
        if (!entry) return;
        let html = `<h2>${{name}}</h2>`;
        if (entry.description) {{
            for (let d of entry.description)
                html += `<p>${{d}}</p>`;
        }}
        if (entry.calculations) {{
            for (let [k,v] of Object.entries(entry.calculations))
                html += `<p><strong>${{k}}:</strong> $$ ${{v}} $$</p>`;
        }}
        if (entry.links) {{
            html += "<h3>Verwandte Themen:</h3><ul>";
            for (let l of entry.links)
                html += `<li><a href="#" onclick="scrollToTopic('${{l}}')">${{l}}</a></li>`;
            html += "</ul>";
        }}
        document.body.innerHTML = html;
        MathJax.typesetPromise();
    }}
    </script>
</head>
<body>
    {content}
</body>
</html>
"""