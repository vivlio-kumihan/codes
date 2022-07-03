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

# # 数字を使う場合、
# # numpyを使ってリストを生成する。
# # reshapeで多重リストが作れる。

# val = np.arange(0,12).reshape(3, 4)
# print(val)
# # [[ 0  1  2  3]
# #  [ 4  5  6  7]
# #  [ 8  9 10 11]]

# df = pd.DataFrame(val, columns = list('abcd'))
# print(df)
# #    a  b   c   d
# # 0  0  1   2   3
# # 1  4  5   6   7
# # 2  8  9  10  11

# # del文というそうだ。
# del df['d']
# print(df)
# #    a  b   c
# # 0  0  1   2
# # 1  4  5   6
# # 2  8  9  10

# # 削除する場合は「drop」を使うそうだ。
# # オプションで「axis」を「1」で垂直方向、つまり列を削除する。
# # del文と違い、変更を確定させる作業が必要。
# df = df.drop(labels = 'b', axis = 1)
# print(df)
# #    a   c
# # 0  0   2
# # 1  4   6
# # 2  8  10

# # オプションで「axis」を「0」で水平方向、つまり行を削除する。
# df = df.drop(labels = 2, axis = 0)
# print(df)
# #    a  c
# # 0  0  2
# # 1  4  6

# df = df.drop(columns = 'c')
# print(df)
# #    a
# # 0  0
# # 1  4

# val = np.arange(12,24).reshape(3, 4)
# df2 = pd.DataFrame(val, columns = list('efgh'))
# print(df2)
# #     e   f   g   h
# # 0  12  13  14  15
# # 1  16  17  18  19
# # 2  20  21  22  23

# # 列を追加するので「axis = 1」。
# df = pd.concat([df, df2], axis = 1)
# print(df)
# #      a   e   f   g   h
# # 0  0.0  12  13  14  15
# # 1  4.0  16  17  18  19
# # 2  NaN  20  21  22  23

# # popの挙動。pooしたものはシリーズとなる。
# # もとのdfから該当の列は抜かれる。
# ser = df.pop('e')
# print(df)

# # 「np.arange」は、任意に付けた最初のインデックス番号から、
# # 引いた数の数字が入った配列を生成すると覚える。
# # 「reshape」は、この場合、「4行の3列」に整形するということ。
# df3 = pd.DataFrame(np.arange(1, 13).reshape(4, 3), columns = list('abc'))
# print(df3)

# # 「loc」を使う。インデックス0番と2番の行に、「a」と「b」の列を抜き取る。
# df3 = df3.loc[[0, 2], 'a':'b']
# print(df3)

for i in range(10):
  print(i)
  print(type(i))

print([i for i in range(10)])

# 多次元配列を簡単に作れるnpはすごい。

df4 = pd.DataFrame(np.arange(1, 5).reshape(2, 2), columns = list('ab'))
print(df4)