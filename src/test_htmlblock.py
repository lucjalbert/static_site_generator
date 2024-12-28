import unittest
from htmlblock import markdown_to_html_node


class TestHTMLBlock(unittest.TestCase):
    def test_paragraph(self):
        # Arrange
        md = """
This is **bolded** paragraph
text in a p
tag here

"""
        solution = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>"
        # Act
        result = markdown_to_html_node(md)
        # Assert
        self.assertEqual(solution, result)

    
    def test_paragraphs(self):
        # Arrange
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""
        solution = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        # Act
        result = markdown_to_html_node(md)
        # Assert
        self.assertEqual(solution, result)


    def test_lists(self):
        # Arrange
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""
        solution = "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>"
        # Act
        result = markdown_to_html_node(md)
        # Assert
        self.assertEqual(solution, result)


    def test_headings(self):
        # Arrange
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""
        solution = "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>"
        # Act
        result = markdown_to_html_node(md)
        # Assert
        self.assertEqual(solution, result)


    def test_blockquotes(self):
        # Arrange
        md = """
> This is a
> blockquote block

this is paragraph text

"""
        solution = "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>"
        # Act
        result = markdown_to_html_node(md)
        # Assert
        self.assertEqual(solution, result)