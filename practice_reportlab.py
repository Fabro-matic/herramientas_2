#from reportlab.pdfgen import canvas

# def hello(c):
#     c.drawString(100,100,"Hello World")
# c = canvas.Canvas("hello.pdf")
# hello(c)
# c.showPage()
# c.save()

from reportlab.pdfgen import canvas
from reportlab.lib import pdfencrypt

enc=pdfencrypt.StandardEncryption("MIC",canPrint=0)

def hello(c):
 c.drawString(100,100,"¡METELE QUE SON PASTELES!")
c = canvas.Canvas("Un lujo.pdf",encrypt=enc)
hello(c)
c.showPage()
c.save()

