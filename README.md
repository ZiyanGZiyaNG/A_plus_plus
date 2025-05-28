# A++ Language
A++ 是一個學習與實驗用的迷你程式語言，
目標是做出一款語法類似Python，但速度與C++相近的語言，主要用於競程
支援整數運算、條件、巢狀控制、輸入/輸出與註解。

## 目錄結構
A_plus_plus/

├── main.py

├── ast_nodes.py

├── compiler_custom.py

├── parser_text.py

├── output.txt (自動產生，結果輸出)

## 支援語法
1. 變數宣告/賦值
2. 輸入
3. 輸出
4. 註解
5. 條件 if/else
6. while 迴圈
7. for 迴圈（逗號分隔，支援變數上下界）

## 如何執行
1. 安裝 Python 3（3.8 以上）
2. 把所有 .py 檔案放在同一資料夾
3. 編輯 main.py 內的 code = """ ... """ 塊，寫上你的 A++ 程式
4. 終端機執行：
   python main.py
5. 執行過程中，如遇 in()，請在終端機直接輸入數字並按 Enter
輸出會寫到桌面的 output.txt 檔案

## 輸入/輸出說明
。遇到 in() 時程式會在終端機停下，等待你輸入一個整數
。直接在終端機輸入數字後按 Enter
。多個 in() 會多次輸入
。所有 out(...) 內容都會寫進 output.txt，每行一個數值

## 注意事項
。只支援 int 型別
。目前不支援函式、陣列、字串等進階語法
。每行只能寫一個語句，且語法必須嚴格對齊
。註解可用 # 或 -- 開頭，支援行尾註
。推薦編譯器為Microsoft Visual Code

## 作者
ZiyanGZiyaNG
