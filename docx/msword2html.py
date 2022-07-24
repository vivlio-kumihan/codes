import os
import glob
from telnetlib import WONT
import mammoth
from bs4 import BeautifulSoup

org_files = glob.glob("./_org/*.docx")
for file in org_files:
  # 'Search Through Pass'からSTPと拡張子を除いたファイル名を抜き出す。
  basename, ext = os.path.splitext( os.path.basename(file) )
  # MSWordで付けられたスタイルをHTML上で変換すさ際の名称を定義する。
  custom_styles = """ b => b
                      i => i
                      u => u
                      p[style-name='見出し'] => h1
                      p[style-name='見出し2'] => h2
                      p[style-name='見出し3'] => h3 """
  # MSWordを処理する。
  with open(file, "rb") as docx_file:
      # MSWord to HTML
      result = mammoth.convert_to_html(docx_file, style_map = custom_styles)
      source = result.value
      print(source)
      # タグの見栄えを調整する。ソースを使ってスープを作るそうだ。
      html = BeautifulSoup(source, 'lxml')
      html = html.prettify()
      # _gen（「general」生成）Directoryへの道標。
      to_gen_file = os.path.join('./_gen', f'modfied_{basename}.html')

      with open(to_gen_file, mode = 'w') as html_file:
          html_file.write(html)