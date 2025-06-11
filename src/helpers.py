from textnode import TextNode, TextType
import re


def type_to_delim(delimiter):
    match delimiter:
        case "**":
            return TextType.BOLD
        case "_":
            return TextType.ITALIC
        case "`":
            return TextType.CODE
        case _:
            raise Exception("Invalid Delimiter")

# def split_nodes_delimiter(old_nodes, delimiter, text_type):
#     new_nodes = []
#     for node in old_nodes:
#         if node.text_type != TextType.TEXT:
#             new_nodes.append(node) 
#             continue
#         if node.text.count(delimiter) % 2 == 1:
#             raise Exception(f"Invalid Markdown missing closing {delimiter}")
#         list_of_strings = node.text.split(delimiter)
#         for string in list_of_strings:
#             if list_of_strings.index(string) % 2 == 0:
#                 new_node = TextNode(string, TextType.TEXT)
#                 new_nodes.append(new_node)
#             else:
#                 new_node = TextNode(string, type_to_delim(delimiter))
#                 new_nodes.append(new_node)
#     return new_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    found = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return found

def extract_markdown_links(text):
    found = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return found 

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    node_list = []
    node_list = split_nodes_link([node])
    node_list = split_nodes_image(node_list)
    node_list = split_nodes_delimiter(node_list, "`", TextType.CODE)
    node_list = split_nodes_delimiter(node_list, "_", TextType.ITALIC)
    node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)
    return node_list
