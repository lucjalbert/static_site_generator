from functools import reduce

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        attribute_acc = ""

        if self.props is None:
            return attribute_acc
        
        for attribute, content in self.props.items():
            attribute_acc += f" {attribute}=\"{content}\""
        return attribute_acc

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf node must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"Leafnode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, children, tag=None, props=None):
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent node must have a tag")
        if not self.children:
            raise ValueError("Parent node must have at least one child")
        
        html_acc = ""
        for child in self.children:
            if isinstance(child, LeafNode):
                html_acc += child.to_html()
            
            elif isinstance(child, ParentNode):
                html_acc += child.to_html()
        
        return f"<{self.tag}>{html_acc}</{self.tag}>"
