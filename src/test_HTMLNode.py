import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("p", "Hello", None, {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.props_to_html(), 'href="https://www.google.com" target="_blank"' )
    
    def test_values(self):
        node = HTMLNode("p", "Hello", None, {"href": "https://www.google.com", "target": "_blank",})

        self.assertEqual(node.tag, 'p')
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"href": "https://www.google.com", "target": "_blank",})

    def test_repr(self):
        node = HTMLNode("p", "Hello", None, {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.__repr__(), "HTMLNode(p, Hello, None, {'href': 'https://www.google.com', 'target': '_blank'})")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')   

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text.")
        self.assertEqual(node.to_html(), "Just text.")

    def test_leaf_to_html_raises_error(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None) 
    
    def test_Leaf_repr(self):
        node = LeafNode("p", "Hello", {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.__repr__(), "LeafNode(p, Hello, {'href': 'https://www.google.com', 'target': '_blank'})")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_empty_parent(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_multiple_children(self):
        child1 = LeafNode("span", "child1")
        child2 = LeafNode("b", "child2")
        parent_node = ParentNode("div", [child1, child2])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><b>child2</b></div>")
    
    def test_to_html_with_attributes(self):
        child = LeafNode("p", "text")
        parent_node = ParentNode("section", [child], {"class": "content", "id": "main"})
        self.assertEqual(parent_node.to_html(), '<section class="content" id="main"><p>text</p></section>')
    
    def test_to_html_deep_nesting(self):
        deep_child = LeafNode("strong", "deep text")
        child = ParentNode("span", [deep_child])
        parent = ParentNode("div", [child])
        wrapper = ParentNode("section", [parent])
        self.assertEqual(wrapper.to_html(), "<section><div><span><strong>deep text</strong></span></div></section>")
    
    def test_to_html_mixed_content(self):
        text_node = LeafNode(None, "Some text")
        child = LeafNode("em", "italic text")
        parent_node = ParentNode("p", [text_node, child])
        self.assertEqual(parent_node.to_html(), "<p>Some text<em>italic text</em></p>")




    
    
 

    
    
if __name__ == "__main__":
    unittest.main()
    