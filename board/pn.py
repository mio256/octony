import math
import csv
from janome.tokenizer import Tokenizer


def get_pn(self):

    # ネガポジ辞書を読む
    np_dic = {}
    # fp = open("/home/mio256/mysite/pn.csv", "rt", encoding="utf-8")
    fp = open("pn.csv", "rt", encoding="utf-8")
    reader = csv.reader(fp, delimiter='\t')
    for i, row in enumerate(reader):
        name = row[0]
        result = row[1]
        np_dic[name] = result
        # if i % 500 == 0: print(i)

    # 小説を読み込む
    responses = self.response_set.all()
    text = ""
    for i in responses:
        text += i.content

    # 形態素解析
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
    cnt = res["p"] + res["n"] + 1
    return "ホワイト" + str(math.floor(res["p"] / cnt * 100)) + "%"
