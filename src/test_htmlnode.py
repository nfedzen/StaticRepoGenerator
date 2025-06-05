import unittest
import io
import contextlib

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_print(self):
        node = HTMLNode("tag", "value", "children", {"href": "https://www.google.com", "target": "_blank"})
        
        result = "HTMLNode(tag, value, children: children, {'href': 'https://www.google.com', 'target': '_blank'})\n"
        
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            print(node)
            actual_output = buf.getvalue()

            self.assertEqual(actual_output, result)
    
    def test_props_to_html(self):
        node = HTMLNode("tag", "value", "children", {"href": "https://www.google.com", "target": "_blank"})
        expected_result = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(node.props_to_html(), expected_result)
    
    def test_init(self):
        node = HTMLNode("tag", "value", "children", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.tag, "tag")
        self.assertEqual(node.value, "value")
        self.assertEqual(node.children, "children")
        self.assertEqual(node.props, {"href": "https://www.google.com", "target": "_blank"})

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

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

    def test_to_html_with_greatgrandchildren(self):
        greatgrandchild_node = LeafNode("b", "greatgrandchild")
        grandchild_node = ParentNode("p", [greatgrandchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><p><b>greatgrandchild</b></p></span></div>",
        )





        


if __name__ == "__main__":
    unittest.main()