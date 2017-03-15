import os
import argparse
import json
import pkg_resources

from photos2geojson import utils
from photos2geojson import simple_gist


LEAFLET_MAP = pkg_resources.resource_filename('photos2geojson', 'leaflet.html')


def main():
    parser = argparse.ArgumentParser(description='EXIF data to gejson')
    
    parser.add_argument(
        'base_dir', 
        help='Basic directory with photos')
    
    parser.add_argument(
        '-g','--gist', 
        dest='gist',
        help='Create github gist with data', 
        action='store_true')

    parser.add_argument(
        '-o','--output', 
        help='Output file',
    )

    parser.add_argument(
        '-l','--leaflet', 
        help='specify location for html leaflet map file',
        default='map.html'
    )


    args = parser.parse_args()
    if not os.path.isdir(args.base_dir):
        print('{} directory does not exist. Choose another one.'.format(args.base_dir))
        exit(1)

    pics = utils.get_pictures(args.base_dir)
    full_locs = list(filter(None, map(utils.parse_exif, pics)))
    geojson_struct = utils.get_geojson_structure(full_locs)

    print('Found', len(pics), 'pics.', len(full_locs), 'pics have valid location data.')

    if args.gist:
        url = simple_gist.upload_gist('pics.geojson', json.dumps(geojson_struct))
        print('Created gist:', url)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(json.dumps(geojson_struct, indent=2))
        print('Geojson written to', args.output)

    if args.leaflet:
        with open(LEAFLET_MAP) as f:
            map_html = f.read()

        # This is kind of dirty / I could replace it with jinja2 
        # but it only one very simple call so what the hell.

        map_with_data = map_html.replace(
            '__geo_json__here_please__', 
            json.dumps(geojson_struct)
        )

        with open(args.leaflet, 'w') as f:
            f.write(map_with_data)
        print('Map written to', args.leaflet)


if __name__ == '__main__':
    main()