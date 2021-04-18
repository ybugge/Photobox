import base64
import io

from flask import Flask, render_template, send_file, abort, redirect, request, flash
from werkzeug.utils import secure_filename

from Services.CfgService import CfgService
from Services.FileFolderService import FileFolderService
from Services.Greenscreen.GreenscreenBackgroundService import GreenscreenBackgroundService
from Services.PrinterService import PrinterService
from Services.Db.ServerDbService import ServerDbSevice
from config.Config import CfgKey, textValue, TextKey

app = Flask(__name__)
app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1920 * 1920


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route(CfgService.get(CfgKey.SERVER_INDEX_PAGE))
def indexPage():

    dbResults = ServerDbSevice.getPictureNames()
    picturePageUrl = []
    if CfgService.get(CfgKey.SERVER_INDEX_PAGE_SHOW_ALL_PICTURES):
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
        printerService = PrinterService()
        pictureData = []
        allowedPrinting = printerService.printingPosible() and  CfgService.get(CfgKey.PRINTER_IS_ACTIVE) and not printerService.hasTooManyPrintingOrderWeb(pictureName)
        for id in ids:
            printUrl = CfgService.get(CfgKey.SERVER_PRINT_PICTURE_PAGE)+"/"+pictureName+"/"+id
            pictureData.append([CfgService.get(CfgKey.SERVER_DOWNLOAD_PICTURE)+"/"+id,printUrl,allowedPrinting])
        return render_template('picture/download.html',name=pictureName, len = len(pictureData), pictureData = pictureData)

@app.route(CfgService.get(CfgKey.SERVER_PRINT_PICTURE_PAGE)+"/<pictureName>/<pictureId>")
def printPicturePage(pictureName,pictureId):
    ids = ServerDbSevice.getPictureUrlIds(pictureName)
    picturePathAndName = ServerDbSevice.getPicturePathAndName(pictureId)

    if (not ids) or (not pictureId in ids) or (not picturePathAndName):
        abort(404)
    else:
        printerService = PrinterService()
        allowedPrinting = printerService.printingPosible() and  CfgService.get(CfgKey.PRINTER_IS_ACTIVE) and not printerService.hasTooManyPrintingOrderWeb(pictureName)

        if not allowedPrinting:
            return redirect(CfgService.get(CfgKey.SERVER_DOWNLOAD_PICTURE_PAGE)+"/"+pictureName)

        printerService.printWeb(pictureName,picturePathAndName[1])

        if printerService.isStatusInPrintWeb(pictureName):
            print_status_hint = textValue[TextKey.WEB_PRINT_STATUS_SUCCESS]
        else:
            print_status_hint = textValue[TextKey.WEB_PRINT_STATUS_FAILED]
        printerStatus = printerService.getPrinterStatus()
        backUrl = CfgService.get(CfgKey.SERVER_DOWNLOAD_PICTURE_PAGE)+"/"+pictureName
        return render_template('picture/print.html',backUrl=backUrl,printerStatus=printerStatus,print_status_hint=print_status_hint)


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
    numberOfPictures = ServerDbSevice.getNumberUsedPictures()
    if numberOfPictures <= CfgService.get(CfgKey.SERVER_GETPICTUREURLIDS_THRASHOLD):
        return base64.b64encode("".encode('utf-8'))

    pictureUrlIds = ServerDbSevice.getRendomPictureUrlIds(CfgService.get(CfgKey.SERVER_GETPICTUREURLIDS_NUMBER))
    pictureUrlsAsString = ""

    for urlId in pictureUrlIds:
        url = "http://"+CfgService.get(CfgKey.SERVER_IP)+":"+CfgService.get(CfgKey.SERVER_PORT)+CfgService.get(CfgKey.SERVER_DOWNLOAD_PICTURE)+"/"+urlId
        pictureUrlsAsString += url +";"
    return base64.b64encode(pictureUrlsAsString.encode('utf-8'))

## upload Background:-------------------------------------------
# https://roytuts.com/upload-and-display-image-using-python-flask/
ALLOWED_BACKGROND_EXTENSIONS = set(['png', 'jpg', 'jpeg']) # wenn das geändert wird: auch in textValue[TextKey.WEB_UPLOAD_BACKGROUND_ERROR_WRONG_TYPE] und upload.html beachten
UPLOAD_BACKGROUND_HTML_PATH = 'background/upload.html'

@app.route(CfgService.get(CfgKey.SERVER_UPLOAD_PICTURE)+"/<uuid>")
def uploadBackground_form(uuid):
    authorizade = ServerDbSevice.getBackgroundUploadAuthorization(uuid)
    if authorizade is None:
        abort(404)
    else:
        return render_template(UPLOAD_BACKGROUND_HTML_PATH,uuid=uuid,url = CfgService.get(CfgKey.SERVER_UPLOAD_PICTURE))

@app.route(CfgService.get(CfgKey.SERVER_UPLOAD_PICTURE), methods=['POST'])
def uploadBackground_image():
    uuid = request.form.get('uuid')
    if uuid is None:
        abort(404)
    authorizade = ServerDbSevice.getBackgroundUploadAuthorization(uuid)
    if authorizade is None:
        abort(404)
    if 'file' not in request.files:
        flash(textValue[TextKey.WEB_UPLOAD_BACKGROUND_ERROR_NO_PICTURE_SELECTED])
        return redirect(request.url+"/"+uuid)
    file = request.files['file']
    if file.filename == '':
        flash(textValue[TextKey.WEB_UPLOAD_BACKGROUND_ERROR_NO_PICTURE_SELECTED])
        return redirect(request.url+"/"+uuid)
    if file and allowed_background_file(file.filename):
        if authorizade["cleanBefore"]:
            FileFolderService.removeIfExist(authorizade["targetPath"])
        filename = secure_filename(file.filename)
        filePath = GreenscreenBackgroundService.getCustomFilePathWithName(authorizade["targetPath"],uuid, filename)
        file.save(filePath)
        flash(textValue[TextKey.WEB_UPLOAD_BACKGROUND_SUCCESS])
        if authorizade["cleanBefore"]:
            flash(textValue[TextKey.WEB_UPLOAD_BACKGROUND_SUCCESS_HINT_CUSTOMBACKGROUND])
        else:
            flash(textValue[TextKey.WEB_UPLOAD_BACKGROUND_SUCCESS_HINT_DEFAULTBACKGROUND])
        return render_template(UPLOAD_BACKGROUND_HTML_PATH,uuid=uuid,url = request.url,pictureUrl=CfgService.get(CfgKey.SERVER_DISPLAY_UPLOAD_PICTURE)+'/'+uuid+"/"+str(hash(filePath)))
    else:
        flash(textValue[TextKey.WEB_UPLOAD_BACKGROUND_ERROR_WRONG_TYPE])
        return redirect(request.url+"/"+uuid)

@app.route(CfgService.get(CfgKey.SERVER_DISPLAY_UPLOAD_PICTURE)+'/<uuid>/<number>')
def displayBackground_image(uuid,number):
    print("PictureHash: "+number)
    if uuid is None:
        abort(404)
    authorizade = ServerDbSevice.getBackgroundUploadAuthorization(uuid)
    if authorizade is None:
        abort(404)
    filePath = GreenscreenBackgroundService.getCustomFilePathWithName(authorizade["targetPath"],uuid)
    imageAsByte = FileFolderService.readImage(filePath)
    return send_file(io.BytesIO(imageAsByte),
                     as_attachment=True,
                     attachment_filename=FileFolderService.getFileName(filePath),
                     mimetype='image/'+FileFolderService.getFileType(filePath).replace("\.",""))

def allowed_background_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_BACKGROND_EXTENSIONS

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(CfgService.get(CfgKey.SERVER_PORT)))
