from flask import Flask, render_template

from Services.CfgService import CfgService
from Services.ServerDbService import ServerDbSevice
from config.Config import CfgKey

app = Flask(__name__)



@app.route(CfgService.get(CfgKey.SERVER_INDEX_PAGE))
def indexPage():
    ServerDbSevice.printAll()
    return render_template('index/index.html')

@app.route(CfgService.get(CfgKey.SERVER_DOWNLOAD_PICTURE_PAGE)+"/<pictureName>")
def downloadPicturePage(pictureName):
    return render_template('picture/download.html',name=pictureName)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(CfgService.get(CfgKey.SERVER_PORT)))
