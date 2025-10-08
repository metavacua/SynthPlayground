from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
import json

@dataclass
class Source:
    """Represents a single source document or URL."""
    id: str
    name: str
    url: str

@dataclass
class Entity:
    """Represents a named entity (e.g., person, organization, topic)."""
    name: str
    type: str  # E.g., 'Person', 'Organization', 'Topic'
    description: Optional[str] = None

@dataclass
class Section:
    """Represents a single section of a report."""
    title: str
    content: str  # Markdown formatted content
    entities: List[Entity] = field(default_factory=list)

@dataclass
class Report:
    """The top-level dataclass for a structured research report."""
    title: str
    summary: str  # Markdown formatted summary
    sections: List[Section]
    sources: List[Source]
    used_sources: List[int] = field(default_factory=list)

    def to_markdown(self) -> str:
        """Serializes the report into a human-readable Markdown document."""
        markdown_str = f"# {self.title}\n\n"
        markdown_str += f"## Executive Summary\n\n{self.summary}\n\n"

        for section in self.sections:
            markdown_str += f"## {section.title}\n\n{section.content}\n\n"
            if section.entities:
                markdown_str += "### Key Entities Mentioned\n"
                for entity in section.entities:
                    markdown_str += f"- **{entity.name}** ({entity.type})\n"
                markdown_str += "\n"

        markdown_str += "## Sources\n\n"
        for i, source in enumerate(self.sources):
            # Check if the source was actually used before listing it.
            if (i + 1) in self.used_sources:
                markdown_str += f"*   **[{i+1}] {source.name}**: {source.url}\n"

        return markdown_str.strip()

    def to_json_ld(self) -> Dict[str, Any]:
        """
        Serializes the report into a machine-readable JSON-LD format.
        This uses basic Schema.org vocabulary for linked data.
        """
        report_data = {
            "@context": "https://schema.org",
            "@type": "Report",
            "headline": self.title,
            "description": self.summary,
            "articleBody": "\n\n".join([s.content for s in self.sections]),
            "author": {
                "@type": "Organization",
                "name": "Jules Agent"
            }
        }

        # Add sources as citations
        citations = []
        for i in self.used_sources:
            source = self.sources[i-1]
            citations.append({
                "@type": "WebPage",
                "name": source.name,
                "url": source.url
            })
        if citations:
            report_data["citation"] = citations

        return report_data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Report':
        """Creates a Report instance from a dictionary, handling nested objects."""
        sections = [
            Section(
                title=s['title'],
                content=s['content'],
                entities=[Entity(**e) for e in s.get('entities', [])]
            ) for s in data['sections']
        ]

        sources = [Source(**s) for s in data.get('sources', [])]

        return cls(
            title=data['title'],
            summary=data['summary'],
            sections=sections,
            sources=sources,
            used_sources=data.get('used_sources', [])
        )