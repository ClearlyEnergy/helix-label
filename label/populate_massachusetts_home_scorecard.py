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
from reportlab.lib.enums import TA_CENTER

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
    frameHeight = document.height-header_frame.height+(0.25*inch)
    column_1 = Frame(document.leftMargin,document.bottomMargin,frameWidth,frameHeight, showBoundary=0)
    f1_header1 = "<font name=Helvetica color=#4c4f52 size=12>ABOUT</font>"
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

    f1_header_2 = "<font name=Helvetica color=#4c4f52 size=12>YEARLY ENERGY USE</font>"
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
   
    f1_header_3 = "<font name=Helvetica color=#4c4f52 size=12>YEARLY COSTS & SAVINGS<super >*</super> </font>"#add prefix
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
    frameHeight_2 = document.height-header_frame.height+(0.25*inch)
    column_2 = Frame(document.leftMargin+frameWidth_2,document.bottomMargin,frameWidth_2+inch,frameHeight_2, showBoundary=0)

    f2_header1 = "<font name=Helvetica color=#4c4f52 size=12>HOME ENERGY USE</font>"
    f2_header1_p = Paragraph(f2_header1,styles['Heading2'])
    Story.append(f2_header1_p)
    f2_text_p = Paragraph('<font size=8.5 color=#736d5e>This shows the estimated total energy use (electricity and heating fuel) of your home for one year. The lower the energy use, the better!</font>',styles['Normal'])
    Story.append(f2_text_p)

    
    scorecard_btu = IMG_PATH+"scorecard_btu.png"
    img_sc_btu = Image(scorecard_btu,width=5*cm,height=12*cm)
    total_energy_usage_base = 205
    total_energy_usage_base_p = Paragraph('<font name=FontAwesome>{}</font>'.format(total_energy_usage_base),styles['Title'])
    f2_text1_p = Paragraph('<font name=Helvetica size=7.5  color=#4c4f52>Energy Use before improvements</font>',styles['Normal'])
    total_energy_usage_improved = 122
    total_energy_usage_improved_p = Paragraph('<font name=FontAwesome>{}</font>'.format(total_energy_usage_improved),styles['Title'])

    f2_text2_p = Paragraph('<font name=Helvetica  size=7.5  color=#4c4f52>Energy Use after recommended improvements</font>',styles['Normal'])

    data_table4 = [[img_sc_btu,total_energy_usage_base_p,f2_text1_p],['','',''],['',total_energy_usage_improved_p,f2_text2_p ]]

    tbl_frame_2 = Table(data_table4)
    
    tblStyle = TableStyle([('LEFTPADDING',(1,0),(1,2),-4*cm),('LEFTPADDING',(2,0),(2,2),-2.5*cm),('TOPPADDING',(0,0),(0,0),cm),('SPAN', (0, 0), (0, -1)),('SPAN',(1,0),(1,1)),('SPAN',(2,0),(2,1)),('VALIGN',(1,0),(2,0),'MIDDLE'),('VALIGN',(1,2),(2,2),'TOP')])
    tbl_frame_2.setStyle(tblStyle)
    Story.append(tbl_frame_2)
    styles.add(ParagraphStyle(name='Centre', alignment=TA_CENTER))
    f2_text3_p = Paragraph('<font size=8.5 color=#736d5e>Estimated percentage of energy use by fuel type:</font>',styles['Centre'])
    Story.append(f2_text3_p)
    propane_percentage=4
    fuel_oil_percentage = 90
    electricity_percentage = 6
    data_f2=[[Paragraph('<font name=Helvetica size=8>{}% Propane</font>'.format(str(propane_percentage)),styles['Normal']),Paragraph('<font name=Helvetica size=8>{}% Fuel Oil</font>'.format(str(fuel_oil_percentage)),styles['Normal']),Paragraph('<font name=Helvetica size=8>{}% Electricity</font>'.format(str(electricity_percentage)),styles['Normal'])]]
    tbl1_frame_2 = Table(data_f2,rowHeights=cm)
    tblStyle1_frame_2 = TableStyle([('LEFTPADDING',(0,0),(-1,-1),cm),('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#c8cacc')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ALIGN',(0,0),(-1,-1),'CENTER')])
    tbl1_frame_2.setStyle(tblStyle1_frame_2)
    Story.append(tbl1_frame_2)

    # creating and populating frame3
    Story.append(FrameBreak)
    frameWidth_3 = document.width/3
    frameHeight_3 = document.height-header_frame.height+(0.25*inch)
    column_3 = Frame(document.leftMargin+frameWidth_3+frameWidth_3+inch,document.bottomMargin,frameWidth_3-inch,frameHeight_3, showBoundary=0)
    f3_header1 = "<font name=Helvetica color=#4c4f52 size=12>HOME CARBON FOOTPRINT</font>"
    f3_header1_p = Paragraph(f3_header1,styles['Heading2'])
    Story.append(f3_header1_p)
    f3_text_p = Paragraph('<font  size=8.5 color=#736d5e>This score shows the'+
                            'estimated carbon missions based on the annual amounts,'+
                             'types,and sources of fuels used in your home. The lower'+
                             'the score, the less carbon is released into the atmosphere to power your home.</font>'
                                ,styles['Normal'])
    Story.append(f3_text_p)

    co2_production_base =16.4
    co2_production_base_p = Paragraph('<font name=Helvetica-Bold>{}</font>'.format(co2_production_base),styles['Normal'])

    co2_text_p = Paragraph('<font name=Helvetica size=7.5 color=#4c4f52>Footprint before improvement</font>',styles['Normal'])
    co2_production_improved = 10.2
    co2_production_improved_p = Paragraph('<font name=Helvetica-Bold >{}</font>'.format(co2_production_improved),styles['Normal'])
    co2_improved_text_p = Paragraph('<font name=Helvetica size=7.5 color=#4c4f52 >Footprint after recommended improvements</font>',styles['Normal'])
    scorecard_ton =IMG_PATH+'scorecard_ton.png'
    img_sc_ton = Image(scorecard_ton,width=5.5*cm,height=10*cm)

    data_tbl1_f3 = [[img_sc_ton,co2_production_base_p,co2_text_p],['','',''],['',co2_production_improved_p,co2_improved_text_p ]]

    tblStyle_f3 = TableStyle([('LEFTPADDING',(1,0),(1,2),-2.5*cm),
    ('LEFTPADDING',(2,0),(2,2),-1.3*cm),('TOPPADDING',(0,0),(0,0),1*cm),
    ('SPAN', (0, 0), (0, -1)),('SPAN',(1,0),(1,1)),('SPAN',(2,0),(2,1)),
    ('VALIGN',(1,0),(2,0),'MIDDLE'),
    ('TOPPADDING',(2,0),(2,0),1.7*cm),('TOPPADDING',(1,0),(1,0),1.2*cm),
    ('VALIGN',(1,2),(2,2),'TOP')])

    tbl1_f3 = Table(data_tbl1_f3)
    tbl1_f3.setStyle(tblStyle_f3)
    Story.append(tbl1_f3)

    f3_text3_p = Paragraph('<font size=8 color=#736d5e>Estimated average carbon footprint (tons/yr):</font>',styles['Centre'])
    Story.append(Spacer(1,8.8))
    Story.append(f3_text3_p)

    fuel_oil_percentage_f3 = 93
    electricity_percentage_f3 = 7
    data_tbl2_f3=[[Paragraph('<font name=Helvetica size=8  color=#16181a><strong>{}%</strong> Fuel Oil</font>'.format(str(fuel_oil_percentage_f3)),styles['Normal']),
    Paragraph('<font name=Helvetica size=8  color=#16181a><strong>{}%</strong> Electricity</font>'.format(str(electricity_percentage_f3)),styles['Normal'])]]

    tbl2_frame_3 = Table(data_tbl2_f3,rowHeights=cm)
    tblStyle2_frame_3 = TableStyle([('LEFTPADDING',(0,0),(-1,-1),cm),
    ('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#c8cacc')),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('ALIGN',(0,0),(-1,-1),'CENTER')])

    tbl2_frame_3.setStyle(tblStyle2_frame_3)
  
    Story.append(tbl2_frame_3)
    

    #  FOOTER FRAME
    Story.append(FrameBreak)
    footer_frame = Frame(document.leftMargin,document.height-0.98*document.height,document.width,0.13*document.height, showBoundary=0)
    foot_text_p1 = Paragraph("<font  size=8 color=#736d5e>* Estimated costs and savings. Actual energy costs may"+
                  "vary and are based on many factors such as occupant behavior,"+ 
                  "weather and utility rates. Please see next page for more on the EPS calculation</font>",styles['Normal'])

    foot_text_p2 = Paragraph("<font  size=8 color=#736d5e>Projections for score improvements and energy"+
                             "savings are estimates based on implementing all of the recommended energy effciency improvements. Ref# 91997."+
                              "</font>",styles['Normal'])

    Story.append(Spacer(1,12))
    Story.append(foot_text_p1)
    Story.append(foot_text_p2)
    footer_address_p = Paragraph('''<font size=9 color=#736d5e>Home Owner |{},{},{},{},{}</font>'''.format(address_line_1,address_line_2,city,state,postal_code),styles['Normal'])
    logo_footer = IMG_PATH+"logo.jpg"
    img_logo_footer = Image(logo,cm,cm)
    footer_text_img_p = Paragraph('''<font size=9 color=#736d5e >Brought to you by</font> <img valign="middle" src="{}logo.jpg" width="30" height="20"/>'''.format(IMG_PATH),styles['Normal'])

    footer_data = [[footer_address_p,'','','',footer_text_img_p]]
    footer_table = Table(footer_data)
    footer_table_style = TableStyle([('LEFTPADDING',(0,0),(0,0),0),('SPAN',(0,0),(3,0)),('ALIGN',(0,0),(0,0),'LEFT'),('VALIGN',(-1,-1),(-1,-1),'MIDDLE'),('ALIGN',(-1,-1),(-1,-1),'RIGHT'),('RIGHTPADDING',(-1,-1),(-1,-1),0)])
    footer_table.setStyle(footer_table_style)
    Story.append(Spacer(1,8))
    Story.append(footer_table)

    # SETTING UP PAGE TEMPLATES
    page_1_frames = [header_frame, column_1,column_2,column_3,footer_frame]
    templates =[]
    templates.append(PageTemplate(frames=page_1_frames,id='firstPage'))
    document.addPageTemplates(templates)

 
    style = styles["Normal"]
    #populate story with paragraphs
    
    # print(Story)
    document.build(Story)#, onFirstPage=myFirstPage, onLaterPages=myLaterPages


if __name__ == '__main__':
    create_pdf()