# %%
from playwright.async_api import async_playwright
import pandas as pd
import io

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
blocks = text.split("Sem: ")

# %%
course = blocks[0].strip().removesuffix(";")

# %%
block = blocks[2]
lines = [l.replace("\n", " ") for l in block.split(";\n")]

# %%
sem_num = int(lines[0].split()[0])
sem_code = lines[0].split()[1].strip()

# %%
start_idx = next(i for i, l in enumerate(lines) if l.startswith("Blok;"))
end_idx = next(i for i, l in enumerate(lines) if "SUMA" in l)

# %%
csv_chunk = "\n".join(lines[start_idx:end_idx+1])

# %%
df = pd.read_csv(io.StringIO(csv_chunk), sep=";")

# %%
cols = df.loc[:, "Ects":"Suma"].columns
df[cols]= df[cols].fillna(0).astype(int)

# %%
cols = df.loc[:, :"Kod"].columns
df[cols] = df[cols].fillna("").astype(str)

# %%
