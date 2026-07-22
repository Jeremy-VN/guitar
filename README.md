# Jeremy's Guitar Lessons

A tiny static website: a contents page (`index.html`) that links to each lesson.
Each lesson is a single self-contained HTML file (audio embedded) in `lessons/`.

## View it anywhere (GitHub Pages)
1. Create a free GitHub account (github.com) if you don't have one.
2. Make a new repository — name it e.g. `guitar-lessons`. (Public repo = free Pages.)
3. Upload the contents of this folder (index.html, the lessons/ folder, lessons.json).
   - Easiest: on the repo page, "Add file" -> "Upload files" -> drag everything in.
4. Repo -> Settings -> Pages -> under "Build and deployment", Source = "Deploy from a branch",
   Branch = `main`, folder = `/ (root)` -> Save.
5. Wait ~1 minute. Your site is live at:  https://<your-username>.github.io/guitar-lessons/
   Bookmark that on your phone.

Note: a free (public) repo means anyone with the exact URL can view it. It is not
listed or advertised anywhere, but it is not private. For truly private hosting you'd
need GitHub Pro (private Pages) or a passworded host — happy to set that up instead.

## Add a new lesson later
1. Drop the new lesson's HTML into `lessons/` (e.g. `2026-08-15-topic.html`).
2. Add an entry to `lessons.json` (copy an existing block; newest date first is fine).
3. Re-run `python3 build_index.py` to regenerate `index.html`, or just hand-edit index.html
   (copy one card block and change the date/title/summary/link).
4. Re-upload the changed files to GitHub. Done.
