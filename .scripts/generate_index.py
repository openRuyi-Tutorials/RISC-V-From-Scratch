#!/usr/bin/env python3
"""Generate index.html from Markdown docs.

This script builds a single documentation portal page from root Markdown files.
It is intended to run both locally and in GitHub Actions.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import argparse
import re

import markdown


@dataclass(frozen=True)
class DocSpec:
    path: str
    label: str
    section_id: str


DOCS = [
    DocSpec("readme.md", "项目总览", "doc-readme"),
    DocSpec("ROADMAP.md", "主线路线", "doc-roadmap"),
    DocSpec("FAQ.md", "FAQ", "doc-faq"),
    DocSpec("CHECKLIST.md", "提交检查", "doc-checklist"),
    DocSpec("README.zh-CN.md", "卷轴模板", "doc-template"),
]

DOC_ID_BY_BASENAME = {Path(item.path).name: item.section_id for item in DOCS}
MD_LINK_RE = re.compile(r"\(([^)]+\.md)(#[^)]+)?\)", re.IGNORECASE)


def rewrite_local_md_links(text: str) -> str:
    def _replace(match: re.Match[str]) -> str:
        raw_path = match.group(1)
        raw_anchor = match.group(2) or ""
        basename = Path(raw_path).name
        target = DOC_ID_BY_BASENAME.get(basename)
        if not target:
            return match.group(0)
        return f"(#{target}{raw_anchor})"

    return MD_LINK_RE.sub(_replace, text)


def render_markdown_to_html(markdown_text: str) -> str:
    parser = markdown.Markdown(
        extensions=[
            "extra",
            "fenced_code",
            "tables",
            "toc",
            "sane_lists",
            "nl2br",
        ],
        output_format="html5",
    )
    return parser.convert(markdown_text)


def build_html(root: Path) -> str:
    top_nav_items = []
    side_nav_items = []
    section_items = []

    for doc in DOCS:
        file_path = root / doc.path
        if not file_path.exists():
            raise FileNotFoundError(f"Missing source doc: {doc.path}")

        raw_md = file_path.read_text(encoding="utf-8")
        normalized_md = rewrite_local_md_links(raw_md)
        rendered = render_markdown_to_html(normalized_md)

        top_nav_items.append(f'<a href="#{doc.section_id}">{doc.label}</a>')
        side_nav_items.append(f'<a href="#{doc.section_id}">{doc.label}</a>')
        section_items.append(
            f"""
            <section id="{doc.section_id}" class="doc-card">
              <header class="doc-header">
                <h2>{doc.label}</h2>
                <a class="source-link" href="{doc.path}">查看源文件</a>
              </header>
              <article class="markdown-body">
                {rendered}
              </article>
            </section>
            """
        )

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    side_nav_html = "\n".join(side_nav_items)
    top_nav_html = " ".join(top_nav_items)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RISC-V From Scratch 文档站</title>
  <style>
    :root {{
      --bg: #f5f7fb;
      --card: #ffffff;
      --text: #1f2937;
      --muted: #4b5563;
      --accent: #0f766e;
      --accent-soft: #ccfbf1;
      --border: #dbe3ea;
      --code-bg: #0f172a;
      --code-text: #e2e8f0;
    }}
    * {{
      box-sizing: border-box;
    }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
      line-height: 1.7;
    }}
    .topbar {{
      position: sticky;
      top: 0;
      z-index: 20;
      backdrop-filter: blur(8px);
      background: rgba(245, 247, 251, 0.92);
      border-bottom: 1px solid var(--border);
    }}
    .topbar-inner {{
      max-width: 1320px;
      margin: 0 auto;
      padding: 14px 20px;
      display: flex;
      flex-wrap: wrap;
      gap: 12px 16px;
      align-items: center;
      justify-content: space-between;
    }}
    .title {{
      font-weight: 700;
      font-size: 18px;
    }}
    .nav {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }}
    .nav-top {{
      display: none;
    }}
    .nav a {{
      text-decoration: none;
      color: var(--text);
      font-size: 14px;
      padding: 6px 10px;
      border-radius: 999px;
      border: 1px solid var(--border);
      background: #fff;
    }}
    .nav a:hover {{
      border-color: var(--accent);
      color: var(--accent);
    }}
    .layout {{
      max-width: 1320px;
      margin: 0 auto;
      padding: 18px 20px 48px;
      display: grid;
      grid-template-columns: 280px minmax(0, 1fr);
      gap: 16px;
      align-items: start;
    }}
    .sidebar {{
      position: sticky;
      top: 78px;
    }}
    .sidebar-card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 16px;
      box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
      padding: 12px;
    }}
    .sidebar-title {{
      font-size: 12px;
      color: var(--muted);
      margin: 2px 4px 8px;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }}
    .side-nav {{
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}
    .side-nav a {{
      text-decoration: none;
      color: var(--text);
      font-size: 14px;
      padding: 8px 10px;
      border-radius: 10px;
      border: 1px solid transparent;
    }}
    .side-nav a:hover {{
      color: var(--accent);
      border-color: var(--border);
      background: #f8fafc;
    }}
    .content {{
      min-width: 0;
    }}
    .banner {{
      margin-bottom: 14px;
      padding: 10px 14px;
      border-radius: 10px;
      border: 1px solid var(--border);
      background: #fff;
      color: var(--muted);
      font-size: 13px;
    }}
    .doc-card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 16px;
      box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
      padding: 20px;
      margin-bottom: 14px;
      scroll-margin-top: 76px;
    }}
    .doc-header {{
      display: flex;
      gap: 10px;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      padding-bottom: 10px;
      border-bottom: 1px dashed var(--border);
    }}
    .doc-header h2 {{
      margin: 0;
      font-size: 20px;
    }}
    .source-link {{
      text-decoration: none;
      color: var(--accent);
      font-size: 13px;
      padding: 4px 8px;
      border-radius: 8px;
      background: var(--accent-soft);
      white-space: nowrap;
    }}
    .markdown-body :is(h1, h2, h3, h4, h5, h6) {{
      margin-top: 1.2em;
      margin-bottom: 0.45em;
      line-height: 1.35;
      scroll-margin-top: 86px;
    }}
    .markdown-body h1 {{
      font-size: 28px;
    }}
    .markdown-body h2 {{
      font-size: 22px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 4px;
    }}
    .markdown-body h3 {{
      font-size: 18px;
    }}
    .markdown-body p, .markdown-body li {{
      margin: 0.45em 0;
    }}
    .markdown-body a {{
      color: var(--accent);
      text-decoration: none;
    }}
    .markdown-body a:hover {{
      text-decoration: underline;
    }}
    .markdown-body pre {{
      background: var(--code-bg);
      color: var(--code-text);
      border-radius: 12px;
      padding: 14px;
      overflow-x: auto;
    }}
    .markdown-body code {{
      font-family: "JetBrains Mono", "SFMono-Regular", Consolas, monospace;
      font-size: 0.9em;
    }}
    .markdown-body :not(pre) > code {{
      background: #eef2f7;
      border-radius: 6px;
      padding: 2px 6px;
      color: #0f172a;
    }}
    .markdown-body table {{
      width: 100%;
      border-collapse: collapse;
      margin: 10px 0;
      font-size: 14px;
    }}
    .markdown-body th, .markdown-body td {{
      border: 1px solid var(--border);
      padding: 8px 10px;
      text-align: left;
      vertical-align: top;
    }}
    .markdown-body blockquote {{
      margin: 10px 0;
      padding: 8px 12px;
      border-left: 4px solid #94a3b8;
      background: #f8fafc;
      color: #334155;
    }}
    @media (max-width: 960px) {{
      .nav-top {{
        display: flex;
      }}
      .layout {{
        grid-template-columns: 1fr;
        padding: 14px 12px 40px;
      }}
      .sidebar {{
        display: none;
      }}
    }}
    @media (max-width: 768px) {{
      .topbar-inner {{
        padding: 12px 14px;
      }}
      .doc-card {{
        padding: 14px;
      }}
      .doc-header {{
        flex-direction: column;
        align-items: flex-start;
      }}
    }}
  </style>
</head>
<body>
  <header class="topbar">
    <div class="topbar-inner">
      <div class="title">RISC-V From Scratch 文档站</div>
      <nav class="nav nav-top">
        {top_nav_html}
      </nav>
    </div>
  </header>

  <main class="layout">
    <aside class="sidebar">
      <div class="sidebar-card">
        <div class="sidebar-title">文档导航</div>
        <nav class="side-nav">
          {side_nav_html}
        </nav>
      </div>
    </aside>
    <section class="content">
      <div class="banner">
        本页由 <code>.scripts/generate_index.py</code> 自动生成。生成时间：{generated_at}
      </div>
      {''.join(section_items)}
    </section>
  </main>
</body>
</html>
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate index.html from markdown docs.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Project root directory (default: current directory).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("index.html"),
        help="Output HTML file path (default: index.html).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    output = args.output if args.output.is_absolute() else (root / args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    html = build_html(root)
    output.write_text(html, encoding="utf-8")
    print(f"Generated {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
