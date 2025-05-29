# A++ Language

A++ 是一個學習與實驗用的迷你程式語言，  
目標是打造語法簡單如 Python，但執行效能接近 C++ 的語言，  
專為演算法競賽與腦洞競程而設計 

支援整數運算、巢狀控制、遞迴函式、輸入輸出與動態陣列！


## 研究動機

為了完成的梗圖：  
![image](https://github.com/ZiyanGZiyaNG/A_plus_plus/blob/main/C%2B%2B%20to%20A%2B%2B.jpg)


##  目錄結構
A_plus_plus/
├── main.py # 執行入口

├── ast_nodes.py # AST 節點定義

├── compiler_custom.py # 編譯器模擬器（可導出輸出）

├── parser_text.py # A++ 語法解析器

├── interpreter.py # A++ 解譯器主程式（已支援 output.txt）

├── output.txt # 結果輸出（自動生成，於桌面）

## 支援語法

| 功能            | 說明                                               |
|-----------------|----------------------------------------------------|
| 變數            | `int x = 10`，支援數值與陣列初始化                 |
| 輸入            | `in()` → 等待使用者輸入一個整數                    |
| 輸出            | `out(x)` → 將數值輸出至 `output.txt`              |
| 註解            | 使用 `#` 或 `--` 開頭，支援行尾註解                |
| 條件            | `if (x > 0) { ... } else { ... }`                  |
| while 迴圈      | `while (x > 0) { ... }`                             |
| for 迴圈        | `for (int i = 0, i < n, ...) { ... }`              |
| 陣列            | `int arr = [1, 2, 3]`，支援 `arr[i]` 存取與賦值     |
| 動態陣列方法    | `arr.increase(x)` 加入元素、`arr.reduce()` 移除    |
| 陣列屬性        | `arr.length` 可取得長度                            |
| 自訂函式        | `func f(n) { return n * n }`，支援遞迴呼叫         |
| return 語法     | `return x`                                          |

##  如何執行

1. 安裝 Python 3.8 以上
2. 將所有 `.py` 放在同一資料夾
3. 編輯 `main.py` 中的 `code = """ ... """` 區塊，寫上你的 A++ 程式
4. 在終端機執行：
5. 執行時遇到 in()，請輸入整數並按 Enter
6. 執行結果將自動寫入「桌面」的 output.txt

## 注意事項

1. 目前僅支援整數 int
2. 每行只能寫一個語句（不支援多語句同行）
3. 尚未支援浮點數、字串、類別、函式巢狀定義
4. 所有輸出皆寫入桌面 output.txt（使用者無需另建）

## 作者
ZiyanGZiyaNG
一律同意搞報他
