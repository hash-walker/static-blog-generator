import os
from markdown_parser import markdown_to_htmlnode

def extract_title(markdown):
    """
    Extract the title (h1) from a markdown string.
    
    Args:
        markdown (str): The markdown content
        
    Returns:
        str: The title text without the # prefix
        
    Raises:
        ValueError: If no h1 header is found
    """
    lines = markdown.split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No h1 header found in markdown file")

def generate_page(from_path, template_path, to_path):
    """
    Generate an HTML page from a markdown file.
    
    Args:
        from_path (str): Path to the markdown file
        template_path (str): Path to the template file
        to_path (str): Path where the HTML file will be written
    """
    print(f"Generating page from {from_path} to {to_path} using {template_path}")
    
    # Calculate the relative path to the CSS file
    depth = len(os.path.relpath(to_path, os.path.dirname(template_path)).split(os.sep)) - 1
    css_path = "../" * (depth - 1) + "index.css" if depth > 0 else "index.css"
    
    # Read the markdown file
    with open(from_path, 'r') as f:
        markdown = f.read()
        
    # Read the template
    with open(template_path, 'r') as f:
        template = f.read()
        
    # Convert markdown to HTML
    html_node = markdown_to_htmlnode(markdown)
    html = html_node.to_html()
    
    # Get the title from the first line of markdown
    title = markdown.split('\n')[0].lstrip('#').strip()
    
    # Replace placeholders in template
    template = template.replace('{{ Title }}', title)
    template = template.replace('{{ Content }}', html)
    template = template.replace('{{ css_path }}', css_path)
    
    # Write the output file
    os.makedirs(os.path.dirname(to_path), exist_ok=True)
    with open(to_path, 'w') as f:
        f.write(template)