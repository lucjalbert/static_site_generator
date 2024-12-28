import unittest

from blocks_markdown import markdown_to_blocks, block_to_block_type, BlockType


class TestBlocksMarkdown(unittest.TestCase):
    def test_newlines(self):
        markdown =     """# This is a heading

    This is a paragraph of text. It has some **bold** and *italic* words inside of it.

    

    * This is the first list item in a list block
    * This is a list item
    * This is another list item
    
    
    
    """
        result = markdown_to_blocks(markdown)
        solution = ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\n* This is a list item\n* This is another list item']
        self.assertEqual(result, solution)

    def test_single_block(self):
        markdown = "this is a single block of text in a markdown file"
        result = markdown_to_blocks(markdown)
        solution = ['this is a single block of text in a markdown file']
        self.assertEqual(result, solution)


    def test_markdown_to_blocks_heading(self):
        # Arrange
        block = """#### this block is 
a heading"""
        solution = BlockType.HEADING

        # Act
        result = block_to_block_type(block)

        # Assert
        self.assertEqual(result, solution)

    
    def test_markdown_to_blocks_code(self):
        # Arrange
        block = """```this block is 
a code block```"""
        solution = BlockType.CODE

        # Act
        result = block_to_block_type(block)

        # Assert
        self.assertEqual(result, solution)

    
    def test_markdown_to_blocks_quote(self):
        # Arrange
        block = """> this block is 
> a quote"""
        solution = BlockType.QUOTE

        # Act
        result = block_to_block_type(block)

        # Assert
        self.assertEqual(result, solution)


    def test_markdown_to_blocks_unordered_list(self):
        # Arrange
        block = """* this block is 
* an unordered list"""
        block_2 = """- this block is 
- another unordered list"""
        solution = BlockType.UNORDERED_LIST

        # Act
        result = block_to_block_type(block)
        result_2 = block_to_block_type(block_2)

        # Assert
        self.assertEqual(result, solution)
        self.assertEqual(result_2, solution)


    def test_markdown_to_blocks_ordered_list(self):
        # Arrange
        block = """1. this block is 
2. an ordered list.
3. it is quite long
4. indeed"""
        solution = BlockType.ORDERED_LIST

        # Act
        result = block_to_block_type(block)

        # Assert
        self.assertEqual(result, solution)


    def test_markdown_to_blocks_paragraph(self):
        # Arrange
        block = """this block is 
a normal
paragraph"""
        solution = BlockType.PARAGRAPH

        # Act
        result = block_to_block_type(block)

        # Assert
        self.assertEqual(result, solution)






class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()