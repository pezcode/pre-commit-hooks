Hooks for [pre-commit](http://pre-commit.com).

## Usage

```yaml
- repo: https://github.com/pezcode/pre-commit-hooks
  rev: v1.0.0
  hooks:
    - id: limit-blank-lines
      args: [--max-blank-lines, '2']  # defaults to: 1
      exclude_types: [python]
```

### limit-blank-lines

Limits consecutive empty lines in text files to a selected amount. `--max-blank-lines=0` removes all empty lines. Supports both normal and Windows newline format.
