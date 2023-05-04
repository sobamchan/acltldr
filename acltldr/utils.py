from typing import Dict, List


def papers_to_markdown_items(papers: List[Dict]) -> List[str]:
    markdown_items = []
    for paper in papers:
        s = f"""- [{paper['title']}]({paper['url']})
  - {', '.join(paper['authors'])}
  - **TLDR**: {paper['tldr']}
"""
        markdown_items.append(s)
    return markdown_items
