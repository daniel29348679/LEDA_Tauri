# LEDA App Compilation Guide

This guide provides step-by-step instructions to compile the LEDA app for Python and package it using PyInstaller, followed by integrating it with Rust Tauri for a desktop application.

## Python Compilation

### Step 1: Setup Files
- Copy all files from the `files` directory into the `earth-api` directory (same location as `app.py`).
- `clean.ps1` need to be applied after pyinstaller compile failed.You must run it in the `earth-api` dir.

### Step 2: Update Syntax
Ensure the following syntax updates are applied to the codebase to match package version requirements:
- Replace `exit(0)` with:
  ```python
  import sys
  sys.exit(0)
  ```
- Replace `exit(1)` with:
  ```python
  import sys
  sys.exit(1)
  ```
- Replace `NoneStr` with `Optional[str]`.

*Note*: The provided files are assumed to have these changes already applied.

### Step 3: Create and Activate Conda Environment
Run the following commands to set up the environment:
```bash
conda create --name=leda python=3.8
conda activate leda
conda install pytorch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 cpuonly -c pytorch
pip install -r requirements.txt
```

### Step 4: Install PyInstaller and Dependencies
Install the required PyInstaller packages:
```bash
pip uninstall dataclasses
pip install "pyinstaller<6"
pip install "pyinstaller-hooks-contrib==2025.4"
```

### Step 5: Modify PyInstaller Hook
Locate the file `hook-transformers.py` in one of the following paths (replace `Daniel` with your username):
- Local installation: `C:\Users\<YourUsername>\.conda\envs\leda\lib\site-packages\_pyinstaller_hooks_contrib\stdhooks\hook-transformers.py`
- Global installation: `C:\ProgramData\anaconda3\envs\leda\lib\site-packages\_pyinstaller_hooks_contrib\stdhooks\hook-transformers.py`

Replace the content starting from line 21 (starting with `except Exception:`) to the end with:
```python
except Exception:
    logger.warning(
        "hook-transformers: failed to query dependency table (transformers.dependency_versions_table.deps)!",
        exc_info=True,
    )
    dependencies = {}

    for dependency_name, dependency_req in dependencies.items():
        try:
            if not is_module_satisfies(dependency_req):
                continue
            datas += copy_metadata(dependency_name)
        except Exception:
            # Can print error message if needed
            # print(f"Skipped {dependency_name} due to error: {e}")
            pass
# Collect source .py files for JIT/torchscript. Requires PyInstaller >= 5.3, no-op in older versions.
module_collection_mode = 'pyz+py'
```

### Step 6: Run PyInstaller
Execute the following command to build the app:
```bash
pyinstaller app.spec
```

### Step 7: Verify the Build
- The compiled app will be located in `dist/leda_app`.
- Run `leda_app.exe` in the `leda_app` folder to test the build.
- If an error occurs (e.g., missing `libzbar-64.dll`), ensure Visual C++ Redistributable(Visual Studio 2013 (VC++ 12.0)) is installed on your system. Most systems should already have this installed.

## Rust Tauri Packaging

### Step 1: Install Tauri CLI
Follow the prerequisites outlined at [Tauri Prerequisites](https://tauri.app/start/prerequisites/). Then, install the Tauri CLI:
```bash
cargo install tauri-cli --version "^2.0.0" --locked
```

### Step 2: Copy Compiled LEDA App
- Copy the compiled `leda_app` folder from `earth-api/dist` to the `leda_tauri` directory.

### Step 3: Develop and Build with Tauri
- For development:
  ```bash
  cargo tauri dev
  ```
- For building the final app:
  ```bash
  cargo tauri build
  ```

### Recommendations for New Tauri API Development
- The original LEDA app listens on port `8000`.
- For a new Tauri API, use port `8001`.
- Update the frontend to explicitly specify the old (`8000`) and new (`8001`) ports to avoid conflicts.