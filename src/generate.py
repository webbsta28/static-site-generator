from blocks import markdown_to_html_node, extract_title
from copy_static import copy_files_recursive
import os


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page {from_path} to {dest_path} using {template_path}")

    with open(from_path) as file:
        content_from_path = file.read()
    with open(template_path) as file:
        content_template_path = file.read()
    
    html_string = markdown_to_html_node(content_from_path).to_html()
    title = extract_title(content_from_path)
    html_template = content_template_path.replace("{{ Title }}", title)
    html_template = html_template.replace(f"{{ Content }}", html_string)
    dest = os.path.dirname(dest_path)
    os.makedirs(dest, exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(html_template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
        for filename in os.listdir(dir_path_content):
            from_path = os.path.join(dir_path_content, filename)
            dest_path = os.path.join(dest_dir_path, filename)
            print(f" * {from_path} -> {dest_path}")
            if os.path.isfile(from_path):
                new_path = dest_path.replace("md", "html")
                generate_page(from_path, template_path, new_path)
            else:
                generate_pages_recursive(from_path, template_path, dest_path)