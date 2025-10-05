import argparse
import subprocess
from pathlib import Path
import os
import shutil
import re


THIS = Path(os.path.dirname(os.path.realpath(__file__)))
ROOT = THIS / ".."
POSTS = ROOT / "_posts"


def run(article, year, month, day):

    article = Path(article)
    subprocess.run(["jupyter", "nbconvert", "--to",
                   "markdown", article/"main.ipynb"])

    article_tag = article.name
    article_path = article/"main.md"

    post_name = f"{year}-{month}-{day}-{article_tag}"

    with open(article_path, "r") as f:
        text = f.read()

    matches = re.findall(
        r'<img\b[^>]*\bsrc\s*=\s*(["\'])([^"\']+)\1', text, flags=re.I)
    for m in matches:
        relative = m[1].replace("assets", f"/assets/{post_name}")
        relative = f"{{{{ '{relative}' | relative_url }}}}"
        text = text.replace(m[1], relative)

    with open(article_path, "w") as f:
        f.write(text)

    post_path = POSTS/f"{post_name}.md"
    shutil.move(article/"main.md", post_path)

    shutil.copytree(article/"assets", ROOT /
                    f"assets/{post_name}")

    print("Done!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Export MD',
        description='export ipynb to markdown')

    parser.add_argument('--article', type=str, action='store')
    parser.add_argument('--year', type=str, action='store')
    parser.add_argument('--month', type=str, action='store')
    parser.add_argument('--day', type=str, action='store')

    args = parser.parse_args()
    run(args.article, args.year, args.month, args.day)
