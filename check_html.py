import glob
from html.parser import HTMLParser

class TagChecker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.void_tags = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
        
    def handle_starttag(self, tag, attrs):
        if tag not in self.void_tags:
            self.stack.append((tag, self.getpos()))
            
    def handle_endtag(self, tag):
        if tag in self.void_tags:
            return
        if not self.stack:
            print(f"Error: Encountered closing tag </{tag}> without an open tag at line {self.getpos()[0]}.")
            return
        last_tag, pos = self.stack.pop()
        if last_tag != tag:
            print(f"Mismatch Error: Expected </{last_tag}> (opened at {pos[0]}), but got </{tag}> at line {self.getpos()[0]}.")
            self.stack.append((last_tag, pos)) # Put it back to trace the rest roughly

checker = TagChecker()
content = open(r'd:\Projects\render.html', encoding='utf-8', errors='ignore').read()
# Note: Since Django tags look like {% %}, HTML parser ignores them mostly, but let's just run it
checker.feed(content)
print(f"Unclosed tags remaining: {checker.stack}")
