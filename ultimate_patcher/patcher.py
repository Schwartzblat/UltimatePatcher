import pathlib
import re
import shutil
import lxml.etree
from androguard.core.apk import APK
from androguard.util import set_log
from ultimate_patcher.apk_utils import *
from ultimate_patcher.config import ManifestKeys

set_log('CRITICAL')
INVOKE_LINE = '\n\tinvoke-static {}, Lcom/smali_generator/TheAmazingPatch;->on_load()V\n\t'


def prepare_smali() -> None:
    print('[+] Assembling the java...')
    subprocess.check_call(['./gradlew', 'assembleRelease'], cwd=str(config.SMALI_GENERATOR_PATH))
    print('[+] Extracting the smali...')
    extract_apk(str(config.SMALI_GENERATOR_OUTPUT_PATH), config.SMALI_GENERATOR_SMALI_PATH)


def get_activities_with_entry_points(apk_path: str) -> list:
    manifest: lxml.etree.Element = APK(apk_path).get_android_manifest_xml()
    activities = []
    for element in manifest.find('.//application').getchildren():
        should_patch = False
        if element.tag == 'activity' or element.tag == 'activity-alias':
            should_patch = element.get(ManifestKeys.EXPORTED) == 'true'
        elif element.tag == 'provider' or element.tag == 'receiver' or element.tag == 'service':
            should_patch = True
        if should_patch:
            activities.append(element)
    return activities


def patch_or_add_function(smali_file_path: pathlib.Path, function_name: str) -> None:
    with open(smali_file_path, 'r') as file:
        smali_file = file.read()
    matches = re.findall(fr'\.method public [^\n]*{function_name}[^\n]*\n[^\n]+', smali_file)
    if len(matches) == 0:
        pass
    for match in matches:
        smali_file = smali_file.replace(match, match + INVOKE_LINE)
    with open(smali_file_path, 'w') as file:
        file.write(smali_file)


def add_static_call_to_on_load(args, class_name: str, function_name: str) -> None:
    smali_file_path = find_smali_file_by_class_name(pathlib.Path(args.temp_path), class_name)
    if smali_file_path is None:
        print(f'[-] Failed to find smali file for {class_name}')
        return
    patch_or_add_function(smali_file_path, function_name)


def patch_entries(args) -> None:
    print('[+] Searching for activities with entry points...')
    activities_to_patch = get_activities_with_entry_points(args.apk_path)
    print(f'[+] Found {len(activities_to_patch)} activities with entry points')
    for activity in activities_to_patch:
        add_static_call_to_on_load(args, activity.get(
            ManifestKeys.TARGET_ACTIVITY if activity.tag == 'activity-alias' else ManifestKeys.NAME),
                                   'onCreate' if 'activity' in activity.tag else '<init>')


def patch_apk(args) -> None:
    print('[+] Preparing the smali...')
    prepare_smali()
    print('[+] Applying the custom smali...')
    shutil.copytree(config.SMALI_GENERATOR_SMALI_PATH / 'smali', pathlib.Path(args.temp_path) / 'smali',
                    dirs_exist_ok=True)
    print('[+] Adding calls to the custom smali...')
    patch_entries(args)
