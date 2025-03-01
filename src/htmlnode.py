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
        
        propy = ""
        for prop in self.props:
            if propy == "":
                propy += f'{prop}="{self.props[prop]}"'
            else:
                propy = f'{propy} {prop}="{self.props[prop]}"'

        return propy
        
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"