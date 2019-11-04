# -*- coding: utf-8 -*-
#! /usr/bin/python
# run with python label/populate_massachusetts_home_scorecard.py


from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, BaseDocTemplate, Frame, PageTemplate, FrameBreak, NextPageTemplate, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, A4

PAGE_HEIGHT=defaultPageSize[1]
PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()

Title = "Hello world"
pageinfo = "platypus example"
def myFirstPage(canvas, doc):
 canvas.saveState()
 canvas.setFont('Times-Bold',16)
 canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-100, Title)
 canvas.setFont('Times-Roman',9)
 canvas.drawString(inch, 0.75 * inch, "First Page / %s" % pageinfo)
 canvas.restoreState()




def myLaterPages(canvas,doc):
    canvas.saveState()
    canvas.setFont('Times-Roman',9)
    canvas.drawString(inch,0.75*inch,"Page %d %s"%(doc.page,pageinfo))
    canvas.restoreState()

def footer(canvas,doc):
    canvas.saveState()
   
    styles = getSampleStyleSheet()
 
    # Header
    footer = Paragraph('Home Owner | 123 Main Street , Whatley, MA 01093 Brought to you by', styles['Normal'])
    w, h = footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, h)
    # Release the canvas
    canvas.restoreState()   


def go():
  
    document = BaseDocTemplate('test.pdf',pagesize=letter,rightMargin=20,leftMargin=20,topMargin=20,bottomMargin=20)
    page1_frames =[]
    page1_frameCount =3
    frameWidth = document.width/page1_frameCount
    frameHeight = document.height-inch
    bottom_margin =document.bottomMargin+0.5*inch

    for frame in range(page1_frameCount):
        leftMargin = document.leftMargin + frame*frameWidth
        column =Frame(leftMargin, bottom_margin,frameWidth,frameHeight)
        page1_frames.append(column)
    

    page2_frames =[]
    page2_frameCount =2
    frameWidth2 = document.width/page2_frameCount
    frameHeight = document.height-.5*inch

    for frame in range(page2_frameCount):
        leftMargin = document.leftMargin + frame*frameWidth2
        column =Frame(leftMargin, document.bottomMargin,frameWidth2,frameHeight)
        page2_frames.append(column)

    templates= []
    templates.append(PageTemplate(frames=page1_frames,id='firstPage',onPage=footer))
    templates.append(PageTemplate(frames=page2_frames,id='secondPage',onPage=footer))

    document.addPageTemplates(templates)

    Story = []
    style = styles["Normal"]
    #populate story with paragraphs
    for i in range(20):
        bogustext = ("This is Paragraph number %s. " % i) *20
        p = Paragraph(bogustext, style)
        if i==10:            
            Story.append(NextPageTemplate('secondPage'))
            Story.append(FrameBreak())
            Story.append(Paragraph("yes",style))
        Story.append(p)
        Story.append(Spacer(1,0.2*inch))
    # print(Story)
    document.build(Story)#, onFirstPage=myFirstPage, onLaterPages=myLaterPages


if __name__ == '__main__':
    go()