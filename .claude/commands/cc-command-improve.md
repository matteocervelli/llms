---
description: Improve an existing Claude Code command based on user feedback or requirements
argument-hint: <command-name> [improvement-description]
---

# Improve Claude Code Command: $1

Improve an existing slash command by analyzing its current implementation and applying enhancements based on provided input.

## Usage

```bash
/cc-command-improve my-command "Add parameter validation and better error handling"
/cc-command-improve run-tests "Add support for pytest markers and coverage reporting"
/cc-command-improve generate-docs "Include API examples and improve formatting"
```

## Process

**⚠️ RECOMMENDED: Use Plan Mode (Shift+Tab twice) for this command to review the improvement strategy before making changes.**

### 1. Load Existing Command

```bash
# Find the command in catalog
!python -m src.tools.command_builder.main list --search "$1"
```

Read the existing command file and analyze its current implementation:
- Frontmatter configuration
- Current functionality
- Parameters and options
- Bash commands
- File references
- Documentation quality

### 2. Analyze Improvement Request

Use sequential-thinking-mcp to understand the improvement request:

1. **What is being requested?**
   - New features to add
   - Problems to fix
   - Quality improvements
   - Performance optimizations

2. **How does it affect the command?**
   - Changes to parameters
   - New bash commands needed
   - Additional file references
   - Template changes
   - Documentation updates

3. **What are the constraints?**
   - Backward compatibility
   - Existing dependencies
   - Command naming conventions
   - Template limitations

### 3. Design Improvements

Plan the changes following best practices:

- **Functionality**: Add requested features while maintaining existing behavior
- **Validation**: Add input validation and error handling
- **Documentation**: Improve descriptions and usage examples
- **Performance**: Optimize bash commands and file operations
- **Usability**: Better argument hints and clear examples

Design considerations:

- Keep commands under 500 lines (split if needed)
- Follow Claude Code command conventions
- Follow naming convention: **[context-]object-action[-modifier]** pattern
- Maintain clarity and readability
- Add comprehensive examples

#### Naming Convention Validation

When improving commands, ensure they follow the **[context-]object-action[-modifier]** naming pattern:

**Pattern Components:**

- **context** (optional): cc-, gh-, project-, pr-, code-, feature-, issue-, ui-, infrastructure-
- **object** (required): What you're working with (command, skill, feature, issue, etc.)
- **action** (required): What you're doing (create, improve, fix, implement, analyze, etc.)
- **modifier** (optional): Additional specifier

**Good Examples:**

- `cc-command-create`, `cc-command-improve` ✓
- `feature-implement`, `issue-fix` ✓
- `gh-milestone-create`, `pr-analyze-failure` ✓

**If improving a non-compliant command name**, consider suggesting a rename:

- `create-command` → `command-create` (object-action order)
- `setup-infrastructure` → `infrastructure-setup` (object-action order)
- `code-quality` → `code-analyze-quality` (add action verb)

#### Using Plan Mode for Design

Plan Mode is particularly valuable during the improvement analysis:

1. Activate Plan Mode (Shift+Tab twice) before analyzing the command
2. Review the existing command structure without making changes
3. Evaluate proposed improvements and their impact
4. Confirm the design approach with the user
5. Exit Plan Mode (Ctrl+D) to implement the improvements

**Key Limitation:** You cannot force Plan Mode programmatically within a slash command. Plan Mode is a user-controlled permission mode that must be manually activated.

**Why Plan Mode?**

- Prevents accidental modifications during analysis
- Allows safe exploration of command structure
- Enables thorough review before implementation
- Provides read-only context for decision-making

### 4. Implement Improvements

Apply changes to the command:

1. **Update Configuration**
   - Modify frontmatter (description, arguments, allowed-tools)
   - Add/update parameters
   - Update bash commands
   - Add file references if needed

2. **Enhance Content**
   - Improve documentation sections
   - Add usage examples
   - Include error handling guidance
   - Add tips and best practices

3. **Validate Changes**
   - Check command syntax
   - Verify bash commands are safe
   - Validate file references exist
   - Ensure template consistency

```bash
# Validate the improved command
!python -m src.tools.command_builder.main validate .claude/commands/$1.md
```

### 5. Test Improvements

Create a test plan:

1. **Functionality Tests**
   - Test with original usage patterns
   - Test with new features
   - Test edge cases
   - Test error conditions

2. **Compatibility Tests**
   - Verify backward compatibility
   - Check integration with other commands
   - Test in different project contexts

3. **Documentation Tests**
   - Verify examples work
   - Check argument hints are clear
   - Validate usage instructions

### 6. Document Changes

Update related documentation:

- Create backup of original command (optional)
- Document what changed and why
- Update usage examples
- Add migration notes if needed

### 7. Finalize

```bash
# Sync catalog to reflect changes
!python -m src.tools.command_builder.main sync

# Show the updated command
!python -m src.tools.command_builder.main list --search "$1"
```

Provide summary:
- What was improved
- New features added
- Breaking changes (if any)
- Migration guide (if needed)
- Usage examples with new features

## Improvement Categories

### Feature Additions
- Add new parameters or options
- Include additional bash commands
- Reference new files or documentation
- Add thinking mode for complex operations

### Quality Improvements
- Better error handling
- Input validation
- Clearer documentation
- More comprehensive examples
- Better argument hints

### Performance Optimizations
- Optimize bash commands
- Reduce redundant operations
- Improve file handling
- Better caching strategies

### Usability Enhancements
- Clearer naming
- Better prompts
- Interactive confirmations
- Progress indicators
- Better feedback messages

## Examples

### Example 1: Add Parameter Validation

```bash
/cc-command-improve my-command "Add validation for required parameters and show error messages"
```

This would:
- Add parameter validation logic
- Include error messages for missing params
- Add usage examples for correct syntax
- Update argument hints

### Example 2: Add Testing Support

```bash
/cc-command-improve run-tests "Add support for running specific test files and coverage reporting"
```

This would:
- Add parameters for test file selection
- Include coverage reporting commands
- Add examples for different test scenarios
- Update documentation with test options

### Example 3: Improve Documentation

```bash
/cc-command-improve generate-docs "Add API examples and improve formatting"
```

This would:
- Include API usage examples
- Improve markdown formatting
- Add more comprehensive descriptions
- Include troubleshooting section

### Example 4: Add Integration

```bash
/cc-command-improve deploy "Integrate with CI/CD pipeline and add health checks"
```

This would:
- Add bash commands for CI/CD integration
- Include health check commands
- Add file references for config files
- Document deployment process

## Best Practices

- **Use Plan Mode**: Activate Plan Mode before running this command to review the improvement strategy safely before implementation
- **Preserve Existing Functionality**: Don't break existing usage patterns
- **Document Changes**: Clearly explain what changed and why
- **Test Thoroughly**: Verify all existing and new features work
- **Maintain Clarity**: Keep commands clear and easy to understand
- **Follow Conventions**: Use established patterns from other commands
- **Add Examples**: Provide comprehensive usage examples
- **Version Aware**: Consider backward compatibility

## Tips

- Review similar commands for improvement ideas
- Use templates as guidance for structure
- Test improvements in isolation first
- Keep improvements focused and incremental
- Document breaking changes clearly
- Provide migration guidance when needed
- Consider user feedback in improvements

## Related Commands

- `/cc-command-create`: Create new commands
- `python -m src.tools.command_builder.main list`: List all commands
- `python -m src.tools.command_builder.main validate`: Validate command files
- `python -m src.tools.command_builder.main sync`: Sync catalog

## Notes

- Always backup complex commands before major changes
- Test improvements in a safe environment first
- Consider creating a new command if changes are too significant
- Keep the original command's scope and purpose intact
- Document improvements in commit messages
