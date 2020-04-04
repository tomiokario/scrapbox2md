import re
import pyperclip


# クリップボードの文字列を取得
input_string = pyperclip.paste()
# クリップボードの文字列を一行ごとに分割して配列に格納
array = input_string.split('\n')


# メッセージ
print("----------------------------------------------------------------------")
print(pyperclip.paste())
print("変換します...")
print("----------------------------------------------------------------------")



# 変数初期化
status = 'normal'
output_string=""


# タイトル(一行目)をh1にする
array[0] = re.sub('^','# ',array[0])


for line in array:
    # 文末に改行文字を追加
    line = line + '\n'
    # 全角スペースを半角スペースに変換
    line = line.replace('\u3000',' ')



    # ソースコードの処理
    if status == 'code':
        # ソースコードモードの終了判定
        if line == '\n':
            line = line.replace('\n','```\n\n')
            status = 'normal'
    
    # 表の処理
    elif status == 'table':
        # スペースのみの行を改行文字に置換
        line = re.sub(' +\n','\n',line)

        # 表モードの終了判定
        if line == '\n':
            line = '\n\n'
            status = 'normal'
        # 処理
        else:
            line = '|' + line
            line = line.replace('\t',' | ').replace('\n',' |\n')
            # 一行目のとき
            if not table_line:
                blank = re.sub('[^\|]','',line)
                add_line = blank.replace('|',':-----------|')
                add_line = re.sub('^:-----------','',add_line)
                line = '\n' + line + add_line + '\n'
                table_line = True


    # 通常の記法処理
    else:

        # h1
        if   '[******* ' in line:
            line = line.replace('[******* ','# ').replace(']','\n')
        elif '[****** ' in line:
            line = line.replace('[****** ','# ').replace(']','\n')
        elif '[***** ' in line:
            line = line.replace('[***** ','# ').replace(']','\n')
        # h2 ~ 4
        elif '[**** ' in line:
            line = line.replace('[**** ','## ').replace(']','\n')
        elif '[*** ' in line:
            line = line.replace('[*** ','### ').replace(']','\n')
        elif '[** ' in line:
            line = line.replace('[** ','#### ').replace(']','\n')
        # 強調
        elif '[* ' in line:
            line = line.replace('[* ','**').replace(']','**\n')


        # ソースコードを認識
        #elif 'code:' in line:
        elif re.match('^code:',line):
            line = line.replace('code:','```')
            status = 'code'

        # 表を認識
        #elif 'table:' in line:
        elif re.match('^table:',line):
            line = line.replace('table:','`').replace('\n','`')
            status = 'table'
            table_line = False

        # 箇条書き
        elif re.match('^ ',line):
            line = line.replace('\t',' ')
            # 5インデント
            line = re.sub('^     ', '\t\t\t\t- ',line)
            # 4インデント
            line = re.sub('^    ' , '\t\t\t- ',line)
            # 3インデント
            line = re.sub('^   '  , '\t\t- ',line)
            # 2インデント
            line = re.sub('^  '   , '\t- ',line)
            # 1インデント
            line = re.sub('^ '    , ' - ',line)
        # 改行のみ
        elif line == '\n':
            line = line
        # 通常文字
        else:
            line = line + '\n'


        # リンクの処理
        ## 画像の場合
        if '[https://gyazo.com/' in line:
            line = line.replace(']', '/raw)' ).replace('[', '![画像](') # githubで画像を載せるには，末尾に\rawが必要
            line = line + '\n'

        ## [http://~~]の場合
        elif '[http://' in line or '[https://' in line:
            line = line.replace('[','').replace(']','')
            line = line + '\n'
        ## [タイトル http://~~]の場合
        elif (('http://' in line) and ('[' in line)) or (('https://' in line) and ('[' in line)):
            line = line.replace(']',')')
            line = re.sub(' http','](http',line)
            line = line + '\n'

    # 表示
    print(line, end="")
    # 出力文字列に追加
    output_string += line


# クリップボードにコピー
pyperclip.copy(output_string)


# メッセージ
print("----------------------------------------------------------------------")
print("変換が完了しました．")
print("クリップボードにコピーしました．")

