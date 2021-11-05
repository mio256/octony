# ネガポジ辞書を読む
import csv

np_dic = {}
fp = open("pn.csv", "rt", encoding="utf-8")
reader = csv.reader(fp, delimiter='\t')
for i, row in enumerate(reader):
    name = row[0]
    result = row[1]
    np_dic[name] = result
    # if i % 500 == 0: print(i)

# 小説を読み込む
fp = open("pn_text.txt", "rt", encoding="utf-8")
text = fp.read()

# 形態素解析
from janome.tokenizer import Tokenizer

tok = Tokenizer()

# 数える
res = {"p": 0, "n": 0, "e": 0}
for t in tok.tokenize(text):
    bf = t.base_form  # 基本形
    # 辞書にあるか確認
    if bf in np_dic:
        r = np_dic[bf]
        if r in res:
            res[r] += 1

# 結果を表示
print(res)
cnt = res["p"] + res["n"] + res["e"]
print("ポジティブ度", res["p"] / cnt)
print("ネガティブ度", res["n"] / cnt)