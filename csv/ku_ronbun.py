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

    # 制作用の中間ファイルを生成させる
    tmp_file = os.path.join('./_tmp', filename)
    df.to_csv(tmp_file,
        encoding = "utf-8",
        index = False,
        columns = ['判定', '発行年', '著者', '論文タイトル', '雑誌名＆巻-号-ページ'],
        sep = ',')

    df = df.dropna(how='all')

    ########## df['Zip']以外の空欄に「〓」を埋める。
    # コラムの抜き出し方がこのやり方ではダメ。何故だ。
    # for col, ser in df.loc[:, ['Adress','Company','Stuff']].iteritems():
    #     ser.fillna("〓", inplace = True)
    for col, ser in df.iteritems():
        if col == '判定':
            continue
        else:
            ser.fillna("〓", inplace = True)

    for col, ser in df[['著者', '論文タイトル', '雑誌名＆巻-号-ページ']].iteritems():
        df[col] = df[col].str.replace(pat = '\n', repl = '▽')

    df_jp = df[['発行年', '著者', '論文タイトル', '雑誌名＆巻-号-ページ']].copy()
    
    ########## アンカーを元に同じグループのものを縦につまんでいく。
    # 摘むきっかけになる行のインデックスが入った配列。
    # 英語を選択する
    en_idx = df['判定'][df['判定'].isna()].index
    tmp_df1 = pd.DataFrame([])
    for idx in en_idx:
        tmp_df1 = tmp_df1.append(df.iloc[idx])
    tmp_df1['著者'] = '■' + tmp_df1['著者'] + '■'
    tmp_df1['論文タイトルと雑誌名'] = tmp_df1['論文タイトル'] + '▼' + tmp_df1['雑誌名＆巻-号-ページ']

    tmp_arr = []
    for idx, cell in tmp_df1['著者'].iteritems():
        cell = re.sub('　', ' ', cell) # 英文に全角スペースで間隔を調整しているのを直す。
        cell = re.sub('\s?,\s?', ', ', cell) # カンマの統一
        cell = re.sub(':\s?', ': ', cell) # コロンの統一
        cell = re.sub(';\s?', '; ', cell) # セミコロンの統一
        cell = re.sub('\s?[)\(（](.+?)[\)）]\s?', r' (\1) ', cell) # 英文に全角カッコを入れているのを適宜修正。
        cell = re.sub('\s\s?', ' ', cell) # あえてスペースのダブりを1つに変更する。
        cell = re.sub('〓', '', cell) # 最後に〓をトル。
        tmp_arr.append(cell)
    tmp_df1['著者'] = tmp_arr

    tmp_arr = []
    for idx, cell in tmp_df1['論文タイトルと雑誌名'].iteritems():
        cell = re.sub('　', ' ', cell) # 英文に全角スペースで間隔を調整しているのを直す。
        cell = re.sub('\s?,\s?', ', ', cell) # カンマの統一
        cell = re.sub(':\s?', ': ', cell) # コロンの統一
        cell = re.sub(';\s?', '; ', cell) # セミコロンの統一
        cell = re.sub('\s?[)\(（](.+?)[\)）]\s?', r'(\1)', cell) # 英文に全角カッコを入れているのを適宜修正。
        cell = re.sub('\s\s?', ' ', cell) # あえてスペースのダブりを1つに変更する。
        cell = re.sub('〓', '', cell) # 最後に〓をトル。
        tmp_arr.append(cell)
    tmp_df1['論文タイトルと雑誌名'] = tmp_arr

    ########## CSVに上書きして完成
    to_gen_file = os.path.join('./_gen', f'en_{filename}')
    tmp_df1.to_csv(to_gen_file,
        encoding = "utf-8",
        index = False,
        columns = ['著者', '論文タイトルと雑誌名'],
        sep = '\t')

    ########## アンカーを元に同じグループのものを縦につまんでいく。
    # 日本語を選択する
    ja_idx = df['判定'][~df['判定'].isna()].index
    tmp_df2 = pd.DataFrame([])
    for idx in ja_idx:
        tmp_df2 = tmp_df2.append(df.iloc[idx])
    tmp_df2['著者'] = '■' + tmp_df2['著者'] + '■'
    tmp_df2['論文タイトルと雑誌名'] = tmp_df2['論文タイトル'] + '▼' + tmp_df2['雑誌名＆巻-号-ページ']

    tmp_arr = []
    for idx, cell in tmp_df2['著者'].iteritems():
        cell = re.sub('(\s?,\s?|，)', '、', cell) # カンマの統一
        cell = re.sub('\s?[)\(（](.+?)[\)）]\s?', r'（\1）', cell) # バラバラの全角カッコを適宜修正。
        cell = re.sub('〓', '', cell) # 最後に〓をトル。
        tmp_arr.append(cell)
    tmp_df2['著者'] = tmp_arr

    tmp_arr = []
    for idx, cell in tmp_df2['論文タイトルと雑誌名'].iteritems():
        cell = re.sub('\s?,\s?', '，', cell) # カンマの統一
        cell = re.sub('\s?:\s?', '：', cell) # コロンの統一
        cell = re.sub('\s?;\s?', '；', cell) # セミコロンの統一
        cell = re.sub('\s?[)\(（](.+?)[\)）]\s?', r'（\1）', cell) # バラバラの全角カッコを適宜修正。
        cell = re.sub('〓', '', cell) # 最後に〓をトル。
        tmp_arr.append(cell)
    tmp_df2['論文タイトルと雑誌名'] = tmp_arr

    ########## CSVに上書きして完成
    to_gen_file = os.path.join('./_gen', f'ja_{filename}')
    tmp_df2.to_csv(to_gen_file,
        encoding = "utf-8",
        index = False,
        columns = ['発行年', '著者', '論文タイトルと雑誌名'],
        sep = '\t')
    
    



    # df = df.drop(labels = pick_idx, axis = 0)
    # for col, i in df.iteritems():
    #     for i in df[col]:
    #         print(i)

    # tmp_df = df.drop(labels = 3, axis =0)
    # print(tmp_df)
    # for i in pick_idx:
    # print(i)
    # print(type(i))
    # print(df[i])
    # df.pop()
    # print(pick_idx)
    # print(puse_idx)
    # # インデックス番号が変わるので、新しい受け皿を生成させておく。
    # df2 = pd.DataFrame({
    #     '発行年': [],
    #     '著者': [],
    #     '論文タイトル': [],
    #     '雑誌名＆巻-号-ページ': []
    # })

    # # データを整理する。とりあえず作成。リファクタリングは後でやる。
    # tmp_arr = []
    # for idx, pick in enumerate(pick_idx[:-1]):
    #     tmp_arr.append(df['Zip'].iloc[pick])
    # df2['郵便'] = pd.Series(tmp_arr)

    # tmp_arr = []
    # for pick, puse in zip(pick_idx, puse_idx):
    #     ad = [row for row in df['Adress'].iloc[pick:puse]]
    #     tmp_arr.append('　'.join(ad))
    # df2['住所'] = pd.Series(tmp_arr)
    # df2['住所'] = df2['住所'].str.replace(pat='\s?〓\s?', repl='')
    # df2['住所'] = df2['住所'].str.strip()

    # tmp_arr = []
    # for pick, puse in zip(pick_idx, puse_idx):
    #     co = [row for row in df['Company'].iloc[pick:puse]]
    #     tmp_arr.append('　'.join(co))
    # df2['会社'] = pd.Series(tmp_arr)
    # df2['会社'] = df2['会社'].str.replace(pat='\s?〓\s?', repl='')
    # df2['会社'] = df2['会社'].str.strip()

    # tmp_arr = []
    # for pick, puse in zip(pick_idx, puse_idx):
    #     sf = [row for row in df['Stuff'].iloc[pick:puse]]
    #     # 「・」を持つ文字列を整理する。
    #     df['Stuff'] = df['Stuff'].str.replace(pat='\s?・\s?', repl='▼')
    #     tmp_arr.append('　'.join(sf))
    # df2['担当'] = pd.Series(tmp_arr)
    # df2['担当'] = df2['担当'].str.replace(pat='\s?〓\s?', repl='')
    # df2['担当'] = df2['担当'].str.strip()

    # for idx, name in df2['担当'].iteritems():
    #     name = name.split()
    #     if len(name) == 2:
    #         name.insert(0, '〓')
    #         df2['担当'].iloc[idx] = name
    #     elif len(name) == 3:
    #         df2['担当'].iloc[idx] = name
    #     else:
    #         df2['担当'].iloc[idx] = ['〓', '〓', '〓']

    # tmp_arr = []
    # for val in df2['担当']:
    #     tmp_arr.append(val)
    # df3 = pd.DataFrame(tmp_arr)
    # df3 = df3.drop(columns = df3.columns[3:])
    # df3.columns = ['役職', '氏', '名']
    # # df3['氏名（役職）'] = df3['氏（役職）'] + "　" + df3['名（役職）']
    # # df3['氏名（役職）'] = [ntzstr.name4justify(name) for name in df3['氏名（役職）']]
    # # df3['氏名'] = df3['氏'] + "　" + df3['名']
    # # df3['氏名'] = [ntzstr.name4justify(name) for name in df3['氏名']]
    # # ゲタを外す。
    # for col, ser in df3[['役職', '氏', '名']].iteritems():
    #     df3[col] = df3[col].str.replace(pat='\s?〓\s?', repl='')
    
    # df2 = pd.concat([df2, df3['役職'], df3['氏'], df3['名']], axis = 1)

    # ########## CSVに上書きして完成
    # to_gen_file = os.path.join('./_gen', filename)
    # df2.to_csv(to_gen_file,
    #     encoding = "utf-16",
    #     index = False,
    #     columns = ['郵便', '住所','会社', '役職', '氏', '名'],
    #     sep = ',')

    # #####################
    # ### オリジナルと中間ファイルを削除する。
    # ### 検証をするときはこれらを外す。
    # os.remove(org_file)
    # os.remove(tmp_file)