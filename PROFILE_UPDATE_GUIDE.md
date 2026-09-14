# Profile update guide

The public profile is rendered from `README.md`. Use the patterns below to keep it consistent and easy to maintain.

## Add an accepted article

Find this marker in `README.md`:

```html
<!-- Add newly accepted articles immediately below this comment. -->
```

Paste one numbered Markdown citation directly below it:

```markdown
1. **Hassan, M.**, Coauthor, A., & Coauthor, B. (YEAR). *Article title*. **Journal Name**. Accepted for publication. [DOI](https://doi.org/DOI-HERE)
```

Renumber the remaining items. Do not add a total publication count to the profile; it becomes outdated quickly.

## Add a published article

Find this marker:

```html
<!-- Add newly selected published articles immediately below this comment. -->
```

Use:

```markdown
1. **Hassan, M.**, Coauthor, A., & Coauthor, B. (YEAR). *Article title*. **Journal Name**, volume, article/page range. [DOI](https://doi.org/DOI-HERE)
```

Keep only selected work on the profile and use Google Scholar for the full record.

## Add a research figure

Use a stable raw GitHub URL and provide meaningful alternative text:

```html
<a href="LINK-TO-FIGURE-IN-REPOSITORY">
  <img src="RAW-GITHUB-IMAGE-URL" width="100%" alt="Plain-language description of the figure">
</a>
<br><sub><b>Short figure title</b><br>One-line explanation</sub>
```

Add figures in pairs so the two-column gallery stays balanced.

## Add a research software project

Copy one `<td width="50%" valign="top">...</td>` block from the **Selected research software** table. Include:

1. A linked project name.
2. A two-sentence maximum description focused on the research contribution.
3. Three short method/domain tags.

Add project cards in pairs. Avoid placeholders, claims without evidence, and large collections of decorative badges.

## Final checklist

- Keep the strongest and most recent work near the top.
- Prefer actual research results over generic GitHub statistics.
- Confirm every DOI, repository link, and figure URL.
- Do not upload a CV containing personal phone numbers or referees' contact details.
- Preview both GitHub light and dark modes before publishing.
- Commit with a focused message, for example: `docs: add new accepted article`.
