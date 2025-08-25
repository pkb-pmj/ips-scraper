# %%
from playwright.async_api import async_playwright

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
await download.save_as("./downloads/" + download.suggested_filename)

# %%
