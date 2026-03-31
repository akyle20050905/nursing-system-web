from app import create_app

# 僅負責啟動應用程式
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)