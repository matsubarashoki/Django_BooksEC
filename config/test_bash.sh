#!/bin/bash

#Ubuntu入れたくなかったから、Git bushで練習や
#実行方法：https://enblog.jp/linux-cmd-forwindows/

#学習元：https://qiita.com/zayarwinttun/items/0dae4cb66d8f4bd2a337

# 入力
read Name
echo "Hello, $Name"
echo -e "Hello,\n$Name" #-eで特殊文字のエスケープ

# echo コメント
echo "コメントや"

# 変数 $変数名 変数の＝の前後は空白無し
variable="変数"
echo $variable

# 配列
declare -a array=("1" "2" "3")
#要素数をカウント
echo ${#array[@]}
echo "------------"
#先頭に追加
array=("4" "${array[@]}")
#末尾に追加
array=(${array[@]} "5")
#　indexで取得
echo ${array[0]}
echo ${array[4]}
echo ${array[@]} #全部取得
echo "------------"

#ループで参照
for v in "${array[@]}"
do
    echo $v
done

#while
v=0
while [ $v -lt 10 ]

#特別な変数
echo $0 #スクリプト名