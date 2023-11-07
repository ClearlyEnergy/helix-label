#!/usr/bin/env python
# encoding: utf-8
"""
Constants.py
"""
import os
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Image

module_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
IMG_PATH = os.path.normpath(os.path.join(module_path, "images"))

CUSTOM_LGRAY = colors.Color(red=(242.0/255),green=(246.0/255),blue=(248.0/255))
CUSTOM_DGRAY = colors.Color(red=(109.0/255),green=(111.0/255),blue=(106.0/255))
CUSTOM_MGRAY = colors.Color(red=(111.0/255),green=(111.0/255),blue=(106.0/255))
CUSTOM_LGREEN = colors.Color(red=(209.0/255),green=(229.0/255),blue=(202.0/255))
CUSTOM_DGREEN = colors.Color(red=(65.0/255),green=(173.0/255),blue=(73.0/255))
CUSTOM_MGREEN = colors.Color(red=(74.0/255),green=(151.0/255),blue=(93.0/255))
CUSTOM_ELECGREEN = colors.Color(red=(113.0/255),green=(168.0/255),blue=(80.0/255))
CUSTOM_LORANGE = colors.Color(red=(242.0/255),green=(151.0/255),blue=(152.0/255))
CUSTOM_ORANGE = colors.Color(red=(217.0/255),green=(92.0/255),blue=(35.0/255))
CUSTOM_YELLOW = colors.Color(red=(255.0/255),green=(221.0/255),blue=(0.0/255))
CUSTOM_LTEAL = colors.Color(red=(53.0/255),green=(196.0/255),blue=(229.0/255))
CUSTOM_DTEAL = colors.Color(red=(54.0/255),green=(109.0/255),blue=(238.0/255)) ## This is the color to customize
FUELS = ['ElectricityGridPurchase', 'NaturalGas', 'FuelOil', 'Propane',  'Wood']
#FUELICONS = [u"",u"\uf06d",u"\uf043",u"\uf043",u"\uf1bb",u"\uf185"]
FUELICONS = [u"\uf0e7",u"\uf06d",u"\uf043",u"\uf043",u"\uf1bb",u"\uf185"]
FUELIMAGES = [Image(IMG_PATH+"/HomeEnergyProfile_icons-03.png",0.4*inch,0.4*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-09.png",0.4*inch,0.4*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-10.png",0.4*inch,0.4*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-11.png",0.4*inch,0.4*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-02.png",0.4*inch,0.4*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-02.png",0.4*inch,0.4*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-04.png",0.4*inch,0.4*inch)]
FUELIMAGESSMALL = [Image(IMG_PATH+"/HomeEnergyProfile_icons-03.png",0.3*inch,0.3*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-09.png",0.3*inch,0.3*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-10.png",0.3*inch,0.3*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-11.png",0.3*inch,0.3*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-02.png",0.3*inch,0.3*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-02.png",0.3*inch,0.3*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-04.png",0.3*inch,0.3*inch)]
FUELLABEL = ['Electric', 'Natural Gas', 'Heating Oil', 'Propane', 'Wood']
FUELUNIT = ['kwh', 'ccf', 'gal', 'gal', 'ton']
FUELCOLOR = [CUSTOM_ELECGREEN, CUSTOM_ORANGE, CUSTOM_DTEAL, CUSTOM_LTEAL, CUSTOM_MGREEN]

FONT_XXL = 30
FONT_XL = 24
FONT_LL = 16
FONT_L = 14
FONT_ML = 12
FONT_H = 10
FONT_T = 9
FONT_S = 8

FONT_NORMAL = 'InterstateLight'
FONT_BOLD = 'InterstateBlack'
CHECK = u"\u2713"
UNCHECKED = u"\u2752"
CHECK_IMG = IMG_PATH+"/HomeEnergyProfile_icons-13.png"



