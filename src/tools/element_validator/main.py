#!/usr/bin/env python3
"""CLI for validating Claude Code elements."""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .validator import ElementValidator, ValidationResult
from .schemas import ElementType


def print_validation_result(result: ValidationResult, verbose: bool = False):
    """Print validation result in a human-readable format."""
    file_name = result.file_path.name if result.file_path else "Unknown"
    element_type = result.element_type.value if result.element_type else "unknown"

    print(f"\n📄 {file_name} ({element_type})")
    print(f"   {result.get_summary()}")

    # Print errors
    if result.errors:
        print(f"\n   ❌ Errors:")
        for error in result.errors:
            location = f" (line {error.line_number})" if error.line_number else ""
            print(f"      • [{error.field}]{location} {error.message}")
            if verbose and error.suggested_fix:
                print(f"        💡 {error.suggested_fix}")

    # Print warnings
    if result.warnings:
        print(f"\n   ⚠️  Warnings:")
        for warning in result.warnings:
            location = f" (line {warning.line_number})" if warning.line_number else ""
            print(f"      • [{warning.field}]{location} {warning.message}")
            if verbose and warning.suggested_fix:
                print(f"        💡 {warning.suggested_fix}")

    # Print frontmatter in verbose mode
    if verbose and result.frontmatter:
        print(f"\n   📋 Frontmatter:")
        for key, value in result.frontmatter.items():
            print(f"      {key}: {value}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Validate Claude Code elements (agents, skills, commands, prompts)"
    )
    parser.add_argument(
        "path",
        type=str,
        help="Path to element file or directory",
    )
    parser.add_argument(
        "--type",
        "-t",
        type=str,
        choices=["agent", "skill", "command", "prompt"],
        help="Element type (auto-detected if not provided)",
    )
    parser.add_argument(
        "--fix",
        "-f",
        action="store_true",
        help="Automatically fix validation errors where possible",
    )
    parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        help="Recursively validate all elements in directory",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed validation information",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Only show files with errors",
    )

    args = parser.parse_args()

    # Convert path to Path object
    path = Path(args.path).expanduser().resolve()

    # Validate path exists
    if not path.exists():
        print(f"❌ Error: Path not found: {path}", file=sys.stderr)
        return 1

    # Parse element type if provided
    element_type = None
    if args.type:
        element_type = ElementType(args.type)

    # Create validator
    validator = ElementValidator()

    # Validate
    if path.is_file():
        # Validate single file
        result = validator.validate_element(path, element_type)

        if not args.quiet or not result.is_valid:
            print_validation_result(result, args.verbose)

        # Apply fixes if requested
        if args.fix and not result.is_valid:
            print(f"\n🔧 Attempting to fix errors...")
            if validator.auto_fix(path, result):
                print(f"✅ Fixes applied to {path.name}")
                # Re-validate
                result = validator.validate_element(path, element_type)
                print(f"\n📄 Re-validation:")
                print_validation_result(result, args.verbose)
            else:
                print(f"⚠️  Could not automatically fix all errors")

        return 0 if result.is_valid else 1

    elif path.is_dir():
        # Validate directory
        results = validator.validate_directory(path, args.recursive)

        if not results:
            print(f"ℹ️  No element files found in {path}")
            return 0

        # Print results
        valid_count = 0
        invalid_count = 0
        warning_count = 0

        for file_path, result in sorted(results.items()):
            if result.is_valid:
                valid_count += 1
                if result.warnings:
                    warning_count += 1
            else:
                invalid_count += 1

            if not args.quiet or not result.is_valid or result.warnings:
                print_validation_result(result, args.verbose)

        # Print summary
        print("\n" + "=" * 60)
        print(f"📊 Summary: {len(results)} files validated")
        print(f"   ✅ Valid: {valid_count}")
        print(f"   ❌ Invalid: {invalid_count}")
        if warning_count:
            print(f"   ⚠️  With warnings: {warning_count}")

        # Apply fixes if requested
        if args.fix and invalid_count > 0:
            print(f"\n🔧 Attempting to fix errors...")
            fixed_count = 0
            for file_path, result in results.items():
                if not result.is_valid:
                    if validator.auto_fix(file_path, result):
                        fixed_count += 1
                        print(f"   ✅ Fixed: {file_path.name}")

            if fixed_count > 0:
                print(f"\n✅ Fixed {fixed_count}/{invalid_count} files")
                print(f"⚠️  Please review changes and re-run validation")
            else:
                print(f"⚠️  Could not automatically fix any files")

        return 0 if invalid_count == 0 else 1

    else:
        print(f"❌ Error: Path is neither a file nor directory: {path}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
