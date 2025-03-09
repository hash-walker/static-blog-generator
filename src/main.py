import os
import sys
import shutil
import logging
from page import generate_pages_recursive

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

def main():
    """Main function to generate the static site."""
    # Get the base path from command line argument or use default
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"
    
    # Get the root directory (parent of src)
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Define paths
    static_dir = os.path.join(root_dir, "static")
    docs_dir = os.path.join(root_dir, "docs")  # Changed from public to docs
    content_dir = os.path.join(root_dir, "content")
    template_path = os.path.join(root_dir, "template.html")
    
    # Copy static files
    logging.info("Starting static file copy")
    copy_directory(static_dir, docs_dir)  # Changed from public to docs
    logging.info("Finished static file copy")
    
    # Generate HTML pages recursively
    logging.info("Generating HTML pages")
    generate_pages_recursive(content_dir, template_path, docs_dir, base_path)  # Added base_path
    logging.info("Finished generating HTML pages")

if __name__ == "__main__":
    main()