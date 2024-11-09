from enum import Enum
from functools import reduce
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href" : text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src" : text_node.url, "alt" : text_node.text})
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")
        

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    def create_inline_node(acc, current_text):
        inline_nodes, inside_delimiter = acc
        inline_nodes.append(TextNode(
            current_text,
            text_type if inside_delimiter else TextType.TEXT
        ))
        return inline_nodes, not inside_delimiter
    
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_text = old_node.text.split(delimiter)

        if len(split_text) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")

        inside_delimiter = False
        if old_node.text[:len(delimiter)] == delimiter:
            del split_text[0]
            inside_delimiter = True
        if old_node.text[-len(delimiter):] == delimiter:
            del split_text[-1]

        inline_nodes, _ = reduce(create_inline_node, split_text, ([], inside_delimiter))
        new_nodes.extend(inline_nodes)

    return new_nodes