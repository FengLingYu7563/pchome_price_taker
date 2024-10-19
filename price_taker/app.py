from flask import Flask, request, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crawl', methods=['POST'])
def crawl():
    keyword = request.form['keyword']

    try:
        # 執行 PChome_clawer.py 腳本並傳入關鍵字
        result_crawl = subprocess.run(['python', './price_taker/PChome_clawer.py', keyword], capture_output=False, text=True, check=True)
        
        # 執行 insert_database.py 腳本
        result_insert = subprocess.run(['python', './price_taker/insert_database.py'], capture_output=False, text=True, check=True)
        
        # 如果成功完成，回傳成功訊息
        return f'爬蟲完成並已插入資料庫，關鍵字: {keyword}'

    except subprocess.CalledProcessError as e:
        # 回傳錯誤訊息
        return f"執行過程中發生錯誤：{e.stderr or '未知錯誤'}"
    except Exception as e:
        # 捕捉其他意外錯誤
        return f"發生未預期的錯誤: {str(e)}"
if __name__ == '__main__':
    app.run()