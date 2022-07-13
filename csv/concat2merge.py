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

# #### DataFrameの連結
df1 = pd.DataFrame({
  'a': ['a0', 'a1', 'a2'],
  'b': ['b0', 'b1', 'b2'],
  'c': ['c0', 'c1', 'c2']
})

df2 = pd.DataFrame({
  'a': ['a3', 'a4', 'a5'],
  'b': ['b3', 'b4', 'b5'],
  'c': ['c3', 'c4', 'c5']
})

df3 = pd.DataFrame({
  'a': ['a6', 'a7', 'a8'],
  'b': ['b6', 'b7', 'b8'],
  'c': ['c6', 'c7', 'c8']
})

# concat 行方向へ繋げる「axis = 0」がキモ
df4 = pd.concat([df1, df2, df3], axis = 0)

# print(df1)
# print(df2)
# print(df4)

# #### Seriesの連結
ser1 = pd.Series(['s1', 's2'])
ser2 = pd.Series(['s3', 's4'])

# 行方向に連結
ser3 = pd.concat([ser1, ser2], axis = 0)
# print(ser3)

# 列方向に連結
ser4 = pd.concat([ser1, ser2], axis = 1)

# nameメソッドでコラム名を追記できる。
# ただし、順番が大切。変更させた上でpdしないと反映しないよ。
ser1.name = "シリーズ1"
ser2.name = "シリーズ2"
ser4 = pd.concat([ser1, ser2], axis = 1)
# print(ser4)

# DataFrameを列方向に連結
df5 = pd.concat([df1, df2], axis = 1)
# print(df5)

# 列の名前の付け方
# 'Series' => '.name'
# 'DataFrame' => 'columns'
# コラムのラベルが重なり合わない箇所は「NaN」が代入される。
dft = df1.copy()
dft.columns = ['a', 'b', 'd']
df6 = pd.concat([df1, dft], axis = 0)
# print(df6)

# この違いは決定的
# dft = df1.copy()
#     a   b    c    d
# 0  a0  b0   c0  NaN
# 1  a1  b1   c1  NaN
# 2  a2  b2   c2  NaN
# 0  a0  b0  NaN   c0
# 1  a1  b1  NaN   c1
# 2  a2  b2  NaN   c2

# コピーをしないと新たに作ったラベルで元のdfが上書きされる。
# dft = df1
#     a   b   d
# 0  a0  b0  c0
# 1  a1  b1  c1
# 2  a2  b2  c2
# 0  a0  b0  c0
# 1  a1  b1  c1
# 2  a2  b2  c2

# 列方向に連結。その際にインデックスを付与していく。
# かち合わないない箇所は「NaN」で埋まる。
# インデックスの挙動に注目。重いこまない。
dft = df1.copy()
dft.index = [0, 2, 100]
df6 = pd.concat([df1, dft], axis = 1)
# print(df6)

