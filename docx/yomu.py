import glob
import os
import sys
sys.path.append('../lib')
import ntzreg
from docx2python import docx2python
from docx2python.iterators import iter_paragraphs

file_path = glob.glob("./*.docx")

for file in file_path:
    # 下準備　ファイル名取得　拡張子を取ったオリジナルのファイル名が欲しい。
    basename, ext = os.path.splitext( os.path.basename(file) )
    # docx2pythonのインスタンスを作成する。
    content = docx2python(file)

    # 本文、ルビ、脚注を抜き出すメソッドを呼んで、オブジェクトに格納する。
    doc = '\n'.join(iter_paragraphs(content.document))
    contents = ntzreg.text_ins_reg(doc)
    with open(f'{basename}.txt', "w") as f:
        f.write(contents)

# documentメソッドなど、解説は下記リンクページ。
# https://docx2python.readthedocs.io/en/latest/index.html#return-value

# # 切っ掛けになったコード その1　ワードから文字列を抜き出すライブラリー
# import docx
# doc = docx.Document('sample.docx')
# all_body = '\n'.join(paragraph.text for paragraph in doc.paragraphs)
# print(all_body)

# # 切っ掛けになったコード その2　ワードから文字列を抜き出すライブラリー
# import docx2txt
# text = docx2txt.process(file)

# # 切っ掛けになったコード その3　ワードから文字列を抜き出すライブラリー
# # extract footnotes
# import glob
# from docx2python import docx2python
# from docx2python.iterators import iter_paragraphs
#
# file_path = glob.glob("./*.docx")
# file = file_path[0]
# content = docx2python(file)
# footnotes = '\n\n'.join(iter_paragraphs(content.footnotes))
# print(footnotes)
