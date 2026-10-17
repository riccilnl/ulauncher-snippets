# Multiple plain-text phrases in one file

Existing `.j2` snippets and their Jinja variables continue to work as before.

Put one optional `phrases.json` file in the same directory configured in
Ulauncher → Extensions → Snippets → **Snippets Directory** (by default `~/snippets`).

```json
{
  "知道了": "知道了",
  "好了": "好了",
  "继续": "继续",
  "验证通过": "验证通过",
  "复核方案": "请重新审查上述方案，核实事实依据。"
}
```

Open Ulauncher, type `snip`, search for a phrase, select it and press Enter.
It uses the same selected clipboard mode (`wl` for Wayland) as `.j2` files;
return to ChatGPT and paste normally. **It does not type or paste automatically.**

- JSON object keys are menu labels; values are plain text to copy.
- Unicode, multiline text (`\n` in JSON), and punctuation work.
- Change `phrases.json` at any time; the list updates on the next query.
- Invalid JSON is ignored and logged without stopping the extension.
- The extension reads the file locally; nothing is uploaded.
- No additional background process or dependency is introduced.
- JSON phrases are **literal text**, not Jinja templates. Keep variable
  prompts in individual `.j2` files using `{{ vars("project") }}`.

Run tests with `python3 -m unittest discover -s tests -v`.

## Compact categories and search

- Type **snip** with no text: shows only **常用短语** and **变量模板**.
- Select **常用短语** to browse entries in `phrases.json`, or **变量模板**
  to browse the original `.j2` templates. The input shows
  `snip 常用短语/` or `snip 变量模板/`.
- Type after the slash to filter within that category, e.g.
  `snip 常用短语/知道`.
- For the fastest access, search across **both** categories by typing
  `snip 知道`, `snip Cora`, etc., without opening a category.
- Only **five** results are shown at once. Type to narrow a longer list.
- **Backspace** the category text after `snip ` to return to the two
  entry points. You can also close and reopen Ulauncher.
- Existing variable-template, clipboard and notification behavior is unchanged.
- Previous settings for more than five rows are capped at five.

No new dependency or background process is required.

