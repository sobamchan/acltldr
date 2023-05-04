import os
import xml.etree.ElementTree as ET

import click
import requests
import sienna
from schnitsum import SchnitSum
from tqdm import tqdm

from acltldr.utils import papers_to_markdown_items


@click.command()
@click.argument("url", type=str)
@click.argument("odir", type=str, default="./")
@click.option("--prefix", type=str, default=None)
@click.option("--use-gpu", is_flag=True, show_default=True, default=False)
def run(url: str, odir: str, prefix: str, use_gpu: bool):
    assert url.endswith(".xml"), "Needs to be a xml file."
    prefix = "out" if prefix is None else prefix

    response = requests.get(url)
    tree = ET.ElementTree(ET.fromstring(response.content))
    root = tree.getroot()
    model = SchnitSum(model_name="sobamchan/bart-large-scitldr", use_gpu=use_gpu)

    papers = []
    for node in tqdm(root[0].findall("paper")):
        _title = (
            ET.tostring(node.find("title"), method="text", encoding="utf8")
            .strip()
            .decode("UTF-8")
        )
        _authors = []
        for _author_node in node.findall("author"):
            _authors.append(
                f"{_author_node.find('first').text} {_author_node.find('last').text}"
            )
        _abst = node.find("abstract").text
        _url = f"https://aclanthology.org/{node.find('url').text}"

        papers.append(
            {
                "title": _title,
                "authors": _authors,
                "abstract": _abst,
                "tldr": model([_abst])[0] if isinstance(_abst, str) else "",
                "url": _url,
            }
        )

    sienna.save(papers, os.path.join(odir, f"{prefix}.papers.jsonl"))

    md_items = papers_to_markdown_items(papers)
    with open(os.path.join(odir, f"{prefix}.papers.md"), "w") as f:
        f.write("\n".join(md_items))


if __name__ == "__main__":
    run()
