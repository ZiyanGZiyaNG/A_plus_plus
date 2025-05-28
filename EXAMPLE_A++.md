# A++ 語言全語法範例（EXAMPLE_A++.md）

本檔案展示 A++ 自訂語言目前支援的所有語法特性，包含變數、輸入/輸出、控制流程、動態陣列、運算子與註解格式。
可搭配 `main.py` 輸入執行測試。

## 📌 語法測試程式碼

  # A++ 語言所有語法範例測試
    
  # 變數與基本運算
    int x = 5
    int y = x + 2
    out(x)
    out(y)
    
  # 四則運算與邏輯比較
    int a = 8
    int b = 3
    out(a + b)
    out(a - b)
    out(a * b)
    out(a / b)
    out(a % b)
    out(a == b)
    out(a >= 8)
    out(a != b)
    
  # 輸入
    int num = in()
    out(num * 2)
    
  # 註解測試
    -- 這也是註解
    out(z)
    
  # if-else 測試
    int score = in()
    if (score >= 60) {
        out(1)
    }
    else {
        out(0)
    }
    
  # while 迴圈
    int w = 3
    while (w > 0) {
        out(w)
        int w = w - 1
    }
    
  # for 迴圈
    int n = 5
    for (int i = 0, i < n, i = i + 1) {
        out(i)
    }
    
  # 陣列初始化與操作
    int arr = [1, 2, 3]
    out(arr[0])
    out(arr[2])
    out(arr.length)
    
  # 陣列動態增刪
    arr.Increase(10)
    arr.Increase(20)
    arr.Reduce()
    out(arr.length)
    
  # 陣列賦值與自動補零
    arr[5] = 88
    out(arr.length)
    out(arr[5])
    out(arr[4])  # 應為0
    
  # 陣列 for 迴圈
    for (int i = 0, i < arr.length, i = i + 1) {
        out(arr[i])
    }
    
    # 陣列輸入範例
    int arr2 = []
    arr2.Increase(in())
    arr2.Increase(in())
    out(arr2[0])
    out(arr2[1])
    out(arr2.length)
