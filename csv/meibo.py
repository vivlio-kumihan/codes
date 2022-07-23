import os
import glob
import shutil
import jaconv
import re
import itertools
import pprint
import pandas as pd
import numpy as np
import sys
sys.path.append('../lib')
import ntzreg
import ntzstr

###################
# 下準備
org_files = glob.glob("./_org/*.csv")
for org_file in org_files:
    filename = os.path.basename(org_file)
    # create deta frame of pandas
    df = pd.read_csv(org_file, encoding='utf-8')

    # 不要なセルを削除する。
    df = df.dropna(how='all')

        ########## セル内の文字列を正規表現で整形
    # セル内が空欄の時に起こるエラー　int, floatが『elif cell is np.nan:』を
    # 『if isinstance(cell, 性質):』で素通しさせてとりあえず解決している。
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
    df_name = df['氏名'].str.split(pat = '\W', n = 1, expand = True)
    df_name.columns =  ['氏', '名']
    for col in df_name:
      df_name[col] = df_name[col].str.strip()
    
    #####################    
    # 氏名にルビを付ける。
    df_ruby = df['ふりがな'].str.split(pat = '\W', n = 1, expand = True)
    df_ruby.columns = ['うじ', 'な']
    for col in df_ruby:
      df_ruby[col] = df_ruby[col].str.strip()

    for col in df_ruby:
        df_ruby[col].fillna("〓〓", inplace = True)
    df_name_with_ruby = pd.concat([df_name, df_ruby], axis = 1)
    tmp_arr = []
    for col, row in df_name_with_ruby.iterrows():
        tmp_arr.append(f'[{row[0]}/{row[2]}] [{row[1]}/{row[3]}]')
    df['name_ruby'] = tmp_arr
    df['mesg'] = '▼①' + df['①'] + '▼②' + df['②'] + '▼③' + df['③'] + '▼④' + df['④']
    df['contents'] = '▼◆' + df['所属名称'] + '▼■' + df['name_ruby'] + df['mesg']

    ########## CSVに上書きして完成
    to_gen_file = os.path.join('./_gen', filename)
    df.to_csv(to_gen_file,
        encoding = "utf-8",
        index = False,
        columns = ['contents'],
        sep = '\t')