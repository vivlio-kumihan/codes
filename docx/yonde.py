import glob
import os
import sys
import docx
from docx.shared import RGBColor

file_path = glob.glob("./*.docx")

for fp in file_path:
    # 下準備　ファイル名取得　拡張子を取り去ったファイル名を確保する。
    basename, ext = os.path.splitext(os.path.basename(fp))
    # 処理するファイルをインスタンス化
    doc = docx.Document(fp)
    # 処理開始
    for pgh in doc.paragraphs:
      for run in pgh.runs:
        # 太字 + イタリック + 下線
        if run.bold and run.italic and run.underline:
          run.bold = False
          run.italic = False
          run.underline = False
          run.font.color.rgb = RGBColor(255, 85, 50)
          # run.text = f'<bld-ita-udl>{run.text}</bld-ita-udl>'
        # 太字 + イタリック
        elif run.bold and run.italic:
          run.bold = False
          run.italic = False
          run.font.color.rgb = RGBColor(255, 190, 50)
          # run.text = f'<bld-ita>{run.text}</bld-ita>'
        # 太字 + 下線
        elif run.bold and run.underline:
          run.bold = False
          run.underline = False
          run.font.color.rgb = RGBColor(115, 255, 50)
          # run.text = f'<bld-udl>{run.text}</bld-udl>'
        # イタリック + 下線
        elif run.italic and run.underline:
          run.italic = False
          run.underline = False
          run.font.color.rgb = RGBColor(50, 175, 255)
          # run.text = f'<ita-udl>{run.text}</ita-udl>'
        elif run.bold:
        # 太字 bold
          run.bold = False
          run.font.color.rgb = RGBColor(125, 50, 255)
          # run.text = f'<bld>{run.text}</bld>'
        # イタリック italic
        elif run.italic:
          run.italic = False
          run.font.color.rgb = RGBColor(225, 50, 255)
          # run.text = f'<ita>{run.text}</ita>'
        # 下線 underline
        elif run.font.underline:
          run.font.underline = False
          run.font.color.rgb = RGBColor(50, 255, 190)
          # run.text = f'<udl>{run.text}</udl>'
        # 上付 superscript
        elif run.font.superscript:
          run.font.superscript = False
          run.font.color.rgb = RGBColor(95, 40, 10)
          # run.text = f'<sps>{run.text}</sps>'
        # 下付 subscript
        elif run.font.subscript:
          run.font.subscript = False
          run.font.color.rgb = RGBColor(10, 95, 85)
          # run.text = f'<sus>{run.text}</sus>'
        else:
          continue
          
    doc.save(f'+++modified_{basename}{ext}')

# ########## other methods
# print("段落の個数：", len(doc.paragraphs))

# ########## sample text
# 'ｺﾉｻｲﾀﾞｶﾗ ﾊﾝｶｸﾓｼﾞﾍﾝｼｭｦ ｾﾞﾝｶｸﾆ ﾍﾝｶﾝｼﾀｲﾃﾞｽﾖﾈ'
# 日本語の[文章]に欧文の(カッコ)が入っているのも変換したい。
# 本来はInDesignの [文字組設定] で解決できるのに、見た目上の (欧文スペース) が入っているやつも。
# それと、１２３４５６７８９０はアラビア数字、ＡＢＣＤ...ＸＹＺはASCIIで統一しておきたい。
# 文章行頭の一字下げや意図的な字下げは、InDesignで操作したいので、行頭のスペースやタブを削除しておきたい。

abcdefg!@#$%^&*()_+-=;':",./<>?"ａｂｃｄｅｆｇ！＠＃＄％＾＆＊（）＿＋−＝；’：”，．／＜＞？”