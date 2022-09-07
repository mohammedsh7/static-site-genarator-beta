import os
import frontmatter
import markdown
from slugify import slugify
from jinja2 import Environment, FileSystemLoader

from settings import CONTENT_DIR


# Grab all of the data files from the content dir
posts = [
    f for f in os.listdir(f"{CONTENT_DIR}/posts") if os.path.isfile(os.path.join(f"{CONTENT_DIR}/posts", f))
]

videos = [
    f for f in os.listdir(f"{CONTENT_DIR}/videos") if os.path.isfile(os.path.join(f"{CONTENT_DIR}/videos", f))
]

# For each file, read the front matter and text
post_data = []
for post in posts:
    with open(f"{CONTENT_DIR}/posts/{post}", "r") as f:
        file_data = frontmatter.load(f)
        metadata = file_data.metadata
        metadata["slug"] = slugify(metadata["title"])
        metadata["type"] = "post"
        content = markdown.markdown(file_data.content)
        post_data.append({"metadata": metadata, "content": content})

video_data = []
for video in videos:
    with open(f"{CONTENT_DIR}/videos/{video}", "r") as f:
        file_data = frontmatter.load(f)
        metadata = file_data.metadata
        metadata["slug"] = slugify(metadata["title"])
        metadata["type"] = "video"
        content = markdown.markdown(file_data.content)
        post_data.append({"metadata": metadata, "content": content})


# Render the home page and save it in the dist directory
env = Environment(loader=FileSystemLoader("./templates"))
template = env.get_template("home.html")

all_data = post_data + video_data
all_metadata = [data["metadata"] for data in all_data]
all_metadata.sort(key=lambda x: x["date"], reverse=True)

render_template = template.render(data=all_metadata)

os.makedirs("dist", exist_ok=True)
with open("dist/index.html", "w") as f:
    f.write(render_template)


# Loop through each file and render into template
for data in all_data:
    type = data["metadata"]["type"]
    template = env.get_template(f"{type}.html")
    render_template = template.render(data=data)
    os.makedirs(f"dist/{type}s", exist_ok=True)
    with open(f"dist/{type}s/{data['metadata']['slug']}.html", "w") as f:
        f.write(render_template)


# Copy static files (css)
os.makedirs("dist/static/css", exist_ok=True)
for file in os.listdir("static/css"):
    with open(f"static/css/{file}", "r") as f:
        with open(f"dist/static/css/{file}", "w") as f2:
            f2.write(f.read())