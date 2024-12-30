import unittest
from main import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_paragraph(self):
        # Arrange
        markdown = """# Tolkien Fan Club

**I like Tolkien**. Read my [first post here](/majesty) (sorry the link doesn't work yet)

> All that is gold does not glitter """
        solution = "Tolkien Fan Club"
        # Act
        result = extract_title(markdown)
        # Assert
        self.assertEqual(result, solution)

    
    def test_no_title_exception(self):
        # Arrange
        markdown = "Tolkien Fan Club"
        # Act and Assert
        with self.assertRaises(SyntaxError) as context_manager:
            extract_title(markdown)
        self.assertEqual(str(context_manager.exception), "Document must start with a title")

    
    def test_whitespace_before_title_exception(self):
        # Arrange
        markdown = "    # Valid title with spaces before"
        # Act and Assert
        with self.assertRaises(SyntaxError) as context_manager:
            extract_title(markdown)
        self.assertEqual(str(context_manager.exception), "Document cannot have spaces before title")