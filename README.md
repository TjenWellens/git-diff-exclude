# git-diff-exclude
`git diff | python ./script.py "^[+-]import"` to not show blocks with only lines changed that are import statements

imagine you have a diff output:
```
diff --git a/file.txt b/file.txt
index 0b669b6..54652ef 100644
--- a/file.txt
+++ b/file.txt
@@ -1,3 +1,4 @@
+import test
 1
 2
 3
@@ -7,4 +8,5 @@
 7
 8
 9
-10
\ No newline at end of file
+10
+bar
\ No newline at end of file
```

but you want to ignore all import statements line changes
`git diff | python ./script.py "^[+-]import"` gives you following output:

```
diff --git a/file.txt b/file.txt
index 0b669b6..54652ef 100644
--- a/file.txt
+++ b/file.txt
@@ -7,4 +8,5 @@
 7
 8
 9
-10
\ No newline at end of file
+10
+bar
```

More detailed: 
* if all line changes in a block (`@@`) match the pattern, the block is excluded from diff output
* if all blocks in a file are excluded, the entire file is excluded from diff output

tip: create an alias
`alias gde='python ~/git-diff-exclude/script.py'` (make it permanent by putting it in `~/.bash_profile`)
so you can call `git diff | gde "^[+-]import"`

useful patterns:
* `"^[+-]\s*$"` empty lines
* `"^[+-]\s*}else$"`, `"^[+-]\s*}$"`, `"^[+-]\s*else$"` for `else {` <-> `else`+ newline + `{`

[regex format](https://docs.python.org/2/library/re.html#regular-expression-syntax)

## Contributing
see [contributing.md](./CONTRIBUTING.md)