from reportlab.pdfgen import canvas


def hello(c):
    c.drawString(250, 500, "Hello World")


c = canvas.Canvas("hello.pdf")
hello(c)
c.showPage()
c.save()
