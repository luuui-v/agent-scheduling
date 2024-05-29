import os
import time
import markdown
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MarkdownHandler(FileSystemEventHandler):
    def __init__(self, input_dir, output_filepath):
        self.input_dir = input_dir
        self.output_filepath = output_filepath

    def on_modified(self, event):
        print(f"Modified: {event.src_path}")
        if event.src_path.endswith('.md'):
            self.convert_markdown_to_html()

    def on_created(self, event):
        print(f"Created: {event.src_path}")
        if event.src_path.endswith('.md'):
            self.convert_markdown_to_html()

    def convert_markdown_to_html(self):
        html_parts = []
        for md_filename in os.listdir(self.input_dir):
            if md_filename.endswith('.md'):
                md_filepath = os.path.join(self.input_dir, md_filename)
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

        with open(self.output_filepath, 'w', encoding='utf-8') as output_file:
            output_file.write(full_html_content)

        print("Markdown files have been converted and combined into a single HTML file successfully!")

def watch_directory(input_dir, output_filepath):
    event_handler = MarkdownHandler(input_dir, output_filepath)
    observer = Observer()
    observer.schedule(event_handler, path=input_dir, recursive=False)
    observer.start()
    print(f"Started watching directory: {input_dir}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    input_dir = '_posts'
    output_filepath = 'combined_blog.html'
    watch_directory(input_dir, output_filepath)
