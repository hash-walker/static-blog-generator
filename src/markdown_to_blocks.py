from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    CODE = "code"
    HEADING = "heading"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    
    new_blocks = []
    
    for block in blocks:
        block = block.strip()

        if not block:
            continue

        lines = block.split("\n")
        block = "\n".join(line.strip() for line in lines)

        new_blocks.append(block)
    
    return new_blocks


def block_to_block_type(block):

    if re.fullmatch(r"```[\s\S]+```", block.strip()):
        return BlockType.CODE
    
    if re.fullmatch(r"#{1,6} .+", block.strip()):
        return BlockType.HEADING
    
    lines = block.split('\n')

    if all(re.fullmatch(r">\s?.*", line) for line in lines):
        return BlockType.QUOTE

    if all(re.fullmatch(r"[-] .+", line) for line in lines):
        return BlockType.UNORDERED_LIST
    
    ordered_list_pattern = re.compile(r"(\d+)[.)] .+")

    if all(ordered_list_pattern.fullmatch(line.strip()) for line in lines):
    
        numbers = [int(ordered_list_pattern.match(line.strip()).group(1)) for line in lines]
        
        # Ensure numbers are sequential (1, 2, 3, ...)
        is_sequential = numbers == list(range(1, len(numbers) + 1))
        
        if is_sequential:
            return BlockType.ORDERED_LIST
    

    return BlockType.PARAGRAPH

