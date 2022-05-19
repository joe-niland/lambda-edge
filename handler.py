import json, boto3
from botocore.exceptions import ClientError
from decimal import Decimal

def originRequest(event, context):
    request = event["Records"][0]["cf"]["request"]
    headers = request["headers"]
    print(request)
    print(headers)

    if request["uri"] == "/origin-request":
        auth_record = { 'event':   'origin-request',
                        'auth_id': 'empty'}

        auth_record = get_item_from_dynamo('truescope.global.user_workspace_data',
                                            'auth0|9069abf5-42cf-4292-9550-31dc2787cfc4', 'auth_id',
                                            sort_key=8, sort_key_identifier='workspace_id')
        auth_record['event'] = 'origin-request'
        auth_record['headers'] = headers

        return {
            "status": "200",
            "statusDescription": "OK",
            "headers": {
                "content-type": [{"key": "Content-Type", "value": "application/json"}]
            },
            "body": json.dumps(auth_record, cls=DecimalEncoder),
        }

    return request

def viewerRequest(event, context):
    request = event["Records"][0]["cf"]["request"]
    headers = request["headers"]
    print(request)
    print(headers)

    if request["uri"] == "/viewer-request":
        auth_record = { 'event':   'viewer-request',
                        'auth_id': 'empty'}

        auth_record = get_item_from_dynamo('truescope.global.user_workspace_data',
                                            'auth0|9069abf5-42cf-4292-9550-31dc2787cfc4', 'auth_id',
                                            sort_key=8, sort_key_identifier='workspace_id')
        auth_record['event'] = 'viewer-request'
        auth_record['headers'] = headers

        return {
            "status": "200",
            "statusDescription": "OK",
            "headers": {
                "content-type": [{"key": "Content-Type", "value": "application/json"}]
            },
            "body": json.dumps(auth_record, cls=DecimalEncoder),
        }

    return request

def get_item_from_dynamo(table_name, partition_key, partition_key_identifier, sort_key, sort_key_identifier):
    dynamodb    = boto3.resource('dynamodb')
    table       = dynamodb.Table(table_name)

    try:
        response = table.get_item(Key={
            partition_key_identifier: partition_key,
            sort_key_identifier: int(sort_key)
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



class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return str(obj)
    return json.JSONEncoder.default(self, obj)