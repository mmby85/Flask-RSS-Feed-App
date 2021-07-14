from flask import Flask, render_template, request,redirect
import xml.etree.ElementTree as et
import xml
import requests



app = Flask(__name__)

def getrss(data):
    stree = et.fromstring(data)

    items = stree[0].findall('item') #.findall('title')

    pos = [ i.tag for i in items[0] ]

    titles = [ i[pos.index('title')].text for i in items ]   
    descriptions =  [ i[pos.index('description')].text for i in items ]   
    links = [ i[pos.index('link')].text for i in items ]     

    feeds = [ [titles[i] ,descriptions[i],links[i]] for i in range(len(titles))]
    return feeds

@app.route('/', methods=['GET','POST'])
def index1():
    feeds = ''
    if request.method == 'POST':
        if request.form['url'] == "":
            return redirect('/')
        print(request.form, request.form['url'])
        data = requests.get(request.form['url'])
        feeds = getrss(data.content)

    return render_template('index.html', list = feeds)

@app.route('/api', methods=['GET'])
def index():
    f = open(r'D:\DevWeb\Flask\FlaskReact\devprojects\api\unrss.xml','r')
    data = f.read()
    f.close()
    
    feeds = getrss(data)

    return {'feed1': feeds }

if __name__ == '__main__':
    app.run(debug=True)
    