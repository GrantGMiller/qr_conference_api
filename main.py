'''
First you will need to setup an account and add a service account and room.
The use the API KEY found on this page: https://qr-room.grant-miller.com/settings in your request body

'''

import requests
import config

# HOST_URL = 'http://192.168.68.105:5000/'
HOST_URL = 'https://qr-room.grant-miller.com/'

s = requests.session()

# Get all the rooms for your account
resp = s.get(
    url='{}/api/get_rooms'.format(HOST_URL),
    data={'apiKey': config.APIKEY},  # get your API key from https://qr-room.grant-miller.com/settings
)
print('resp.text=', resp.text)
print('resp.json=', resp.json())

rooms = resp.json()

# Get the "book now" url for each room
# opening this url will ask the user to login with their Microsoft account and then book the room
# some URLs are one-time-use only, as indicated by the room['dynamicQR'] property
for room in rooms:
    resp = s.get(
        url='{}api/get_book_now_url'.format(HOST_URL),
        data={
            'apiKey': config.APIKEY,  # get your API key from https://qr-room.grant-miller.com/settings
            'roomID': room['id'],
        },
    )

    url = resp.json()
    print('room=', room, ', url=', url)

# Get the "book now" QR code for each room, save it to a file
# opening this QR/url will ask the user to login with their Microsoft account and then book the room
# some QRs are one-time-use only. This is indicated by the room['dynamicQR'] property
for room in rooms:
    resp = s.get(
        url='{}api/get_book_now_qr'.format(HOST_URL),
        data={
            'apiKey': config.APIKEY,  # get your API key from https://qr-room.grant-miller.com/settings
            'roomID': room['id'],
        },
    )
    with open(f'qr_{room["email"]}.png', mode='wb') as file:
        file.write(resp.content)
