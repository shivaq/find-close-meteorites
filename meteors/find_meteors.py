# -*- coding: utf-8 -*-

import math
import requests

# 2箇所の緯度経度から、2箇所間の距離を計算
def calc_dist(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    h = math.sin((lat2 - lat1) / 2 ) ** 2 + \
     math.cos(lat1) * \
     math.cos(lat2) * \
     math.sin( (lon2 - lon1 ) / 2) ** 2

    return 6372.8 * 2 * math.asin(math.sqrt(h))

# 引数: 隕石データリスト
# 返り値: 引数のリストの distance キーの値
def get_dist(meteor):
    return meteor.get( 'distance', math.inf)

# 直接このモジュールが呼び出されていた場合
if __name__ == '__main__':
    # 基準となる、緯度経度をセット
    my_loc = ( 35.028249, 135.769686)

    # NASA の隕石情報 JSON API を取得
    meteor_resp = requests.get('https://data.nasa.gov/resource/y77d-th95.json')
    # JSON データを整形
    meteor_data = meteor_resp.json()

    # JSON データをループ
    for meteor in meteor_data:
        # 緯度経度キーがない場合 →continue(つまり、現在の要素のターンの以降の処理をスキップ)
        if not ('reclat' in meteor and 'reclong' in meteor): continue
        # 現在の要素に distance キー、calc_dist() の返り値 バリュー を追記
        meteor['distance'] = calc_dist(float(meteor['reclat']),
                                       float(meteor['reclong']),
                                       my_loc[0],
                                       my_loc[1])

    # JSON データをソート。引数に get_dist ファンクション
    # get_dist() の返り値は 引数のリストの distance キーの値
    #  →distance の値でソート
    meteor_data.sort(key=get_dist)

    # ソートされた JSON リストの TOP 10 を出力
    print(meteor_data[0:10])
