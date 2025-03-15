# Ultimate Patcher

#### This repo will be a generic APK patcher that works with java instead of smali.

# Currently, this project is in POC stage, it's working but not fully tested.

## How it works

1. Decompile the APK with apktool
2. Compile the patch's java code with gradlew to apk
3. Extract the smali code of your patch apk
4. Copy it to the original apk
5. Add a call to the patch entry point in the original apk within every onCreate and init of exposed classes.
6. Recompile the apk with apktool
7. Sign the apk with uber-apk-signer

And that's it. When the app will be launched, the patch will be executed by the onCreate of the MainActivity.

## Installation

1. Clone the repo.

```bash
git clone git@github.com:Schwartzblat/UltimatePatcher.git
```

2. Override the java files in the `./smali_generator/app/src/main/com/smali_generator/*` with your own patch code.
3. Setup the python environment.

```bash
python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

4. Run the script with the path to the apk you want to patch.

```bash
python main.py -p apk_to_patch.apk -o output_apk.apk
```
