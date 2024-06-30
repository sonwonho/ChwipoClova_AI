import pdfkit


class Web2PDF(pdfkit.PDFKit):
    def command(self, path=None):
        return ["xvfb-run"] + super().command(path)


def get_pdf(url):
    options = {
        "margin-top": "0",
        "margin-right": "0",
        "margin-bottom": "0",
        "margin-left": "0",
        "disable-smart-shrinking": True,
    }
    r = Web2PDF(url, "url", options)
    return r.to_pdf()


if __name__ == "__main__":
    url = "www.google.com"

    result = get_pdf(url)
    print(result)
