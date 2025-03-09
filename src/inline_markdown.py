from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split text nodes based on a delimiter.
    
    Args:
        old_nodes (list[TextNode]): List of nodes to process
        delimiter (str): The delimiter to split on (e.g., "**" for bold)
        text_type (TextType): The type to assign to text between delimiters
        
    Returns:
        list[TextNode]: New list of nodes with text between delimiters assigned the specified type
        
    Raises:
        ValueError: If there are unclosed delimiters
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # If the node is not a text node, keep it as is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        # Split the text on the delimiter
        sections = old_node.text.split(delimiter)
        
        # If there's no delimiter, keep the node as is
        if len(sections) == 1:
            new_nodes.append(old_node)
            continue
            
        # Check for unclosed delimiters
        if len(sections) % 2 == 0:
            raise ValueError(f"Unclosed delimiter {delimiter}")
            
        current_nodes = []
        # Process the sections
        for i in range(len(sections)):
            # Skip empty sections at the start or end
            if not sections[i] and (i == 0 or i == len(sections) - 1):
                continue
                
            # If we're in between delimiters (odd index)
            if i % 2 == 1:
                if sections[i]:
                    current_nodes.append(TextNode(sections[i], text_type))
            else:
                current_nodes.append(TextNode(sections[i], TextType.TEXT))
                
        # Only add nodes if we found some
        if current_nodes:
            new_nodes.extend(current_nodes)
                
    return new_nodes 