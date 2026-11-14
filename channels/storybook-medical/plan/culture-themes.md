# Culture themes: music follows the story's place (a culture font only where it truly fits)

User, 2026-11-09 (HCS04 rough cut): "for each country we create the story about we use the theme and music about
it. Some music can be shared across multiple cultures and countries. The font of the subtitles also can follow the
theme."

Set per episode in `episode.json`: `"theme": {"culture": "...", "font": "..."}`. **Fonts (user, 2026-11-09): keep the
channel's original Montserrat Black for captions and stamps; use a culture font only where it truly fits** (Lalezar
for the Persian story, approved). A plain SemiBold caption and IM Fell English for Onesimus were tried the same day
and dropped. Name tags stay Montserrat. Music always follows the culture: prompts name its real instruments and mode,
and say "no Western orchestra" when the culture isn't Western.

| Theme | Stories | Font (captions + stamps) | Music (prompt core) | Shared with |
|---|---|---|---|---|
| **persia** | HCS04 golden eye (Burnt City), HCS05 al-Razi, Avicenna | `lalezar` (Persian display face with Latin letters) | santur, setar / tar, ney, daf + tombak; dastgah Homayoun or Shur | Arab / Islamic golden age (oud, qanun, maqam) when the story is set there |
| **colonial-english** | HCS06 Onesimus (Boston 1721), Montagu | `montserrat` (IM Fell tried, dropped) | harpsichord, solo cello, baroque chamber strings | 1700s Britain and its colonies |
| **modern-default** | Forssmann 1929, Marshall 1984, Bågenholm 1999, Snow 1854, Semmelweis 1847 | `montserrat` (channel default) | per story (period chamber / modern score) | everything without a strong cultural setting |
| **caribbean-colonial** | HCS07 Finlay (Havana 1881-1900) | `montserrat` | slow Cuban habanera / contradanza in a minor key: solo piano, tres guitar, soft guiro and claves; 19th-century Western instruments are right here | Spanish colonial Caribbean, 1800s Latin America |
| *(to add when a story needs it)* | West Africa, India (Sushruta), Nordic, East Asia | pick a Google font with Latin letters; only if it truly fits the story; test at 88 px with the 14 px stroke | the region's own instruments | |

**Check before using a font:** it must exist in `@remotion/google-fonts` and contain Latin letters, and a caption page
must stay legible on a phone at the Short's size. Add it to `THEME_FONTS` in `remotion/StorybookShort.tsx` with its
weight and size scale.
