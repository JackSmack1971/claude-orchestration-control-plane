# Git and filesystem safety

- Do not use destructive recovery commands such as `git reset --hard`, broad `git clean`, force-push, or mass checkout/restore to erase work.
- Do not delete untracked user files as a cleanup shortcut.
- Inspect `git status` and the relevant diff before destructive or wide-scope repository changes.
- Preserve unrelated working-tree changes.
- Never rewrite shared history unless the user explicitly requests it and the consequences are understood.
