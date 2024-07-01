import asyncio

from playwright.async_api import async_playwright


async def get_pdf(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        await page.emulate_media(media="screen")
        pdf_bytes = await page.pdf(prefer_css_page_size=True)
        await browser.close()
        return pdf_bytes


if __name__ == "__main__":
    # Example usage
    url = "https://www.naver.com"
    # output_path = "html-to-pdf-output.pdf"
    b = asyncio.run(get_pdf(url))
    print(b)
