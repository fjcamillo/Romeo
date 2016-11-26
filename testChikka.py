import requests

payload = {
"message_type":"SEND",
"mobile_number":"639071878493",
"shortcode": "292901343",
"message_id":"34abc5de11209b",
"message": "Hi Rommel",
"client_id": "2b9be5d5c8ed8cc0f82e1a50605e895b86185f4e3be995f55bd5830bd12cd18c",
"secret_key": "f36247fb05d604a38294aa369d69cdb6e37e299e90080d642d9d489149b4e556"
}

r = requests.post("https://post.chikka.com/smsapi/request", data=payload)
response = r.json()
print response
