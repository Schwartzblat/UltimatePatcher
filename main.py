import argparse
import shutil

from ultimate_patcher.apk_utils import *
from artifactory import prepare_artifactory
from ultimate_patcher.patcher import patch_apk


def get_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-p', '--apk-path', dest='apk_path', help='APK path', required=True)
    parser.add_argument('-o', '--output', dest='output', help='Output APK path', required=False, default='output.apk')
    parser.add_argument('-t', '--temp', dest='temp_path', help='Temp path for extracted content', required=False,
                        default='./temp')
    parser.add_argument('--arch', dest='arch', help='Architecture', required=False, default='arm64-v8a',
                        choices=['arm64-v8a', 'armeabi-v7a', 'x86', 'x86_64'])
    parser.add_argument('--artifactory', dest='artifactory', help='Artifactory path', required=False, default='./artifactory.json')
    return parser.parse_args()


def check_args(args) -> None:
    if not os.path.exists(args.apk_path):
        print('APK file not found')
        exit(1)


def clean_up(args):
    shutil.rmtree(args.temp_path, ignore_errors=True)
    if os.path.exists(args.artifactory):
        os.remove(args.artifactory)

def main():
    args = get_args()
    check_args(args)
    try:
        print('[+] Extracting APK...')
        extract_apk(args.apk_path, str(pathlib.Path(args.temp_path) / config.EXTRACTED_TEMP_DIR))

        print('[+] Finding artifacts...')
        prepare_artifactory(args)

        print('[+] Patching APK...')
        patch_apk(args)

        print('[+] Compiling APK...')
        compile_apk(str(pathlib.Path(args.temp_path) / config.EXTRACTED_TEMP_DIR), args.output)

        print('[+] Signing APK...')
        sign_apk(args.output)
    finally:
        print('[+] Cleaning up...')
        clean_up(args)


if __name__ == '__main__':
    main()
