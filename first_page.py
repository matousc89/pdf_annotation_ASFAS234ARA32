"""
First you need to install the IBM PLex Sans font.
"""
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.lib import utils
from reportlab.lib.colors import blue, black, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Plex', 'IBMPlexSans-Regular.ttf'))

def create_first_page():
    TOP = (29.7 - 5) * cm
    LEFT = 4 * cm
    RIGHT = (21 - 4) * cm
    FONT_SIZE = 10
    FONT = "Plex"
    text = "PyJournal year 2020"
    image_path = "logo.png"

    # text right
    font = FONT
    font_size = FONT_SIZE
    canvas = Canvas("first_page.pdf", pagesize=A4)
    canvas.setFont(font, font_size)
    canvas.setFillColor(black)
    text_width = pdfmetrics.stringWidth(text, font, font_size)
    text_height = int(FONT_SIZE * 1.2) # TODO not correct
    canvas.drawString(RIGHT - text_width, TOP - text_height, text)

    # logo
    img = utils.ImageReader(image_path)
    img_width, img_height = img.getSize()
    aspect = img_height / float(img_width)
    display_width = 100
    display_height = (display_width * aspect)
    canvas.drawImage(image_path, LEFT, TOP - display_height,
                        width=display_width, height=display_height, mask="auto")

    canvas.save()


def create_pagenumbers(first_number, last_number):
    WIDTH = 21 * cm
    TOP = (29.7 - 5) * cm
    LEFT = 4 * cm
    RIGHT = WIDTH - 4 * cm
    FONT_SIZE = 9
    FONT = "Plex"

    FROM_BOTTOM = 1.5 * cm
    font = FONT
    font_size = FONT_SIZE
    canvas = Canvas("pagenumbers.pdf", pagesize=A4)
    canvas.setFillColor(black)
    text_height = int(font_size * 1.2)  # TODO not correct

    for k in range(first_number, last_number):
        canvas.setFont(font, font_size)
        text = str(k)
        text_width = pdfmetrics.stringWidth(text, font, font_size)
        canvas.drawString((WIDTH // 2) - text_width, FROM_BOTTOM, text)
        canvas.showPage()

    canvas.save()

def insert_first_page(paper_path, output_path):
    create_first_page()

    output = PdfFileWriter()
    paper = PdfFileReader(open(paper_path, "rb"))
    page_num = paper.getNumPages()
    overlay = PdfFileReader(open("first_page.pdf", "rb"))

    for pn in range(page_num):
        paper_page = paper.getPage(pn)
        if pn == 0:
            overlay_page = overlay.getPage(pn)
            paper_page.mergePage(overlay_page)
        output.addPage(paper_page)

    outputStream = open(output_path, "wb")
    output.write(outputStream)
    outputStream.close()


def insert_pagenumbers(paper_path, output_path, start_page=False, end_page=False,
                   first_number=1):
    output = PdfFileWriter()
    paper = PdfFileReader(open(paper_path, "rb"))
    page_num = paper.getNumPages()

    start_page = 1 if not start_page else start_page
    end_page = page_num if not end_page else end_page
    last_number = first_number + end_page - start_page + 1

    create_pagenumbers(first_number, last_number)

    overlay = PdfFileReader(open("pagenumbers.pdf", "rb"))

    number = 0
    for pn in range(page_num):
        paper_page = paper.getPage(pn)
        if start_page <= pn + 1 <= end_page:
            overlay_page = overlay.getPage(number)
            paper_page.mergePage(overlay_page)
            number += 1
        output.addPage(paper_page)

    outputStream = open(output_path, "wb")
    output.write(outputStream)
    outputStream.close()




if __name__ == "__main__":
    PAPER_PATH = "pyjournal_latex_template.pdf"
    OUTPUT_PATH = "output.pdf"

    #insert_first_page(PAPER_PATH, OUTPUT_PATH)

    insert_pagenumbers(PAPER_PATH, OUTPUT_PATH, start_page=2, end_page=False, first_number=2)



