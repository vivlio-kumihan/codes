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
# from lib import ntzreg  #=> 同じ階層にlibディレクトリがある場合。

###################
# 下準備
org_files = glob.glob("./_org/*.csv")
for org_file in org_files:
    filename = os.path.basename(org_file)
    # create deta frame of pandas
    df = pd.read_csv(org_file, encoding='utf-8')

    # 制作用の中間ファイルを生成させる
    tmp_file = os.path.join('./_tmp', filename)
    df.to_csv(tmp_file,
        encoding = "utf-8",
        index = False,
        columns = ['Zip','Adress','Company','Stuff'],
        sep = ',')

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
    
    ########## 不要な行を削除する。
    for idx, cell in df['Zip'].iteritems():
        if pd.isna(cell):
            continue
        else:
            if cell == '郵便番号':
                df.drop(index = idx, inplace = True)
    
    df = df.dropna(how='all')

    ########## df['Zip']以外の空欄に「〓」を埋める。
    # コラムの抜き出し方がこのやり方ではダメ。何故だ。
    # for col, ser in df.loc[:, ['Adress','Company','Stuff']].iteritems():
    #     ser.fillna("〓", inplace = True)
    for col, ser in df.iteritems():
        if col == "Zip":
            continue
        else:
            ser.fillna("〓", inplace = True)
    
    df = df.append({'Zip': '〓', 'Adress': '〓', 'Company': '〓', 'Stuff': '〓'}, ignore_index=True)
    
    ########## アンカーを元に同じグループのものを縦につまんでいく。
    # 摘むきっかけになる行のインデックスが入った配列。
    pick_idx = df['Zip'][~df['Zip'].isna()].index
    puse_idx = df['Zip'][~df['Zip'].isna()].index[1:]

    # インデックス番号が変わるので、新しい受け皿を生成させておく。
    df2 = pd.DataFrame({
        '郵便' : [],
        '住所' : [],
        '会社' : [],
        '担当' : [],
    })

    # データを整理する。とりあえず作成。リファクタリングは後でやる。
    tmp_arr = []
    for idx, pick in enumerate(pick_idx[:-1]):
        tmp_arr.append(df['Zip'].iloc[pick])
    df2['郵便'] = pd.Series(tmp_arr)

    tmp_arr = []
    for pick, puse in zip(pick_idx, puse_idx):
        ad = [row for row in df['Adress'].iloc[pick:puse]]
        tmp_arr.append('　'.join(ad))
    df2['住所'] = pd.Series(tmp_arr)
    df2['住所'] = df2['住所'].str.replace(pat='\s?〓\s?', repl='')
    df2['住所'] = df2['住所'].str.strip()

    tmp_arr = []
    for pick, puse in zip(pick_idx, puse_idx):
        co = [row for row in df['Company'].iloc[pick:puse]]
        tmp_arr.append('　'.join(co))
    df2['会社'] = pd.Series(tmp_arr)
    df2['会社'] = df2['会社'].str.replace(pat='\s?〓\s?', repl='')
    df2['会社'] = df2['会社'].str.strip()

    tmp_arr = []
    for pick, puse in zip(pick_idx, puse_idx):
        sf = [row for row in df['Stuff'].iloc[pick:puse]]
        # 「・」を持つ文字列を整理する。
        df['Stuff'] = df['Stuff'].str.replace(pat='\s?・\s?', repl='▼')
        tmp_arr.append('　'.join(sf))
    df2['担当'] = pd.Series(tmp_arr)
    df2['担当'] = df2['担当'].str.replace(pat='\s?〓\s?', repl='')
    df2['担当'] = df2['担当'].str.strip()

    for idx, name in df2['担当'].iteritems():
        name = name.split()
        if len(name) == 2:
            name.insert(0, '〓')
            name.insert(1, '〓')
            name.insert(2, '〓')
            df2['担当'].iloc[idx] = name
        elif len(name) == 3:
            name.insert(4, '〓')
            name.insert(5, '〓')
            df2['担当'].iloc[idx] = name
        else:
            df2['担当'].iloc[idx] = ['〓', '〓', '〓', '〓', '〓']

    tmp_arr = []
    for val in df2['担当']:
        tmp_arr.append(val)
    df3 = pd.DataFrame(tmp_arr)
    df3 = df3.drop(columns = df3.columns[5:])
    df3.columns = ['役職', '氏（役職）', '名（役職）', '氏', '名']
    df3['氏名（役職）'] = df3['氏（役職）'] + "　" + df3['名（役職）']
    df3['氏名（役職）'] = [ntzstr.name4justify(name) for name in df3['氏名（役職）']]
    df3['氏名'] = df3['氏'] + "　" + df3['名']
    df3['氏名'] = [ntzstr.name4justify(name) for name in df3['氏名']]
    # ゲタを外す。
    for col, ser in df3[['役職', '氏名（役職）', '氏名']].iteritems():
        df3[col] = df3[col].str.replace(pat='\s?〓\s?', repl='')
    
    df2 = pd.concat([df2, df3['役職'], df3['氏名（役職）'], df3['氏名']], axis = 1)

    ########## CSVに上書きして完成
    to_gen_file = os.path.join('./_gen', filename)
    df2.to_csv(to_gen_file,
        encoding = "utf-16",
        index = False,
        columns = ['郵便', '住所','会社', '役職', '氏名（役職）', '氏名'],
        sep = ',')

    # #####################
    # ### オリジナルと中間ファイルを削除する。
    # ### 検証をするときはこれらを外す。
    # os.remove(org_file)
    # os.remove(tmp_file)