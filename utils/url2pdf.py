import asyncio

from playwright.async_api import async_playwright


async def get_pdf(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0"
        )
        page = await context.new_page()
        await page.goto(url)
        await page.emulate_media(media="screen")
        pdf_bytes = await page.pdf(prefer_css_page_size=True)
        await browser.close()
        return pdf_bytes


async def url_to_pdf(url, output_path):
    pdf_data = await get_pdf(url)
    with open(output_path, "bw") as f:
        f.write(pdf_data)


if __name__ == "__main__":
    # Example usage
    url = "https://www.wanted.co.kr/wd/225097"
    output_path = "html-to-pdf-output.pdf"
    asyncio.run(url_to_pdf(url, output_path))
