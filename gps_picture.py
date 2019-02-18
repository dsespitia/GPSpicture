import platform
import argparse
import os
import gmaps
from PIL import Image
from PIL.ExifTags import TAGS
from ipywidgets.embed import embed_minimal_html

# Validar con la cabecera de JPG los archivos en el sistema
def search(path):
    tipo = b'\xFF\xD8\xFF\xE0\x00\x10\x4A\x46'
    lista = []
    log = len(tipo)
    for ruta, direc, files in os.walk(path, topdown=True):
        if platform.system() == "Linux":
            for det in files:
                vict = ruta + os.sep + det
                if os.access(vict, os.R_OK) and os.path.isfile(vict):
                    f = open(vict, "rb")
                    b = f.read(log)
                    if b == tipo:
                        lista.append(vict)
        elif platform.system() == "Windows":
            ext = "jpg"
            for det in files:
                if det.endswith('.' + ext):
                    vict = ruta + os.sep + det
                    f = open(vict, "rb")
                    b = f.read(log)
                    if b == tipo:
                        lista.append(vict)
    return lista


# Create maps using API Google Map
def marker(locations):
    gmaps.configure(api_key=os.environ["GOOGLE_API_KEY"])
    fig = gmaps.figure()
    layer = gmaps.marker_layer(locations)
    fig.add_layer(layer)
    return(fig)

# Create maps using API Google Map
def heat(locations):
    gmaps.configure(api_key=os.environ["GOOGLE_API_KEY"])
    fig = gmaps.figure()
    layer = gmaps.heatmap_layer(locations)
    fig.add_layer(layer)
    return(fig)


#Detect geocode in metadata of files
def gpsinfo(path):
    picture = Image.open(path)
    infopic = picture._getexif()
    for (tag,value) in infopic.items():
        tagname = TAGS.get(tag, tag)
        if tagname == "GPSInfo":
            if value[1][0] == "N" and value[3][0] == "E":
                lat = value[2][0][0] + (value[2][1][0]/60) + (value[2][2][0]/(3600*value[2][2][1]))
                lon = value[4][0][0] + (value[4][1][0]/60) + (value[4][2][0]/(3600*value[4][2][1]))
            elif value[1][0] == "N" and value[3][0] == "W":
                lat = value[2][0][0] + (value[2][1][0]/60) + (value[2][2][0]/(3600*value[2][2][1]))
                lon = (value[4][0][0] + (value[4][1][0]/60) + (value[4][2][0]/(3600*value[4][2][1])))*-1
            elif value[1][0] == "S" and value[3][0] == "E":
                lat = (value[2][0][0] + (value[2][1][0]/60) + (value[2][2][0]/(3600*value[2][2][1])))*-1
                lon = value[4][0][0] + (value[4][1][0]/60) + (value[4][2][0]/(3600*value[4][2][1]))
            elif value[1][0] == "S" and value[3][0] == "W":
                lat = (value[2][0][0] + (value[2][1][0]/60) + (value[2][2][0]/(3600*value[2][2][1])))*-1
                lon = (value[4][0][0] + (value[4][1][0]/60) + (value[4][2][0]/(3600*value[4][2][1])))*-1
    convert = (lat,lon)
    return(convert)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help='specify path of jpg files')
    parser.add_argument("-T","--type", type=str, help='select marker or heatmap', default="marker")
    args = parser.parse_args()
    if args.path == None:
        print(parser.print_usage)
        exit(0)
    elif os.path.exists(args.path):
        lista = search(args.path)
        imagenes = []
        locations = []
        for img in lista:
            pic = Image.open(img)
            info = pic._getexif()
            if not info is None:
                for (tag, value) in info.items():
                    tagname = TAGS.get(tag, tag)
                    if tagname == "GPSInfo":
                        if value[1][0]:
                            imagenes.append(img)
        if len(imagenes) == 0:
            print("no jpg file contains location data")
            exit(0)
        else:
            for loc in imagenes:
                locs = gpsinfo(loc)
                locations.append(locs)
        if args.type == "marker":
            geopic = marker(locations)
            embed_minimal_html('export.html', views=[geopic])
        else:
            geopic = heat(locations)
            embed_minimal_html('export.html', views=[geopic])
    else:
        print("Path do not exist")
        exit(0)

if __name__ == '__main__':
    main()
