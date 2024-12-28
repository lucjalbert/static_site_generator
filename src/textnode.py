import re
from enum import Enum
from htmlnode import LeafNode


# Enum for different text types
class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


# Class used to store markdown information in nodes
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


# Create an HTML leaf node based on an object's TextType property
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
        

# Create TextNode objects out of raw text with markdown delimiters
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    # Iterate over all nodes in the list of old nodes
    for old_node in old_nodes:

        # If a node is not of type text, immediately append and move on. This program does not support nested markdown syntax
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Create a list for current iteration nodes and another for sections between the markdown symbol
        split_nodes = []
        sections = old_node.text.split(delimiter)
        # If the length of text sections when split on delimiter is even, that means there is an odd amount of delimiters. Invalid markdown syntax
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        
        # Now we iterate over each text section
        for i in range(len(sections)):
            
            # If the delimiter is on the very start or end, split can create empty list elements. Ignore those and move on
            if sections[i] == "":
                continue
            
            # Even index means it is raw text, even if the delimiter is first it will create an empty element making the text within delimiter's index odd
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        
        # Add current iteration nodes and continue looping over nodes
        new_nodes.extend(split_nodes)
    return new_nodes


# Same as split_nodes_delimiter except for images 
def split_nodes_image(old_nodes):
    new_nodes = []
    
    # Loop over all nodes in the list of old nodes
    for old_node in old_nodes:
        
        # If a node's type is not raw Text, move on. This program does not support nested markdown syntax
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue       
        
        old_node_text_copy = old_node.text
        # Use Regex to store all images in an (alt_text, url) list of tuples
        images = extract_markdown_images(old_node_text_copy)
        
        if not images:
            new_nodes.append(old_node)
            continue

        for image in images:

            # Recreate the original image markdown syntax from Regex results
            markdown_link = f"![{image[0]}]({image[1]})"
            
            # Split original text using full image as delimiter and save the first element of the list, giving us the text before the image
            text_before = old_node_text_copy.split(markdown_link, 1)[0]

            # Create TextNodes based on the data acquired, text_before could be empty if image is first because that would create an empty first list element when splitting
            if text_before:
                new_nodes.append(TextNode(text_before, TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))

            # Slice the Node's text to exclude processed text
            used_text_len = len(text_before) + len(markdown_link)
            old_node_text_copy = old_node_text_copy[used_text_len:]
        
        # Make sure there isn't any text left after the last image
        if old_node_text_copy:       
            new_nodes.append(TextNode(old_node_text_copy, TextType.TEXT))

    return new_nodes



# See split_nodes_image for proper breakdown
def split_nodes_link(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        old_node_text_copy = old_node.text
        links = extract_markdown_links(old_node_text_copy)
        if not links:
            new_nodes.append(old_node)
            continue        
        for link in links:
            markdown_link = f"[{link[0]}]({link[1]})"
            text_before = old_node_text_copy.split(markdown_link)[0]

            if text_before:
                new_nodes.append(TextNode(text_before, TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

            used_text_len = len(text_before) + len(markdown_link)
            old_node_text_copy = old_node_text_copy[used_text_len:]
        
        if old_node_text_copy:
        
            new_nodes.append(TextNode(old_node_text_copy, TextType.TEXT))
    return new_nodes


# Regex functions that return a list of tuples containing user input for images and links
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


# Use all split functions to translate a full string of markdown to a list of TextNode objects
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes