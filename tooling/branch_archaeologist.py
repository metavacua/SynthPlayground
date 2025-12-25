#!/usr/bin/env python3
"""
Branch Archaeologist - Repository Branch Analysis Tool

Systematically analyzes all repository branches to construct a semantic knowledge
graph documenting development history. This serves as machine-readable institutional
memory for agents to query and learn from past work, both successful and failed attempts.

Usage:
    python3 tooling/branch_archaeologist.py [--output-dir PATH]

The script will:
1. Extract branch metadata from git
2. Classify branches by status, theme, and purpose
3. Identify relationships (convergences, version series, thematic groups)
4. Generate machine-readable outputs (JSON-LD, YAML-LD, TTL)
5. Generate human-readable documentation
6. Update metadata index

Output locations:
- Machine-readable: knowledge_core/branch_archaeology.{jsonld,yaml,ttl}
- Human-readable: docs/BRANCH_ARCHAEOLOGY.md
- Metadata: knowledge_core/branch_archaeology_meta.yaml
"""

import re
import json
import yaml
import subprocess
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple
from pathlib import Path


class BranchArchaeologist:
    """Analyzes repository branches and constructs semantic knowledge graphs."""

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.branches = []
        self.relationships = []
        self.statistics = {}

    def extract_branch_data(self) -> List[Dict]:
        """Extract branch metadata from git."""
        print("Extracting branch data from git...")

        cmd = [
            "git",
            "branch",
            "-r",
            "--format=%(refname:short)|%(objectname)|%(authordate:iso8601)|%(committerdate:iso8601)|%(subject)",
        ]

        result = subprocess.run(
            cmd, cwd=self.repo_path, capture_output=True, text=True, check=True
        )

        branches = []
        for line in result.stdout.strip().split("\n"):
            parts = line.split("|")
            if len(parts) >= 5:
                branches.append(
                    {
                        "name": parts[0].replace("origin/", ""),
                        "full_name": parts[0],
                        "commit_hash": parts[1],
                        "author_date": parts[2],
                        "committer_date": parts[3],
                        "subject": parts[4] if len(parts) > 4 else "",
                    }
                )

        print(f"  Found {len(branches)} branches")
        return branches

    def classify_branch(
        self, name: str, date_str: str, subject: str
    ) -> Tuple[str, List[str]]:
        """Classify branch based on name patterns and metadata."""
        name_lower = name.lower()
        subject_lower = subject.lower()

        # Parse date
        try:
            # Handle ISO 8601 format with timezone
            date_part = date_str.split("+")[0].split("-")[0].split("T")[0]
            if " " in date_str:
                date_part = date_str.split(" ")[0]
            date = datetime.fromisoformat(date_part)
            days_old = (datetime.now() - date).days
        except (ValueError, AttributeError):
            days_old = 999

        tags = []
        status = "unknown"

        # Classification patterns
        if name_lower.startswith("feat-") or name_lower.startswith("feat/"):
            tags.append("feature")
            status = "experimental" if days_old > 60 else "active"
        elif name_lower.startswith("bugfix"):
            tags.append("bugfix")
            status = "stalled" if days_old > 60 else "active"
        elif name_lower.startswith("refactor"):
            tags.append("refactor")
            status = "stalled" if days_old > 60 else "active"
        elif name_lower.startswith("docs"):
            tags.append("documentation")
            status = "stalled" if days_old > 60 else "active"
        elif name_lower.startswith("chore"):
            tags.append("maintenance")
            status = "archived"
        elif name_lower.startswith("test"):
            tags.append("testing")
            status = "experimental"
        elif "protocol" in name_lower:
            tags.extend(["protocol", "core"])
        elif "aorp" in name_lower:
            tags.extend(["aorp", "core"])
        elif "chc" in name_lower:
            tags.extend(["chc", "core"])
        elif "chomsky" in name_lower:
            tags.extend(["formal-theory", "experimental"])
        elif "experiment" in name_lower:
            tags.append("experimental")
            status = "experimental"
        elif "cleanup" in name_lower:
            tags.append("cleanup")
            status = "archived"
        elif name_lower.startswith("dependabot"):
            tags.extend(["dependencies", "automated"])
            status = "automated"
        elif name_lower.startswith("repobird") or name_lower.startswith("gitauto"):
            tags.append("automated")
            status = "automated"

        # Subject-based classification
        if "merge" in subject_lower:
            tags.append("merge")
        if "fix" in subject_lower:
            tags.append("fix")
        if "add" in subject_lower or "implement" in subject_lower:
            tags.append("addition")
        if "delete" in subject_lower or "remove" in subject_lower:
            tags.append("deletion")
        if "refactor" in subject_lower:
            tags.append("refactor")

        # Determine status if not yet set
        if status == "unknown":
            if days_old > 90:
                status = "stalled"
            elif days_old > 30:
                status = "inactive"
            else:
                status = "active"

        return status, list(set(tags))

    def identify_relationships(self, branches: List[Dict]) -> List[Dict]:
        """Identify relationships between branches."""
        relationships = []

        # Group by commit hash to find convergence
        by_commit = defaultdict(list)
        for branch in branches:
            by_commit[branch["commit_hash"]].append(branch["name"])

        # Find convergent branches
        for commit_hash, branch_names in by_commit.items():
            if len(branch_names) > 1:
                for i, branch1 in enumerate(branch_names):
                    for branch2 in branch_names[i + 1 :]:
                        relationships.append(
                            {
                                "type": "converges_to",
                                "source": branch1,
                                "target": branch2,
                                "commit_hash": commit_hash,
                                "explanation": "Both branches point to the same commit",
                            }
                        )

        # Extract version series
        series = defaultdict(list)
        for branch in branches:
            name = branch["name"]
            match = re.match(r"(.+?)[-_]v(\d+)(?:[-_.]|$)", name)
            if match:
                base_name = match.group(1)
                version = int(match.group(2))
                series[base_name].append((version, name))

        # Sort by version and create supersedes relationships
        for base_name, versions in series.items():
            sorted_versions = [name for ver, name in sorted(versions)]
            for i in range(len(sorted_versions) - 1):
                relationships.append(
                    {
                        "type": "supersedes",
                        "source": sorted_versions[i + 1],
                        "target": sorted_versions[i],
                        "explanation": f"Version progression in {base_name} series",
                    }
                )

        # Find thematic relationships
        by_theme = defaultdict(list)
        themes = [
            "protocol",
            "aorp",
            "chc",
            "chomsky",
            "research",
            "self-improvement",
            "yaml-ld",
            "refactor",
            "dbpedia",
            "test",
            "doc",
        ]

        for branch in branches:
            name_lower = branch["name"].lower()
            for theme in themes:
                if theme in name_lower:
                    by_theme[theme].append(branch["name"])

        # Add thematic relationships
        for theme, branch_names in by_theme.items():
            if len(branch_names) > 1:
                for branch_name in branch_names:
                    relationships.append(
                        {
                            "type": "thematic_group",
                            "source": branch_name,
                            "target": theme,
                            "explanation": f"Part of {theme} development theme",
                        }
                    )

        return relationships

    def build_knowledge_graph(self) -> Dict:
        """Build comprehensive knowledge graph."""
        print("Building knowledge graph...")

        # Extract and classify branches
        self.branches = self.extract_branch_data()

        for branch in self.branches:
            status, tags = self.classify_branch(
                branch["name"], branch["author_date"], branch["subject"]
            )
            branch["status"] = status
            branch["tags"] = tags
            branch["purpose"] = (
                branch["subject"] if branch["subject"] else f"Branch: {branch['name']}"
            )

        # Identify relationships
        self.relationships = self.identify_relationships(self.branches)
        print(f"  Identified {len(self.relationships)} relationships")

        # Build statistics
        status_counts = defaultdict(int)
        tag_counts = defaultdict(int)

        for branch in self.branches:
            status_counts[branch["status"]] += 1
            for tag in branch["tags"]:
                tag_counts[tag] += 1

        self.statistics = {"byStatus": dict(status_counts), "byTag": dict(tag_counts)}

        # Construct knowledge graph
        kg = {
            "@context": {
                "@vocab": "http://metavacua.io/ontology/branch#",
                "git": "http://metavacua.io/ontology/git#",
                "schema": "http://schema.org/",
                "dcterms": "http://purl.org/dc/terms/",
                "name": "schema:name",
                "description": "schema:description",
                "dateCreated": "schema:dateCreated",
                "commitHash": "git:commitHash",
                "status": "git:status",
                "tags": "schema:keywords",
                "purpose": "dcterms:purpose",
                "convergesTo": "git:convergesTo",
                "supersedes": "git:supersedes",
                "thematicGroup": "git:thematicGroup",
            },
            "@type": "BranchKnowledgeGraph",
            "dateGenerated": datetime.now().isoformat(),
            "totalBranches": len(self.branches),
            "statistics": self.statistics,
            "branches": self.branches,
            "relationships": self.relationships,
        }

        return kg

    def save_json_ld(self, kg: Dict, output_path: Path):
        """Save as JSON-LD."""
        with open(output_path, "w") as f:
            json.dump(kg, f, indent=2)
        print(f"  Saved JSON-LD to {output_path}")

    def save_yaml_ld(self, kg: Dict, output_path: Path):
        """Save as YAML-LD."""
        with open(output_path, "w") as f:
            yaml.dump(kg, f, default_flow_style=False, sort_keys=False, width=120)
        print(f"  Saved YAML-LD to {output_path}")

    def save_turtle(self, kg: Dict, output_path: Path):
        """Save as Turtle RDF."""
        lines = [
            "@prefix branch: <http://metavacua.io/ontology/branch#> .",
            "@prefix git: <http://metavacua.io/ontology/git#> .",
            "@prefix schema: <http://schema.org/> .",
            "@prefix dcterms: <http://purl.org/dc/terms/> .",
            "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .",
            "",
            "<http://metavacua.io/resource/branch-archaeology>",
            "    a branch:BranchKnowledgeGraph ;",
            f'    schema:dateCreated "{kg["dateGenerated"]}"^^xsd:dateTime ;',
            f'    branch:totalBranches {kg["totalBranches"]} ;',
            '    schema:description "Archaeological analysis of repository branches documenting development history" .',
            "",
        ]

        # Branches
        for branch in kg["branches"]:
            branch_uri = f"<http://metavacua.io/resource/branch/{branch['name'].replace('/', '-')}>"
            lines.extend(
                [
                    f"{branch_uri}",
                    "    a git:Branch ;",
                    f'    schema:name "{branch["name"]}" ;',
                    f'    git:commitHash "{branch["commit_hash"]}" ;',
                    f'    git:status "{branch["status"]}" ;',
                    f'    schema:dateCreated "{branch["author_date"]}" ;',
                ]
            )

            for tag in branch["tags"]:
                lines.append(f'    schema:keywords "{tag}" ;')

            lines.extend(["    .", ""])

        # Relationships
        for rel in kg["relationships"]:
            if rel["type"] == "converges_to":
                source_uri = f"<http://metavacua.io/resource/branch/{rel['source'].replace('/', '-')}>"
                target_uri = f"<http://metavacua.io/resource/branch/{rel['target'].replace('/', '-')}>"
                lines.append(f"{source_uri} git:convergesTo {target_uri} .")

        with open(output_path, "w") as f:
            f.write("\n".join(lines))
        print(f"  Saved Turtle to {output_path}")

    def save_documentation(self, kg: Dict, output_path: Path):
        """Generate and save human-readable documentation."""
        # Use a simplified version for now
        lines = [
            "# Repository Branch Archaeology",
            "",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}",
            "",
            "## Executive Summary",
            "",
            f"This document provides a comprehensive archaeological analysis of **{kg['totalBranches']} branches**.",
            "",
            "### Statistics",
            "",
            "| Status | Count |",
            "|--------|-------|",
        ]

        for status, count in sorted(
            kg["statistics"]["byStatus"].items(), key=lambda x: -x[1]
        ):
            lines.append(f"| {status.capitalize()} | {count} |")

        lines.extend(
            [
                "",
                "For detailed analysis, query the machine-readable formats:",
                "- `knowledge_core/branch_archaeology.jsonld`",
                "- `knowledge_core/branch_archaeology.yaml`",
                "- `knowledge_core/branch_archaeology.ttl`",
                "",
            ]
        )

        with open(output_path, "w") as f:
            f.write("\n".join(lines))
        print(f"  Saved documentation to {output_path}")

    def run(self, output_dir: str = None):
        """Run complete branch archaeology analysis."""
        print("=== Branch Archaeologist ===")
        print()

        # Build knowledge graph
        kg = self.build_knowledge_graph()

        # Determine output paths
        if output_dir:
            base_path = Path(output_dir)
        else:
            base_path = self.repo_path / "knowledge_core"

        docs_path = self.repo_path / "docs"
        docs_path.mkdir(exist_ok=True)

        # Save outputs
        print("\nSaving outputs...")
        self.save_json_ld(kg, base_path / "branch_archaeology.jsonld")
        self.save_yaml_ld(kg, base_path / "branch_archaeology.yaml")
        self.save_turtle(kg, base_path / "branch_archaeology.ttl")
        self.save_documentation(kg, docs_path / "BRANCH_ARCHAEOLOGY.md")

        print("\n=== Analysis Complete ===")
        print(f"Total branches: {kg['totalBranches']}")
        print(f"Relationships: {len(kg['relationships'])}")
        print("\nStatus breakdown:")
        for status, count in sorted(
            kg["statistics"]["byStatus"].items(), key=lambda x: -x[1]
        ):
            print(f"  {status}: {count}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Analyze repository branches and construct semantic knowledge graph"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Output directory for generated files (default: knowledge_core/)",
    )
    parser.add_argument(
        "--repo",
        type=str,
        default=".",
        help="Path to git repository (default: current directory)",
    )

    args = parser.parse_args()

    archaeologist = BranchArchaeologist(repo_path=args.repo)
    archaeologist.run(output_dir=args.output_dir)


if __name__ == "__main__":
    main()
