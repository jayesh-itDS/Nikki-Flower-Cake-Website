import re

# Read the file
with open('templates/pages/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace {{ STATIC_URL }}images/... with {% static 'images/...' %}
def replace_static(match):
    image_path = match.group(1)
    return "{% static '" + image_path + "' %}"

pattern = r'\{\{ STATIC_URL \}\}images/([^\s"\'>]+)'
content = re.sub(pattern, replace_static, content)

# Write back
with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Replaced all {{ STATIC_URL }}images/... with {% static \'images/...\' %}')
print('✅ File updated successfully')
