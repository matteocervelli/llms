#!/usr/bin/env python3
"""
Dependency Checker Script

Enhanced dependency analysis tool for Feature-Implementer v2 architecture.
Analyzes dependencies, checks compatibility, detects conflicts, and generates reports.

Usage:
    python dependency-checker-script.py --analyze --project-root .
    python dependency-checker-script.py --check-compatibility --new-deps "httpx>=0.27.0"
    python dependency-checker-script.py --check-conflicts --new-deps "package1,package2"
    python dependency-checker-script.py --full-report --output report.md

Author: Feature-Implementer v2
License: MIT
"""

import argparse
import json
import re
import subprocess
import sys
from importlib.metadata import distributions
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from urllib.request import urlopen
from urllib.error import URLError


class VersionSpecifier:
    """Parse and compare version specifiers."""

    @staticmethod
    def parse_version(version_str: str) -> Tuple[int, ...]:
        """
        Parse version string into tuple of integers.

        Args:
            version_str: Version string (e.g., "1.2.3")

        Returns:
            Tuple of integers (e.g., (1, 2, 3))
        """
        # Remove pre-release tags (alpha, beta, rc)
        version_str = re.sub(r'[a-zA-Z]+.*$', '', version_str)
        parts = version_str.split('.')
        return tuple(int(p) for p in parts if p.isdigit())

    @staticmethod
    def parse_specifier(spec: str) -> Tuple[str, str]:
        """
        Parse version specifier into operator and version.

        Args:
            spec: Version specifier (e.g., ">=1.0.0", "~=2.0")

        Returns:
            Tuple of (operator, version)
        """
        match = re.match(r'([><=~^!]+)(.+)', spec.strip())
        if match:
            return match.group(1), match.group(2)
        return '==', spec.strip()

    @staticmethod
    def satisfies(version: str, specifier: str) -> bool:
        """
        Check if version satisfies specifier.

        Args:
            version: Version string (e.g., "1.2.3")
            specifier: Version specifier (e.g., ">=1.0.0")

        Returns:
            True if version satisfies specifier
        """
        op, spec_ver = VersionSpecifier.parse_specifier(specifier)
        v = VersionSpecifier.parse_version(version)
        sv = VersionSpecifier.parse_version(spec_ver)

        if op == '==':
            return v == sv
        elif op == '>=':
            return v >= sv
        elif op == '>':
            return v > sv
        elif op == '<=':
            return v <= sv
        elif op == '<':
            return v < sv
        elif op == '~=':  # Compatible release
            # ~=1.2 means >=1.2, <2.0
            return v >= sv and v < (sv[0] + 1,)
        elif op == '!=':
            return v != sv
        return False


class DependencyAnalyzer:
    """Analyze project dependencies and detect conflicts."""

    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize dependency analyzer.

        Args:
            project_root: Project root directory
        """
        self.project_root = project_root or Path.cwd()
        self.requirements_file = self._find_requirements_file()
        self.pyproject_file = self.project_root / "pyproject.toml"
        self.installed_packages = self._get_installed_packages()

    def _find_requirements_file(self) -> Optional[Path]:
        """Find requirements.txt in project."""
        candidates = [
            self.project_root / "requirements.txt",
            self.project_root / "requirements" / "base.txt",
        ]
        for candidate in candidates:
            if candidate.exists():
                return candidate
        return None

    def _get_installed_packages(self) -> Dict[str, str]:
        """Get installed packages with versions."""
        packages = {}
        for dist in distributions():
            name = dist.metadata["Name"]
            ver = dist.metadata["Version"]
            packages[name.lower()] = ver
        return packages

    def parse_requirements_txt(self) -> Dict[str, str]:
        """
        Parse requirements.txt.

        Returns:
            Dict mapping package names to version specifiers
        """
        if not self.requirements_file:
            return {}

        requirements = {}
        content = self.requirements_file.read_text()
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # Parse package specification
            match = re.match(r'([a-zA-Z0-9_-]+)([><=~!].+)?', line)
            if match:
                pkg = match.group(1).lower()
                spec = match.group(2) or ''
                requirements[pkg] = spec

        return requirements

    def parse_pyproject_toml(self) -> Dict[str, str]:
        """
        Parse pyproject.toml dependencies.

        Returns:
            Dict mapping package names to version specifiers
        """
        if not self.pyproject_file.exists():
            return {}

        requirements = {}
        content = self.pyproject_file.read_text()

        # Find dependencies section
        in_dependencies = False
        for line in content.splitlines():
            if '[project.dependencies]' in line or 'dependencies = [' in line:
                in_dependencies = True
                continue

            if in_dependencies:
                if line.strip().startswith('['):
                    break
                if line.strip().startswith(']'):
                    break

                # Parse dependency line
                match = re.search(r'"([a-zA-Z0-9_-]+)([><=~!].+)?"', line)
                if match:
                    pkg = match.group(1).lower()
                    spec = match.group(2) or ''
                    requirements[pkg] = spec

        return requirements

    def analyze_current_dependencies(self) -> Dict[str, Dict]:
        """
        Analyze current project dependencies.

        Returns:
            Dict with dependency analysis
        """
        req_txt = self.parse_requirements_txt()
        pyproject = self.parse_pyproject_toml()

        # Merge dependencies
        all_deps = {**req_txt, **pyproject}

        analysis = {
            'total': len(all_deps),
            'installed': {},
            'missing': [],
            'sources': {
                'requirements.txt': len(req_txt),
                'pyproject.toml': len(pyproject)
            }
        }

        for pkg, spec in all_deps.items():
            if pkg in self.installed_packages:
                analysis['installed'][pkg] = {
                    'version': self.installed_packages[pkg],
                    'specifier': spec,
                    'satisfies': VersionSpecifier.satisfies(
                        self.installed_packages[pkg], spec
                    ) if spec else True
                }
            else:
                analysis['missing'].append(pkg)

        return analysis

    def check_compatibility(self, new_deps: List[str], python_version: str = "3.11") -> Dict:
        """
        Check compatibility of new dependencies.

        Args:
            new_deps: List of new dependencies with specifiers
            python_version: Target Python version

        Returns:
            Compatibility analysis dict
        """
        analysis = {
            'python_version': python_version,
            'compatible': [],
            'warnings': [],
            'errors': []
        }

        for dep in new_deps:
            # Parse dependency
            match = re.match(r'([a-zA-Z0-9_-]+)([><=~!].+)?', dep)
            if not match:
                analysis['errors'].append(f"Invalid dependency format: {dep}")
                continue

            pkg = match.group(1).lower()
            spec = match.group(2) or ''

            # Check if already installed
            if pkg in self.installed_packages:
                current_ver = self.installed_packages[pkg]
                if spec and not VersionSpecifier.satisfies(current_ver, spec):
                    analysis['warnings'].append(
                        f"{pkg}: Current version {current_ver} doesn't satisfy {spec}"
                    )
                else:
                    analysis['compatible'].append(f"{pkg}{spec}")
            else:
                analysis['compatible'].append(f"{pkg}{spec}")

        return analysis

    def detect_conflicts(self, new_deps: List[str]) -> List[Dict]:
        """
        Detect version conflicts with new dependencies.

        Args:
            new_deps: List of new dependencies

        Returns:
            List of conflicts detected
        """
        conflicts = []
        current_deps = {**self.parse_requirements_txt(), **self.parse_pyproject_toml()}

        for dep in new_deps:
            match = re.match(r'([a-zA-Z0-9_-]+)([><=~!].+)?', dep)
            if not match:
                continue

            pkg = match.group(1).lower()
            new_spec = match.group(2) or ''

            if pkg in current_deps:
                current_spec = current_deps[pkg]
                if current_spec != new_spec:
                    conflicts.append({
                        'package': pkg,
                        'current': current_spec,
                        'new': new_spec,
                        'type': 'version_mismatch'
                    })

        return conflicts

    def build_dependency_tree(self, max_depth: int = 2) -> str:
        """
        Build simple dependency tree.

        Args:
            max_depth: Maximum depth to traverse

        Returns:
            Tree representation as string
        """
        deps = {**self.parse_requirements_txt(), **self.parse_pyproject_toml()}

        tree_lines = ["Dependency Tree:", ""]
        for pkg, spec in sorted(deps.items()):
            version = self.installed_packages.get(pkg, "not installed")
            tree_lines.append(f"├── {pkg}{spec} (installed: {version})")

        return "\n".join(tree_lines)

    def generate_report(self, output_format: str = "markdown") -> str:
        """
        Generate dependency analysis report.

        Args:
            output_format: Output format (markdown, json)

        Returns:
            Report string
        """
        analysis = self.analyze_current_dependencies()

        if output_format == "json":
            return json.dumps(analysis, indent=2)

        # Markdown report
        report = ["# Dependency Analysis Report", ""]

        report.append(f"## Summary")
        report.append(f"- Total dependencies: {analysis['total']}")
        report.append(f"- Installed: {len(analysis['installed'])}")
        report.append(f"- Missing: {len(analysis['missing'])}")
        report.append("")

        if analysis['installed']:
            report.append("## Installed Dependencies")
            for pkg, info in sorted(analysis['installed'].items()):
                status = "✅" if info['satisfies'] else "⚠️"
                report.append(f"- {status} {pkg}=={info['version']} (requires: {info['specifier']})")
            report.append("")

        if analysis['missing']:
            report.append("## Missing Dependencies")
            for pkg in analysis['missing']:
                report.append(f"- ❌ {pkg}")
            report.append("")

        report.append(self.build_dependency_tree())

        return "\n".join(report)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Dependency analysis tool")
    parser.add_argument('--analyze', action='store_true', help="Analyze current dependencies")
    parser.add_argument('--check-compatibility', action='store_true', help="Check new dep compatibility")
    parser.add_argument('--check-conflicts', action='store_true', help="Detect version conflicts")
    parser.add_argument('--full-report', action='store_true', help="Generate full report")
    parser.add_argument('--project-root', type=Path, default=Path.cwd(), help="Project root directory")
    parser.add_argument('--new-deps', type=str, help="Comma-separated new dependencies")
    parser.add_argument('--python-version', type=str, default="3.11", help="Target Python version")
    parser.add_argument('--output', type=Path, help="Output file path")
    parser.add_argument('--output-format', choices=['markdown', 'json', 'tree'], default='markdown')

    args = parser.parse_args()

    analyzer = DependencyAnalyzer(args.project_root)

    if args.analyze or args.full_report:
        report = analyzer.generate_report(args.output_format)
        if args.output:
            args.output.write_text(report)
            print(f"Report written to {args.output}")
        else:
            print(report)

    if args.check_compatibility:
        if not args.new_deps:
            print("Error: --new-deps required for compatibility check")
            sys.exit(1)

        new_deps = [d.strip() for d in args.new_deps.split(',')]
        result = analyzer.check_compatibility(new_deps, args.python_version)

        print(f"\nCompatibility Check (Python {result['python_version']})")
        print(f"Compatible: {len(result['compatible'])}")
        print(f"Warnings: {len(result['warnings'])}")
        print(f"Errors: {len(result['errors'])}")

        if result['compatible']:
            print("\n✅ Compatible:")
            for dep in result['compatible']:
                print(f"  - {dep}")

        if result['warnings']:
            print("\n⚠️  Warnings:")
            for warning in result['warnings']:
                print(f"  - {warning}")

        if result['errors']:
            print("\n❌ Errors:")
            for error in result['errors']:
                print(f"  - {error}")

    if args.check_conflicts:
        if not args.new_deps:
            print("Error: --new-deps required for conflict check")
            sys.exit(1)

        new_deps = [d.strip() for d in args.new_deps.split(',')]
        conflicts = analyzer.detect_conflicts(new_deps)

        print(f"\nConflict Detection")
        print(f"Conflicts found: {len(conflicts)}")

        if conflicts:
            print("\n⚠️  Conflicts:")
            for conflict in conflicts:
                print(f"  - {conflict['package']}: current={conflict['current']}, new={conflict['new']}")
        else:
            print("\n✅ No conflicts detected")


if __name__ == "__main__":
    main()
