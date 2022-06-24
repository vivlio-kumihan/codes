import os
import glob
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
# from lib import ntzreg  #=> 同じ階層にlibディレクトリがある場合。

###################
# 下準備
org_files = glob.glob("./_org/*.csv")
for org_file in org_files:
    filename = os.path.basename(org_file)
    # create deta frame of pandas
    df = pd.read_csv(org_file, encoding='utf-8')
    # # 制作用の中間ファイルを生成させる
    # tmp_file = os.path.join('./_tmp', filename)
    df.to_csv(org_file,
        encoding = "utf-8",
        index = False,
        columns = ['Zip','Adress','Company','Stuff'],
        sep = ',')

    ########## セル内の文字列を正規表現で整形
    for col, ser in df.iteritems():
        for idx, cell in ser.iteritems():
            if pd.isna(cell):
                continue
            else:
                cell = ntzreg.cellstr(cell)
                ser[idx] = cell
    
    for idx, cell in df['Zip'].iteritems():
        if pd.isna(cell):
            continue
        else:
            if cell == '郵便番号':
                df['Zip'].drop(index=idx)
                
    df = df.dropna(how='all')

            
            

        # print(cell)
        # print(cell[29])
        # print(type(cell[29]))

        # # print(type(row))
        # if isinstance(cell, str):
        #         print(cell)
        #         print("消す")


    # for i in df['〒']:
    #     print(i)


    # #####################
    # # 氏名
    # tmp_df = pd.DataFrame([df['姓'], df['名']])
    # for col, td in tmp_df.iterrows():
    #     td.fillna("〓〓", inplace = True)
    #     df[col] = td
    # df['氏名'] = df['姓'] + "　" + df['名']

    # #####################
    # # 演奏者名
    # # 7文字揃え
    # df["演奏者名"] = [ntzstr.name7justify(name) for name in df["氏名"]]

    # #####################
    # # 作／編曲者名
    # # 4文字揃え
    # df["本人用"] = [ntzstr.name4justify(name) for name in df["氏名"]]

    # #####################
    # # コラムの整理
    # # 例外的に区切り文字が「・」なので先に処理をする。
    # df['編曲者名2'] = df['編曲者名2'].str.replace(pat='・', repl='/')
    # # 3つのコラムを整理する。
    # for col, ser in pd.DataFrame([df['作曲者名'], df['編曲者名1'], df['編曲者名2']]).iterrows():
    #     ser.fillna("〓〓", inplace = True)
    #     for idx, cell in ser.iteritems():
    #         cell = re.sub('本人', df['本人用'][idx], cell)
    #         cell = re.sub('\.\s?', '. ', cell)
    #         cell = re.sub(',\s?', '/', cell)
    #         cell = re.sub('，\s?', '/', cell)
    #         cell = re.sub('、\s?', '/', cell)
    #         ser[idx] = cell.split('/')
    #     df[col] = ser

    # # df['編曲者名']、df['編曲者名(既成曲)']をまとめる。
    # # この2つのシリーズに仮の名前をつける。
    # tmp_df = df['編曲者名1'] + df['編曲者名2']
    # # 上のコードで便宜上つけたゲタ「〓〓」を外す。
    # for idx, arr in tmp_df.iteritems():
    #     tmp_df[idx] = [str for str in arr if str != '〓〓']
    # # セル内（配列）で重複した要素をつまむ。
    # for idx, arr in tmp_df.iteritems():
    #     tmp_df[idx] = list(sorted(set(arr), key = arr.index))
    # # 生成したシリーズを改めてdf['編曲者名']へ代入。
    # df['編曲者名'] = tmp_df

    # # df['作／編曲者名']の生成。df['作曲者名']、df['編曲者名']をまとめる。
    # for col, ser in pd.DataFrame([df['作曲者名'], df['編曲者名']]).iterrows():
    #     for idx, arr in ser.iteritems():
    #         td[idx] = '/'.join(s for s in arr)
    #     df[col] = td
    # df['作／編曲者名'] = df['作曲者名'] + '▼' +  df['編曲者名']
    
    # #####################
    # # 学年
    # for grade in df['学年']:
    #     grade = re.sub('[小中学高校]+', '', grade)
    #     df['grade'] = grade
    # df['学年'] = '（' + df['grade'] + '）'

    # #####################
    # # 順番
    # df_num = pd.Series(list(range(1, len(df) + 1)))
    # for idx, n in df_num.iteritems():
    #     df_num[idx] = f'{n}.'
    # df['順番'] = df_num

    ###################
    # CSVに上書きして完成
    to_gen_file = os.path.join('./_gen', filename)
    df.to_csv(to_gen_file,
        encoding = "utf-16",
        index = False,
        columns = ['Zip','Adress','Company','Stuff'],
        sep = ',')

    # #####################
    # ### オリジナルと中間ファイルを削除する。
    # ### 検証をするときはこれらを外す。
    # os.remove(org_file)
    # os.remove(tmp_file)

# # 付けたゲタ「〓」を外す方法
# # 本編のやり方
# tmp_df[idx] = [str for str in arr if str != '〓〓']
# # 別の方法
# for idx, str in enumerate(arr):
#     if '〓〓' in str:
#         arr.pop(idx)
