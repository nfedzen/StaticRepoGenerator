import unittest
import io
import contextlib

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_print(self):
        node = HTMLNode("tag", "value", "children", {"href": "https://www.google.com", "target": "_blank"})
        
        result = "HTMLNode(tag, value, children, {'href': 'https://www.google.com', 'target': '_blank'})\n"
        
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            print(node)
            actual_output = buf.getvalue()

            self.assertEqual(actual_output, result)
    
    def test_props_to_html(self):
        node = HTMLNode("tag", "value", "children", {"href": "https://www.google.com", "target": "_blank"})
        expected_result = " href=https://www.google.com target=_blank"
        self.assertEqual(node.props_to_html(), expected_result)
    
    def test_init(self):
        node = HTMLNode("tag", "value", "children", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.tag, "tag")
        self.assertEqual(node.value, "value")
        self.assertEqual(node.children, "children")
        self.assertEqual(node.props, {"href": "https://www.google.com", "target": "_blank"})

#Testing commit





        


if __name__ == "__main__":
    unittest.main()