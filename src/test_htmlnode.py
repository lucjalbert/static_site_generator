import unittest

from htmlnode import HTMLNode


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

if __name__ == "__main__":
    unittest.main()