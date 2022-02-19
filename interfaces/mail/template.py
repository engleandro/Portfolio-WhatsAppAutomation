"""static method: send_by_html => bool response_status
response = client.send_email(
    Source='string',
    Destination={
        'ToAddresses': [
            'string',
        ],
        'CcAddresses': [
            'string',
        ],
        'BccAddresses': [
            'string',
        ]
    },
    Message={
        'Subject': {
            'Data': 'string',
            'Charset': 'string'
        },
        'Body': {
            'Text': {
                'Data': 'string',
                'Charset': 'string'
            },
            'Html': {
                'Data': 'string',
                'Charset': 'string'
            }
        }
    },
    ReplyToAddresses=[
        'string',
    ],
    ReturnPath='string',
    SourceArn='string',
    ReturnPathArn='string',
    Tags=[
        {
            'Name': 'string',
            'Value': 'string'
        },
    ],
    ConfigurationSetName='string')
"""