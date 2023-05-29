# -*- coding: utf-8 -*-
"""
Colorful Getting Earthquake Infomation from YahooJapan
Version: 1.1
Author: DarkRix
"""

import console, concurrent.futures, os, re, urllib.request, ui, keyboard

def _tg(source, tag):
    _hd = source.read().decode() # htmlの読み込み
    _ht = tag.split('.')[0] # 読み込むタグの選択
    _tn = '.'.join(tag.split('.')[1:]) # 読み込むクラスの選択
    _tgi = ''.join(_hd.split('<{} class="{}">'.format(_ht, _tn))[1:]) # 読み込んだタグとそのクラスで分割
    _tgs = _tgi.split('</{}>'.format(_ht))[0].replace('  ','').split('<{} '.format(_ht))[0] # 読み込んだタグの終わりで分割し、整形
    _tga = re.sub('(\n\n)', '', _tgs) # 改行を一括削除
    _tgt = re.sub('<!.+\n', '', _tga).replace('><', '>\n<') # 整形
    return _tgt

def _r(d):
    _r0 = '発生時刻'
    _r1 = '震源地'
    _r2 = '最大震度'
    _r3 = 'マグニチュード'
    _r4 = '深さ'
    _r5 = '緯度/経度'
    _r6 = '情報'
    _rd0 = '・発生時刻: '
    _rd1 = '\n・震源地: '
    _rd2 = '\n・最大震度: '
    _rd3 = '\n・地震の規模: M'
    _rd4 = '\n・深さ: '
    _rd5 = '\n・緯度/経度: '
    _rd6 = '\n・津波情報: '
    _sw = '。'
    _eq = re.sub('([ ])', '', d) # 不要なスペースを削除
    _eq1 = re.sub('(\n\n)','', _eq) # 改行を一括削除
    _eq2 = _eq1.replace(_r0, _rd0) # 発生時刻を「・発生時刻: 」へ置き換え
    _eq3 = _eq2.replace(_r1, _rd1) # 震源地を改行してから「・震源地: 」へ置き換え
    _eq4 = _eq3.replace(_r2, _rd2) # 最大震度を改行してから「・最大震度: 」へ置き換え
    _eq5 = _eq4.replace(_r3, _rd3) # マグニチュードを改行してから「地震の規模: M」へ置き換え
    _eq6 = _eq5.replace(_r4, _rd4) # 深さを改行してから「・深さ: 」へ置き換え
    _eq7 = _eq6.replace(_r5, _rd5) # 緯度/経度を改行してから「・緯度/経度: 」へ置き換え
    _eq8 = _eq7.replace(_r6, _rd6).split(_sw)[0] # 情報を改行してから「・津波情報: 」へ置き換えて「。」で分割して整形

    return _eq8.split('\n') # 改行で分割

def main():
    _u = "https://typhoon.yahoo.co.jp/weather/earthquake/" # YahooJapanの地震情報
    _ua = 'Mozilla/5.0 (Linux; U; Android 8.0; en-la; Nexus Build/JPG991) AppleWebKit/511.2 (KHTML, like Gecko) Version/5.0 Mobile/11S444 YJApp-ANDROID jp.co.yahoo.android.yjtop/4.01.1.5' # Android端末のYahooアプリに偽装
    _d = urllib.request.urlopen(urllib.request.Request(_u, headers={'User-Agent': _ua})) # 定義したユーザーエージェントに従いURLへアクセス
    _t = _tg(_d, 'div.eqDetail') # htmlを受け渡し、divタグの「eqDetail」を選択

    return '\n'.join(_r(''.join(re.findall('<.+>(.+)<.+>', _t)))) # タグ内の文字列だけを抽出

if __name__ == '__main__':
    keyboard.insert_text(concurrent.futures.ThreadPoolExecutor(os.cpu_count()*99999).submit(main).result())
