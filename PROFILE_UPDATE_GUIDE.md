# Profile update guide

The public profile is rendered from `README.md`. Publication highlights are automatically refreshed every Monday from the public ORCID record and the accepted-publication feed.

## Replace the profile portrait

Replace `assets/mahbub-hassan-professional.png` with a new PNG using the same filename. A portrait-oriented image works best. The README controls its displayed size, so no other file needs to be edited.

This image is public because it is stored in the profile repository. The CV remains private and should not be added to this repository.

## Add or remove a skill logo

In the **Methods and research tools** section of `README.md`, copy one existing logo line and change its image URL, `alt`, and `title`. Use an official or stable icon source and include only tools you actively use. Keep the main logo row to roughly 8–12 items; add specialised transportation or analysis software to the compact badge row below it.

## Add an accepted article

Open `data/accepted_publications.json` and add one object:

```json
{
  "authors": "**Hassan, M.**, Coauthor, A., & Coauthor, B.",
  "year": 2026,
  "title": "Article title",
  "journal": "Journal Name",
  "doi": "10.xxxx/example"
}
```

Commit the data file. GitHub Actions will validate it, regenerate the accepted-paper list, update the accepted-venue badges, and commit the refreshed README. Leave `doi` empty until one is assigned.

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

Published venue badges come from ORCID automatically. Add a new published work to the public ORCID record; the Monday workflow will include its journal. Use the **Update publication highlights** workflow's `Run workflow` button for an immediate refresh.

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
