import os
import inspect
import streamlit as st


def show_readme():
    current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parent_dir = os.path.dirname(current_dir)
    markdown_file_path = parent_dir + "/README.md"

    if not os.path.exists(markdown_file_path):
        st.error("Markdown file does not exist.")
        st.stop()

    with open(markdown_file_path, 'r', encoding="utf-8") as outfile:
        markdown_content = outfile.read()

    st.markdown(markdown_content, unsafe_allow_html=True)
