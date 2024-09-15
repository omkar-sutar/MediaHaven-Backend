import env
from auth import authorize
import os
from flask import request, Response
from req_resp import *
from flask import send_from_directory
from urllib.parse import unquote
import utils
from thumbnails.tasks import transform_filename, compress_image, TMP_DIR
from utils import profile

logger = utils.get_logger()

def send_partial_file(range_header,path):
        byte_range = range_header.replace('bytes=', '').split('-')
        start = int(byte_range[0])
        end = int(byte_range[1]) if byte_range[1] else os.path.getsize(path) - 1
        
        chunk_size = end - start + 1
        with open(path, 'rb') as f:
            f.seek(start)
            chunk = f.read(chunk_size)
        
        # Create a partial response with the correct status code (206) and headers
        response = Response(chunk, 206, mimetype='application/octet-stream', 
                            content_type='application/octet-stream',
                            direct_passthrough=True)
        response.headers.add('Content-Range', f'bytes {start}-{end}/{os.path.getsize(path)}')
        response.headers.add('Content-Length', str(chunk_size))
        return response

class MediaHandler:
    @authorize
    def List(user):
        dirname=user["username"]
        dirpath=os.path.join(os.getenv(env.DATA_DIR),dirname)
        
        files=os.listdir(dirpath)
        result = []
        allowed_filetypes=request.args.get("extensions",None)
        if allowed_filetypes is not None and type(allowed_filetypes)!=str:
            logger.debug("Got unexpected allowed_filetypes",allowed_filetypes)
            return ResponseInvalidArguments("Unexpected value for 'extensions' query param")
        for file in files:
            filepath = os.path.join(dirpath,file)
            if not os.path.isfile(filepath) or (allowed_filetypes and not any(filepath.endswith(ext) for ext in allowed_filetypes.split(','))):
                continue
            ctime = os.path.getctime(filepath)
            #date = datetime.fromtimestamp(mtime)
            #date=date.isoformat()
            #date_formatted=f"{date.year}-{date.month}-{date.day}-{date.hour}-{date.min}-{date.second}-{date.microsecond}"
            meta={"ctime":ctime}
            result.append({"filename":file,"meta":meta})
        
        sortKey = request.args.get("sortby",None)
        sortOrder = request.args.get("orderby","").lower()
        if sortKey=="ctime":
            result = sorted(result,key=lambda d:d["meta"]["ctime"],reverse=(True if sortOrder=="desc" else False))
        return {"files":result},200
    
    @authorize
    def Get(user,filename):
        filename = os.path.basename(filename) # To make sure filename is not relative path
        dirname=user["username"]
        dirpath=os.path.join(os.getenv(env.DATA_DIR),dirname)
        filepath=os.path.join(dirpath,filename)
        if not os.path.isfile(filepath):
            return {"message":"Invalid file"},404
        
        # Check if the Range header is present in the request
        range_header = request.headers.get('Range')
        if range_header:
            print(range_header)
        if range_header:
            return send_partial_file(range_header,filepath)

        try:
            quality = request.args.get("quality",100,type=int)
            if quality>100 or quality<10:
                raise ValueError
        except ValueError:
            return ResponseInvalidArguments("Quality should be integer 10-100")
        if quality!=100:
            try:
                logger.debug(f"Quality: {quality}")
                filepath=compress_image(filepath,quality)
                filename = os.path.basename(filepath)
                dirpath=os.path.join(dirpath,TMP_DIR)
            except:
                pass
        return send_from_directory(dirpath,filename)
    
    @authorize
    def GetThumbnails(user):
        # if not ValidateJSONContentType(request.headers):
        #     return ResponseInvalidContentType
        
        userdirname=user["username"]
        userdirpath=os.path.join(os.getenv(env.DATA_DIR),userdirname)
        thumbnaildirpath = os.path.join(userdirpath,os.getenv(env.THUMBNAIL_DIR))

        
        # Extract list of filenames from request body
        body = request.json
        filenames=body.get("filenames",[])
        result={}
        for filename in filenames:
            filename = os.path.basename(filename) # To make sure filename is not relative path
            filepath = os.path.join(thumbnaildirpath,transform_filename(filename))
            if not os.path.isfile(filepath):
                continue
            data = utils.EncodeFileToBase64(filepath=filepath)
            result[filename]=data
        response = {"thumbnails":result}
        #time.sleep(5)
        return response,200


    
    @authorize
    def Upload(user):
        logger.debug(f"file upload request from {user['username']}")
        dirname=user["username"]
        dirpath=os.path.join(os.getenv(env.DATA_DIR),dirname)
        
    
        if 'files' not in request.files:
            logger.debug("no files received")
            return ({'error': 'No files part in the request'}), 400

        files = request.files.getlist('files')

        if len(files) == 0:
            return ({'error': 'No files selected for uploading'}), 400

        saved_files = []
        for file in files:
            if file.filename == '':
                return ({'error': 'One or more files have no filename'}), 400
            file.filename = os.path.basename(file.filename)
            file_path = os.path.join(dirpath, unquote(file.filename))
            file.save(file_path)
            saved_files.append(file.filename)
        logger.debug("file received")

        return ({'message': 'Files successfully uploaded', 'files': saved_files}), 200


