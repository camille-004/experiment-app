from __future__ import annotations

import itertools
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

import re


@dataclass
class HTMLBlock:
    name: str
    content: str


@dataclass
class HTMLProcessor:
    file_path: Path

    def process(self) -> None:
        content = self.file_path.read_text()
        blocks = self._split_blocks(content)
        formatted = self._format_blocks(blocks)
        self.file_path.write_text(formatted)

    def _split_blocks(self, content: str) -> list[HTMLBlock]:
        blocks = []
        for m in re.finditer(r"{%.*?%}", content):
            blocks.append(HTMLBlock(name=m.group(), content=""))
        return blocks
    
    def _format_blocks(self, blocks: list[HTMLBlock]) -> str:
        formatted = [f"{block.name}\n" for block in blocks]
        return "".join(formatted)
    

@dataclass
class HTMLPostProcessor:
    directory: Path

    def run(self) -> None:
        for file in self._find_html_files():
            processor = HTMLProcessor(file_path=file)
            processor.process()
        
    def _find_html_files(self) -> Iterator[Path]:
        return self.directory.glob("**/*.html")


def main() -> None:
    directory = Path("frontend/templates")
    processor = HTMLPostProcessor(directory=directory)
    processor.run()


if __name__ == "__main__":
    main()
