"""
Base classes for report generation.
Provides MarkdownFormatter utilities and BaseReportSection abstract class.
"""

import os
from typing import Dict, List, Tuple, Optional, Any
from abc import ABC, abstractmethod

from config import Config
from exceptions import ReportSaveError
from visual_registry import get_registry


class MarkdownFormatter:
    """Enhanced utility for Markdown formatting with rich output support."""

    # ==========================================================================
    # BASIC FORMATTING
    # ==========================================================================

    @staticmethod
    def h1(text: str) -> str:
        """Level 1 header."""
        return f"# {text}\n"

    @staticmethod
    def h2(text: str) -> str:
        """Level 2 header."""
        return f"## {text}\n"

    @staticmethod
    def h3(text: str) -> str:
        """Level 3 header."""
        return f"### {text}\n"

    @staticmethod
    def h4(text: str) -> str:
        """Level 4 header."""
        return f"#### {text}\n"

    @staticmethod
    def bold(text: str) -> str:
        """Bold text."""
        return f"**{text}**"

    @staticmethod
    def italic(text: str) -> str:
        """Italic text."""
        return f"*{text}*"

    @staticmethod
    def code(text: str) -> str:
        """Inline code."""
        return f"`{text}`"

    @staticmethod
    def code_block(text: str, lang: str = "") -> str:
        """Fenced code block."""
        return f"```{lang}\n{text}\n```\n"

    # ==========================================================================
    # LIST FORMATTING
    # ==========================================================================

    @staticmethod
    def bullet(text: str) -> str:
        """Single bullet point."""
        return f"- {text}\n"

    @staticmethod
    def numbered(num: int, text: str) -> str:
        """Numbered list item."""
        return f"{num}. {text}\n"

    @staticmethod
    def bullet_list(items: List[str]) -> str:
        """Create a bullet list from items."""
        return "".join(f"- {item}\n" for item in items)

    @staticmethod
    def numbered_list(items: List[str]) -> str:
        """Create a numbered list from items."""
        return "".join(f"{i}. {item}\n" for i, item in enumerate(items, 1))

    # ==========================================================================
    # TABLE FORMATTING
    # ==========================================================================

    @staticmethod
    def table_row(cells: List[str]) -> str:
        """Single table row."""
        return f"| {' | '.join(str(c) for c in cells)} |\n"

    @staticmethod
    def table_separator(num_cols: int) -> str:
        """Table header separator."""
        return f"| {' | '.join(['---'] * num_cols)} |\n"

    @staticmethod
    def table(headers: List[str], rows: List[List[Any]], align: str = "left") -> str:
        """
        Create a complete markdown table.

        Args:
            headers: Column header names
            rows: List of row data (each row is a list of values)
            align: Alignment ('left', 'center', 'right')

        Returns:
            Complete markdown table string
        """
        if not headers or not rows:
            return ""

        # Alignment markers
        align_map = {"left": ":---", "center": ":---:", "right": "---:"}
        align_marker = align_map.get(align, ":---")

        lines = []
        # Header row
        lines.append(f"| {' | '.join(str(h) for h in headers)} |")
        # Separator with alignment
        lines.append(f"| {' | '.join([align_marker] * len(headers))} |")
        # Data rows
        for row in rows:
            cells = [str(c) if c is not None else "" for c in row]
            # Pad row if needed
            while len(cells) < len(headers):
                cells.append("")
            lines.append(f"| {' | '.join(cells[:len(headers)])} |")

        return "\n".join(lines) + "\n"

    # ==========================================================================
    # SPECIAL FORMATTING
    # ==========================================================================

    @staticmethod
    def link(text: str, url: str) -> str:
        """Markdown hyperlink."""
        return f"[{text}]({url})"

    @staticmethod
    def image(alt_text: str, path: str) -> str:
        """Markdown image."""
        return f"![{alt_text}]({path})"

    @staticmethod
    def horizontal_rule() -> str:
        """Horizontal rule/divider."""
        return "---\n"

    @staticmethod
    def blockquote(text: str) -> str:
        """Blockquote for interpretations/insights."""
        lines = text.strip().split('\n')
        return "\n".join(f"> {line}" for line in lines) + "\n"

    @staticmethod
    def definition_list(items: Dict[str, str]) -> str:
        """
        Create a definition-style list (term: definition format).

        Args:
            items: Dictionary of term -> definition pairs

        Returns:
            Formatted definition list
        """
        lines = []
        for term, definition in items.items():
            lines.append(f"- **{term}**: {definition}")
        return "\n".join(lines) + "\n"

    @staticmethod
    def key_value(key: str, value: Any, bold_key: bool = True) -> str:
        """Format a key-value pair."""
        k = f"**{key}**" if bold_key else key
        return f"- {k}: {value}\n"

    @staticmethod
    def metric(name: str, value: Any, unit: str = "", precision: int = 2) -> str:
        """Format a metric with optional unit and precision."""
        if isinstance(value, float):
            formatted_value = f"{value:,.{precision}f}"
        elif isinstance(value, int):
            formatted_value = f"{value:,}"
        else:
            formatted_value = str(value)

        if unit:
            return f"- **{name}**: {formatted_value} {unit}\n"
        return f"- **{name}**: {formatted_value}\n"

    @staticmethod
    def percentage(name: str, value: float, precision: int = 1) -> str:
        """Format a percentage metric."""
        return f"- **{name}**: {value:.{precision}f}%\n"

    @staticmethod
    def interpretation(text: str) -> str:
        """Format an interpretation/insight as an italicized blockquote."""
        return f"\n> *{text}*\n\n"

    @staticmethod
    def warning(text: str) -> str:
        """Format a warning note."""
        return f"\n> **Warning**: {text}\n\n"

    @staticmethod
    def note(text: str) -> str:
        """Format an informational note."""
        return f"\n> **Note**: {text}\n\n"

    # ==========================================================================
    # STATISTICAL FORMATTING HELPERS
    # ==========================================================================

    @staticmethod
    def stat_summary(name: str, mean: float, median: float, std: float,
                     min_val: float, max_val: float, precision: int = 2) -> str:
        """Format a statistical summary block."""
        lines = [
            f"### {name}\n",
            f"| Statistic | Value |",
            f"|:---|---:|",
            f"| Mean | {mean:,.{precision}f} |",
            f"| Median | {median:,.{precision}f} |",
            f"| Std Dev | {std:,.{precision}f} |",
            f"| Min | {min_val:,.{precision}f} |",
            f"| Max | {max_val:,.{precision}f} |",
            ""
        ]
        return "\n".join(lines)

    @staticmethod
    def percentile_table(name: str, p25: float, p50: float, p75: float,
                         precision: int = 2) -> str:
        """Format a percentile summary."""
        return (
            f"| Percentile | {name} |\n"
            f"|:---|---:|\n"
            f"| 25th | {p25:,.{precision}f} |\n"
            f"| 50th (Median) | {p50:,.{precision}f} |\n"
            f"| 75th | {p75:,.{precision}f} |\n"
        )


class BaseReportSection(ABC):
    """Abstract base class for all report sections."""

    def __init__(self, config: Config):
        self.config = config
        self.md = MarkdownFormatter()

    @abstractmethod
    def generate(self, data: Any) -> str:
        """Generate section content. Must be implemented by subclasses."""
        pass

    @abstractmethod
    def get_filename(self) -> str:
        """Get section filename. Must be implemented by subclasses."""
        pass

    def save(self, content: str) -> str:
        """Save section content to file."""
        try:
            filepath = self._get_filepath()
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return filepath
        except Exception as e:
            raise ReportSaveError(filepath, str(e))

    def _get_filepath(self) -> str:
        """Get full filepath for section output."""
        return os.path.join(self.config.output_dir, self.get_filename())

    def _link_images(self, image_dir: str, pattern: str = "*.png") -> List[str]:
        """Find and create markdown links for images (recursively in subdirectories)."""
        import glob
        fig_path = os.path.join(self.config.figure_dir, image_dir)
        # Use ** for recursive search in subdirectories
        imgs = glob.glob(os.path.join(fig_path, "**", pattern), recursive=True)
        # Also include images in the immediate directory
        imgs.extend(glob.glob(os.path.join(fig_path, pattern)))
        links = []
        for img in sorted(set(imgs)):
            # Use relative path from report location (figures/...)
            rel_path = os.path.relpath(img, self.config.output_dir)
            name = os.path.basename(img).replace('_', ' ').replace('.png', '')
            # Include subdirectory name in the image caption for context
            subdir = os.path.basename(os.path.dirname(img))
            if subdir and subdir != os.path.basename(fig_path):
                name = f"{subdir} - {name}"
            links.append(f"![{name}]({rel_path})")
        return links

    def _embed_image(self, rel_path: str, alt_text: str = "") -> str:
        """Create markdown image embed."""
        return f"![{alt_text}]({rel_path})"

    def _link_from_registry(self, **filters) -> List[str]:
        """Get visualization links from registry."""
        try:
            registry = get_registry()
            registry.set_output_dir(self.config.output_dir)
            visuals = registry.query(**filters)
            return registry.to_markdown_links(visuals)
        except Exception as e:
            print(f"[WARNING] Registry query failed: {e}")
            return []

    def _format_number(self, value: Any, precision: int = 2) -> str:
        """Format a number with commas and precision."""
        if value is None:
            return "N/A"
        if isinstance(value, float):
            return f"{value:,.{precision}f}"
        if isinstance(value, int):
            return f"{value:,}"
        return str(value)

    def _safe_get(self, data: Dict, *keys, default: Any = None) -> Any:
        """Safely get nested dictionary values."""
        result = data
        for key in keys:
            if isinstance(result, dict):
                result = result.get(key, default)
            else:
                return default
        return result if result is not None else default
