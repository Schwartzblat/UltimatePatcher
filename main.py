import argparse
from ultimate_patcher.apk_utils import *
from ultimate_patcher.patcher import patch_apk

def get_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-p', '--apk-path', dest='apk_path', help='APK path', required=True)
    parser.add_argument('-o', '--output', dest='output', help='Output APK path', required=False, default='output.apk')
    parser.add_argument('-t', '--temp', dest='temp_path', help='Temp path for extracted content', required=False, default='./extracted')
    return parser.parse_args()


def check_args(args) -> None:
    if not os.path.exists(args.apk_path):
        print('APK file not found')
        exit(1)


def main():
    args = get_args()
    check_args(args)
    print('[+] Extracting APK...')
    extract_apk(args.apk_path, args.temp_path)

    print('[+] Patching APK...')
    patch_apk(args.temp_path)

    print('[+] Compiling APK...')
    compile_apk(args.temp_path, args.output)

    print('[+] Signing APK...')
    sign_apk(args.output)

if __name__ == '__main__':
    main()
