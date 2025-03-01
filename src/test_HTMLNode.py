import unittest

from htmlnode import HTMLNode

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
    
    
if __name__ == "__main__":
    unittest.main()
    