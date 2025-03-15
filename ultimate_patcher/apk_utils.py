import os
import subprocess
from ultimate_patcher import config


def extract_apk(apk_path: str, output_path: str = './extracted') -> None:
    if os.path.exists(output_path):
        return
    subprocess.check_call(
        [
            "java",
            "-jar",
            config.APKTOOL_PATH,
            "-q",
            "d",
            # "-r",
            "--output",
            output_path,
            apk_path,
        ],
        timeout=20 * 60,
    )


def compile_apk(input_path: str = './extracted', output_path: str = 'output.apk') -> None:
    subprocess.check_call([
        "java",
        "-jar",
        config.APKTOOL_PATH,
        "-q",
        "build",
        "--use-aapt2",
        input_path,
        "--output",
        output_path
    ],
        timeout=20 * 60,

    )


def sign_apk(apk_path: str, output_path: str = 'signed-output.apk') -> None:
    subprocess.check_call(
        [
            "java",
            "-jar",
            config.UBER_APK_SIGNER_PATH,
            "--apks",
            apk_path
        ],
        timeout=20 * 60,
    )
    os.remove(apk_path)
    os.rename(
        f'{apk_path.removesuffix(".apk")}-aligned-debugSigned.apk',
        output_path,
    )
