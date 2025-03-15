import pathlib
import shutil
from ultimate_patcher.apk_utils import *


def prepare_smali() -> None:
    print('[+] Assembling the java...')
    subprocess.check_call(['./gradlew', 'assembleRelease'], cwd=str(config.SMALI_GENERATOR_PATH))
    print('[+] Extracting the smali...')
    extract_apk(str(config.SMALI_GENERATOR_OUTPUT_PATH), config.SMALI_GENERATOR_SMALI_PATH)


def patch_apk(extracted_path: str) -> None:
    print('[+] Preparing the smali...')
    prepare_smali()
    print('[+] Applying the custom smali...')
    shutil.copytree(config.SMALI_GENERATOR_SMALI_PATH / 'smali', pathlib.Path(extracted_path) / 'smali', dirs_exist_ok=True)
