import argparse
import subprocess
from pathlib import Path
import os
import shutil


THIS = Path(os.path.dirname(os.path.realpath(__file__)))
ROOT = THIS / ".."
POSTS = ROOT / "_posts"


def run(article, year, month, day):

    article = Path(article)
    subprocess.run(["jupyter", "nbconvert", "--to",
                   "markdown", article/"main.ipynb"])

    article_tag = article.name
    post_name = f"{year}-{month}-{day}-{article_tag}"
    shutil.move(article/"main.md", POSTS/f"{post_name}.md")

    shutil.copytree(article/f"{article_tag}", ROOT /
                    "assets/img"/f"{article_tag}")

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
