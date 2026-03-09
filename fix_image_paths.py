import re

# Read the file
with open('templates/pages/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace {% static 'filename.jpg' %} with {% static 'images/filename.jpg' %}
def fix_static_path(match):
    filename = match.group(1)
    # Skip if already has 'images/' prefix
    if filename.startswith('images/'):
        return "{% static '" + filename + "' %}"
    return "{% static 'images/" + filename + "' %}"

pattern = r"\{% static '([^']+)' %\}"
content = re.sub(pattern, fix_static_path, content)

# Write back
with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Added images/ prefix to all static image paths')
print('✅ File updated successfully')
