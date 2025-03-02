class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children = None, props: map = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):

        if self.props is None:
            return ""
        
        return " ".join(f'{key}="{value}"' for key, value in self.props.items())
        
        
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag , value, None, props)
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        
    
    def to_html(self):
        if self.tag == None:
            return self.value
        else:
            props_str = self.props_to_html()
            return f"<{self.tag}{' ' + props_str if props_str else ''}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag = None, children = [], props = {}):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("no tag")
        elif self.children is None:
            raise ValueError("no childrens")
        
        result = ""
        
        for node in self.children:
            result += node.to_html()
                
        props_str = self.props_to_html()
        return f"<{self.tag}{' ' + props_str if props_str else ''}>{result}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
