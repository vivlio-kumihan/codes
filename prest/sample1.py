import os
import glob
import jaconv
import re
import pandas as pd
import numpy as np
import sys
sys.path.append('../lib')
import ntzreg
import ntzstr

###################
org_files = glob.glob("../csv/_org/*.csv")
for org_file in org_files:
    filename = os.path.basename(org_file)
    # CSVのデータをPandasで扱うための下準備。
    # pd（Pandas）に「read_csv()」という関数を充ててCSVをオブジェクト化する。
    # dfはPandasのライブラリーを使う際に慣用句的に充てる変数。DataFrameの略。
    df = pd.read_csv(org_file, encoding='utf-8')
                                                        # <=== CSVの読み込み。

    ########## 不要なセルを削除する。
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
                # cellにあるオブジェクトが文字列であれば、
                # 自作の関数を充てて正規化をする。セル内改行を取ったり、半角カナを全角に置き換えたりの処理。
                cell = ntzreg.cellstr(cell)
                                                        # <=== 定義したメソッドにセル内改行や日本語の正規化の処理をさせる。
                tmp_df.append(cell)
        df[label] = tmp_df


    # ######################################################################################
    # ######### sample1-1
    # # 不要な列の削除と順番変更
    # # 出力するCSVに、指定の順番でコラム名を一行を書くだけ。
    # ######### CSVに上書きして完成                              
    # to_gen_file = os.path.join('../csv/_gen', filename)
    # df.to_csv(to_gen_file,
    #     encoding = "utf-8",
    #     index = False,
    #     columns = ['演題', '演者', '対談', '学会名', '開催初日', '開催終了日', '会場', '開催地'],
    #     sep = '\t')
    #                                                     # <=== この一行で不要な列を取り去って並べ替え、
    #                                                     # <=== 『\t』区切りのCSVで書き出す。


    # #######################################################################################
    # ######### sample1-2
    # # コラムの合体と行の抜き出し。
    # # 列の合成
    # # 仕込み　年月日の整理                                     
    # for col, ser in df[['開催初日', '開催終了日']].iteritems():
    #     tmp_arr = []
    #     for cell in ser:
    #         if cell is np.nan:
    #             tmp_arr.append(cell)
    #         else:
    #             cell = re.sub('(\d\d?\/\d\d?)\/(\d\d?)', r'20\2/\1', cell) 
    #                                                     # <=== 日取りの書式を正規表現で整える。
    #             tmp_arr.append(cell)
    #     df[col] = tmp_arr
    # # # 『期日』ラベルを生成する。
    # df['期日'] = df['開催初日'] + '–' + df['開催終了日']
    #                                                     # <=== 2つの列を合成する。

    # # ######## アンカーを元に同じグループのものを縦につまんでいく。
    # # 摘むきっかけになる行のインデックスが入った配列。
    # # 英語を選択する。
    # # アンカーの生成。
    # tdf = df.copy()
    # en_idx = tdf['判定'][~tdf['判定'].isna()].index
    # #                                                     # <=== 『判定』の列にデータが入っていないセルの『否定』となり、
    # #                                                     #      『判定』の列にデータが入っているセルのインデックスを集める。
    # df_en = pd.DataFrame([], columns = df.columns)
    # #                                                     # <=== 空のデータフレームを生成する。
    # # # 該当するインデックスを元にデータを収集。           
    # for idx in en_idx:
    #     df_en = pd.concat([df_en, pd.DataFrame([tdf.loc[idx]])], axis = 0)
    # #                                                     # <=== 収集する。

    # ######## CSVに上書きして完成
    # to_gen_file = os.path.join('../csv/_gen', f'en_{filename}')
    # df_en.to_csv(to_gen_file,
    #     encoding = "utf-8",
    #     index = False,
    #     columns = ['演題', '演者', '対談', '学会名', '期日', '会場', '開催地'],
    #     sep = '\t')


    #######################################################################################
    ######### sample1-3
    # コラムの合体と行の抜き出し。
    # 列の合成
    # 仕込み　年月日の整理
    for col, ser in df[['開催初日', '開催終了日']].iteritems():
        tmp_arr = []
        for cell in ser:
            if cell is np.nan:
                tmp_arr.append(cell)
            else:
                cell = re.sub('(\d\d?\/\d\d?)\/(\d\d?)', r'20\2/\1', cell) 
                                                        # <=== 日取りの書式を正規表現で整える。
                tmp_arr.append(cell)
        df[col] = tmp_arr
    # # 『期日』ラベルを生成する。
    df['期日'] = df['開催初日'] + '–' + df['開催終了日']

    ######## アンカーを元に同じグループのものを縦につまんでいく。
    # 摘むきっかけになる行のインデックスが入った配列。
    # 英語を選択する。
    # アンカーの生成。
    tdf = df.copy()
    en_idx = tdf['判定'][~tdf['判定'].isna()].index
    #                                                     # <=== 『判定』の列にデータが入っていないセルの『否定』となり、
    #                                                     #      『判定』の列にデータが入っているセルのインデックスを集める。
    df_en = pd.DataFrame([], columns = df.columns)
    #                                                     # <=== 空のデータフレームを生成する。
    # # 該当するインデックスを元にデータを収集。           
    for idx in en_idx:
        df_en = pd.concat([df_en, pd.DataFrame([tdf.loc[idx]])], axis = 0)
    #                                                     # <=== 収集する。

    ######## CSVに上書きして完成
    to_gen_file = os.path.join('../csv/_gen', f'en_{filename}')
    df_en.to_csv(to_gen_file,
        encoding = "utf-8",
        index = False,
        columns = ['演題', '演者', '対談', '学会名', '期日', '会場', '開催地'],
        sep = '\t')

    ############################################################### 国内用の書き出し。
    # 摘むきっかけになる行のインデックスが入った配列。
    # 国内用のアンカーの生成。
                                                        # <=== 国際版の要領で国内版の表組を生成させる。
    tdf = df.copy()
    ja_idx = tdf['判定'][tdf['判定'].isna()].index
    df_ja = pd.DataFrame([], columns = df.columns)
    # 該当するインデックスを収集。
    for idx in ja_idx:
        df_ja = pd.concat([df_ja, pd.DataFrame([tdf.loc[idx]])], axis = 0)

    # 『演者』を7文字揃えする。
    df_ja['出演者'] = [ntzstr.name7justify(name) for name in df_ja['演者']]
                                                        # <=== 『演者』を7文字揃え、『出演者』ととして別名で保存する。
    # 『本人』を4文字揃えで置き換える。
    df_ja['対談用'] = [ntzstr.name4justify(name) for name in df_ja['演者']]
                                                        # <=== 『対談』の「本人」に置き換えるために
                                                        #       4文字揃えにし『対談用』で別名保存する。

    tmp_ser = []
    for idx, cell in df_ja['対談'].iteritems():
        if cell is np.nan:
            tmp_ser.append(cell)
        else:
            cell = re.sub('本人', df_ja['対談用'][idx], cell)  # <=== 正規表現で置き換えているところ。
            tmp_ser.append(cell)
    df_ja['対談'] = tmp_ser

    ######## CSVに上書きして完成
    to_gen_file = os.path.join('../csv/_gen', f'ja_{filename}')
    df_ja.to_csv(to_gen_file,
        encoding = "utf-8",
        index = False,
        columns = ['出演者', '対談', '学会名', '期日', '会場', '開催地'],
        sep = '\t')


    ######################################################################################
    # DataFrameにappendを充てるのは廃止予定。concat置き換えバージョン作成中。

    # # 単純にDataFrameをforで回すとカラム名が出てくる。
    # for col in tdf:
    #     print(col)

    # # iteritemsで回すと以下の通り。
    # for col, ser in tdf.iteritems():
    #     print(f'colounm is {col}')
    #     print(f'Series content is {ser}')
    #     for idx, cell in ser.iteritems():
    #         print(f'index is {idx}')
    #         print(f'cell content is {cell}')