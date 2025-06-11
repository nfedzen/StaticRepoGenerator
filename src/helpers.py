from textnode import TextNode, TextType

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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node) 
            continue
        if node.text.count(delimiter) % 2 == 1:
            raise Exception(f"Invalid MarkdownL missing closing {delimiter}")
        list_of_strings = node.text.split(delimiter)
        for string in list_of_strings:
            if list_of_strings.index(string) % 2 == 0:
                new_node = TextNode(string, TextType.TEXT)
                new_nodes.append(new_node)
            else:
                new_node = TextNode(string, type_to_delim(delimiter))
                new_nodes.append(new_node)
    print(new_nodes)
    return new_nodes
