import os
import glob
import copy
import shutil
import jaconv
import re
import shutil
import pprint
import pandas as pd
import numpy as np
import sys
sys.path.append('../lib')
import ntzreg
import ntzstr
import ntzarr
# from lib import ntzreg  #=> 同じ階層にlibディレクトリがある場合。

###################
# 下準備
org_files = glob.glob("./_org/*.csv")
for org_file in org_files:
    # 「ファイル名 + 拡張子」を取得する。
    filename = os.path.basename(org_file)
    # create deta frame of pandas
    df = pd.read_csv(org_file, encoding='utf-8')
    # 制作用の中間ファイルを生成させる。
    tmp_file = os.path.join('./_tmp', filename)
    df.to_csv(tmp_file,
        encoding = "utf-8",
        index = False,
        columns=['名前', 'フリガナ', '役職', '担当', '部活動', 'エピソード'],
        sep = ',')

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

    #####################
    # '氏名'
    # 正規表現で、ASCII（日本語も含む）、数字、アンダースコア意外の1文字を
    # 区切り文字のパターンとして渡す。
    # 複数回、ランダムに繰り返されていても区切り文字として認識する。
    # オプション「n」で、最初の区切り文字だけを認識させる。
    # オプション「expand」は対応する文字がない場合はNaNを入れる。
    df_name = df['名前'].str.split(pat = '\W', n = 1, expand = True)
    df_name.columns =  ['氏', '名']
    df_name['氏'] = df_name['氏'].str.strip()
    df_name['名'] = df_name['名'].str.strip()
    # ファイル名など変換用。このコード内で使用するためのもの。
    df['氏名'] = df_name['氏'] + "　" + df_name['名']
    
    #####################    
    # 氏名にルビを付ける。
    df_ruby = df['フリガナ'].str.split(pat = '\W', n = 1, expand = True)
    df_ruby.columns = ['ウジ', 'ナ']
    df_ruby['ウジ'] = df_ruby['ウジ'].str.strip()
    df_ruby['ナ'] = df_ruby['ナ'].str.strip()
    df_name_with_ruby = pd.concat([df_name, df_ruby], axis = 1)
    tmp_arr = []
    for col, row in df_name_with_ruby.iterrows():
        tmp_arr.append(f'[{row[0]}/{row[2]}] [{row[1]}/{row[3]}]')
    df['氏名ルビ付'] = tmp_arr

    #####################
    # 写真ファイル用
    # 5文字揃え
    df_name_5justy = [ntzstr.name5justify(name) for name in df["氏名"]]
    # 写真の読み込みとSeries化
    ser_photo = pd.Series(glob.glob('./_org/*.psd'), name = '@写真名')
    for idx, photo_file in ser_photo.iteritems():
        basename, ext = os.path.splitext(os.path.basename(photo_file))
        ser_photo[idx] = basename

    # 抜き取る写真ファイルのインデックスを検索する。
    # 対応するdf_nameをforで回す。
    for idx in range(len(df_name)):
        # 不思議な書き方。df、df_name、ser_photoと個数が合致するDataFrameだったら何でもかまわない。
        catch_idx = ser_photo[ser_photo.str.contains(df_name['氏'][idx]) & ser_photo.str.contains(df_name['名'][idx])].index
        order = idx + 1
        name = f'img_{order:03}_{df_name_5justy[idx]}'
        if not catch_idx.size == 0:
            if catch_idx[0] >= 0:
                ser_photo_name = ser_photo[catch_idx[0]]
                os.rename(f'./_org/{ser_photo_name}.psd', f'./_gen/{name}.psd')
        else:
            shutil.copy2(f'./_org/〓〓〓〓.psd', f'./_gen/{name}.psd')


    # # CSVとして書き出し
    # to_gen_file = os.path.join('./_gen', filename)
    # df.to_csv(to_gen_file,
    #     encoding = "utf-16",
    #     index = False,
    #     columns = ['氏名ルビ付', '役職', '教科・科目', '部活動', 'エピソード', '@写真名'],
    #     sep = ',')


    # # #####################
    # # ### オリジナルと中間ファイルを削除する。
    # # # 検証をするときはこれらを外す。
    # # os.remove(org_file)
    # # os.remove(to_tmp_file)

# # nanだけの不要な行列を削除する。
# # df = df.dropna(how='all').dropna(how='all', axis = 1)

# # 0で桁数を埋める。
# for idx, tmp_name in df['名前'].iteritems():
#     print(f'{idx + 1:03}')

# for idx, val in df['名前'].iteritems():
    # print(f'{idx:03}')
    # print(val)

#################### debug
# print(catch_idx)
# for name in ser_photo:
#     print(name)
#################### debug
# if catch_idx[0]: