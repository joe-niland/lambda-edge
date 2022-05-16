import json, boto3
from botocore.exceptions import ClientError

def viewerRequest(event, context):
    request = event["Records"][0]["cf"]["request"]
    headers = request["headers"]
    print(request)
    print(headers)

    if request["uri"] == "/view-auth-table":
        auth_record = {'auth_id': 'empty'}

        auth_record = get_item_from_dynamo('truescope.global.user_workspace_data',
                                            'auth0|9069abf5-42cf-4292-9550-31dc2787cfc4',
                                            'auth_id')
        return {
            "status": "200",
            "statusDescription": "OK",
            "headers": {
                "content-type": [{"key": "Content-Type", "value": "application/json"}]
            },
            "body": json.dumps(auth_record),
        }

    return request


def get_item_from_dynamo(table_name, key, key_identifier):
    dynamodb    = boto3.resource('dynamodb')
    table       = dynamodb.Table(table_name)

    try:
        response = table.get_item(Key={
            key_identifier: key
        })
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print(f'get_item dynamo response: {response}')
            if 'Item' in response:
                return response['Item']
        else:
            return None

    except ClientError:
        print (f'Could not get item from {table.name}')
        raise
