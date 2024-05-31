import os
import markdown

def convert_markdown_to_html(input_dir, output_filepath):
    html_parts = []
    for md_filename in os.listdir(input_dir):
        if md_filename.endswith('.md'):
            md_filepath = os.path.join(input_dir, md_filename)
            with open(md_filepath, 'r', encoding='utf-8') as md_file:
                md_content = md_file.read()
            html_content = markdown.markdown(md_content)
            post_header = f'<h2>{md_filename}</h2>'
            html_parts.append(post_header)
            html_parts.append(f'<div class="post">{html_content}</div>')

    html_header = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Combined Blog Posts</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }
        h1 { text-align: center; }
        h2 { border-bottom: 1px solid #ccc; padding-bottom: 5px; }
        .post { margin-bottom: 40px; }
    </style>
</head>
<body>
    <h1>All Blog Posts</h1>
"""
    html_footer = """
</body>
</html>
"""

    full_html_content = html_header + '\n'.join(html_parts) + html_footer

    with open(output_filepath, 'w', encoding='utf-8') as output_file:
        output_file.write(full_html_content)

    print("Markdown files have been converted and combined into a single HTML file successfully!")

if __name__ == "__main__":
    input_dir = os.path.join(os.path.dirname(__file__), '..', '_posts')
    output_filepath = os.path.join(os.path.dirname(__file__), '..', 'combined_blog.html')

    print(f"Input directory: {input_dir}")
    print(f"Output file: {output_filepath}")

    print("Starting conversion process...")
    convert_markdown_to_html(input_dir, output_filepath)
    print("Conversion process finished.")
