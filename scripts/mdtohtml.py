import os
import markdown
import json

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
            output_file.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog Posts</title>
    <nav><a href="../index.html" alt="Home Button to main page"><button>Go Back</button></a></nav>
    <style>
        body { background-color: #fbfbff; font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }
        h1 { text-align: center; color: #040f16; }
        .post { margin-bottom: 40px; }
    </style>
</head>
<body>
    <h1>The Blog ...</h1>
    <p>No posts available.</p>
</body>
</html>""")
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
                'date': md_filename[:10]  # Extract date from filename
            }
            posts.append(post)

    # Sort posts by date
    posts.sort(key=lambda x: x['date'], reverse=True)

    html_header = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog Posts</title>

    <div class="navigation" id="navbar">
        <p class="name" style="font-family: regular-black;">CODY OUTFLEET</p>
        <nav><a href="../index.html" alt="Home Button to main page" style= "transition: .5s;">GO BACK</a></nav>
        
        </div>
    <div class="blog-title"><h1>The Blog.</h1></div>

    <style>

        /* First Font Family */
            @font-face {
            font-family: bold-black;
            src: url(./assets/fonts/PlayfairDisplay-Black.ttf);
            }

        /* third Font Family */
            @font-face {
            font-family: regular-black;
            src: url(./assets/fonts/PlayfairDisplay-Regular.ttf);
            }


        .name {
            color: #5c5c5c;
        }
        #navbar {
            background-color: #000000;
            width: 100%;
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: center;
            height: 3em;
            gap: 30vw;
            font-size: 15px;
        }

        #navbar a {
            text-decoration: none;
            color: white;
            padding-left: 10px;
            padding-right: 10px;
            font-family: regular-black;

        }

        #navbar a:hover {
            background-color: #ffffff;
            color: #000000;
            border-radius: 4px;
            padding: 10px;
        }

        .blog-title {
            font-family: bold-black;
            width: 100%;
            background-color: #2145bb;
            color: white;
            text-align: center;
            margin: 0;

        }

        .blog-title h1 {
            margin: 0;
        }

        body {
            background-color: #f6f6f6;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
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
            margin-top: 20px;
            margin-bottom: 20px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            padding: 10px;
            border-radius: 5px;
            font-family: regular-black;
        }
        
        .post-list-item:hover {
            background-color: #dcdcdc;
        }
        .post-content {
            flex-basis: 60%;
            max-width: 800px;
            padding: 0 20px;
            border-left: 1px solid #ccc;
            overflow-y: auto;
        }
        .post {
            margin-bottom: 60px;
        }
        h2 {
            color: rgb(0, 0, 0);
            font-size: 28px;
            margin-bottom: 20px;
            font-family: regular-black;
        }
        .thumbnail {
            width: 100%;
            max-width: 500px;
            height: auto;
            display: block;
            margin: 0 auto 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        

        p {
            color: #494949;
            font-size: 18px;
            line-height: 1.8;
            font-family: regular-black;
        }
        a {
            color: #007bff;
            text-decoration: none;
            transition: color 0.3s ease;
        }
        a:hover {
            color: #0056b3;
        }
    </style>

</head>
<body>
    <div class="container">
        <div class="post-list">
"""

    html_footer = """
        </div>
        <div class="post-content">
        </div>
    </div>
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            const posts = """ + json.dumps(posts) + """;

            const postList = document.querySelector(".post-list");
            const postContent = document.querySelector(".post-content");

            function showFullPost(post) {
                postContent.innerHTML = `
                    <h2>${post.title}</h2>
                    ${post.thumbnail ? `<img class="thumbnail" src="${post.thumbnail}" alt="${post.title}">` : ""}
                    <div>${post.content}</div>
                `;
            }

            function renderPostList() {
                postList.innerHTML = "";
                posts.forEach((post) => {
                    const listItem = document.createElement("div");
                    listItem.classList.add("post-list-item");
                    listItem.textContent = post.title;
                    listItem.addEventListener("click", () => showFullPost(post));
                    postList.appendChild(listItem);
                });
            }

            renderPostList();
            // Show the latest post by default
            if (posts.length > 0) {
                showFullPost(posts[0]);
            }
        });
    </script>
</body>
</html>
"""

    with open(output_filepath, 'w', encoding='utf-8') as output_file:
        output_file.write(html_header + html_footer)

    print("Markdown files have been converted and combined into a single HTML file successfully!")

if __name__ == "__main__":
    input_dir = os.path.join(os.path.dirname(__file__), '../_posts')
    output_filepath = os.path.join(os.path.dirname(__file__), '../blog.html')
    print(f"Input directory: {input_dir}")
    print(f"Output file: {output_filepath}")
    print("Starting conversion process...")
    convert_markdown_to_html(input_dir, output_filepath)
