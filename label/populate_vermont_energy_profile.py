# -*- coding: utf-8 -*-
#! /usr/bin/python
# run with python label/populate_vermont_energy_profile.py

#import time
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.graphics.shapes import Drawing, Rect


#d = Drawing(400,200)
#pc = Pie()
#pc.x = 150
#pc.y = 50
#pc.data = [10,20,30,40,50,60]
#pc.labels = ['a','b','c','d','e','f']
#pc.slices.strokeWidth=0.5
#pc.slices[3].popout = 20
#pc.slices[3].strokeWidth = 2
#pc.slices[3].strokeDashArray = [2,2]
#pc.slices[3].labelRadius = 1.75
#pc.slices[3].fontColor = colors.red
#d.add(pc, '')

#       apply(Drawing.__init__,(self,width,height)+args,kw)
        # adding a pie chart to the drawing 
#        self._add(self,Pie(),name='pie',validate=None,desc=None)


class flowable_fig(Flowable):
    def __init__(self, imgdata):
        Flowable.__init__(self)
        self.img = ImageReader(imgdata)

    def draw(self):
        self.canv.drawImage(self.img, 0, 0, height = -2*inch, width=4*inch)

#class flowable_drawing(Flowable):
#    def __init__(self, drawdata):
#        Flowable.__init__(self)
#        self.draw = Drawing.

#    def draw(self):
#        self.canv.drawImage(self.img, 0, 0, height = -2*inch, width=4*inch)

def myFirstPage(canvas, doc):  
    canvas.saveState()  
    customColor = colors.Color(red=(209.0/255),green=(229.0/255),blue=(202.0/255))
    canvas.setFillColor(colors.Color(red=(209.0/255),green=(229.0/255),blue=(202.0/255)))
    canvas.rect(20,20,570,750,fill=1)
    canvas.restoreState()  

def write_vermont_energy_profile_pdf(data_dict):
    doc = SimpleDocTemplate("label.pdf",pagesize=letter,
                            rightMargin=20,leftMargin=20,
                            topMargin=20,bottomMargin=20)
                            
    font_xxl = 28
    font_xl = 24
    font_l = 14
    font_h = 10
    font_t = 9
    font_normal = 'Helvetica'
    font_bold = 'Helvetica-Bold'
    font_italic = 'Helvetica-Oblique'

    Story=[]
    Story.append(Spacer(1, 12))

    ### HEADER
    vthep_logo = "./images/VHESLogoV4.jpg"
    im = Image(vthep_logo, 1.63*inch, 1.75*inch)
    
    wedge = "./images/wedge.png"
    im2 = Image(wedge, 3.70*inch, 1.70*inch)

    styles = getSampleStyleSheet()
    p = ParagraphStyle('headers', alignment = TA_LEFT, fontSize = font_l, fontName = font_normal, textColor=colors.white)
    p2 = ParagraphStyle('headers', alignment = TA_LEFT, fontSize = font_xxl, fontName = 'Helvetica-Bold', textColor=colors.white)
    #styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT))

    text_use_1 = Paragraph("THIS HOME'S ANNUAL EXPECTED ENERGY COST", p)
    text_use_2 = Paragraph('$'+"{:,}".format(data_dict['score']), p2)

    text_cost_1 = Paragraph("THIS HOME'S ANNUAL EXPECTED ENERGY USE", p)
    text_cost_2 = Paragraph("{:,}".format(data_dict['score_btu'])+'MMBtu', p2)

    header_table = Table([[im, [text_use_1, text_use_2], im2]],
        colWidths=[1.63 * inch, 2.14 * inch, 3.77 * inch],
        rowHeights=[1.75 * inch], spaceBefore=0, spaceAfter=20)
    header_table.setStyle(TableStyle([('BACKGROUND',(1,0),(-2,0),colors.HexColor('#f3901d')),
        ('BACKGROUND',(2,0),(-1,0),colors.HexColor('#41ad49')),
        ('TEXTCOLOR',(1,0),(-1,0),colors.white), 
        ('INNERGRID', (0, 0), (-1, -1), 5, colors.white),
        ('BOX', (0, 0), (-1, -1), 10, colors.white), 
        ('ALIGN', (0,0), (-1,-1), 'CENTER'), 
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE') 
        ]))
    Story.append(header_table)

    ### BODY
    ##BODY LEFT
    p3 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_t, fontName = font_normal, leading = 12, spaceBefore = 24)
    p4 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_h, fontName = font_bold, leading = 12, spaceBefore = 24, spaceAfter = 24)
    p5 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_t, fontName = font_bold, leading = 12)
    p6 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_t, fontName = font_normal, leading = 12, spaceBefore = 0)
    text_left_1 = Paragraph("The Vermont Home Energy Profile is a report on ...", p3)
    text_left_2 = Paragraph("Create generic text here", p3)
    text_left_3 = Paragraph("Energy usage and costs are estimates only. See reverse side for details.", p3)
    text_left_4 = Paragraph("HOME INFORMATION", p4)
    text_left_5 = Paragraph("LOCATION:", p5)
    text_left_6 = Paragraph(data_dict['street'],p6)
    text_left_7 = Paragraph(data_dict['city'] + ", " + data_dict["state"] + " " + data_dict["zipcode"], p6)
    text_left_8 = Paragraph("YEAR BUILT:", p5)
    text_left_9 = Paragraph(str(data_dict['yearbuilt']),p6)
    text_left_10 = Paragraph("CONDITIONED FLOOR AREA:",p5)
    text_left_11 = Paragraph(str(data_dict['finishedsqft']),p6)
    text_left_12 = Paragraph("REPORT INFORMATION", p4)
    text_left_13 = Paragraph("PROFILE ISSUE DATE:", p5)
    text_left_14 = Paragraph("GENERATED BY:", p5)
    text_left_15 = Paragraph("AFFILIATION:", p5)
     
    ##BODY RIGHT
    chevron = "./images/chevron_green.jpg"
    im2 = Image(chevron, 5.90*inch, 0.6*inch)
    
    p7 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_xl, fontName = font_bold, spaceBefore = -38, leftIndent = 10, textColor=colors.white)
    p8 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_l, fontName = font_bold, spaceBefore = -6, leftIndent = 120, spaceAfter = 30)
    tc1 = Paragraph('$'+"{:,}".format(data_dict['score']), p7)
    tc2 = Paragraph("Expected Annual Energy Costs", p8)
    
    p14 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_t, fontName = font_bold,  spaceBefore = 0)
    p15 = ParagraphStyle('body_left', alignment = TA_RIGHT, fontSize = font_t, fontName = font_normal,  spaceBefore = -12)
    p16 = ParagraphStyle('body_left', alignment = TA_RIGHT, fontSize = font_t, fontName = font_normal,  spaceBefore = 0)
    tct1 = Paragraph("<font name='Helvetica-Bold'>The breakdown of fuel usage is an estimate </font>based on the fuels used in this home", p14)
    tct3 = Paragraph(data_dict['heatingfuel'], p14)
    tct4 = Paragraph('$'+"{:,}".format(data_dict['fuel_score']), p15)
    tct5 = Paragraph("{:,}".format(data_dict['fuel_cons']) + ' gal', p16)
    tct6 = Paragraph("{:,}".format(data_dict['fuel_cost']) + ' $/gal', p16)
    tct7 = Paragraph("Electric", p14)
    tct8 = Paragraph('$'+"{:,}".format(data_dict['elec_score']), p15)
    tct9 = Paragraph("{:,}".format(data_dict['elec_cons']) + ' kwh', p16)
    tct10 = Paragraph("{:,}".format(data_dict['elec_cost']) + ' $/kwh', p16)
    cost_table = Table([[[tct1], [tct3, tct4, tct5, tct6, tct7, tct8, tct9, tct10]]], colWidths = [2.95*inch, 2.95*inch])
    cost_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND',(0,0),(-1,-1),colors.white),
     ]))
    
    p9 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_h, fontName = font_bold, spaceBefore = -30, leftIndent = 10, textColor=colors.white)
    p10 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_l, fontName = font_bold, spaceBefore = -14, leftIndent = 120, spaceAfter = 30)
    p11 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_t, fontName = font_normal,  spaceBefore = -10, spaceAfter = 0, backColor = 'white')
    p12 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_t, fontName = font_normal,  spaceBefore = -1, spaceAfter = 0, backColor = 'white')
    p13 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_t, fontName = font_normal,  spaceBefore = -1, spaceAfter = 12, backColor = 'white')
    
    tc3 = Paragraph('TAKE ACTION!', p9)
    tc4 = Paragraph("Reduce Your Energy Waste", p10)
    tb1 = Paragraph("☐ &nbsp; Contact a certified energy professional to learn how to make your home more efficient and comfortable and what financial incentives are available.", p11)
    tb2 = Paragraph("☐ &nbsp; Ensure insulation levels meet Vermont Residential Building Energy Standards.", p12)
    tb3 = Paragraph("☐ &nbsp; Discover if unseen air leaks are contributing to heat loss and creating uncomfortable drafts in your home.", p12)
    tb4 = Paragraph("☐ &nbsp; Verify all appliances and mechanical equipment are ENERGY STAR&reg; certified.", p13)

    p14 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_t, fontName = font_italic,  spaceBefore = -1, spaceAfter = 12, backColor = 'white')
    tc5 = Paragraph('ACHIEVEMENTS', p9)
    tc6 = Paragraph("Completed Certifications and Measures", p10)
    tb5 = Paragraph("☑ &nbsp; Generated a Vermont Home Energy Profile.", p11)
    tb6 = Paragraph("Congratulations! You've taken the first step to understanding your home's energy use… ", p14)
    
    
    
    body_table = Table([[[text_left_1, text_left_2, text_left_3, text_left_4, text_left_5, text_left_6, text_left_7, 
        text_left_8, text_left_9, text_left_10, text_left_11, text_left_12, text_left_13, text_left_14, text_left_15], 
        [im2, tc1, tc2, cost_table, Spacer(1, 12), im2, tc3, tc4, tb1, tb2, tb3, tb4, im2, tc5, tc6, tb5, tb6]]], 
        colWidths = [1.63 * inch, 6.07 * inch])
    body_table.setStyle(TableStyle([
#        ('BACKGROUND',(1,0),(-1,0),colors.HexColor('#41ad49')), 
        ('ALIGN', (0,0), (-1,-1), 'LEFT'), 
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    Story.append(body_table)
    
#    pic = flowable_fig(vthep_logo)
#    Story.append(pic)

#    Story.append(cost_table)

    doc.build(Story, onFirstPage=myFirstPage)

 
#styles=getSampleStyleSheet()
#styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
#ptext = '<font size=12>%s</font>' % formatted_time


if __name__ == '__main__':
    data_dict = {'street': '123 Main St', 'city': 'Montpelier', 'state': 'VT', 'zipcode': '05000', 
        'yearbuilt': 2005, 'finishedsqft': 2200, 'score': 3137, 'score_btu': 93, 
        'heatingfuel': 'Heating Oil', 'fuel_score': 1531, 'fuel_cons': 500, 'fuel_cost': 2.5, 'elec_score': 1600, 'elec_cons': 15000, 'elec_cost': 0.2}
    write_vermont_energy_profile_pdf(data_dict)
