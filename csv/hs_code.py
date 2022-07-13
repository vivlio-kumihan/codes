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
        columns = ['高校コード', '校名よみ', '設置者', '種別', '校名'],
        sep = ',')
    # 不要なセルを削除する。
    df = df.dropna(how='all')

    tmp_df = []
    for yomi in df['校名よみ']:
        yomi = jaconv.h2z(yomi[0], kana=True, ascii=False, digit=False)
        yomi = jaconv.kata2hira(yomi)
        tmp_df.append(yomi)
    df['校名よみ'] = tmp_df

    df['設置者'] = df['設置者'].str.replace(pat='国立', repl='国　　立')
    df['設置者'] = df['設置者'].str.replace(pat='公立', repl='公　　立')
    df['設置者'] = df['設置者'].str.replace(pat='私立', repl='私　　立')

    df['種別'] = '（' + df['種別'] + '）'

    idx_arr_l = []
    for idx, i in df['設置者'].iteritems():
        if i == '9':
            idx_arr_l.append(idx + 1)
        else:
            continue
    to_insert = 0
    idx_arr_f = [to_insert] + idx_arr_l
    idx_arr_f = idx_arr_f[:-1]

    for first, last in zip(idx_arr_f, idx_arr_l):
        dfn = df.iloc[first:last]
        print(dfn)
        # for idx, i in dfn['設置者'].duplicated(keep = 'first').iteritems():
        #     if i == False:
        #         print(idx, dfn['設置者'][idx], dfn['種別'][idx], dfn['校名'][idx])
    # print(df1)
    # for idx, i in df['設置者'].duplicated(keep = 'False').iteritems():
    #     print(idx, i)
    # print(df['設置者'].duplicated(keep = 'first'))

    # ########## アンカーを元に同じグループのものを縦につまんでいく。
    # # 日本語を選択する
    # ja_idx = df2['判定'][~df2['判定'].isna()].index
    # tdf_ja = pd.DataFrame([])
    # for idx in ja_idx:
    #     tdf_ja = tdf_ja.append(df2.iloc[idx])


    ######### CSVに上書きして完成
    to_gen_file = os.path.join('./_gen', f'modified_{filename}')
    df.to_csv(to_gen_file,
        encoding = "utf-8",
        index = False,
        columns = ['校名よみ', '設置者', '種別', '校名', '高校コード'],
        sep = '\t')
    

    # #####################
    # ### オリジナルと中間ファイルを削除する。
    # ### 検証をするときはこれらを外す。
    # os.remove(org_file)
    os.remove(tmp_file)


    # # 仕込み
    # # セルの調整　空のセルには〓を埋める。
    # # セル内改行を改行マークで置き換える。
    # for col, ser in df.iteritems():
    #     if col == '判定' or col == '発表年':
    #         continue
    #     else:
    #         ser.fillna("〓", inplace = True)
    #         tmp_arr = []
    #         for cell in ser:
    #             cell = re.sub('\n', '▼', cell)
    #             tmp_arr.append(cell)
    #         df[col] = tmp_arr
    # # 列の合成
    # # 期日を生成する。
    # for col, ser in df[['開催初日', '開催終了日']].iteritems():
    #     tmp_arr = []
    #     for cell in ser:
    #         cell = re.sub('(\d\d?\/\d\d?)\/(\d\d?)', r'20\2/\1', cell) 
    #         tmp_arr.append(cell)
    #     df[col] = tmp_arr
    # df['期日'] = df['開催初日'] + '-' + df['開催終了日']
    # # 出演者を生成する。
    # df['出演者'] = df['演者'] + '▽' + df['演者2']
    # # データフレームを別名で保存する。
    # df2 = pd.DataFrame(df[['判定', '発表年', '出演者', '演題', '学会名', '会場', '開催地', '期日']])
    # # もう列の合成をする必要はないので、空欄に埋めていた〓などを削除する。
    # for col, ser in df2.iteritems():
    #     if col == '判定' or col == '発表年':
    #         continue
    #     else:
    #         tmp_arr = []
    #         for cell in ser:
    #             cell = re.sub('▽〓', '', cell)
    #             cell = re.sub('〓', '', cell)
    #             tmp_arr.append(cell)
    #     df2[col] = tmp_arr
    
    # ######### アンカーを元に同じグループのものを縦につまんでいく。
    # # 摘むきっかけになる行のインデックスが入った配列。
    # # 英語を選択する。
    # # アンカーの生成。
    # en_idx = df2['判定'][df2['判定'].isna()].index
    # # 該当するインデックスを元にデータを収集。
    # tdf_en = pd.DataFrame([])
    # for idx in en_idx:
    #     tdf_en = tdf_en.append(df2.iloc[idx])

    # ########## CSVに上書きして完成
    # to_gen_file = os.path.join('./_gen', f'en_{filename}')
    # tdf_en.to_csv(to_gen_file,
    #     encoding = "utf-8",
    #     index = False,
    #     columns = ['発表年', '出演者', '演題', '学会名', '会場', '開催地', '期日'],
    #     sep = '\t')

    # for col, ser in tdf_ja.iteritems():
    #     if col == '判定' or col == '発表年':
    #         continue
    #     else:
    #         tmp_arr = []
    #         for cell in ser:
    #             if isinstance(cell, float):
    #                 tmp_arr.append(cell)
    #             elif isinstance(cell, int):
    #                 tmp_arr.append(cell)
    #             elif cell is np.nan:
    #                 tmp_arr.append(cell)
    #             else:
    #                 cell = re.sub('(\s?,\s?|，)', '、', cell) # カンマの統一
    #                 cell = re.sub(' ', '　', cell) # カンマの統一
    #                 cell = re.sub('、　', '、', cell) # カンマの統一

    #                 cell = re.sub('\s?[)\(（](.+?)[\)）]\s?', r'（\1）', cell) # バラバラの全角カッコを適宜修正。
    #                 tmp_arr.append(cell)
    #         tdf_ja[col] = tmp_arr

    # for idx, group in tdf_ja['出演者'].iteritems():
    #     groups = group.split('、')
    #     tmp_groups = []
    #     for name in groups:
    #         # 氏名揃え　4文字揃え
    #         # 前後の空白を取り去ってから
    #         name = name.strip()
    #         # 文字列にスペースが入っていない場合の処理をする。
    #         if re.search(r"\s", name):
    #             # 氏名を配列として格納
    #             shimei = name.split()
    #             uji_size = len(shimei[0])
    #             mei_size = len(shimei[1])
    #             # 〓　〓 or 〓　〓〓 or 〓〓　〓 or 〓　〓〓〓 or 〓〓〓　〓
    #             if uji_size == 1 and mei_size == 1 or uji_size == 1 and mei_size == 2 or uji_size == 2 and mei_size == 1 or uji_size == 1 and mei_size == 3 or uji_size == 3 and mei_size == 1:
    #                 justifed_shimei = f'{shimei[0]}　{shimei[1]}'
    #             else:
    #                 justifed_shimei = f'{shimei[0]}{shimei[1]}'
    #         else:
    #             justifed_shimei = name
    #         tmp_groups.append(justifed_shimei)
    #     tdf_ja['出演者'][idx] = '、'.join(tmp_groups)

    # tdf_ja['出演者'] = '■' + tdf_ja['出演者'] + '▼'
    # tdf_ja['演題'] = tdf_ja['演題'] + '▼'
