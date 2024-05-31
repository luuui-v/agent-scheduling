import os
import markdown
import re

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

    html_parts = []
    for md_filename in os.listdir(input_dir):
        if md_filename.endswith('.md'):
            md_filepath = os.path.join(input_dir, md_filename)
            with open(md_filepath, 'r', encoding='utf-8') as md_file:
                md_content = md_file.read()

            front_matter, body_content = parse_front_matter(md_content)
            html_content = markdown.markdown(body_content)

            post_header = f'<h2>{front_matter.get("title", md_filename)}</h2>'
            if 'thumbnail' in front_matter:
                post_header += f'<img class="thumbnail" src="{front_matter["thumbnail"]}" alt="{front_matter.get("title", "thumbnail")}">'
            
            html_parts.append(post_header)
            html_parts.append(f'<div class="post">{html_content}</div>')

    html_header = """
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
        h2 { border-bottom: 1px solid #ccc; padding-bottom: 5px; color: #0b4f6c; }
        .thumbnail { width: 100px; height: auto; }
        .post { margin-bottom: 40px; }
    </style>
</head>
<body>
    <h1>All Blog Posts</h1>
    <div class="container">
        <div class="post-list">
            <!-- Post list will be dynamically inserted here -->
        </div>
        <div class="post-content">
            <!-- Full post view will be dynamically inserted here -->
        </div>
    </div>

    <script>
        // JavaScript for handling click events on post list items
        document.addEventListener("DOMContentLoaded", function() {
            const postList = document.querySelector(".post-list");
            const postContent = document.querySelector(".post-content");

            // Sample data for demonstration
            const posts = [
                { title: "Post 1", content: "Content of post 1" },
                { title: "Post 2", content: "Content of post 2" },
                { title: "Post 3", content: "Content of post 3" }
            ];

            // Function to display full post content when a list item is clicked
            function showFullPost(post) {
                postContent.innerHTML = `
                    <h2>${post.title}</h2>
                    <p>${post.content}</p>
                `;
            }

            // Function to render post list
            function renderPostList() {
                postList.innerHTML = "";
                posts.forEach((post, index) => {
                    const listItem = document.createElement("div");
                    listItem.classList.add("post-list-item");
                    listItem.textContent = post.title;
                    listItem.addEventListener("click", () => showFullPost(post));
                    postList.appendChild(listItem);
                });
            }

            // Render post list when the page loads
            renderPostList();
        });
    </script>





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
    input_dir = os.path.join(os.path.dirname(__file__), '../_posts')
    output_filepath = os.path.join(os.path.dirname(__file__), '../combined_blog.html')
    print(f"Input directory: {input_dir}")
    print(f"Output file: {output_filepath}")
    print("Starting conversion process...")
    convert_markdown_to_html(input_dir, output_filepath)
