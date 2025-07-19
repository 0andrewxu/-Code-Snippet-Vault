Code Snippet Vault
===================

Personal CLI to capture, tag, and search code snippets locally.

Goals
- Quick add from stdin or a file
- Tags, language detection, notes
- Fuzzy search and filters
- Plain JSON storage under `vault/`

Status
- WIP, building iteratively in spare time.

Usage
- Add: `echo "print('hi')" | python -m snipvault.cli add --tags py,util --note "print hello"`
- Search: `python -m snipvault.cli search hello`
