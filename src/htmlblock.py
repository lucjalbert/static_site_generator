from blocks_markdown import markdown_to_blocks, block_to_block_type
from htmlnode import HTMLNode
from blocks_markdown import BlockType
from textnode import text_to_textnodes, text_node_to_html_node

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    div_node_children = []

    for block in markdown_blocks:
        block_type= block_to_block_type(block)
        
        tag = block_type_to_html_tag(block, block_type)
        value = get_block_content(block, block_type)

        # Lists require every children to also be wrapped in li nodes
        if block_type in [BlockType.ORDERED_LIST, BlockType.UNORDERED_LIST]:
            lines = value.split("\n")
            list_nodes = []
            for line in lines:
                list_node_children = text_to_children(line)
                html_node = HTMLNode("li", None, list_node_children)
                list_nodes.append(html_node)
            children = list_nodes
        else:
            children = text_to_children(value)
        
        props = get_block_props(block)

        # Code blocks require nested pre/code tags which can't be handled by the standard HTMLNode method
        if block_type == BlockType.CODE:
            html_block = HTMLNode("pre", None, [
                HTMLNode("code", value, children, props)
                ], None)
            div_node_children.append(html_block)
            continue

        html_block = HTMLNode(tag, value, children, props)
        div_node_children.append(html_block)
    
    div_node = HTMLNode("div", None, div_node_children, None)
    return div_node



def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = [text_node_to_html_node(text_node) for text_node in text_nodes]
    return children


def block_type_to_html_tag(block, block_type):
    match block_type:
        case BlockType.HEADING:
            return f"h{get_heading_number(block)}"
        case BlockType.CODE:
            return None
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"
        case BlockType.PARAGRAPH:
            return "p"


def get_block_content(block, block_type):
    match block_type:
        case BlockType.HEADING:
            return block.lstrip("#").strip()
        case BlockType.CODE:
            return block.strip("`")
        case BlockType.QUOTE:
            return quote_strip(block)
        case BlockType.UNORDERED_LIST:
            return ulist_strip(block)
        case BlockType.ORDERED_LIST:
            return olist_strip(block)
        case BlockType.PARAGRAPH:
            return block

def quote_strip(block):
    lines = block.split("\n")
    stripped_lines = [line.lstrip("> ") for line in lines]
    return "\n".join(stripped_lines)

def ulist_strip(block):
    lines = block.split("\n")
    stripped_lines = [line.lstrip("* ").lstrip("- ") for line in lines]
    return "\n".join(stripped_lines)

def olist_strip(block):
    lines = block.split("\n")
    stripped_lines = [lines[i].lstrip(f"{i + 1}. ") for i in range(0, len(lines))]
    return "\n".join(stripped_lines)


def get_block_props(block):
    pass


def get_heading_number(block):
    split_block = block.split()
    return len(split_block[0])