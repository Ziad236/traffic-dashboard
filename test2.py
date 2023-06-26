import matplotlib.font_manager

font_list = matplotlib.font_manager.findSystemFonts()
for font in font_list:
    print(font)