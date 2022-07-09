import glob
import os
import sys
import zipfile
from pathlib import Path

file_path = glob.glob("./*.docx")

docx_path = Path(file_path[0])
# これは関数か？　ZIPファイルをこれで解凍している。
docx_zip = zipfile.ZipFile(docx_path)
zipped_files = docx_zip.namelist()

# 画像を保存するフォルダーの生成
img_dir = Path("doc_images")
img_dir.mkdir(exist_ok=True)

for file in zipped_files:
    if file.startswith("word/media/"):
        # 画像ファイルを開く
        img_file = docx_zip.open(file)
        # 画像ファイルの読み込み
        img_bytes = img_file.read()
        # 保存する画像ファイル名には、「docxファイル名_」を先頭に付ける
        img_path = img_dir / (docx_path.stem + "_" + Path(file).name)
        # 画像ファイルの保存
        with img_path.open(mode="wb") as f:
            f.write(img_bytes)
        img_file.close()

docx_zip.close()