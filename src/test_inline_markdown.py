import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_single_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_multiple_delimiters(self):
        node = TextNode("This has `code` and `more code` blocks", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This has ")
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[3].text, "more code")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)
        self.assertEqual(new_nodes[4].text, " blocks")

    def test_bold_text(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " text")

    def test_italic_text(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " text")

    def test_multiple_nodes(self):
        nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and this is `code` text", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " and this is ")
        self.assertEqual(new_nodes[3].text, "code")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)
        self.assertEqual(new_nodes[4].text, " text")

    def test_no_delimiters(self):
        node = TextNode("This is just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is just plain text")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_unclosed_delimiter(self):
        node = TextNode("This `code is not closed", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_empty_delimiter_sections(self):
        node = TextNode("Text ``with`` empty", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Text ")
        self.assertEqual(new_nodes[1].text, "with")
        self.assertEqual(new_nodes[2].text, " empty")

    def test_adjacent_delimiters(self):
        node = TextNode("Text**bold**_italic_", TextType.TEXT)
        # First split on bold
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        # Then split result on italic
        final_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(len(final_nodes), 3)
        self.assertEqual(final_nodes[0].text, "Text")
        self.assertEqual(final_nodes[1].text, "bold")
        self.assertEqual(final_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(final_nodes[2].text, "italic")
        self.assertEqual(final_nodes[2].text_type, TextType.ITALIC)

if __name__ == "__main__":
    unittest.main() 