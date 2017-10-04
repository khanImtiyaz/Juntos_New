from twilio.rest import Client

account = "ACf2a39d5b59da4e7243ecdc6ca821f5cb"
token = "93692a1d46f38de1dd4dc036f79ceae5"
client = Client(account, token)

def send_sms(number,message):
	if number:
		message = client.messages.create(to=str(number), from_="+14157671737",body=message)
	return message



