import pandas as pd
from .models import activation_code
from cryptography.fernet import Fernet
import qrcode
from PIL import Image
import os
from django.conf import settings
import numpy as np
from io import BytesIO

def codeKey():
	key = b'RM3fYkFQIJQXuLsqGtY_cUGCgjRBQqKARQwB95wh08c='
	return key


def chekDatafram(key):
	datafram = pd.DataFrame.from_records(activation_code.objects.values("file").all(),columns=['file'])
	dataframe = pd.DataFrame.from_records(activation_code.objects.values("file").all(),columns=['file'])
	cipher_suite = Fernet(key)
	for i in datafram.index:
		d = cipher_suite.decrypt(datafram["file"][i].encode())
		dataframe["file"][i] = d.decode("utf-8")
	datafram['file2'] = dataframe['file']

	return datafram


def dataWrap(row,col_num,key):
	
	if col_num == 0:
		cipher_suite = Fernet(key)
		dataActive = cipher_suite.decrypt(row[col_num].encode())
		data = dataActive.decode("utf-8")
		return data
	elif col_num == 2:
		cipher_suite = Fernet(key)
		dataActive = cipher_suite.decrypt(row[0].encode())
		data = dataActive.decode("utf-8")
		qr = qrcode.QRCode(
		    version = 1,
		    error_correction = qrcode.constants.ERROR_CORRECT_H,
		    box_size = 4,
		    border = 4,
		)
		qr.add_data(data)
		qr.make(fit=True)
		img = qr.make_image()
		img = img.convert('RGB')
		# r, g, b = img.getpixel((1, 1))
		# color = (r,g,b)
		# im = Image.new("RGB", img.size, color)
		# g = image_parts[1]
		r, g, b = img.split()
		img = Image.merge("RGB", (r, g, b))
		img.save(settings.MEDIA_ROOT+"image.bmp")
		return settings.MEDIA_ROOT+"image.bmp"
	else:
		return row[col_num]