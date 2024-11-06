import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank",})
        expected_result = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(node.props_to_html(), expected_result)

    def test_props_to_html_none(self):
        node = HTMLNode(props=None)
        expected_result = ""
        self.assertEqual(node.props_to_html(), expected_result)
    
    def test_props_to_html_empty(self):
        node = HTMLNode(props={})
        expected_result = ""
        self.assertEqual(node.props_to_html(), expected_result)

    def test_props_to_html_quotes(self):
        node = HTMLNode(props={"title": "Bob's page"})
        expected_result = " title=\"Bob's page\""
        self.assertEqual(node.props_to_html(), expected_result)
    
    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

class TestLeafNode(unittest.TestCase):
    def test_leaf_values(self):
        leaf_node = LeafNode("h1", "Here is a value")


        self.assertEqual(leaf_node.tag, "h1")

        self.assertEqual(leaf_node.value, "Here is a value")

        self.assertEqual(leaf_node.props, None)

    def test_to_html(self):
        leaf_node = LeafNode("p", "This is a paragraph of text.")
        leaf_node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(leaf_node.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(leaf_node2.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

        leaf_node_tagless = LeafNode(None, "This should print by itself")
        self.assertEqual(leaf_node_tagless.to_html(), "This should print by itself")

        with self.assertRaises(ValueError):
            leaf_node_valueless = LeafNode("h1", None)
            leaf_node_valueless.to_html()
        
        leaf_node_multiprops = LeafNode("a", "Click me!", {"href": "https://www.google.com", "class": "link-button", "id": "main-link"})
        self.assertEqual(leaf_node_multiprops.to_html(), "<a href=\"https://www.google.com\" class=\"link-button\" id=\"main-link\">Click me!</a>")

class TestParentNode(unittest.TestCase):
    def test_parent_values(self):
        with self.assertRaises(ValueError):
            parent_node = ParentNode(None, "h1")
            parent_node.to_html()

        with self.assertRaises(ValueError):
            parent_node = ParentNode(LeafNode(None, "Text"), None)
            parent_node.to_html()

        with self.assertRaises(ValueError):
            parent_node = ParentNode(LeafNode(None, "Text"), "")
            parent_node.to_html()

if __name__ == "__main__":
    unittest.main()