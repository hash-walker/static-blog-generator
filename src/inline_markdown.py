from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split text nodes based on a delimiter and convert the delimited text to a specific type.
    
    Args:
        old_nodes (list[TextNode]): List of nodes to process
        delimiter (str): The delimiter to split on (e.g. **, _, `)
        text_type (TextType): The type to assign to delimited text
        
    Returns:
        list[TextNode]: New list of nodes with text split on delimiters
        
    Raises:
        ValueError: If a closing delimiter is not found
    """
    new_nodes = []
    
    # Process each node in the input list
    for old_node in old_nodes:
        # If the node is not a text node, keep it as is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Split the text on the delimiter
        pieces = old_node.text.split(delimiter)
        
        # If no delimiter was found, keep the node as is
        if len(pieces) == 1:
            new_nodes.append(old_node)
            continue
            
        # Ensure we have matching pairs of delimiters
        if len(pieces) % 2 == 0:
            raise ValueError(
                f"Invalid markdown: Unclosed delimiter {delimiter}"
            )
            
        # Process the pieces
        for i in range(len(pieces)):
            piece = pieces[i]
            # Skip empty pieces
            if not piece:
                continue
                
            # Every second piece (1-based index) is delimited
            if i % 2 == 1:
                new_node = TextNode(piece, text_type)
            else:
                new_node = TextNode(piece, TextType.TEXT)
            new_nodes.append(new_node)
            
    return new_nodes 