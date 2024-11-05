import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("Text here", TextType.LINK, "here is a url")
        node2 = TextNode("Text here", TextType.LINK, "here is a url")
        self.assertEqual(node, node2)
    
    def test_eq_failure(self):
        node = TextNode("Text here", TextType.LINK, "here is a url")
        node2 = TextNode("Different text here", TextType.LINK, "here is a url")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()