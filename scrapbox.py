import re
import pyperclip


#######################################################################
# method
#######################################################################

# 通常変換を行う関数
def normal_conversion(line):
    # 強調
    if '[******* ' in line:
        line = line.replace('[******* ','# ').replace(']','\n')
    elif '[****** ' in line:
        line = line.replace('[****** ','# ').replace(']','\n')
    elif '[***** ' in line:
        line = line.replace('[***** ','# ').replace(']','\n')
    elif '[**** ' in line:
        line = line.replace('[**** ','## ').replace(']','\n')
    elif '[*** ' in line:
        line = line.replace('[*** ','### ').replace(']','\n')
    elif '[** ' in line:
        line = line.replace('[** ','#### ').replace(']','\n')
    elif '[* ' in line:
        line = line.replace('[* ','**').replace(']','**\n')


    # 箇条書き
    elif re.match('^ ',line) or re.match('^\t',line):
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


    # 画像リンク
    if '[https://gyazo.com/' in line:
        line = line.replace(']', '/raw)' ).replace('[', '![画像](') # githubで画像を載せるには，末尾に\rawが必要
        line = line + '\n'

    # webリンク[http://~~]
    elif '[http://' in line or '[https://' in line:
        line = line.replace('[','').replace(']','')
        line = line + '\n'
    # タイトル付きwebリンク
    elif (('http://' in line) and ('[' in line)) or (('https://' in line) and ('[' in line)):
        line = line.replace(']',')')
        line = re.sub(' http','](http',line)
        line = line + '\n'

    # 文字列を返す
    return line





#######################################################################
# main
#######################################################################


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
        # 現在のインデントが最初以下になったらコード記法の終了を判定
        if re.match('^ *', line.replace('\t',' ')).end() <= indent_depth:
            line = '```\n\n' + normal_conversion(line)
            status = 'normal'
    
    # 表の処理
    elif status == 'table':
        # スペースのみの行を改行文字に置換
        line = re.sub(' +\n','\n',line)

        # 現在のインデントが最初以下になったら表記法の終了を判定
        if re.match('^ *', line.replace('\t',' ')).end() <= indent_depth:
            line = '```\n\n' + normal_conversion(line)
            status = 'normal'
        # 終了しない場合，表の変換処理
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
        # ソースコードを認識
        if re.match('^\s*code:',line):
            # インデントを数える
            indent_depth = re.match('^ *', line.replace('\t',' ')).end()
            # 変換準備
            status = 'code'
            line = re.sub('^\s*code:','```',line)


        # 表を認識
        elif re.match('^table:',line):
            # インデントを数える
            indent_depth = re.match('^ *', line.replace('\t',' ')).end()
            # 変換準備
            status = 'table'
            table_line = False
            line = line.replace('table:','`').replace('\n','`')

        else:
            # 通常の場合の変換
            line = normal_conversion(line)


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

