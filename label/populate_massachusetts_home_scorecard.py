# -*- coding: utf-8 -*-
#! /usr/bin/python
# run with python label/populate_massachusetts_home_scorecard.py


from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer,Table,TableStyle, BaseDocTemplate, Frame, PageTemplate, FrameBreak, NextPageTemplate, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import letter, landscape
import pkg_resources
from reportlab.lib import colors
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing, String

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
    # Story.append(Spacer(1,0.005*cm))
    document = SimpleDocTemplate('test.pdf',pagesize=landscape(letter),rightMargin=20,leftMargin=20,topMargin=20,bottomMargin=20)
    styles = getSampleStyleSheet()
    ##HEADER
    logo = IMG_PATH+"logo.jpg"
    home_energy_use =IMG_PATH+'home_energy_use.png'
    img_logo = Image(logo,2*cm,1.3*cm)
    
    header_text ='''<font name=Helvetica size=28>Your Massachusetts Home Scorecard</font>'''
    header_text2="<font name=helvetica size=8.2 color=#505752>This scorecard compares home energy use and carbon footprint to an average home in MA, and shows improvements based on recommended technology.</font>"
    hp1 = Paragraph(header_text,styles['Heading1'])
    hp2 = Paragraph(header_text2,styles['BodyText'])
    header_text3 = "<font name=helvetica size=6.5 color=#514C45> HOME ENERGY USE </font>"
    header_text4 = " <font color=white> 205</font>"
    hp4 = Paragraph(header_text4,styles['Title'])
    hp3 = Paragraph(header_text3,styles['Normal'])
    # data = [[img_logo,[hp1,hp2],'','','','','',[hp3,hp4]]]
    sm_data = [[hp3],[hp4]]
    sm_table= Table(sm_data,rowHeights=0.7*cm)
    sm_tableStyle = TableStyle([('ALIGN', (0, 0), (0, 0), 'LEFT'),('LEFTPADDING',(0,0),(0,0),0.5),('BOTTOMPADDING',(0,1),(0,1),0),('BACKGROUND',(0,1),(0,1),colors.gray),('RIGHTPADDING',(0,0),(0,0),0.5),('INNERGRID', (0,0), (-1,-1), 0.1, colors.gray),('BOX', (0,0), (-1,-1), 0.1, colors.gray)])
    sm_table.setStyle(sm_tableStyle)
    data = [[img_logo,[hp1,hp2],'','','','','',sm_table]]
    tblStyle = TableStyle([('LEFTPADDING',(1,0),(1,0),0),('VALIGN', (0, 0), (0, 0), 'MIDDLE'),('ALIGN', (0, 0), (0, 0), 'RIGHT'),('ALIGN', (-1, 0), (-1, 0), 'LEFT'),('SPAN', (1, 0), (6, 0))])
    tbl = Table(data)
    tbl.setStyle(tblStyle)
    Story.append(tbl)
    header_frame = Frame(document.leftMargin,document.height-0.05*document.height,document.width,0.12*document.height, showBoundary=0)
    Story.append(FrameBreak)
    osme = header_frame.height
    # print(osme, document.bottomMargin)

    ##CREATING FRAMES FOR PAGE1
    # creating and populating frame1
    
    frameWidth = document.width/3
    frameHeight = document.height-header_frame.height+(0.2*inch)
    column_1 = Frame(document.leftMargin,document.bottomMargin,frameWidth,frameHeight, showBoundary=0)
    f1_header1 = "<font color=black>ABOUT</font>"
    f1_header1_p = Paragraph(f1_header1,styles['Heading2'])
    f1_text1 = '<font color=black>Address</font>'
    f1_text1_p = Paragraph(f1_text1,styles['Normal'])
    address_line_1 = "123 Main St."
    address_line_2 = ''
    city='Whately'
    state = 'MA'
    postal_code= '01903'
    address = '<font color=black>{}, {}, {}, {}, {}</font>'.format(address_line_1,address_line_2,city,state,postal_code)
    address_p = Paragraph(address,styles['Normal'])
    Story.append(f1_header1_p)
    
    Story.append(f1_text1_p)
    Story.append(Spacer(1, 5))
    Story.append(address_p)
    Story.append(Spacer(1, 5))
    #create style for pragraphs in frame_1
    styles.add(ParagraphStyle(name='f1_leading',leading=16))
    year_built ='1850'
    year_built_header_p = Paragraph('Year Built',styles['f1_leading'])
    year_built_p=Paragraph('<font name=Helvetica-Bold>{}</font>'.format(year_built),styles['f1_leading'])
    
    conditioned_floor_area = 2735
    conditioned_floor_area_header_p = Paragraph('Sq. Footage',styles['f1_leading'])
    conditioned_floor_area_p  = Paragraph('<font name=Helvetica-Bold>{}</font>'.format(str(conditioned_floor_area)),styles['f1_leading'])
   
    number_of_bedrooms =3
    number_of_bedrooms_p = Paragraph('<font name=Helvetica-Bold>{}</font>'.format(str(number_of_bedrooms)),styles['f1_leading'])
    number_of_bedrooms_header_p = Paragraph('# of Bedrooms',styles['f1_leading'])

    primary_heating_fuel_type_header_p = Paragraph('Primary Heating Fuel',styles['f1_leading'])
    primary_heating_fuel_type = 'Fuel Oil'
    primary_heating_fuel_type_p = Paragraph('<font name=Helvetica-Bold>{}</font>'.format(str(primary_heating_fuel_type)),styles['f1_leading'])


    assessment_date = 'N/A'
    assessment_date_p = Paragraph('<font name=Helvetica-Bold>{}</font>'.format(str(assessment_date)),styles['f1_leading'])
    assessment_date_header_p = Paragraph('Assessment Date',styles['f1_leading'])

    company_header_p =Paragraph('Energy Specialist',styles['f1_leading'])
    company ='Dave Saves'
    company_p =Paragraph('<font name=Helvetica-Bold>{}</font>'.format(str(company)),styles['f1_leading'])



    data1_f1=[[[year_built_header_p,year_built_p],[conditioned_floor_area_header_p,conditioned_floor_area_p]],
              [[number_of_bedrooms_header_p,number_of_bedrooms_p],[primary_heating_fuel_type_header_p,primary_heating_fuel_type_p]],
              [[assessment_date_header_p,assessment_date_p],[company_header_p,company_p]]
              ]
    tbl_frame_1 = Table(data1_f1)
    tbl_frame_1_tableStyle = TableStyle([('ALIGN', (0, 0), (0, -1),'LEFT'),('LEFTPADDING',(0,0),(0,-1),0)])
    tbl_frame_1.setStyle(tbl_frame_1_tableStyle)
    Story.append(tbl_frame_1)

    Story.append(Story.append(Spacer(1, 12)))

    f1_header_2 = "<font color=black>YEARLY ENERGY USE</font>"
    f1_header2_p = Paragraph(f1_header_2,styles['Heading2'])
    Story.append(f1_header2_p)
    

    electric_energy_usage_base_header_p =Paragraph('electricity',styles['f1_leading'])
    electric_energy_usage_base = 3.613
    electric_energy_usage_base_p =Paragraph('<font name=Helvetica-Bold>{} kWh</font>'.format(str(electric_energy_usage_base)),styles['f1_leading'])

    fuel_energy_base_header_p = Paragraph('Fuel Oil',styles['f1_leading'])
    fuel_energy_base = 1.324
    fuel_energy_base_p = Paragraph('<font name=Helvetica-Bold>{} gallons</font>'.format(str(fuel_energy_base)),styles['f1_leading'])

    data2_f1 =[[[electric_energy_usage_base_header_p,electric_energy_usage_base_p],[fuel_energy_base_header_p,fuel_energy_base_p]]]
    tbl1_frame_1 = Table(data2_f1)
    tbl1_frame_1_tableStyle = TableStyle([('ALIGN', (0, 0), (0, -1),'LEFT'),('LEFTPADDING',(0,0),(0,-1),0)])
    tbl1_frame_1.setStyle(tbl1_frame_1_tableStyle)
    Story.append(tbl1_frame_1)

    Story.append(Story.append(Spacer(1, 12)))
   
    f1_header_3 = "<font color=black>YEARLY COSTS & SAVINGS<super >*</super> </font>"#add prefix
    f1_header3_p = Paragraph(f1_header_3,styles['Heading2'])
    Story.append(f1_header3_p)


    total_energy_cost_base=4343
    total_energy_cost_base_text_p= Paragraph('<font size=8>Pre-upgrade Energy cost per yr</font>',styles['Normal'])



    total_energy_cost_improved=2798
    total_energy_cost_improved_text_p= Paragraph('<font size=8>Post-upgrade Energy Cost per yr</font>',styles['Normal'])

    save = total_energy_cost_base-total_energy_cost_improved
    save_text_p= Paragraph('<font size=8>Estimated Energy Savings per yr</font>',styles['Normal'])

    total_energy_cost_base_p = Paragraph('<font name=Helvetica-Bold>${}</font>'.format(str(total_energy_cost_base)),styles['f1_leading'])
    total_energy_cost_improved_p =  Paragraph('<font name=Helvetica-Bold>${}</font>'.format(str(total_energy_cost_improved)),styles['f1_leading'])
    save_p =  Paragraph('<font name=Helvetica-Bold>${}</font>'.format(str(save)),styles['f1_leading'])

    data3_f1 = [[[total_energy_cost_base_p,total_energy_cost_base_text_p],
                 [total_energy_cost_improved_p,total_energy_cost_improved_text_p],
                 [Paragraph('SAVE',styles['Normal']),save_p,save_text_p]
                    ]]

    tbl3_frame_1 = Table(data3_f1)
    tbl3_frame_1_tableStyle = TableStyle([('ALIGN', (0, 0), (-1, 0),'CENTRE')])
    tbl3_frame_1.setStyle(tbl3_frame_1_tableStyle)
    Story.append(tbl3_frame_1)


    #drawing piecharts
    #first pie
    pie_data_1 =[total_energy_cost_base]
    pie_1= Pie()
    pie_1.width=2.3*cm
    pie_1.height=2.3*cm
    pie_1.data=pie_data_1
    # pie_title_1 = String("Before")
    drawing =Drawing()
    drawing.add(pie_1)
    
    
    # Story.append(drawing)
    #second pie
    pie_data_2 =[total_energy_cost_base,total_energy_cost_improved]
    pie_2= Pie()
    pie_2.width=2.3*cm
    pie_2.height=2.3*cm
    pie_2.data=pie_data_2
    # pie_title_1 = String("Before")
    drawing1 =Drawing()
    # pie_2.x = 150
    # pie_2.y = 65
    drawing1.add(pie_2)
    data_table3 = [[drawing,drawing1]]
    tbl_pie = Table(data_table3)#figure out how to get the piecharts in the column in order
    # Story.append(tbl_pie)



    # creating and populating frame2
    Story.append(FrameBreak)
    frameWidth_2 = document.width/3
    frameHeight_2 = document.height-header_frame.height+(0.2*inch)
    column_2 = Frame(document.leftMargin+frameWidth_2,document.bottomMargin,frameWidth_2+inch,frameHeight_2, showBoundary=0)

    f2_header1 = "<font color=black>HOME ENERGY USE</font>"
    f2_header1_p = Paragraph(f2_header1,styles['Heading2'])
    Story.append(f2_header1_p)
    f2_text_p = Paragraph('<font size=8.5 color=#736d5e>This shows the estimated total energy use (electricity and heating fuel) of your home for one year. The lower the energy use, the better!</font>',styles['Normal'])
    Story.append(f2_text_p)

    

    # page1_frames =[]
    # page1_frameCount =3
    # frameWidth = document.width/page1_frameCount
    # frameHeight = document.height-inch
    # bottom_margin =document.bottomMargin+0.5*inch


    
    # for frame in range(page1_frameCount):
    #     leftMargin = document.leftMargin + frame*frameWidth
    #     column =Frame(leftMargin, bottom_margin,frameWidth,frameHeight)
    #     page1_frames.append(column)
    

    # page2_frames =[]
    # page2_frameCount =2
    # frameWidth2 = document.width/page2_frameCount
    # frameHeight = document.height-.5*inch

    # for frame in range(page2_frameCount):
    #     leftMargin = document.leftMargin + frame*frameWidth2
    #     column =Frame(leftMargin, document.bottomMargin,frameWidth2,frameHeight)
    #     page2_frames.append(column)

    # templates= []
    # templates.append(PageTemplate(frames=page1_frames,id='firstPage',onPage=footer))
    # templates.append(PageTemplate(frames=page2_frames,id='secondPage',onPage=footer))

    page_1_frames = [header_frame, column_1,column_2]
    templates =[]
    templates.append(PageTemplate(frames=page_1_frames,id='firstPage'))
    document.addPageTemplates(templates)

 
    style = styles["Normal"]
    #populate story with paragraphs
    
    # print(Story)
    document.build(Story)#, onFirstPage=myFirstPage, onLaterPages=myLaterPages


if __name__ == '__main__':
    create_pdf()