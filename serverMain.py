import base64
import io

from flask import Flask, render_template, send_file, abort
from cryptography.fernet import Fernet

from Services.CfgService import CfgService
from Services.FileFolderService import FileFolderService
from Services.ServerDbService import ServerDbSevice
from config.Config import CfgKey

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route(CfgService.get(CfgKey.SERVER_INDEX_PAGE))
def indexPage():
    dbResults = ServerDbSevice.getPictureNames()
    picturePageUrl = []
    for dbResult in dbResults:
        picturePageUrl.append(CfgService.get(CfgKey.SERVER_DOWNLOAD_PICTURE_PAGE)+"/"+dbResult)
    return render_template('index/index.html',len = len(picturePageUrl), picturePageUrl = picturePageUrl)


#https://stackoverflow.com/questions/11017466/flask-to-return-image-stored-in-database
@app.route(CfgService.get(CfgKey.SERVER_DOWNLOAD_PICTURE_PAGE)+"/<pictureName>")
def downloadPicturePage(pictureName):
    ids = ServerDbSevice.getPictureUrlIds(pictureName)
    if not ids:
        abort(404)
    else:
        pictureUrls = []
        for id in ids:
            pictureUrls.append(CfgService.get(CfgKey.SERVER_DOWNLOAD_PICTURE)+"/"+id)
        return render_template('picture/download.html',name=pictureName, len = len(pictureUrls), pictureUrls = pictureUrls)


@app.route(CfgService.get(CfgKey.SERVER_DOWNLOAD_PICTURE)+"/<urlId>")
def downloadPicture(urlId):
    picturePathAndName = ServerDbSevice.getPicturePathAndName(urlId)
    if not picturePathAndName:
        abort(404)
    else :
        imageAsByte = FileFolderService.readImage(picturePathAndName[1])
        return send_file(io.BytesIO(imageAsByte),
                         as_attachment=True,
                         attachment_filename=CfgService.get(CfgKey.PROJECTNAME)+"_"+picturePathAndName[0]+'.png',
                         mimetype='image/png')

@app.route(CfgService.get(CfgKey.SERVER_RANDOM_URLIDS))
def getRandomPictureUris():
    #key = Fernet.generate_key()
    #cipher_suite = Fernet(key)
    pictureUrlIds = ServerDbSevice.getRendomPictureUrlIds(CfgService.get(CfgKey.SERVER_GETPICTUREURLIDS_NUMBER))
    #pictureUrlsAsString = key.decode('utf-8')

    pictureUrlsAsString = ""

    for urlId in pictureUrlIds:
        url = "http://"+CfgService.get(CfgKey.SERVER_IP)+":"+CfgService.get(CfgKey.SERVER_PORT)+CfgService.get(CfgKey.SERVER_DOWNLOAD_PICTURE)+"/"+urlId
        pictureUrlsAsString += url +";"
    #     pictureUrlsAsString += cipher_suite.encrypt(url).decode('uft-8')+";"
    #
    # testSplitted = pictureUrlsAsString.split(";")
    # testKey = bytes(testSplitted[0],'utf-8')
    # test_cipher_suite = Fernet(testKey)
    # for testResultRaw in testSplitted[1:]:
    #     testResult = bytes(testResultRaw[-1],'utf-8')
    #     print(test_cipher_suite.decrypt(testResult))
    # return pictureUrlsAsString
    return pictureUrlsAsString

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(CfgService.get(CfgKey.SERVER_PORT)))
