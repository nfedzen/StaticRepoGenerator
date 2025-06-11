import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from helpers import type_to_delim, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is Italic", TextType.ITALIC)
        node2 = TextNode("This is Bold", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_none(self):
        node = TextNode("No Url", TextType.LINK)
        self.assertEqual(node.url, None)
        
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.to_html(), "<b>This is a text node</b>")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.to_html(), "<i>This is a text node</i>")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.to_html(), "<code>This is a text node</code>")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.to_html(), "<a href=\"www.google.com\">This is a text node</a>")

    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.to_html(), "<img src=\"www.google.com\" alt=\"This is a text node\"></img>")
    
    def test_one_delim_middle(self):
        node = TextNode("We are testing **markdown** today", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_node[0].text, "We are testing ")
        self.assertEqual(new_node[0].text_type, TextType.TEXT)
        self.assertEqual(new_node[1].text, "markdown")
        self.assertEqual(new_node[1].text_type, TextType.BOLD)
        self.assertEqual(new_node[2].text, " today")
        self.assertEqual(new_node[2].text_type, TextType.TEXT)
   
    def test_one_delim_start(self):
        node2 = TextNode("**We** are testing markdown today", TextType.TEXT)
        new_node = split_nodes_delimiter([node2], "**", TextType.BOLD)
        self.assertEqual(new_node[0].text, "")
        self.assertEqual(new_node[0].text_type, TextType.TEXT)
        self.assertEqual(new_node[1].text, "We")
        self.assertEqual(new_node[1].text_type, TextType.BOLD)
        self.assertEqual(new_node[2].text, " are testing markdown today")
        self.assertEqual(new_node[2].text_type, TextType.TEXT)

    def test_one_delim_end(self):
        node3 = TextNode("We are testing markdown **today**", TextType.TEXT)
        new_node = split_nodes_delimiter([node3], "**", TextType.BOLD)
        self.assertEqual(new_node[0].text, "We are testing markdown ")
        self.assertEqual(new_node[0].text_type, TextType.TEXT)
        self.assertEqual(new_node[1].text, "today")
        self.assertEqual(new_node[1].text_type, TextType.BOLD)
        self.assertEqual(new_node[2].text, "")
        self.assertEqual(new_node[2].text_type, TextType.TEXT)

if __name__ == "__main__":
    unittest.main()