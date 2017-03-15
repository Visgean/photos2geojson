import os
import argparse
import json

from photos2geojson import utils
from photos2geojson import simple_gist

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
        default='./ouput.geojson')

    args = parser.parse_args()

    if not os.path.isdir(args.base_dir):
        print('{} directory does not exist. Choose another one.'.format(args.base_dir))
        exit(1)

    if not args.output:
        output_file = ''
    else:
        output_file = args.output


    pics = utils.get_pictures(args.base_dir)
    exif_data = list(filter(None, map(utils.get_exif, pics)))
    locs = map(utils.parse_exif, exif_data)
    full_locs = list(filter(None, locs))
    geojson_struct = utils.get_geojson_structure(full_locs)

    print('Found', len(pics), 'pics.', len(full_locs), 'pics have valid location data.')

    if args.gist:
        url = simple_gist.upload_gist('pics.geojson', json.dumps(geojson_struct))
        print('Created gist:', url)
    else:
        with open(output_file, 'w') as f:
            f.write(json.dumps(geojson_struct, indent=2))
        print('Geojson written to', output_file)

if __name__ == '__main__':
    main()