from flask import Flask, render_template, request, redirect, url_for
from googleapiclient.discovery import build
import requests
import os

app = Flask(__name__)

# Replace with your API key and Custom Search Engine ID
API_KEY = 'AIzaSyCGyqf36D5k3QghaZLhAqb1R2OUtRFraF8'
CX = '0d386b282da5209ea'
SERVICE = build('customsearch', 'v1', developerKey=API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    image_number = int(request.form['imageNumber'])
    search_response = SERVICE.cse().list(
        q=keyword,
        cx=CX,
        searchType='image',
        num=image_number
    ).execute()

    images = search_response.get('items', [])
    if not os.path.exists('./images'):
        os.makedirs('./images')
    else:
        for file in os.listdir('./images'):
            os.remove(os.path.join('./images', file))

    for i, item in enumerate(images):
        img_url = item['link']
        img_data = requests.get(img_url).content
        with open(f'./images/image_{i}.jpg', 'wb') as handler:
            handler.write(img_data)

    return redirect(url_for('results'))

@app.route('/results')
def results():
    image_files = os.listdir('./images')
    return render_template('results.html', images=image_files)

if __name__ == '__main__':
    app.run(debug=True)
