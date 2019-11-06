# -*- coding: utf-8 -*-
#! /usr/bin/python
# run with python label/populate_massachusetts_home_scorecard.py


from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer,Table,TableStyle, BaseDocTemplate, Frame, PageTemplate, FrameBreak, NextPageTemplate, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import letter, A4
import pkg_resources
from reportlab.lib import colors

PAGE_HEIGHT=defaultPageSize[1]
PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()


IMG_PATH = pkg_resources.resource_filename('label', 'images/')
FONT_PATH = pkg_resources.resource_filename('label', '.fonts/')
CUSTOM_LGREEN = colors.Color(red=(209.0/255),green=(229.0/255),blue=(202.0/255))
CUSTOM_DGREEN = colors.Color(red=(65.0/255),green=(173.0/255),blue=(73.0/255))
CUSTOM_MGREEN = colors.Color(red=(146.0/255),green=(200.0/255),blue=(74.0/255))
CUSTOM_LORANGE = colors.Color(red=(242.0/255),green=(151.0/255),blue=(152.0/255))
CUSTOM_YELLOW = colors.Color(red=(254.0/255),green=(230.0/255),blue=(153.0/255))

def myFirstPage(canvas, doc):
 canvas.saveState()
 canvas.setFont('Times-Bold',16)

 canvas.setFont('Times-Roman',9)

 canvas.restoreState()




def myLaterPages(canvas,doc):
    canvas.saveState()
    canvas.setFont('Times-Roman',9)

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


def create_pdf():
  
    Story = []
    document = BaseDocTemplate('test.pdf',pagesize=letter,rightMargin=20,leftMargin=20,topMargin=20,bottomMargin=20)
    ##HEADER
    logo = IMG_PATH+"logo.jpg"
    home_energy_use =IMG_PATH+'home_energy_use.png'
    img_logo = Image(logo,4*cm,4*cm)
    img_home = Image(home_energy_use,4*cm,4*cm)
    data =[[img_logo,['Your Massachusetts Home Scorecard','This scorecard compares home energy use and carbon footprint to an average home in MA, and shows improvements based on recommended technology.'],img_home]]

    header_table = Table(data,
                    colWidths=[5*cm,25*cm,5*cm],
                    rowHeights=[8*cm])
    Story.append(header_table)
    ##creating frames
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

 
    style = styles["Normal"]
    #populate story with paragraphs
    
    # print(Story)
    document.build(Story)#, onFirstPage=myFirstPage, onLaterPages=myLaterPages


if __name__ == '__main__':
    create_pdf()