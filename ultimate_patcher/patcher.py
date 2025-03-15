import subprocess
from ultimate_patcher.apk_utils import *
from ultimate_patcher import config


def prepare_smali() -> None:
    print('[+] Assembling the java...')
    subprocess.check_call(['./gradlew', 'assembleRelease'], cwd=str(config.SMALI_GENERATOR_PATH))
    print('[+] Extracting the smali...')
    extract_apk(str(config.SMALI_GENERATOR_OUTPUT_PATH), config.SMALI_GENERATOR_PATH / 'extracted')


def patch_apk(extracted_path: str) -> None:
    prepare_smali()
    print(extracted_path)
