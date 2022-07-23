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

# # #### DataFrameの連結
# df1 = pd.DataFrame({
#   'a': ['a0', 'a1', 'a2'],
#   'b': ['b0', 'b1', 'b2'],
#   'c': ['c0', 'c1', 'c2']
# })

# df2 = pd.DataFrame({
#   'a': ['a3', 'a4', 'a5'],
#   'b': ['b3', 'b4', 'b5'],
#   'c': ['c3', 'c4', 'c5']
# })

# df3 = pd.DataFrame({
#   'a': ['a6', 'a7', 'a8'],
#   'b': ['b6', 'b7', 'b8'],
#   'c': ['c6', 'c7', 'c8']
# })

# # concat 行方向へ繋げる「axis = 0」がキモ
# df4 = pd.concat([df1, df2, df3], axis = 0)

# # print(df1)
# # print(df2)
# # print(df4)

# # #### Seriesの連結
# ser1 = pd.Series(['s1', 's2'])
# ser2 = pd.Series(['s3', 's4'])

# # 行方向に連結
# ser3 = pd.concat([ser1, ser2], axis = 0)
# # print(ser3)

# # 列方向に連結
# ser4 = pd.concat([ser1, ser2], axis = 1)

# # nameメソッドでコラム名を追記できる。
# # ただし、順番が大切。変更させた上でpdしないと反映しないよ。
# ser1.name = "シリーズ1"
# ser2.name = "シリーズ2"
# ser4 = pd.concat([ser1, ser2], axis = 1)
# # print(ser4)

# # DataFrameを列方向に連結
# df5 = pd.concat([df1, df2], axis = 1)
# # print(df5)

# # 列の名前の付け方
# # 'Series' => '.name'
# # 'DataFrame' => 'columns'
# # コラムのラベルが重なり合わない箇所は「NaN」が代入される。
# dft = df1.copy()
# dft.columns = ['a', 'b', 'd']
# df6 = pd.concat([df1, dft], axis = 0)
# # print(df6)

# # この違いは決定的
# # dft = df1.copy()
# #     a   b    c    d
# # 0  a0  b0   c0  NaN
# # 1  a1  b1   c1  NaN
# # 2  a2  b2   c2  NaN
# # 0  a0  b0  NaN   c0
# # 1  a1  b1  NaN   c1
# # 2  a2  b2  NaN   c2

# # コピーをしないと新たに作ったラベルで元のdfが上書きされる。
# # dft = df1
# #     a   b   d
# # 0  a0  b0  c0
# # 1  a1  b1  c1
# # 2  a2  b2  c2
# # 0  a0  b0  c0
# # 1  a1  b1  c1
# # 2  a2  b2  c2

# # 列方向に連結。その際にインデックスを付与していく。
# # かち合わないない箇所は「NaN」で埋まる。
# # インデックスの挙動に注目。思いこまない。
# dft = df1.copy()
# dft.index = [0, 2, 100]
# df6 = pd.concat([df1, dft], axis = 1)
# # print(df6)


# dft = df1.copy()
# dft.index = [0, 2, 100]
# # 'outer'は「NaN」で埋めて全てを連結する。
# # df7 = pd.concat([df1, dft], axis = 1, join = 'outer')
# # 'inner'は値を持っているという意味で共通するインデックスを合成して返す。
# df7 = pd.concat([df1, dft], axis = 1, join = 'inner')
# # print(df7)

# # 'join_axes'という引数はないと言われた。
# # print(df1)
# # dft = df1.copy()
# # dft.index = [0, 2, 100]
# # print(dft)
# # df8 = pd.concat([df1, dft], axis = 1)
# # print(df8)
# # df9 = pd.concat([df1, dft], axis = 1, join_axes = [df1.index])
# # print(df9)

# # インデックスを引き直す
# df10 = pd.concat([df1, df2], axis = 0, ignore_index = True)
# # print(df10)

# ##### merge関数

# # 元データ
# left_df = pd.DataFrame({
#   'a': ['a0', 'a1', 'a2'],
#   'b': ['b0', 'b1', 'b2'],
#   'key': ['k0', 'k1', 'k2']
# })

# right_df = pd.DataFrame({
#   'c': ['a0', 'a1', 'a2'],
#   'd': ['b0', 'b1', 'b2'],
#   'key': ['k0', 'k1', 'k2']
# })

# キーになる列の内容が同じでないと機能しない。つまり列の長さにも厳しい。
# df1 = pd.merge(left_df, right_df, on = 'key')
# print(df1)

# キーになる列の名前が異なる時の対処。結果はただのconcat。
# left2 = left_df.copy()
# left2.columns = ['e', 'f', 'key_left']
# df2 = pd.merge(left2, right_df, left_on = 'key_left', right_on = 'key')
# print(df2)

#     e   f key_left   c   d key
# 0  a0  b0       k0  a0  b0  k0
# 1  a1  b1       k1  a1  b1  k1
# 2  a2  b2       k2  a2  b2  k2

###################### # SeriesをDFに追加するやり方を探る。
# ser1 = pd.Series(['a3', 'b3', 'left_k3'], columns = ['a', 'b', 'key'])
# left_df = pd.concat([left_df, ser1], axis = 0)

# print(left_df)
# print(right_df)

# # dfに行を追加するこは出来るが、インデックスを平すことができない。
# left_df.loc[-1] = ['a3', 'b3', 'left_k3']
# # print(left_df)
# #      a   b      key
# #  0  a0  b0       k0
# #  1  a1  b1       k1
# #  2  a2  b2       k2
# # -1  a3  b3  left_k3

# # right_df.loc[-1] = ['c3', 'c3', 'right_k3']
# # # print(right_df)
# # #      c   d       key
# # #  0  a0  b0        k0
# # #  1  a1  b1        k1
# # #  2  a2  b2        k2
# # # -1  c3  c3  right_k3

# # 2つのdfで、同じキーをもつ値を集めてくれる。すごい機能。
# df3 = pd.merge(left_df, right_df, on = ['key'], how = 'inner')
# # print(df3)

# # 値の不足分はNaNで埋めて、インデックスは平にしてくれる。
# df4 = pd.merge(left_df, right_df, on = ['key'], how = 'outer')
# # print(df4)
# #      a    b       key    c    d
# # 0   a0   b0        k0   a0   b0
# # 1   a1   b1        k1   a1   b1
# # 2   a2   b2        k2   a2   b2
# # 3   a3   b3   left_k3  NaN  NaN
# # 4  NaN  NaN  right_k3   c3   c3

# # 左のキーを基準とする。値がなければその行は削除される。
# df5 = pd.merge(left_df, right_df, on = ['key'], how = 'left')
# # print(df5)
# #     a   b      key    c    d
# # 0  a0  b0       k0   a0   b0
# # 1  a1  b1       k1   a1   b1
# # 2  a2  b2       k2   a2   b2
# # 3  a3  b3  left_k3  NaN  NaN

# # 右のキーを基準とする。値がなければその行は削除される。
# df6 = pd.merge(left_df, right_df, on = ['key'], how = 'right')
# # print(df6)
# #      a    b       key   c   d
# # 0   a0   b0        k0  a0  b0
# # 1   a1   b1        k1  a1  b1
# # 2   a2   b2        k2  a2  b2
# # 3  NaN  NaN  right_k3  c3  c3

# left2 = left_df.copy()
# left2['key2'] = ['k20', 'k21', 'k22', 'k23']

# right2 = right_df.copy()
# right2['key2'] = ['k20', 'k21', 'k21', 'k22']

# df = pd.DataFrame(
#   [
#   ['a0', 'a1', 'a2'],
#   ['b0', 'b1', 'b2'],
#   ['c0', 'c1', 'c2'],
#   ['k0', 'k1', 'k2']
#   ],
#   columns = ['あ', 'い', 'う']
#   )
# tdf = pd.DataFrame(
#   [
#   ['ta0', 'ta1', 'ta2'],
#   ['tb0', 'tb1', 'tb2'],
#   ['tc0', 'tc1', 'tc2'],
#   ['tk0', 'tk1', 'tk2']
#   ],
#   columns = ['あ', 'い', 'う']
#   )

# tdf = pd.DataFrame([], columns = df.columns)
# rag = [1, 3]
# for i in rag:
#   tdf = pd.concat([tdf, pd.DataFrame([df.loc[i]])], axis = 0, ignore_index = True)
# print(tdf)
# # print(df.loc[i])
# # print(df)
# # print(df.columns)
# # print(df.index)

df = pd.DataFrame(
  [
    ['あ', 'い', 'う', 'え', 'お'],
    ['あ', 'き', 'く', 'け', 'こ'],
    ['あ', 'し', 'す', 'せ', 'そ'],
    ['た', 'ち', 'つ', 'て', 'と'],
    ['た', 'に', 'ぬ', 'ね', 'の'],
    ['は', 'ひ', 'ふ', 'へ', 'ほ']
  ],
  columns = ['一列', '二列', '三列', '四列', '五列']
)
# print(df)
# tdf = df.loc[1]
tdf = pd.DataFrame([])
tdf = pd.concat([tdf, pd.DataFrame([df.loc[2]])], axis = 0)
# print(tdf)
tmp_arr = []
for idx, bl in df['一列'].duplicated(keep = 'first').iteritems():
  if bl == False:
    tmp_arr.append(idx)

# print(tmp_arr)
df.loc[0] = pd.Series()
print(df.loc[1])

# arr = [i for i in df['一列'].duplicated(keep = 'first').index]
#     # en_idx = tdf['判定'][~tdf['判定'].isna()].index

# print(arr)