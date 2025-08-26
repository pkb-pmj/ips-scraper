# %%
from playwright.async_api import async_playwright
import pandas as pd
import io
import pdfplumber

# %%
playwright = await async_playwright().start()
# Use playwright.chromium, playwright.firefox or playwright.webkit
# Pass headless=False to launch() to see the browser UI
browser = await playwright.firefox.launch(headless=False)
page = await browser.new_page()

# %%
await page.close()
await browser.close()
await playwright.stop()

# %%
await page.goto("https://asystent.usos.pw.edu.pl/programoffer/studiestype/index/rodzaj/W/tab/1")

# %%
await page.get_by_label("Wpisz frazę").fill("inżynieria i analiza danych")
await page.get_by_role("button", name="Szukaj").click()

# %%
select = page.get_by_label("Wybierz cykl dydaktyczny")
options = await select.locator("option").all()

# %%
option = options[0]
# %%
await select.select_option(value=await option.get_attribute("value"))
# await page.locator('[id="grid_studiestype"]').wait_for(state="detached")
# print("table replaced")
await page.locator('[id="oc_loader"]').wait_for(state="hidden")
print("finished")

# %%
await page.locator("table").locator("tbody").locator("tr").nth(1).locator("a").click()

# %%
await page.get_by_text("Plan studiów").click()

# %%
# Start waiting for the download
async with page.expect_download() as download_info:
    # Perform the action that initiates download
    await page.get_by_text("Eksportuj do CSV").first.click()
download = await download_info.value

# Wait for the download process to complete and save the downloaded file somewhere
filepath = "./downloads/" + download.suggested_filename
await download.save_as(filepath)

# %%
with open(filepath, "r", encoding="windows-1250") as f:
    text = f.read()

# %%
lines = text.split(";\n")

# %%
breakpoints = [i for i, l in enumerate(lines) if l.endswith('\n')]
blocks = [lines[i + 1:j] for i, j in zip(breakpoints, breakpoints[1:] + [len(lines)])]
headers = [lines[i] for i in breakpoints]
course = lines[0].strip()

# %%
block = blocks[1]
header = headers[1]
lines = [l.replace("\n", " ") for l in block]

# %%
sem_num = int(header.split()[1])
sem_code = header.split()[2].strip()

# %%
csv_chunk = "\n".join(lines)

# %%
df = pd.read_csv(io.StringIO(csv_chunk), sep=";")

# %%
cols = df.loc[:, "Ects":"Suma"].columns
df[cols]= df[cols].fillna(0).astype(int)

# %%
cols = df.loc[:, :"Kod"].columns
df[cols] = df[cols].fillna("").astype(str)

# %%
async def download_syllabus(code: str):
    await page.locator("tr").filter(has_text=code).locator('[data-original-title="Wydruk sylabusa"]').click()
    await page.get_by_text("Generuj raport").wait_for(state="visible")

    await page.get_by_label("Część").select_option(label="Część I")
    await page.get_by_label("Język").select_option(label="polski")
    async with page.expect_download() as download_info:
        await page.get_by_text("Generuj raport").click()
    download = await download_info.value
    filepath = "./downloads/sylabus/" + code + ".pdf"
    await download.save_as(filepath)
    await page.get_by_text("×").filter(visible=True).click()

# %%
def extract_effects_from_syllabus(code: str):
    filepath = "./downloads/sylabus/" + code + ".pdf"
    with pdfplumber.open(filepath) as pdf:
        tables = [t for p in pdf.pages for t in p.extract_tables()]
    effects = set(e for t in tables for r in t if r[0] == "Powiązane kierunkowe efekty uczenia się" for e in r[-1].split(", "))
    return effects

# %%
for code in df["Kod"][df["Kod"] != ""]:
    await download_syllabus(code)
    effects = extract_effects_from_syllabus(code)
    print(code, effects)

# %%
