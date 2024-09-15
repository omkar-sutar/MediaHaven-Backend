ResponseUnauthorized = {"message":"User unauthorized"},401
#ResponseInvalidArguments = {"message":"Invalid arguments"},400
ResponseInvalidContentType = {"message":"Invalid Content-Type"},400

ContentTypeHeader = "Content-Type"
ContentTypeJSON = "application/json"

def ValidateJSONContentType(headers: dict):
    if headers.get(ContentTypeHeader,"")!=ContentTypeJSON:
        return False
    return True


def ResponseInvalidArguments(message):
    return {"message":f'Invalid arguments: {message}'},400