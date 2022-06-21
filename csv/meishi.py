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


# read CSV file
file_paths = glob.glob("./_org/*.csv")

for org_file in file_paths:
    #####################
    # 「ファイル名 + 拡張子」を取得する。
    filename = os.path.basename(org_file)

    # create deta frame of pandas
    df_in = pd.read_csv(org_file, encoding = 'utf-8')

    # 制作用の中間ファイルを生成させた上で、改めてDFを生成して作業の開始。
    to_tmp_file = os.path.join('./_tmp', filename)    
    df_in.to_csv(to_tmp_file,
        encoding = "utf-8",
        index = False,
        columns=["順番", "氏名", "ふりがな", "役職１", "役職２", "〒", "事務所所在地", "電話", "FAX", "メール"],
        sep = ',')

    df = pd.read_csv(to_tmp_file, encoding='utf-8')

    df = df.dropna(how='all').dropna(how='all', axis = 1)

    ########## セル内の文字列を正規表現で整形
    # セル内が空欄の時に起こるエラー　int, floatが『elif cell is np.nan:』の
    # 条件分岐で上手く作用してくれないので、『if isinstance(cell, 性質):』で解決している。
    for label in df.columns:
        tmp_df = []
        for cell in df[label]:
            if isinstance(cell, float):
                tmp_df.append(cell)
            elif isinstance(cell, int):
                tmp_df.append(cell)
            elif cell is np.nan:
                tmp_df.append(cell)
            else:
                # 入ってきたcellに正規化を充てる。
                cell = ntzreg.cellstr(cell)
                tmp_df.append(cell)
        df[label] = tmp_df

    # 氏名を5文字で揃える。写真ファイルに付ける氏名用。
    tmp_name = []
    for str in df['氏名']:
        arr = str.split()
        uji = arr[0]
        mei = arr[1]
        uji_size = len(arr[0])
        mei_size = len(arr[1])
        if uji_size == 2 and mei_size == 2:
            tmp_name.append(f'{arr[0]}　{arr[1]}')
        elif uji_size == 1 and mei_size == 2 or uji_size == 2 and mei_size == 1:
            tmp_name.append(f'{arr[0]}　　{arr[1]}')
        elif uji_size == 1 and mei_size == 3 or uji_size == 3 and mei_size == 1:
            tmp_name.append(f'{arr[0]}　{arr[1]}')
        elif uji_size == 2 and mei_size == 3 or uji_size == 3 and mei_size == 2:
            tmp_name.append(f'{arr[0]}{arr[1]}')
        else:
            tmp_name.append('')
    df['氏名写真用'] = tmp_name

    # 氏名にルビを付ける。
    tmp_df = (df['氏名'] + ' ' + df['ふりがな'])
    tmp_name_ruby = []
    for str in tmp_df:
        arr = str.split()
        tmp_name_ruby.append(f'[{arr[0]}/{arr[2]}] [{arr[1]}/{arr[3]}]')
    df['氏名ルビ付'] = tmp_name_ruby

    # 役職
    df['役職'] = df['役職１'] + "・"+ df['役職２']

    # read psd file
    photo_file_path = sorted(glob.glob("./*.psd"))
    tmp_photo = []
    for photo_file in photo_file_path:
        basename, ext = os.path.splitext(os.path.basename(photo_file))
        tmp_photo.append(basename)
    df['元ファイル名'] = sorted(tmp_photo)

    df['@写真名'] = 'img' + df['元ファイル名'] + '_' + df['氏名写真用'] + '.psd'

    # 設定した写真名をファイルに一括でファイル名を上書きする。
    i = 0
    for file_name in photo_file_path:
        os.rename(file_name, df['@写真名'][i])
        i += 1

    # CSVとして書き出し
    to_gen_file = os.path.join('./_gen', filename)
    df.to_csv(to_gen_file,
        encoding = "utf-16",
        index = False,
        # columns = ["氏名ルビ付", "役職", "〒", "事務所所在地", "電話", "FAX", "メール"],
        columns = ["氏名ルビ付", "役職", "〒", "事務所所在地", "電話", "FAX", "メール", '@写真名'],
        sep = ',')


    # # #####################
    # # ### オリジナルと中間ファイルを削除する。
    # # # 検証をするときはこれらを外す。
    # # os.remove(org_file)
    # # os.remove(to_tmp_file)