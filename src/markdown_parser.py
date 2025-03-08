import re
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter

def extract_markdown_images(text):
    """
    Extract all markdown images from text.
    
    Args:
        text (str): The markdown text to parse
        
    Returns:
        list[tuple]: List of tuples containing (alt_text, url)
    """
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return [(alt.strip(), url.strip()) for alt, url in matches]

def extract_markdown_links(text):
    """
    Extract all markdown links from text.
    
    Args:
        text (str): The markdown text to parse
        
    Returns:
        list[tuple]: List of tuples containing (anchor_text, url)
    """
    # Use negative lookbehind (?<!) to ensure we don't match image links
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return [(text.strip(), url.strip()) for text, url in matches]

def split_nodes_image(old_nodes):
    """
    Split text nodes based on markdown image syntax.
    
    Args:
        old_nodes (list[TextNode]): List of nodes to process
        
    Returns:
        list[TextNode]: New list of nodes with images split into separate nodes
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # If the node is not a text node, keep it as is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        # Find all images in the text
        images = extract_markdown_images(old_node.text)
        if not images:
            new_nodes.append(old_node)
            continue
            
        # Process the text, splitting on each image
        current_text = old_node.text
        for alt_text, url in images:
            # Split on the image markdown
            image_markdown = f"![{alt_text}]({url})"
            parts = current_text.split(image_markdown, 1)
            
            # Add the text before the image if it's not empty
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                
            # Add the image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            
            # Update the remaining text
            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""
                
        # Add any remaining text
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
            
    return new_nodes

def split_nodes_link(old_nodes):
    """
    Split text nodes based on markdown link syntax.
    
    Args:
        old_nodes (list[TextNode]): List of nodes to process
        
    Returns:
        list[TextNode]: New list of nodes with links split into separate nodes
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # If the node is not a text node, keep it as is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        # Find all links in the text
        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue
            
        # Process the text, splitting on each link
        current_text = old_node.text
        for anchor_text, url in links:
            # Split on the link markdown
            link_markdown = f"[{anchor_text}]({url})"
            parts = current_text.split(link_markdown, 1)
            
            # Add the text before the link if it's not empty
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                
            # Add the link node
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            
            # Update the remaining text
            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""
                
        # Add any remaining text
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
            
    return new_nodes 

def text_to_textnodes(text):
    """
    Convert a markdown-formatted text string into a list of TextNode objects.
    
    Args:
        text (str): The markdown text to convert
        
    Returns:
        list[TextNode]: List of TextNode objects representing the text
    """
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Split on delimiters for basic markdown
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    # Split on images and links
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes 