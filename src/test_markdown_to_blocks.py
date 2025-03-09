import unittest
from markdown_to_blocks import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_input(self):
        self.assertEqual(markdown_to_blocks(""), [])
        self.assertEqual(markdown_to_blocks("\n\n\n"), [])

    def test_single_block(self):
        self.assertEqual(
            markdown_to_blocks("Just one block"),
            ["Just one block"]
        )

    def test_multiple_newlines(self):
        md = "First block\n\n\n\nSecond block"
        self.assertEqual(
            markdown_to_blocks(md),
            ["First block", "Second block"]
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is a normal paragraph with **bold** and _italic_ text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        # Empty block should be paragraph
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
        
    def test_heading(self):
        # Test all heading levels
        for i in range(1, 7):
            block = "#" * i + " Heading"
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)
            
        # Test invalid heading (no space after #)
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)
        
    def test_code(self):
        block = "```\ndef hello():\n    print('world')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        
        # Test with language specification
        block = "```python\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        
        # Test invalid code block (missing end backticks)
        self.assertEqual(block_to_block_type("```\ncode"), BlockType.PARAGRAPH)
        
    def test_quote(self):
        # Single line quote
        self.assertEqual(block_to_block_type(">This is a quote"), BlockType.QUOTE)
        
        # Multi-line quote
        block = ">First line\n>Second line\n>Third line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        
        # Invalid quote (missing > on second line)
        block = ">First line\nSecond line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
    def test_unordered_list(self):
        # Single item
        self.assertEqual(block_to_block_type("- Item 1"), BlockType.UNORDERED_LIST)
        
        # Multiple items
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        
        # Invalid list (missing space after -)
        self.assertEqual(block_to_block_type("-Invalid"), BlockType.PARAGRAPH)
        
        # Invalid list (inconsistent markers)
        block = "- Item 1\n* Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
    def test_ordered_list(self):
        # Single item
        self.assertEqual(block_to_block_type("1. Item"), BlockType.ORDERED_LIST)
        
        # Multiple items
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        
        # Invalid list (wrong order)
        block = "1. First\n3. Third\n2. Second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        # Invalid list (not starting with 1)
        block = "2. First\n3. Second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        # Invalid list (missing space after number)
        block = "1.First"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == '__main__':
    unittest.main()

