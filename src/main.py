import os
import shutil
from htmlblock import markdown_to_html_node

def main():
    tree_source = "./static"
    tree_destination = "./public"
    content_path = "./content"
    template_path = "./template.html"
    destination_path = "./public"
    
    if os.path.exists(tree_destination):
        shutil.rmtree(tree_destination)
    
    os.makedirs(tree_destination, exist_ok=True)
    
    if not os.path.exists(tree_source):
        raise FileNotFoundError
    
    copy_tree(tree_source, tree_destination)

    generate_pages_recursive(content_path, template_path, destination_path)


def copy_tree(tree_source, tree_destination):
    for name in os.listdir(tree_source):
        original_path = f"{tree_source}/{name}"
        destination_path = f"{tree_destination}/{name}"

        if not os.path.isfile(original_path):
            os.makedirs(destination_path, exist_ok=True)
            copy_tree(original_path, destination_path)
        else:
            shutil.copy(original_path, destination_path)
        

def extract_title(markdown):
    if not markdown.startswith("# "):
        if markdown.strip().startswith("# "):
            raise SyntaxError("Document cannot have spaces before title")
        raise SyntaxError("Document must start with a title")
    
    markdown_lines = markdown.split("\n")
    header_content = markdown_lines[0].lstrip("# ")
    return header_content


def generate_page(content_path, template_path, destination_path):
    print(f"Generating page from {content_path} to {destination_path} using {template_path}")
    
    with open(content_path, "r") as file:
        try:
            markdown_document = file.read()
        except FileNotFoundError:
            print("Content markdown file not found")

    with open(template_path, "r") as file:
        try:
            template = file.read()
        except FileNotFoundError:
            print("Template file not found")

    html_content = markdown_to_html_node(markdown_document)
    page_title = extract_title(markdown_document)
    html_page = template.replace("{{ Title }}", page_title).replace("{{ Content }}", html_content)


    destination_directory = os.path.dirname(destination_path)
    if not os.path.exists(os.path.dirname(destination_directory)):
        os.makedirs(destination_directory, exist_ok=True)
    
    with open(destination_path, "w") as file:
        file.write(html_page)


def generate_pages_recursive(content_dir_path, template_path, destination_dir_path):
    print(f"WORKING DIRECTORY: {content_dir_path}")
    for element in os.listdir(content_dir_path):
        print(element)
        element_src_path = os.path.join(content_dir_path, element)
        element_dest_path = os.path.join(destination_dir_path, element.replace(".md", ".html"))
        print(element_src_path)
        print(element_dest_path)

        if os.path.isfile(element_src_path):
            generate_page(element_src_path, template_path, element_dest_path)
        else:
            os.makedirs(element_dest_path, exist_ok=True)
            generate_pages_recursive(element_src_path, template_path, element_dest_path)

    
if __name__ == "__main__":
    main()