import os
import shutil
import logging
from page import generate_page

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def copy_directory(src, dst):
    """
    Recursively copy a directory from src to dst.
    First deletes the destination directory if it exists.
    
    Args:
        src (str): Source directory path
        dst (str): Destination directory path
    """
    # Delete destination directory if it exists
    if os.path.exists(dst):
        logging.info(f"Removing existing directory: {dst}")
        shutil.rmtree(dst)
    
    # Create destination directory
    logging.info(f"Creating directory: {dst}")
    os.makedirs(dst)
    
    # Walk through the source directory
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        
        if os.path.isfile(src_path):
            # Copy file
            logging.info(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy2(src_path, dst_path)
        else:
            # Recursively copy directory
            logging.info(f"Copying directory: {src_path} -> {dst_path}")
            copy_directory(src_path, dst_path)

def process_markdown_files(content_dir, public_dir, template_path):
    """
    Process all markdown files in the content directory and its subdirectories.
    
    Args:
        content_dir (str): Content directory path
        public_dir (str): Public directory path
        template_path (str): Template file path
    """
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file.endswith('.md'):
                # Get the markdown file path
                md_path = os.path.join(root, file)
                
                # Calculate the relative path from content_dir
                rel_path = os.path.relpath(md_path, content_dir)
                
                # Convert the path to HTML
                html_path = os.path.join(
                    public_dir,
                    os.path.splitext(rel_path)[0] + '.html'
                )
                
                # Create the directory if it doesn't exist
                os.makedirs(os.path.dirname(html_path), exist_ok=True)
                
                # Generate the HTML page
                logging.info(f"Generating page from {md_path} to {html_path}")
                generate_page(md_path, template_path, html_path)

def main():
    """Main function to generate the static site."""
    # Get the root directory (parent of src)
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Define paths
    static_dir = os.path.join(root_dir, "static")
    public_dir = os.path.join(root_dir, "public")
    content_dir = os.path.join(root_dir, "content")
    template_path = os.path.join(root_dir, "template.html")
    
    # Copy static files
    logging.info("Starting static file copy")
    copy_directory(static_dir, public_dir)
    logging.info("Finished static file copy")
    
    # Generate HTML pages
    logging.info("Generating HTML pages")
    process_markdown_files(content_dir, public_dir, template_path)
    logging.info("Finished generating HTML pages")

if __name__ == "__main__":
    main()