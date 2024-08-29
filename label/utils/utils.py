# implemented this class so that we can colour our frames, for this particular project we wanted to colour the first frame
import csv
import os
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.lib.colors import toColor
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_LEFT, TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Flowable, SimpleDocTemplate, Frame, Image, Table, TableStyle
from reportlab.platypus import Paragraph
from label.utils.constants import *


class ColorFrameSimpleDocTemplate(SimpleDocTemplate, object):
    def handle_frameBegin(self, **kwargs):
        super(ColorFrameSimpleDocTemplate, self).handle_frameBegin(**kwargs)

        if hasattr(self.frame, 'background'):
            self.frame.drawBackground(self.canv)

        if hasattr(self.frame, 'roundedBackground'):
            self.frame.drawRoundedBackground(self.canv)


class ColorFrame(Frame, object):
    """ Extends the reportlab Frame with the ability to draw a background color. """

    def __init__(
            self, x1, y1, width, height, leftPadding=6, bottomPadding=6,
            rightPadding=6, topPadding=6, id=None, showBoundary=0,
            overlapAttachedSpace=None, _debug=None, background=None, roundedBackground=None):

        Frame.__init__(
            self, x1, y1, width, height, leftPadding,
            bottomPadding, rightPadding, topPadding, id, showBoundary,
            overlapAttachedSpace, _debug)
        if background is not None:
            self.background = background
        if roundedBackground is not None:
            self.roundedBackground = roundedBackground

    def drawBackground(self, canv):
        color = toColor(self.background)

        canv.saveState()
        canv.setFillColor(color)
        canv.rect(
            self._x1, self._y1, self._x2 - self._x1, self._y2 - self._y1,
            stroke=0, fill=1
        )
        canv.restoreState()

    def drawRoundedBackground(self, canv):
        color = toColor(self.roundedBackground)

        canv.saveState()
        canv.setFillColor(color)
        canv.roundRect(
            self._x1, self._y1, self._x2 - self._x1, self._y2 - self._y1,
            4, stroke=0, fill=1
        )
        canv.restoreState()

    def addFromList(self, drawlist, canv):
        if self.background:
            self.drawBackground(canv)
        Frame.addFromList(self, drawlist, canv)


class Hes_Image(Image):

    def wrap(self, availWidth, availHeight):
        height, width = Image.wrap(self, availWidth, availHeight)
        return width, height

    def draw(self):

        # Image.canv.
        self.canv.drawString(100, 400, '8uiuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu')
        # self.canv.rotate(45)
        Image.draw(self)

class flowable_text(Flowable):
    def __init__(self, offset_x, offset_y, text, font_size):
        Flowable.__init__(self)
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.text = text
        self.font_size = font_size
        
    def draw(self):
        self.canv.setFont("InterstateBlack", self.font_size)
        self.canv.setFillColor(colors.gray)
        self.canv.drawString(self.offset_x*inch, (self.offset_y-0.1)*inch, self.text)     

class flowable_triangle(Flowable):
    def __init__(self, imgdata, offset_x, offset_y, height, width, text, side='right'):
        Flowable.__init__(self)
        self.img = ImageReader(imgdata)
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.height = height
        self.width = width
        self.text = text
        self.side = side

    def draw(self):
        self.canv.drawImage(self.img, self.offset_x*inch, self.offset_y*inch, height = self.height*inch, width=self.width*inch)
        self.canv.setFont("InterstateBlack", 7)
        self.canv.setFillColor(colors.gray)
        t = self.canv.beginText()
#        t.setFont("FontAwesome", 30)
        if self.side == 'right':
            t.setTextOrigin((self.offset_x)*inch, (self.offset_y-0.1)*inch)
        elif self.side == 'left':
            t.setTextOrigin((self.offset_x-0.4)*inch, (self.offset_y-0.1)*inch)
        elif self.side == 'low':
            t.setTextOrigin((self.offset_x)*inch, (self.offset_y-0.3)*inch)
        elif self.side == 'high':
            t.setTextOrigin((self.offset_x)*inch, (self.offset_y+0.1)*inch)
        t.textLines(self.text)
        self.canv.drawText(t)
#        self.canv.drawString(self.offset_x*inch, (self.offset_y-0.1)*inch, self.text)

class Charts():
    
    def pie_chart(data_dict, fuels, fuel_icons, fuel_color):
        drawing = Drawing(width=1.0*inch, height=1.0*inch)
        data = []
        labels = []
        order = []

        for num, fuel in enumerate(fuels):
            if ('energyCost'+fuel in data_dict) and (data_dict['energyCost'+fuel] is not None) and (data_dict['energyCost'+fuel] > 0):
                data.append(int(data_dict['energyCost'+fuel]))
                labels.append(fuel_icons[num])
                order.append(num)
        if not order: #check fuel unit conversions
            for num, fuel in enumerate(fuels):
                if ('siteEnergyUse'+fuel in data_dict) and (data_dict['siteEnergyUse'+fuel] is not None) and (data_dict['siteEnergyUse'+fuel] > 0):
                    data.append(int(data_dict['siteEnergyUse'+fuel]))
                    labels.append(fuel_icons[num])
                    order.append(num)
        pie = Pie()
        pie.sideLabels = False
        pie.x = 5
        pie.y = 10
        pie.width = 1.0*inch
        pie.height = 1.0*inch
        pie.data = data
    #    pie.labels = labels
        pie.slices.strokeColor = colors.white
        pie.slices.strokeWidth = 0.01
        pie.simpleLabels = 0
        for i in range(len(data)):
            pie.slices[i].labelRadius = 0.5
            pie.slices[i].fillColor = fuel_color[order[i]]
            pie.slices[i].fontName = 'FontAwesome'
            pie.slices[i].fontSize = 16
        drawing.add(pie)
        return drawing
        
    # Wedge (start at 0.62; end at 4.82)
    def wedge(data_dict, eui=False):
        if data_dict['systemDefinedPropertyType'] and data_dict['systemDefinedPropertyType'] != 'N/A':
            espm_score_mapping = Scores.map_scores(data_dict['systemDefinedPropertyType'])
        else:
            espm_score_mapping = Scores.map_scores('Office')

        if data_dict['energy_star_score']:
            site_max = float(espm_score_mapping['1']) * data_dict['site_total'] / float(espm_score_mapping[str(int(min(data_dict['energy_star_score'],99.0)))])
            site_min = float(espm_score_mapping['100']) * data_dict['site_total'] / float(espm_score_mapping[str(int(min(data_dict['energy_star_score'],99.0)))])
            site_median = float(espm_score_mapping['50']) * data_dict['site_total'] / float(espm_score_mapping[str(int(min(data_dict['energy_star_score'],99.0)))])
        else:
            site_max = float(espm_score_mapping['1']) * data_dict['site_total'] / float(espm_score_mapping['50'])
            site_min = 0.0
            site_median = float(espm_score_mapping['50']) * data_dict['site_total'] / float(espm_score_mapping['50'])

        offset_x = 0.53+data_dict['site_total']/site_max*(4.75-0.53)
        max_to_med = site_max / site_median
        min_to_med = site_min / site_median

        if eui: 
            site_median = data_dict['medianSiteIntensity']
            site_max = max_to_med * site_median
            site_min = min_to_med * site_median
            txt = flowable_text(min(offset_x-0.5,2), 2.2, "This building's energy use intensity: " + str(round(data_dict['siteIntensity'],1)) + " kBtu/sq.ft.",9)
        else:
            site_max = round(site_max)
            site_min = round(site_min)
            site_median = round(site_median)
            txt = flowable_text(min(offset_x-0.5,2), 2.2, "This building's usage: " + str("{:,}".format(int(data_dict['site_total']))) + " MMBtu",9)

        if eui:
            wedge_img = IMG_PATH+"/wedgei.png"
        else:
            wedge_img = IMG_PATH+"/wedge.png"
        triangle = IMG_PATH+"/triangle.png"
        triangle2 = IMG_PATH+"/triangle2.png"
        wedge = Image(wedge_img, 5.0*inch, 2.25*inch)
        # triangle for actual building consumption
        pic = flowable_triangle(triangle,offset_x, 1.78, 0.2, 0.288,'')
        # triangle for net zero building, set at zero bar along with text
        pic2 = flowable_triangle(triangle2, 0.62, 0.44, 0.08, 0.138,"Net zero \n building","left")
        # if median is available, add it in as triangle on line
        pic3 = None
        offset_x = 0.62 + site_median/site_max*(4.75-0.53)
        if offset_x < 4.3:
            pic3 = flowable_triangle(triangle2,offset_x, 0.44,0.08, 0.138,"Median building","left")
        offset_x = 0.62 + 105.0/site_max*(4.82-0.62)
        # text for maximum reference
        txt2 = flowable_text(4.82, 0.44, str("{:,}".format(int(site_max))),7)
    
        return wedge, txt, txt2, pic, pic2, pic3
    
class Tables():
    def cost_table(data_dict):
        pc251 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = FONT_T, textColor = CUSTOM_DGRAY, fontName = FONT_BOLD,  spaceBefore = 0)
        pc252 = ParagraphStyle('body_left', alignment = TA_RIGHT, fontSize = FONT_T, textColor = CUSTOM_DGRAY, fontName = FONT_BOLD,  spaceBefore = -12)
        pc253 = ParagraphStyle('body_left', alignment = TA_RIGHT, fontSize = FONT_T, textColor = CUSTOM_DGRAY, fontName = FONT_NORMAL,  spaceBefore = 0)

        tct = []
        
        num_fuel = 0
        for num, fuel in enumerate(FUELS):
            if ('energyCost'+fuel in data_dict) and (data_dict['energyCost'+fuel] is not None) and (data_dict['energyCost'+fuel] != 0.0):
                data_dict['energyRate'+fuel] = data_dict['energyCost'+fuel]/(data_dict['siteEnergyUse'+fuel]/FUELFACTOR[num])
                num_fuel+=1
            elif ('energyCost'+fuel in data_dict) and (data_dict['siteEnergyUse'+fuel] != 0.0) and (data_dict['siteEnergyUse'+fuel] is not None):
                num_fuel+=1
        if data_dict['onSiteRenewableSystemGeneration'] != 0.0:
            num_fuel+=1
            
        for num, fuel in enumerate(FUELS):
            if ('siteEnergyUse'+fuel in data_dict) and (data_dict['siteEnergyUse'+fuel] is not None):
                cons = data_dict['siteEnergyUse'+fuel]/FUELFACTOR[num]
                if ('energyCost'+fuel in data_dict) and (data_dict['energyCost'+fuel] is not None) and (data_dict['energyCost'+fuel] != 0.0):
                    if  (data_dict['energyCost'+fuel] is not None) :
                        pc251.textColor = FUELCOLOR[num]
                        if num_fuel > 3:
                            tct.append([FUELIMAGESSMALL[num],  [Paragraph(FUELLABEL[num], pc251),Paragraph('$'+"{:,}".format(int(data_dict['energyCost'+fuel])), pc252), Paragraph("{:,}".format(int(cons)) + ' ' + FUELUNIT[num] + ' at {0:.2f}'.format(data_dict['energyRate'+fuel]) + ' $/'+FUELUNIT[num], pc253),], ''])
                        else:
                            tct.append([FUELIMAGES[num],  [Paragraph(FUELLABEL[num], pc251),Paragraph('$'+"{:,}".format(int(data_dict['energyCost'+fuel])), pc252), Paragraph("{:,}".format(int(cons)) + ' ' + FUELUNIT[num], pc253), Paragraph('{0:.2f}'.format(data_dict['energyRate'+fuel]) + ' $/'+FUELUNIT[num], pc253)], ''])
                elif (cons is not None) and (cons != 0.0):
                        cons = data_dict['siteEnergyUse'+fuel]/FUELFACTOR[num]
                        if num_fuel > 3:
                            tct.append([FUELIMAGESSMALL[num],  [Paragraph(FUELLABEL[num], pc251), Paragraph("{:,}".format(int(cons)) + ' ' + FUELUNIT[num], pc253),]])
                        else:
                            tct.append([FUELIMAGES[num],  [Paragraph(FUELLABEL[num], pc251), Paragraph("{:,}".format(int(cons)) + ' ' + FUELUNIT[num], pc253)], ''])

        if (data_dict['onSiteRenewableSystemGeneration'] is not None) and (data_dict['onSiteRenewableSystemGeneration'] != 0):
            pc251.textColor = FUELCOLOR[-1]
            if (data_dict['energyCostElectricityOnsiteSolarWind'] is not None) and (data_dict['energyCostElectricityOnsiteSolarWind'] != 0.0):
                if num_fuel > 3:
                    tct.append([FUELIMAGESSMALL[-1],[Paragraph("<font name='FontAwesome'>"+FUELICONS[-1]+"</font> Solar", pc251), Paragraph('$'+"{:,}".format(int(-1.0*data_dict['energyCostElectricityOnsiteSolarWind'])), pc252), Paragraph("{:,}".format(int(data_dict['onSiteRenewableSystemGeneration'])) + ' kwh', pc253)],''])
                else:
                    tct.append([FUELIMAGES[-1],[Paragraph("<font name='FontAwesome'>"+FUELICONS[-1]+"</font> Solar", pc251), Paragraph('$'+"{:,}".format(int(-1.0*data_dict['energyCostElectricityOnsiteSolarWind'])), pc252), Paragraph("{:,}".format(int(data_dict['onSiteRenewableSystemGeneration'])) + ' kwh', pc253)],''])
            else:
                if num_fuel > 3:
                    tct.append([FUELIMAGESSMALL[-1],[Paragraph("<font name='FontAwesome'>"+FUELICONS[-1]+"</font> Solar", pc251), Paragraph("{:,}".format(int(data_dict['onSiteRenewableSystemGeneration'])) + ' kwh', pc253)]])
                else:
                    tct.append([FUELIMAGES[-1],[Paragraph("<font name='FontAwesome'>"+FUELICONS[-1]+"</font> Solar", pc251), Paragraph("{:,}".format(int(data_dict['onSiteRenewableSystemGeneration'])) + ' kwh', pc253)]])
        
        cost_subTable = Table(tct, colWidths = [0.5*inch, 1.83*inch, 0.2*inch, 2.0*inch])
        cost_subTableStyle = TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ])

        row_ind = 0
        for num, fuel in enumerate(FUELS):
            if ('siteEnergyUse'+fuel in data_dict) and (data_dict['siteEnergyUse'+fuel] is not None) and (float(data_dict['siteEnergyUse'+fuel]) != 0.0):
                cost_subTableStyle.add('BACKGROUND',(2,row_ind),(-1,-num_fuel+row_ind),FUELCOLOR[num])
                if num_fuel != 1:
                    cost_subTableStyle.add('LINEBELOW', (0, row_ind), (-2, -num_fuel+row_ind), 1, CUSTOM_MGRAY),
                row_ind += 1
        if data_dict['onSiteRenewableSystemGeneration'] != 0:
            cost_subTableStyle.add('BACKGROUND',(2,num_fuel-1),(-1,-1),FUELCOLOR[-1])
            cost_subTableStyle.add('LINEABOVE', (0, row_ind),(-1, -num_fuel+row_ind),1, CUSTOM_MGRAY)
        
        cost_subTable.setStyle(cost_subTableStyle)    
        
        return cost_subTable

class Scores():
    
    def map_scores(property_type):
        category_map = {
            'Convenience Store with Gas Station': 'Retail Store', 'Enclosed Mall': 'Retail Store', 'Lifestyle Center': 'Retail Store', 'Strip Mall': 'Retail Store', 'Supermarket/Grocery Store': 'Retail Store', 'Vehicle Dealership': 'Retail Store', 'Wholesale Club/Supercenter': 'Retail Store', 'Other - Mall': 'Retail Store',
            'Bank Branch': 'Office', 'Financial Office': 'Office',
            'Adult Education': 'K-12 School', 'College/University': 'K-12 School', 'Pre-school/Daycare': 'K-12 School', 'Vocational School': 'K-12 School', 'Other - Education': 'K-12 School',
            'Aquarium': 'Hotel', 'Bar/Nightclub': 'Hotel', 'Bowling Alley': 'Hotel', 'Casino': 'Hotel', 'Convention Center': 'Hotel', 'Fitness Center/Health Club/Gym': 'Hotel', 'Ice/Curling Rink': 'Hotel', 'Indoor Arena': 'Hotel', 'Movie Theater': 'Hotel', 'Museum': 'Hotel', 'Performing Arts': 'Hotel', 'Race Track': 'Hotel', 'Roller Rink': 'Hotel', 'Social/Meeting Hall': 'Hotel', 'Stadium (Closed)': 'Hotel', 'Stadium (Open)': 'Hotel', 'Zoo': 'Hotel', 'Other - Entertainment/Public Assembly': 'Hotel', 'Other - Recreation': 'Hotel', 'Other - Stadium': 'Hotel',
            'Bar/Nightclub': 'Hotel', 'Convenience Store with Gas Station': 'Convenience Store without Gas Station', 'Fast Food Restaurant': 'Hotel', 'Food Sales': 'Hotel', 'Food Service': 'Hotel', 'Restaurant': 'Hotel', 'Supermarket/Grocery Store': 'Hotel', 'Wholesale Club/Supercenter': 'Hotel', 'Other - Restaurant/Bar': 'Hotel',
            'Ambulatory Surgical Center': 'Hospital (General Medical & Surgical)','Outpatient Rehabilitation/Physical Therapy': 'Medical Office', 'Residential Care Facility': 'Senior Living Community', 'Urgent Care/Clinic/Other Outpatient': 'Medical Office', 'Other - Specialty Hospital': 'Hospital (General Medical & Surgical)', 
            'Barracks': 'Multifamily Housing', 'Prison/Incarceration': 'Residence Hall/Dormitory', 'Other - Lodging/Residential': 'Multifamily Housing',
            'Manufacturing/Industrial Plant': 'Wastewater Treatment Plant',
            'Mixed Use Property': 'Office', 'Veterinary Office': 'Medical Office', 'Parking': 'Warehouse', 'Courthouse': 'Office', 'Fire Station': 'Office', 'Library': 'Office', 'Mailing Center/Post Office': 'Office', 'Police Station': 'Office', 'Prison/Incarceration': 'Office', 'Social/Meeting Hall': 'Office', 'Transportation Terminal/Station': 'Office', 'Other - Public Services': 'Office',
            'Laboratory': 'Data Center', 'Other - Technology/Science': 'Data Center',
            'Personal Services (Health/Beauty, Dry Cleaning, etc.)': 'Retail Store', 'Repair Services (Vehicle, Shoe, Locksmith, etc.)': 'Retail Store', 'Other - Services': 'Retail Store',
            'Drinking Water Treatment & Distribution': 'Wastewater Treatment Plant', 'Energy/Power Station': 'Wastewater Treatment Plant', 'Other - Utility': 'Wastewater Treatment Plant',
            'Self-Storage Facility': 'Warehouse', 'Distribution Center': 'Warehouse', 'Non-Refrigerated Warehouse': 'Warehouse', 'Refrigerated Warehouse': 'Warehouse', 'Garage': 'Warehouse',
            'Other': 'Office'
        }

        espm_score_mapping = {}
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'energy_star_score.csv')
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                espm_score_mapping[row['Category']] = row
        if property_type in espm_score_mapping:
            ret_vals = espm_score_mapping[property_type]
        else:
            ret_vals = espm_score_mapping[category_map[property_type]]
        return ret_vals
        
        
        

class Highlights():
    
    def score_box(data_dict, category):
        pc101 = ParagraphStyle('column_1', alignment = TA_CENTER, fontSize = FONT_H, fontName = FONT_BOLD, textColor=colors.white, leading=14)
        pc102 = ParagraphStyle('column_1', alignment = TA_CENTER, fontSize = FONT_XXL, fontName = FONT_BOLD, textColor = colors.white)
        pc103 = ParagraphStyle('column_2', alignment = TA_CENTER, fontSize = FONT_S, fontName = FONT_BOLD, textColor = colors.white, spaceBefore=26)
        if category == 'ESTAR_SCORE':
            if data_dict['energy_star_score']:
                text_c101 = Paragraph("ENERGY STAR SCORE", pc101)
                text_c102 = Paragraph(str(int(data_dict['energy_star_score']))+'/100', pc102)
                text_c103 = Paragraph('50=median, 75=high performer', pc103)
            else:
                text_c101 = Paragraph("ENERGY CONSUMPTION", pc101)
                text_c102 = Paragraph(str(int(data_dict['site_total'])), pc102)               
                text_c103 = Paragraph('MMBtu', pc103)
        elif category == 'GHG':
            if data_dict['totalLocationBasedGHGEmissions']:
                text_c101 = Paragraph("GREENHOUSE GAS EMISSIONS", pc101)
                text_c102 = Paragraph(str(int(data_dict['totalLocationBasedGHGEmissions'])), pc102)
                text_c103 = Paragraph("mt CO2e", pc103)
            else:
                text_c101 = Paragraph("ENERGY CONSUMPTION", pc101)
                text_c102 = Paragraph(str(int(data_dict['site_total'])), pc102)               
                text_c103 = Paragraph('MMBtu', pc103)
        elif category == 'EUI':
                text_c101 = Paragraph("ENERGY USE INTENSITY", pc101)
                text_c102 = Paragraph(str(int(data_dict['siteIntensity'])), pc102)               
                text_c103 = Paragraph('kBtu/sq.ft.', pc103)
        elif category == 'EU':
                text_c101 = Paragraph("ENERGY CONSUMPTION", pc101)
                text_c102 = Paragraph(str(int(data_dict['site_total'])), pc102)               
                text_c103 = Paragraph('kBtu/sq.ft.', pc103)
        else:
            text_c101 = Paragraph("TBD", pc101)
            text_c102 = Paragraph('value', pc102)
            text_c103 = Paragraph('range', pc103)
        
        return text_c101, text_c102, text_c103
        
    def cost_box(data_dict, text_color):
        pc231 = ParagraphStyle('column_2', alignment = TA_CENTER, fontSize = FONT_LL, fontName = FONT_BOLD, textColor = colors.white)
        pc202 = ParagraphStyle('column_2', alignment = TA_LEFT, fontSize = FONT_L, fontName = FONT_BOLD, textColor = text_color)
        if data_dict['energyCost']:
            if data_dict['energyCost'] >= 1000000.0:
                pc231 = ParagraphStyle('column_2', alignment = TA_CENTER, fontSize = FONT_ML, fontName = FONT_BOLD, textColor = colors.white)
            else:
                pc231 = ParagraphStyle('column_2', alignment = TA_CENTER, fontSize = FONT_L, fontName = FONT_BOLD, textColor = colors.white)
            text_c231 = Paragraph('${:,.0f}'.format(data_dict['energyCost']), pc231)
            text_c232 = Paragraph('Annual Energy Cost', pc202)
        elif ('percentElectricity' in data_dict) and data_dict['percentElectricity']:
            text_c231 = Paragraph('{:,.0f}%'.format(data_dict['percentElectricity']), pc231)
            text_c232 = Paragraph('Electrified', pc202)
        else:
            site_total = 0.0
            for fuel in ['siteEnergyUseElectricityGridPurchase', 'siteEnergyUseNaturalGas', 'siteEnergyUseFuelOil1', 'siteEnergyUseFuelOil2', 'siteEnergyUseFuelOil4', 'siteEnergyUseFuelOil5And6', 'siteEnergyUseDiesel', 'siteEnergyUseKerosene', 'siteEnergyUsePropane', 'siteEnergyUseDistrictSteam', 'siteEnergyUseDistrictHotWater', 'siteEnergyUseDistrictChilledWater', 'siteEnergyUseCoalAnthracite', 'siteEnergyUseCoalBituminous', 'siteEnergyUseCoke', 'siteEnergyUseWood', 'siteEnergyUseOther']:
                if fuel in data_dict and data_dict[fuel] and data_dict[fuel] > 0.0:
                    site_total += data_dict[fuel]
            percent_electric = 100.0 * data_dict['siteEnergyUseElectricityGridPurchase'] / site_total
            text_c231 = Paragraph('{:,.0f}%'.format(percent_electric), pc231)
            text_c232 = Paragraph('Electrified', pc202)
        return text_c231, text_c232

    def usage_box(data_dict, category='EU'):
        if category == 'EU_kbtu':
            site_total = data_dict['site_total']
            if site_total >= 100000.0:
                pc201 = ParagraphStyle('column_2', alignment = TA_CENTER, fontSize = FONT_H, fontName = FONT_BOLD, textColor = colors.white)
                text_c201 = Paragraph(str("{:,}".format(int(site_total)))+"<font size=6> kBtu </font>", pc201)
            elif site_total < 100000.0 and site_total > 10000.0:
                pc201 = ParagraphStyle('column_2', alignment = TA_CENTER, fontSize = FONT_ML, fontName = FONT_BOLD, textColor = colors.white)
                text_c201 = Paragraph(str("{:,}".format(int(site_total)))+"<font size=8> MMBtu </font>", pc201)
            elif site_total < 10000.0 and site_total > 1000.0:
                pc201 = ParagraphStyle('column_2', alignment = TA_CENTER, fontSize = FONT_L, fontName = FONT_BOLD, textColor = colors.white)
                text_c201 = Paragraph(str("{:,}".format(int(site_total)))+"<font size=9> MMBtu </font>", pc201)
            else:
                pc201 = ParagraphStyle('column_2', alignment = TA_CENTER, fontSize = FONT_LL, fontName = FONT_BOLD, textColor = colors.white)
                text_c201 = Paragraph(str("{:,}".format(int(site_total)))+"<font size=10> MMBtu </font>", pc201)
        elif category == 'EU':
            site_total = data_dict['site_total'] / 1000.0 #kBtu to MMBtu
            if site_total >= 1000000.0:
                pc201 = ParagraphStyle('column_2', alignment = TA_CENTER, fontSize = FONT_L, fontName = FONT_BOLD, textColor = colors.white)
                text_c201 = Paragraph(str("{:,}".format(int(site_total)))+"<font size=6> MMBtu </font>", pc201)
            elif site_total >= 100000.0:
                pc201 = ParagraphStyle('column_2', alignment = TA_CENTER, fontSize = FONT_L, fontName = FONT_BOLD, textColor = colors.white)
                text_c201 = Paragraph(str("{:,}".format(int(site_total)))+"<font size=6> MMBtu </font>", pc201)
            elif site_total < 100000.0 and site_total > 10000.0:
                pc201 = ParagraphStyle('column_2', alignment = TA_CENTER, fontSize = FONT_L, fontName = FONT_BOLD, textColor = colors.white)
                text_c201 = Paragraph(str("{:,}".format(int(site_total)))+"<font size=8> MMBtu </font>", pc201)
            elif site_total < 10000.0 and site_total > 1000.0:
                pc201 = ParagraphStyle('column_2', alignment = TA_CENTER, fontSize = FONT_L, fontName = FONT_BOLD, textColor = colors.white)
                text_c201 = Paragraph(str("{:,}".format(int(site_total)))+"<font size=9> MMBtu </font>", pc201)
            else:
                pc201 = ParagraphStyle('column_2', alignment = TA_CENTER, fontSize = FONT_LL, fontName = FONT_BOLD, textColor = colors.white)
                text_c201 = Paragraph(str("{:,}".format(int(site_total)))+"<font size=10> MMBtu </font>", pc201)
        elif category == 'EUI':
            pc201 = ParagraphStyle('column_2', alignment = TA_CENTER, fontSize = FONT_L, fontName = FONT_BOLD, textColor = colors.white)
            text_c201 = Paragraph(str(int(data_dict['siteIntensity']))+"<font size=8> kBtu/sqft </font>", pc201)
        
        return text_c201
        
    def cert_commercial(data_dict, font_size, font_normal, font_color, icon, num_line):
        t_cert = []
        pc272 = ParagraphStyle('body_left', alignment = TA_LEFT, textColor = font_color, fontSize = font_size, fontName = font_normal,  spaceBefore = -1, spaceAfter = 0, leading=10, backColor = 'white', bulletIndent = 12, firstLineIndent = 0, leftIndent = 12, rightIndent = 6)
        if 'energyStarCertificationYears' in data_dict and data_dict['energyStarCertificationYears']:
            t_cert.append([Paragraph('''<img src="'''+icon+'''" height="12" width="12"/> EPA ENERGYSTAR® Certified Building''', pc272)])
            num_line += 1
        
        t_cert.append(Paragraph("", pc272))
        t_cert = [t_cert]

        return t_cert, num_line

    def general_commercial(data_dict, font_size, font_normal, font_color, icon, num_line, includes = ['ghg','eui']):
        t_achieve = []
        pc272 = ParagraphStyle('body_left', alignment = TA_LEFT, textColor = font_color, fontSize = font_size, fontName = font_normal,  spaceBefore = -1, spaceAfter = 0, leading=10, backColor = 'white', bulletIndent = 12, firstLineIndent = 0, leftIndent = 12, rightIndent = 6)
        
        if 'ghg' in includes:
            t_achieve.append([Paragraph('''<img src="'''+icon+'''" height="12" width="12"/> '''+"This building’s greenhouse gas emissions were: " + str("{:,}".format(data_dict['totalLocationBasedGHGEmissions']))+" metric tons CO2e", pc272)])
            num_line += 1
        if 'eui' in includes:
            t_achieve.append([Paragraph('''<img src="'''+icon+'''" height="12" width="12"/> '''+"This building’s energy use intensity was: " + str(int(data_dict['siteIntensity']))+" kBtu/sq.ft.", pc272)])
            num_line += 1

        if 'yoy_percent_change_site_eui' in data_dict:
            if data_dict['yoy_percent_change_site_eui'] and abs(data_dict['yoy_percent_change_site_eui']) > 0:
                if num_line < 5:
                    t_achieve.append([Paragraph('''<img src="'''+icon+'''" height="12" width="12"/> '''+"Change in energy use intensity since last year: " + str("{:.1f}".format(data_dict['yoy_percent_change_site_eui']))+"%", pc272)])
                    num_line += 1
        if 'yoy_percent_change_elec' in data_dict:
            if data_dict['yoy_percent_change_elec'] and abs(data_dict['yoy_percent_change_elec']) > 0:
                if num_line < 5:
                    t_achieve.append([Paragraph('''<img src="'''+icon+'''" height="12" width="12"/> '''+"Change in electricity consumption since last year: " + str("{:.1f}".format(data_dict['yoy_percent_change_elec']))+"%", pc272)])
                    num_line += 1
        if 'yoy_percent_change_water' in data_dict:
            if data_dict['yoy_percent_change_water'] and abs(data_dict['yoy_percent_change_water']) > 0:
                if num_line < 5:
                    t_achieve.append([Paragraph('''<img src="'''+icon+'''" height="12" width="12"/> '''+"Change in water consumption since last year: " + str("{:.1f}".format(data_dict['yoy_percent_change_water']))+"%", pc272)])
                    num_line += 1
        if 'yoy_percent_change_ng' in data_dict:
            if data_dict['yoy_percent_change_ng'] and abs(data_dict['yoy_percent_change_ng']) > 0:
                if num_line < 5:
                    t_achieve.append([Paragraph('''<img src="'''+icon+'''" height="12" width="12"/> '''+"Change in natural gas consumption since last year: " + str("{:.1f}".format(data_dict['yoy_percent_change_ng']))+"%", pc272)])
                    num_line += 1

        if num_line < 5:
            if data_dict['percentBetterThanSiteIntensityMedian']:
                better_worse = 'more' if data_dict['percentBetterThanSiteIntensityMedian'] < 0.0 else 'less'
                t_achieve.append([Paragraph('''<img src="'''+icon+'''" height="12" width="12"/> '''+"This building is " +  str(abs(data_dict['percentBetterThanSiteIntensityMedian']))+ "% " + better_worse + " efficient than the property type national median", pc272)])
                num_line += 1
            elif data_dict['medianSiteIntensity']:
                t_achieve.append([Paragraph('''<img src="'''+icon+'''" height="12" width="12"/> '''+"The national median energy use intensity for a " +  data_dict['systemDefinedPropertyType'].lower()+ " was: " + str(data_dict['medianSiteIntensity'])+" kBtu/sq.ft.", pc272)])
                num_line += 1

        return t_achieve, num_line

    def solar_commercial(data_dict, font_size, font_normal, font_color, icon, num_line):
        t_achieve = []
        pc272 = ParagraphStyle('body_left', alignment = TA_LEFT, textColor = font_color, fontSize = font_size, fontName = font_normal,  spaceBefore = -1, spaceAfter = 0, leading=10, backColor = 'white', bulletIndent = 12, firstLineIndent = 0, leftIndent = 12, rightIndent = 6)
        pc273 = ParagraphStyle('body_left', alignment = TA_LEFT, textColor = font_color, fontSize = font_size, fontName = font_normal)
        if data_dict['onSiteRenewableSystemGeneration'] > 0.0 and num_line <= 5:
            t_achieve.append([Paragraph('''<img src="'''+icon+'''" height="12" width="12"/> '''+"This building generated " + str("{:,}".format(data_dict['onSiteRenewableSystemGeneration'])) + ' KWh of solar or wind on site', pc273)])
            num_line +=1

        if (data_dict['numberOfLevelOneEvChargingStations'] > 0 or data_dict['numberOfLevelTwoEvChargingStations'] > 0 or data_dict['numberOfDcFastEvChargingStations'] > 0) and num_line <= 5:
            t_achieve.append([Paragraph('''<img src="'''+icon+'''" height="12" width="12"/> '''+"This building has an electric vehicle charging on-site", pc273)])
            num_line +=1

        return t_achieve, num_line


def validate_data_dict(data_dict: dict) -> bool:
    is_valid = True
    msg = ''

    #Data tests
    if ('siteEnergyUseElectricityGridPurchaseKwh' in data_dict and data_dict['siteEnergyUseElectricityGridPurchaseKwh'] > 0.0):
        data_dict['siteEnergyUseElectricityGridPurchase'] = data_dict['siteEnergyUseElectricityGridPurchaseKwh'] * FUELFACTOR[0]
    
    #Concatenate fuels
    oil_list = ['Diesel', 'FuelOil1', 'FuelOil2', 'FuelOil4', 'FuelOil5And6']
    data_dict['siteEnergyUseFuelOil'] = 0.0
    data_dict['energyCostFuelOil'] = 0.0
    for oil in oil_list:
        if 'siteEnergyUse'+oil in data_dict:
            if data_dict['siteEnergyUse'+oil] is not None:
                data_dict['siteEnergyUseFuelOil'] += data_dict['siteEnergyUse'+oil]
            if data_dict['energyCost'+oil] is not None:
                data_dict['energyCostFuelOil'] += data_dict['energyCost'+oil]
    propane_list = ['Propane', 'Kerosene']
    for propane in propane_list:
        if 'siteEnergyUse'+propane in data_dict:
            if data_dict['siteEnergyUse'+propane] is not None:
                data_dict['siteEnergyUsePropane'] += data_dict['siteEnergyUse'+propane]
            if data_dict['energyCost'+propane] is not None:
                data_dict['energyCostPropane'] += data_dict['energyCost'+propane]
    district_list = ['DistrictSteam', 'DistrictHotWater', 'DistrictChilledWater']
    for district in district_list:
        if 'siteEnergyUse'+district in data_dict:
            if data_dict['siteEnergyUse'+district] is not None:
                data_dict['siteEnergyUseDistrictSteam'] += data_dict['siteEnergyUse'+district]
            if data_dict['energyCost'+district] is not None:
                data_dict['energyCostDistrictSteam'] += data_dict['energyCost'+district]
    
    #Recalculate site total if there is at least electricity
    if ('siteEnergyUseElectricityGridPurchaseKwh' in data_dict and data_dict['siteEnergyUseElectricityGridPurchaseKwh'] > 0.0 and data_dict['site_total'] in [0,None]):
        data_dict['site_total'] = 0.0
        for num, fuel in enumerate(FUELS):
            if ('energyCost'+fuel in data_dict) and data_dict['siteEnergyUse'+fuel]:
                data_dict['site_total'] += data_dict['siteEnergyUse'+fuel]/1000.0
        
    # Check that site_total exists and has data -> meaning it has energy usage by (mmbtu)
    if not data_dict.get('site_total', None):
        is_valid = False
        msg += 'No site_total found or is Zero; '

    return is_valid, msg, data_dict
