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
