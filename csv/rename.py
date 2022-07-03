import os
import glob
import copy
import shutil
import jaconv
import re
import pprint
import pandas as pd
import numpy as np
import sys
sys.path.append('../lib')
import ntzreg
import ntzstr
import ntzarr
# from lib import ntzreg  #=> 同じ階層にlibディレクトリがある場合。

# # read CSV file
# file_paths = glob.glob("./_org/*.csv")

# for org_file in file_paths:
#     # 「ファイル名 + 拡張子」を取得する。
#     filename = os.path.basename(org_file)
#     # create deta frame of pandas
#     df_in = pd.read_csv(org_file, encoding = 'utf-8')
#     # コラムを整えた制作開始用の中間ファイルを生成させる。
#     # _tmpディレクトリに確保する。
#     to_tmp_file = os.path.join('./_tmp', filename)    
#     df_in.to_csv(to_tmp_file,
#         encoding = "utf-8",
#         index = False,
#         columns=['名前'],
#         sep = ',')
#     # 改めて、_tmpディレクトリに生成させたDFを使って作業の開始。
#     df = pd.read_csv(to_tmp_file, encoding='utf-8')
#     # 不要な行列を削除する。
#     df = df.dropna(how='all').dropna(how='all', axis = 1)

    # ########## セル内の文字列を正規表現で整形
    # # セル内が空欄の時に起こるエラー　int, floatが『elif cell is np.nan:』を
    # # 『if isinstance(cell, 性質):』で素通しさせてとりあえず解決している。
    # for label in df.columns:
    #     tmp_df = []
    #     for cell in df[label]:
    #         if isinstance(cell, float):
    #             tmp_df.append(cell)
    #         elif isinstance(cell, int):
    #             tmp_df.append(cell)
    #         elif cell is np.nan:
    #             tmp_df.append(cell)
    #         else:
    #             # 入ってきたcellに正規化を充てる。
    #             cell = ntzreg.cellstr(cell)
    #             tmp_df.append(cell)
    #     df[label] = tmp_df

    # # 正規表現で、ASCII（日本語も含む）、数字、アンダースコア以外の1文字を
    # # 区切り文字のパターンとして渡す。
    # # 複数回、ランダムに繰り返されていても区切り文字として認識する。
    # tmp_df = df['名前'].str.split(pat = '\W',  expand = True)
    # tmp_df.columns =  ['氏', '名']
    # tmp_df.fillna("〓〓", inplace = True)
    # df['名前'] = tmp_df['氏'] + "　" + tmp_df['名']
    # print(df['名前'])
    
    # tmp_name = []
    # for str in df['名前']:
    #     # 中黒を区切り文字とした場合と、
    #     # 区切り文字として認識する
    #     # 欧文スペース、全角スペース、タブの1つ以上の繰り返しを削除する。
    #     if '・' in str:
    #         arr = str.split('・')
    #     else:
    #         arr = str.split()
    #     # 「氏」「名」の間に全角スペースを入れて体裁を整える。
    #     uji = arr[0]
    #     mei = arr[1]
    #     tmp_name.append(f'{arr[0]}　{arr[1]}')
    # df['名前'] = tmp_name

    # # CSVとして書き出し
    # to_gen_file = os.path.join('./_gen', filename)
    # df.to_csv(to_gen_file,
    #     encoding = "utf-8",
    #     index = False,
    #     columns = ["名前"],
    #     sep = ',')

    # # photo_file_path = glob.glob("./_org/*.psd")
    # # tmp_photo = []
    # # for photo_file in photo_file_path:
    # #     basename, ext = os.path.splitext(os.path.basename(photo_file))
    # #     select_df = df[df['名前'] == basename]
    # #     basename = ntzstr.name5justify(basename)
    # #     os.rename(photo_file, f'img_{select_df.index[0]:03}_{basename}{ext}')

    # # #####################
    # # ### オリジナルと中間ファイルを削除する。
    # # # 検証をするときはこれらを外す。
    # # os.remove(org_file)
    # # os.remove(to_tmp_file)