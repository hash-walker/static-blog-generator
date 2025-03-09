import unittest
from textnode import TextNode, TextType
from markdown_parser import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_htmlnode
)

class TestMarkdownParser(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ], matches)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([
            ("to boot dev", "https://www.boot.dev")
        ], matches)

    def test_extract_multiple_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ], matches)

    def test_extract_no_images(self):
        matches = extract_markdown_images("This text has no images")
        self.assertListEqual([], matches)

    def test_extract_no_links(self):
        matches = extract_markdown_links("This text has no links")
        self.assertListEqual([], matches)

    def test_extract_complex_urls(self):
        text = """
        Here are some complex URLs:
        ![img](https://example.com/path?param=1&other=2)
        [link](https://api.example.com/v1/data?id=123#section)
        """
        img_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        self.assertListEqual([
            ("img", "https://example.com/path?param=1&other=2")
        ], img_matches)
        self.assertListEqual([
            ("link", "https://api.example.com/v1/data?id=123#section")
        ], link_matches)

    def test_extract_mixed_content(self):
        text = """
        # My Blog Post
        
        Here's a ![logo](https://example.com/logo.png) and a [link](https://example.com).
        
        And another ![image](https://example.com/image.jpg) with [another link](https://example.com/page).
        """
        img_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        self.assertListEqual([
            ("logo", "https://example.com/logo.png"),
            ("image", "https://example.com/image.jpg")
        ], img_matches)
        self.assertListEqual([
            ("link", "https://example.com"),
            ("another link", "https://example.com/page")
        ], link_matches)

    def test_extract_empty_text(self):
        self.assertListEqual([], extract_markdown_images(""))
        self.assertListEqual([], extract_markdown_links(""))

    def test_extract_whitespace_handling(self):
        text = """
        [ link ](  https://example.com  )
        ![  image  ](  https://example.com/img.png  )
        """
        img_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        self.assertListEqual([
            ("image", "https://example.com/img.png")
        ], img_matches)
        self.assertListEqual([
            ("link", "https://example.com")
        ], link_matches)

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_image_single_node(self):
        node = TextNode("![image](https://example.com/img.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("image", TextType.IMAGE, "https://example.com/img.png")],
            new_nodes,
        )

    def test_split_link_single_node(self):
        node = TextNode("[link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("link", TextType.LINK, "https://example.com")],
            new_nodes,
        )

    def test_split_image_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_link_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_image_no_images(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_link_no_links(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_image_multiple_nodes(self):
        nodes = [
            TextNode("Start ", TextType.TEXT),
            TextNode("![img1](url1)![img2](url2)", TextType.TEXT),
            TextNode(" end", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("img1", TextType.IMAGE, "url1"),
                TextNode("img2", TextType.IMAGE, "url2"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_multiple_nodes(self):
        nodes = [
            TextNode("Start ", TextType.TEXT),
            TextNode("[link1](url1)[link2](url2)", TextType.TEXT),
            TextNode(" end", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "url1"),
                TextNode("link2", TextType.LINK, "url2"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_non_text_node(self):
        node = TextNode("![img](url)", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_link_non_text_node(self):
        node = TextNode("[link](url)", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_text_to_textnodes_simple(self):
        text = "This is **text** with an _italic_ word"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            nodes,
        )

    def test_text_to_textnodes_complex(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_text_to_textnodes_empty(self):
        nodes = text_to_textnodes("")
        self.assertListEqual([TextNode("", TextType.TEXT)], nodes)

    def test_text_to_textnodes_no_special_chars(self):
        text = "This is just plain text"
        nodes = text_to_textnodes(text)
        self.assertListEqual([TextNode(text, TextType.TEXT)], nodes)

    def test_text_to_textnodes_only_delimiters(self):
        text = "**_`[text](url)`_**"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode(
                    "_`[text](url)`_",
                    TextType.BOLD,
                ),
            ],
            nodes,
        )

    def test_text_to_textnodes_multiple_images_and_links(self):
        text = "![img1](url1)![img2](url2)[link1](url1)[link2](url2)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("img1", TextType.IMAGE, "url1"),
                TextNode("img2", TextType.IMAGE, "url2"),
                TextNode("link1", TextType.LINK, "url1"),
                TextNode("link2", TextType.LINK, "url2"),
            ],
            nodes,
        )

    def test_text_to_textnodes_mixed_nested(self):
        text = "**Bold _italic `code`_**"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Bold _italic `code`_", TextType.BOLD),
            ],
            nodes,
        )



class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# Heading 1

## Heading 2 with **bold**

### Heading _3_ with italic
"""
        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2 with <b>bold</b></h2><h3>Heading <i>3</i> with italic</h3></div>",
        )

    def test_quotes(self):
        md = """
> This is a quote
> with multiple lines
> and **bold** text

> Another quote with
> _italic_ text
"""
        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><quote>This is a quote with multiple lines and <b>bold</b> text</quote><quote>Another quote with <i>italic</i> text</quote></div>",
        )

    def test_unordered_lists(self):
        md = """
- First item with **bold**
- Second item with _italic_
- Third item with `code`
"""
        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item with <b>bold</b></li><li>Second item with <i>italic</i></li><li>Third item with <code>code</code></li></ul></div>",
        )

    def test_ordered_lists(self):
        md = """
1. First item with **bold**
2. Second item with _italic_
3. Third item with `code`
"""
        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item with <b>bold</b></li><li>Second item with <i>italic</i></li><li>Third item with <code>code</code></li></ol></div>",
        )

    def test_mixed_content(self):
        self.maxDiff = None
        md = """
# Main Heading

This is a paragraph with **bold** and _italic_ text.

```
def hello():
    print("world")
```

> A quote with `code`
> and multiple lines

1. First ordered item
2. Second ordered item

- Unordered item 1
- Unordered item 2
"""
        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Main Heading</h1><p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p><pre><code>def hello():\n    print(\"world\")\n</code></pre><quote>A quote with <code>code</code> and multiple lines</quote><ol><li>First ordered item</li><li>Second ordered item</li></ol><ul><li>Unordered item 1</li><li>Unordered item 2</li></ul></div>",
        )


if __name__ == "__main__":
    unittest.main() 