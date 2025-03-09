import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter
from htmlnode import HTMLNode

class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_delimiter_basic(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_delimiter_multiple(self):
        node = TextNode("This is **bold** text with **more bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text with ", TextType.TEXT),
                TextNode("more bold", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_split_nodes_delimiter_empty_delimited(self):
        node = TextNode("This is **** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_delimiter_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_delimiter_no_delimiters(self):
        node = TextNode("This is text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_delimiter_multiple_nodes(self):
        nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("**bold**", TextType.TEXT),
            TextNode(" and ", TextType.TEXT),
            TextNode("**more bold**", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("more bold", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_split_nodes_delimiter_non_text_node(self):
        node = TextNode("**bold**", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_delimiter_unclosed(self):
        node = TextNode("This **is unclosed", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_nodes_delimiter_different_types(self):
        node = TextNode("This is _italic_ and `code`", TextType.TEXT)
        italic_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        code_nodes = split_nodes_delimiter(italic_nodes, "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
            code_nodes,
        )

if __name__ == "__main__":
    unittest.main() 