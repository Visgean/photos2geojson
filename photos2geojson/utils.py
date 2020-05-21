from datetime import datetime

import exifread
import glob
import os
import json



picture_extensions = ['.jpg', '.jpeg', '.png']

def get_extension(filename):
    filename, file_extension = os.path.splitext(filename)
    return file_extension.lower()


def get_pictures(directory):
    is_img = lambda f: get_extension(f) in picture_extensions
    files = glob.iglob(directory + '/**/*', recursive=True)
    abs_files = map(os.path.abspath, files)
    return list(filter(is_img, abs_files))


def get_exif(filename):
    try:
        with open(filename, 'rb') as f:
            return exifread.process_file(f)
    except:
        return


def parse_date(exif_info):
    if not exif_info:
        return    
    date = exif_info.get('Image DateTime')
    if not date:
        return
    try:
        return datetime.strptime(str(date.values), '%Y:%m:%d %H:%M:%S').date()
    except ValueError:
        return


# based on: https://gist.github.com/snakeye/fdc372dbf11370fe29eb

def convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    try:
        d = float(value.values[0].num) / float(value.values[0].den)
        m = float(value.values[1].num) / float(value.values[1].den)
        s = float(value.values[2].num) / float(value.values[2].den)
    except (ZeroDivisionError, IndexError) as e:
        d = m = s = 0

    return d + (m / 60.0) + (s / 3600.0)
    
def get_exif_location(exif_data):
    """
    Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)
    """
    lat = None
    lon = None

    gps_latitude = exif_data.get('GPS GPSLatitude')
    gps_latitude_ref = exif_data.get('GPS GPSLatitudeRef')
    gps_longitude = exif_data.get('GPS GPSLongitude')
    gps_longitude_ref = exif_data.get('GPS GPSLongitudeRef')

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = convert_to_degress(gps_latitude)
        if gps_latitude_ref.values[0] != 'N':
            lat = round(0 - lat, 6)

        lon = convert_to_degress(gps_longitude)
        if gps_longitude_ref.values[0] != 'E':
            lon = round(0 - lon, 6)
    return lat, lon


def parse_exif(filename):
    exif_data = get_exif(filename)

    if not exif_data:
        return None

    lat, lon = get_exif_location(exif_data)
    date = parse_date(exif_data)

    if (lat, lon) == (None, None):
        return None

    return {
        'filename': filename,
        'lat': lat,
        'lon': lon,
        'date': date
    }


def get_geojson_structure(parsed_data):
    "parsed_data are expected to be result of parse_exif()"

    feature_list = [
        {
            "type": "Feature",
            "properties": {
                "date": exif_dict['date'].isoformat() if exif_dict['date'] else '',
                "filename": exif_dict['filename'],  
            },

            "geometry": {
                "type": "Point",
                "coordinates": [
                    exif_dict['lon'],
                    exif_dict['lat']
                ]
            }
        }
        for exif_dict in parsed_data
    ]

    return {
      "type": "FeatureCollection",
      "features": feature_list
    }
