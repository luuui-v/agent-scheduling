import os
import markdown
import json
from datetime import datetime

def parse_front_matter(content):
    """Parse the front matter from a markdown content string."""
    front_matter = {}
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) > 2:
            front_matter_content = parts[1]
            body_content = parts[2]
            for line in front_matter_content.splitlines():
                if ": " in line:
                    key, value = line.split(": ", 1)
                    front_matter[key.strip()] = value.strip()
            return front_matter, body_content
    return front_matter, content

def convert_markdown_to_html(input_dir, output_filepath):
    if not os.path.exists(input_dir):
        print(f"Directory {input_dir} does not exist. Creating an empty HTML file.")
        with open(output_filepath, 'w', encoding='utf-8') as output_file:
            output_file.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Combined Blog Posts</title>
    <nav><a href="../index.html" alt="Home Button to main page"><button>Go Back</button></a></nav>
    <style>
        body { background-color: #fbfbff; font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }
        h1 { text-align: center; color: #040f16; }
        .post { margin-bottom: 40px; }
    </style>
</head>
<body>
    <h1>All Blog Posts</h1>
    <p>No posts available.</p>
</body>
</html>
            """)
        print("Created an empty HTML file.")
        return

    posts = []
    for md_filename in os.listdir(input_dir):
        if md_filename.endswith('.md'):
            md_filepath = os.path.join(input_dir, md_filename)
            with open(md_filepath, 'r', encoding='utf-8') as md_file:
                md_content = md_file.read()

            front_matter, body_content = parse_front_matter(md_content)
            html_content = markdown.markdown(body_content)
            post = {
                'title': front_matter.get("title", md_filename),
                'thumbnail': front_matter.get("thumbnail"),
                'content': html_content,
                'date': md_filename[:10]  # Convert datetime to string
            }
            posts.append(post)

    # Sort posts by date
    posts.sort(key=lambda x: x['date'], reverse=True)

    html_header = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Combined Blog Posts</title>
    <nav><a href="../index.html" alt="Home Button to main page"><button>Go Back</button></a></nav>
    <style>
        body {
            background-color: #f6f6f6;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 40px;
            font-size: 36px;
            text-transform: uppercase;
        }
        .container {
            display: flex;
            justify-content: space-between;
            width: 100%;
            max-width: 1200px;
            height: calc(100vh - 80px);
        }
        .post-list {
            flex-basis: 30%;
            max-width: 300px;
            overflow-y: auto;
        }
        .post-list-item {
            margin-bottom: 20px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            padding: 10px;
            border-radius: 5px;
   
