# Setup

[Install uv](https://docs.astral.sh/uv/#installation) (Python package manager with global cache, written in Rust)

`uv sync` to install dependencies

The script uses [Playwright](https://playwright.dev/python/docs/library) for browser automation.

[Install browser(s)](https://playwright.dev/python/docs/browsers#install-browsers):
`uvx playwright install [firefox|webkit|chromium]`

Docs say `playwright install`, but it doesn't work for me, as `uv add` doesn't install a global command.

# Usage

Chromium works, Firefox not always, Webkit not tested.

Step through the cells more or less in order (skip closing the browser at the beginning obviously), replace values (strings/numbers) with the ones you need. If necessary or more convenient, navigate manually. The most important automated part is downloading all syllabuses and extracting effects, the rest can be easily done manually.

To scrape elective courses, navigate manually and then use the flow starting at "Eksportuj do CSV" - it should work the same, but there might still be some bugs because the data returned by USOS is formatted slightly differently.

The final output is `./output.csv`, which can be directly pasted into the table in your text editor of choice.
