# LEDA 應用程式編譯與 Tauri 打包指南

本指南介紹如何編譯舊版 Python LEDA 應用程式並使用 Rust Tauri 進行打包。

## 編譯 Python LEDA 應用程式

1. **複製檔案**
   - 將 `files` 目錄中的所有檔案複製到 `earth-api` 目錄（與 `app.py` 位於同一目錄）。

2. **設置 Conda 環境**
   - 執行以下命令以建立環境：
     ```bash
     conda env create -f environment.yml
     ```

3. **修改程式碼以適配相容性**
   - 更新以下語法以符合 Python 套件版本要求：
     - 將 `exit(0)` 替換為：
       ```python
       import sys
       sys.exit(0)
       ```
     - 將 `exit(1)` 替換為：
       ```python
       import sys
       sys.exit(1)
       ```
     - 將 `NoneStr` 替換為 `Optional[str]`。
   - 移除 `dataclasses` 套件並安裝相容的 `pyinstaller` 版本：
     ```bash
     pip uninstall dataclasses
     pip install "pyinstaller<6"
     ```
   - 修改 PyInstaller 的 hook 檔案，位於：
     ```
     C:\Users\<你的用戶名>\.conda\envs\leda\lib\site-packages\_pyinstaller_hooks_contrib\stdhooks\hook-transformers.py
     ```
     將第 29 行的程式碼：
     ```python
     if not is_module_satisfies(dependency_req):
     ```
     替換為：
     ```python
     for dependency_name, dependency_req in dependencies.items():
         try:
             if not is_module_satisfies(dependency_req):
                 continue
             datas += copy_metadata(dependency_name)
         except Exception:
             # 可選擇印出錯誤訊息
             # print(f"Skipped {dependency_name} due to error: {e}")
             pass
     ```

4. **建構應用程式**
   - 使用以下命令透過 PyInstaller 建構應用程式：
     ```bash
     pyinstaller app.spec
     ```

5. **重新匯出 Conda 環境（可選）**
   - 若需重新匯出 Conda 環境，請使用：
     ```bash
     conda env export > environment.yml
     ```

## Rust Tauri 打包

1. **安裝 Tauri CLI**
   - 參考 [Tauri 前置條件](https://tauri.app/start/prerequisites/) 的要求。
   - 安裝指定版本的 Tauri CLI：
     ```bash
     cargo install tauri-cli --version "^2.0.0" --locked
     ```

2. **複製編譯完成的 LEDA 應用程式**
   - 將 `earth-api/dist` 目錄中的 `leda_app` 複製到 `leda_tauri` 目錄。

3. **開發與建構命令**
   - 開發模式：
     ```bash
     cargo tauri dev
     ```
   - 建構應用程式：
     ```bash
     cargo tauri build
     ```

4. **開發新 Tauri API 的建議**
   - 原有 LEDA 應用程式監聽埠 `8000`。
   - 新 Tauri API 建議監聽埠 `8001`。
   - 更新前端程式碼，明確指定舊埠（`8000`）和新埠（`8001`），以避免衝突。

## 注意事項
- 將檔案路徑中的 `<你的用戶名>` 替換為你的實際用戶名。
- 確保所有依賴套件與使用的 Python 和 Tauri 版本相容。
- 修改完成後，徹底測試應用程式以確保功能正常。