import argparse
import glob
import os
import shutil

from mutagen.flac import FLAC


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('dest')
    parser.add_argument('-n', '--dry-run', action='store_true')

    return parser.parse_args()


def get_new_name(source, dest, artist, date, album, track_number, title):
    path = '{}/{}/{} - {}'.format(dest, artist, date, album)
    _, extension = os.path.splitext(source)
    filename = '{:02d} - {}{}'.format(track_number, title, extension)
    dest_path = os.path.join(path, filename).replace(' ', '_')
    print('Copying ' + source)
    print('to ' + dest_path)
    print()
    return dest_path


def get_field(field):
    return field[0].replace('/', '-')


def extract_and_copy(source, dest, dry_run):
    source_pattern = '{}/**/*.flac'.format(source)
    for file_path in glob.iglob(source_pattern, recursive=True):
        file = FLAC(file_path)
        dest_path = get_new_name(file_path, dest,
                                 get_field(file['artist']),
                                 get_field(file['date']),
                                 get_field(file['album']),
                                 int(get_field(file['tracknumber'])),
                                 get_field(file['title']))
        if not dry_run:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(file_path, dest_path)


def main():
    args = parse_arguments()
    extract_and_copy(args.source, args.dest, args.dry_run)


if __name__ == '__main__':
    main()
