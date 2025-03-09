import os
from pathlib import Path
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

def generate_page(from_path, template_path, to_path, base_path="/"):
    """
    Generate an HTML page from a markdown file.
    
    Args:
        from_path (str): Path to the markdown file
        template_path (str): Path to the template file
        to_path (str): Path where the HTML file will be written
        base_path (str): Base path for URLs (default: "/")
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
    title = extract_title(markdown)
    
    # Replace placeholders in template
    template = template.replace('{{ Title }}', title)
    template = template.replace('{{ Content }}', html)
    template = template.replace('{{ css_path }}', css_path)
    
    # Replace absolute URLs with base path
    template = template.replace('href="/', f'href="{base_path}')
    template = template.replace('src="/', f'src="{base_path}')
    
    # Write the output file
    os.makedirs(os.path.dirname(to_path), exist_ok=True)
    with open(to_path, 'w') as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path="/"):
    """
    Recursively generate HTML pages from markdown files in a directory.
    
    Args:
        dir_path_content (str): Path to the content directory
        template_path (str): Path to the template file
        dest_dir_path (str): Path to the destination directory
        base_path (str): Base path for URLs (default: "/")
    """
    # Convert paths to Path objects for easier manipulation
    content_path = Path(dir_path_content)
    dest_path = Path(dest_dir_path)
    
    # Walk through all files and directories in content_path
    for item in content_path.rglob("*.md"):
        # Get the relative path from content directory
        rel_path = item.relative_to(content_path)
        
        # Create the destination path with .html extension
        dest_file = dest_path / rel_path.with_suffix('.html')
        
        # Generate the HTML page
        generate_page(str(item), template_path, str(dest_file), base_path)