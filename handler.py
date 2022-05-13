import json


def viewerRequest(event, context):
    request = event["Records"][0]["cf"]["request"]
    headers = request["headers"]
    print(request)
    print(headers)

    if request["uri"] == "/dump-viewer-request-event":
        return {
            "status": "200",
            "statusDescription": "OK",
            "headers": {
                "content-type": [{"key": "Content-Type", "value": "application/json"}]
            },
            "body": json.dumps(event),
        }

    return request
