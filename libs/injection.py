import streamlit.components.v1 as components


def manage_injections():
    inject_html("statcounter.html")


def inject_html(html_file):
    HtmlFile = open(f"injection/{html_file}", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height=1)
