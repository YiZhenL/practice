from flaskblog import create_app  # 從 flaskblog 模組中匯入應用程式工廠函式 create_app

# 使用工廠模式創建 Flask 應用實例
app = create_app()

# 判斷程式是否直接執行
if __name__ == '__main__':
    # 啟動 Flask 開發伺服器，並啟用 debug 模式
    # debug=True 允許即時重新載入程式碼並顯示詳細的錯誤訊息，適合開發階段使用
    app.run(debug=True)
