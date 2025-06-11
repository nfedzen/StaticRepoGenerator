import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from helpers import type_to_delim, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image, text_to_textnodes


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
        self.assertEqual(new_node[0].text, "We")
        self.assertEqual(new_node[0].text_type, TextType.BOLD)
        self.assertEqual(new_node[1].text, " are testing markdown today")
        self.assertEqual(new_node[1].text_type, TextType.TEXT)

    def test_one_delim_end(self):
        node3 = TextNode("We are testing markdown **today**", TextType.TEXT)
        new_node = split_nodes_delimiter([node3], "**", TextType.BOLD)
        self.assertEqual(new_node[0].text, "We are testing markdown ")
        self.assertEqual(new_node[0].text_type, TextType.TEXT)
        self.assertEqual(new_node[1].text, "today")
        self.assertEqual(new_node[1].text_type, TextType.BOLD)
    
    def test_two_delim_middle(self):
        node3 = TextNode("We are _testing_ _markdown_ today", TextType.TEXT)
        new_node = split_nodes_delimiter([node3], "_", TextType.ITALIC)
        self.assertEqual(new_node[0].text, "We are ")
        self.assertEqual(new_node[0].text_type, TextType.TEXT)
        self.assertEqual(new_node[1].text, "testing")
        self.assertEqual(new_node[1].text_type, TextType.ITALIC)
        self.assertEqual(new_node[2].text, " ")
        self.assertEqual(new_node[2].text_type, TextType.TEXT)
        self.assertEqual(new_node[3].text, "markdown")
        self.assertEqual(new_node[3].text_type, TextType.ITALIC)
        self.assertEqual(new_node[4].text, " today")
        self.assertEqual(new_node[4].text_type, TextType.TEXT)

    def test_not_wrapped_delim(self):
        node3 = TextNode("We are _testing markdown today", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            new_node = split_nodes_delimiter([node3], "_", TextType.BOLD)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
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

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        node_list = text_to_textnodes(text)
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
            node_list,
        )

if __name__ == "__main__":
    unittest.main()