from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


# split full markdown documents into blocks
def markdown_to_blocks(markdown):
    markdown_blocks = []
    markdown_lines = markdown.split("\n")
    current_block = ""

    for line in markdown_lines:
        # remove all whitespace and trailing newline of each line
        stripped_line = line.strip()
        # If the stripped line has content, it is saved in the current block
        if stripped_line:
            if current_block:
                current_block += ("\n" + stripped_line)
            else:
                current_block += stripped_line
        # If the stripped line is empty and the current block has content, it's the end of the block and it can be added.
        # If the block does not have content, it's an empty line to be skipped
        else:
            if current_block:
                markdown_blocks.append(current_block)
            current_block = ""
    # Since the loop cannot update the current block and add it to the list in one iteration, it's possible a block is not added during the last iteration of the loop
    if current_block:
        markdown_blocks.append(current_block)
    return markdown_blocks


def block_to_block_type(block):
    block_words = block.split()
    block_lines = block.split("\n")
    
    if (len(block_words[0]) in range(1, 7)) and (set(block_words[0]) == {"#"}):
        return BlockType.HEADING
    
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    is_quote = list(filter(lambda line: line.startswith(">"), block_lines))
    if len(is_quote) == len(block_lines):
        return BlockType.QUOTE
    
    is_unordered_list = list(filter(lambda line: line.startswith("* ") or line.startswith("- "), block_lines))
    if len(is_unordered_list) == len(block_lines):
        return BlockType.UNORDERED_LIST
    
    if all(line.startswith(f"{i + 1}. ") for i, line in enumerate(block_lines)):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH