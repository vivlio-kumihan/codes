import sys
import re
import pandas as pd
import numpy as np
sys.path.append('../lib')
import ntzreg


# 氏名揃え　4文字揃え
def name4justify(ins):
    justifed_name = ""
    # 前後の空白を取り去ってから
    ins = ins.strip()
    # 文字列にスペースが入っていない場合の処理をする。
    if re.search(r"\s", ins):
        # 氏名を配列として格納
        name = ins.split()
        uji_size = len(name[0])
        mei_size = len(name[1])
        # 〓　〓 or 〓　〓〓 or 〓〓　〓 or 〓　〓〓〓 or 〓〓〓　〓
        if uji_size == 1 and mei_size == 1 or uji_size == 1 and mei_size == 2 or uji_size == 2 and mei_size == 1 or uji_size == 1 and mei_size == 3 or uji_size == 3 and mei_size == 1:
            justifed_name = f'{name[0]}　{name[1]}'
        else:
            justifed_name = f'{name[0]}{name[1]}'
    else:
        justifed_name = ins
        
    return justifed_name

# 氏名揃え　5文字揃え
def name5justify(ins):
    justifed_name = ""
    # 文字列にスペースが入っていない場合の処理をする。
    if re.search(r"\s", ins):
        # 1 splitは優秀。オプション無しで＃2と同じ処理をしてくれる。
        name = ins.split()
        # 2 だから、この処理は不要です。
        # name = [n.strip() for n in ins.sprit()]
        uji_size = len(name[0])
        mei_size = len(name[1])
        # 〓　　　〓
        if uji_size == 1 and mei_size == 1:
            justifed_name = f'{name[0]}　　　{name[1]}'
        # 〓〓　〓〓 or 〓　〓〓〓 or 〓〓〓　〓
        elif uji_size == 2 and mei_size == 2 or uji_size == 1 and mei_size == 3 or uji_size == 3 and mei_size == 1:
            justifed_name = f'{name[0]}　{name[1]}'
        # 〓　　〓〓 or 〓〓　　〓
        elif uji_size == 1 and mei_size == 2 or uji_size == 2 and mei_size == 1:
            justifed_name = f'{name[0]}　　{name[1]}'
        # 〓〓 〓〓〓 or 〓〓〓　〓〓 or 〓〓〓　〓〓〓 or 〓〓〓　〓〓〓〓 or 〓〓〓〓　〓〓〓 or other
        else:
            justifed_name = f'{name[0]}{name[1]}'
    else:
        justifed_name = ins
        
    return justifed_name


# 氏名揃え　7文字揃え
def name7justify(ins):
    justifed_name = ""
    ins = ntzreg.cellstr(ins)
    # 文字列にスペースが入っていない場合の処理をする。
    if re.search(r"\s", ins):
        name = ins.split()
        uji_size = len(name[0])
        mei_size = len(name[1])
        # 〓　　　　　〓
        if uji_size == 1 and mei_size == 1:
            justifed_name = f'{name[0]}　　　　　{name[1]}'
        # 〓　〓　〓　〓
        elif uji_size == 2 and mei_size == 2:
            justifed_name = f'{name[0][0]}　{name[0][1]}　{name[1][0]}　{name[1][1]}'
        # 〓　　　〓　〓
        elif uji_size == 1 and mei_size == 2:
            justifed_name = f'{name[0]}　　　{name[1][0]}　{name[1][1]}'
        # 〓　〓　　　〓
        elif uji_size == 2 and mei_size == 1:
            justifed_name = f'{name[0][0]}　{name[0][1]}　　　{name[1]}'
        # 〓　　　〓〓〓 or 〓〓〓　　　〓
        elif uji_size == 1 and mei_size == 3 or uji_size == 3 and mei_size == 1:
            justifed_name = f'{name[0]}　　　{name[1]}'
        # 〓　〓　〓〓〓
        elif uji_size == 2 and mei_size == 3:
            justifed_name = f'{name[0][0]}　{name[0][1]}　{name[1]}'
        # 〓〓〓　〓　〓
        elif uji_size == 3 and mei_size == 2:
            justifed_name = f'{name[0]}　{name[1][0]}　{name[1][1]}'
        # 〓〓〓　〓〓〓
        elif uji_size == 3 and mei_size == 3:
            justifed_name = f'{name[0]}　{name[1]}'
        # 〓〓〓　〓〓〓〓 or 〓〓〓〓　〓〓〓
        elif uji_size == 3 and mei_size == 4 or uji_size == 4 and mei_size == 3:
            justifed_name = f'{name[0]}{name[1]}'
        else:
            justifed_name = "例外発生" + f'{name[0]}{name[1]}'
    else:
        justifed_name = ins
        
    return justifed_name


# 氏名揃え　ルビ付き　4文字揃え
def name4justify_with_ruby(df_shimei, df_kana):
    justifed_name = ""
    tmp_names_with_ruby = []
    for shimei, kana in zip(df_shimei, df_kana):
        if kana is np.nan:
            tmp_names_with_ruby.append(np.nan)
        else:
            name = shimei.split()
            ruby = kana.split()
            uji_size = len(name[0])
            mei_size = len(name[1])
            # 〓　〓 => 〓　　〓
            if uji_size == 1 and mei_size == 1:
                justifed_name = f"[{name[0]}/{ruby[0]}]　　[{name[1]}/{ruby[1]}]"
            # 〓　〓〓 or 〓〓　〓
            elif uji_size == 1 and mei_size == 2 or uji_size == 2 and mei_size == 1:
                justifed_name = f"[{name[0]}/{ruby[0]}]　[{name[1]}/{ruby[1]}]"
            # 〓〓　〓〓 or 〓　〓〓〓 or 〓〓〓　〓
            # 〓〓 〓〓〓 or 〓〓〓　〓〓 or 〓〓〓　〓〓〓 or 〓〓〓　〓〓〓〓 or 〓〓〓〓　〓〓〓 ... other
            else:
                justifed_name = f"[{name[0]}/{ruby[0]}][{name[1]}/{ruby[1]}]"            
            tmp_names_with_ruby.append(justifed_name)
    return tmp_names_with_ruby


# 氏名揃え　ルビ付き　5文字揃え
def name5justify_with_ruby(df_shimei, df_kana):
    justifed_name = ""
    tmp_names_with_ruby = []
    for shimei, kana in zip(df_shimei, df_kana):
        if kana is np.nan:
            tmp_names_with_ruby.append(np.nan)
        else:
            name = shimei.split()
            ruby = kana.split()
            uji_size = len(name[0])
            mei_size = len(name[1])
            # 〓　〓 => 〓　　　〓
            if uji_size == 1 and mei_size == 1:
                justifed_name = f"[{name[0]}/{ruby[0]}]　　　[{name[1]}/{ruby[1]}]"
            # 〓　　〓〓 or 〓〓　　〓
            elif uji_size == 1 and mei_size == 2 or uji_size == 2 and mei_size == 1:
                justifed_name = f"[{name[0]}/{ruby[0]}]　　[{name[1]}/{ruby[1]}]"
            # 〓〓　〓〓 or 〓　〓〓〓 or 〓〓〓　〓
            elif uji_size == 2 and mei_size == 2 or uji_size == 1 and mei_size == 3 or uji_size == 3 and mei_size == 1:
                justifed_name = f"[{name[0]}/{ruby[0]}] [{name[1]}/{ruby[1]}]"
            # 〓〓 〓〓〓 or 〓〓〓　〓〓 or 〓〓〓　〓〓〓 or 〓〓〓　〓〓〓〓 or 〓〓〓〓　〓〓〓 ... other
            else:
                justifed_name = f"[{name[0]}/{ruby[0]}][{name[1]}/{ruby[1]}]"            
            tmp_names_with_ruby.append(justifed_name)
    return tmp_names_with_ruby

# 氏名揃え　ルビ付き　5文字揃え
def name5justify_with_ruby_plusZS(df_shimei, df_kana):
    justifed_name = ""
    tmp_names_with_ruby = []
    for shimei, kana in zip(df_shimei, df_kana):
        if kana is np.nan:
            tmp_names_with_ruby.append(np.nan)
        else:
            name = shimei.split()
            ruby = kana.split()
            uji_size = len(name[0])
            mei_size = len(name[1])
            # 〓　〓 => 〓　　　〓
            if uji_size == 1 and mei_size == 1:
                justifed_name = f"[{name[0]}/{ruby[0]}]　　　[{name[1]}/{ruby[1]}]"
            # 〓　　〓〓 or 〓〓　　〓
            elif uji_size == 1 and mei_size == 2 or uji_size == 2 and mei_size == 1:
                justifed_name = f"[{name[0]}/{ruby[0]}]　　[{name[1]}/{ruby[1]}]"
            # 〓〓　〓〓 or 〓　〓〓〓 or 〓〓〓　〓
            # 〓〓 〓〓〓 or 〓〓〓　〓〓 or 〓〓〓　〓〓〓 or 〓〓〓　〓〓〓〓 or 〓〓〓〓　〓〓〓 ... other
            else:
                justifed_name = f"[{name[0]}/{ruby[0]}]　[{name[1]}/{ruby[1]}]"
            tmp_names_with_ruby.append(justifed_name)
    return tmp_names_with_ruby


# 氏名のそれぞれの漢字にルビを付与
def each_han_with_ruby(name, ruby):
    tmp_name_with_ruby = []
    for index in range(len(name)):
        shimei = name[index].split()
        furigana = ruby[index].split()
        name_with_ruby = ""
        for num in range(len(shimei)):
            name_with_ruby += f"[{shimei[num]}/{furigana[num]}]"
        tmp_name_with_ruby.append(name_with_ruby)
    
    return tmp_name_with_ruby


# 日付を入れたら月・日・曜日だけを配列で返すコード。
# option w => ウィーク => 曜日の意味。
def extdate(str, option = "d"):
    str = re.sub("(月|日)", r" \1 ", str)
    if "w" in option:
        str = re.sub(r"[\(|（]\s*?(?=[月火水木金土日])", "", str)
        str = re.sub(r"(?<=[月火水木金土日])\s*?[\)）]", "", str)
    arr = str.split()
    return arr[::2]

# str = "12月20日"
# str = "12月20日（月）"
# print(ntzstr.extdate(str, "w"))