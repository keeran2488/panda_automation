from __future__ import absolute_import, unicode_literals
import string
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from celery import shared_task, current_task
from django.conf import settings

from .models import activation_code
from accounts.models import (
	districtBangladesh,
	)
import pandas as pd
from cryptography.fernet import Fernet
from accounts.code import codeKey

User = get_user_model()
key = codeKey()



@shared_task
def activate_code_update():
	count=0
	countData=0
	countInsert=0
	columns = ['Activation code', 'Date']
	dataCount = pd.read_excel(settings.MEDIA_ROOT + 'activeCode.xls')['Activation code']
	total_user = int(len(dataCount))
	df = pd.read_excel(settings.MEDIA_ROOT + 'activeCode.xls')

	# infoactive = activation_code.objects.values("file").all()
	datafram = pd.DataFrame.from_records(activation_code.objects.values("file").all(),columns=['file'])
	dataframe = pd.DataFrame.from_records(activation_code.objects.values("file").all(),columns=['file'])
	cipher_suite = Fernet(key)
	for i in datafram.index:
		d = cipher_suite.decrypt(datafram["file"][i].encode())
		dataframe["file"][i] = d.decode("utf-8")


	datafram['file2'] = dataframe['file']

	for i in df.index:
		count+=1
		file=df[columns[0]][i]
		
		chekData = datafram[datafram['file2'] == file]
		# chekData = datafram[datafram['file'].index == chekData['file'].index]
		# print(chekData['file'].values[0])
		date=df[columns[1]][i]
		info = activation_code.objects.extra(where=['file=%s'], params=[chekData['file'].values[0]])
		print(info)
		if info :
			info = activation_code.objects.filter(file=chekData['file'].values[0]).update(check=True,active_check=True,active_date=date)
			if info:
				countData+=1
		else:
			countInsert+=1

			
		current_task.update_state(state='PROGRESS',
                                  meta={'current': countData, 'total': int(total_user),
                                        'percent': int((float(count) / int(total_user)) * 100)})
		uid_sales = ""
		uid_customer = ""

	return {'current': countData, 'total': total_user, 'percent': 100}


@shared_task
def activation_code_insert(product_name,product_number):
	count=0
	countData=0
	countInsert=0
	# dataCount = pd.read_csv(settings.MEDIA_ROOT + 'code.txt',header=None)
	# total_user = int(dataCount[0].count())
	# data = pd.read_csv(settings.MEDIA_ROOT + 'code.txt',index_col=0,header=None)
	for x in range(product_number):
		count+=1
		flag = 0
		info = False
		result_sales = ""

		while flag == 0:
			uid_sales 	 = get_random_string(length=int(9), allowed_chars='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
			result_sales = '%s-%s' % ("REN0"+product_name[0], uid_sales)
			# seles 		 = activation_code.objects.extra(where=['sales_code=%s'], params=[result_sales])

			cipher_suite = Fernet(key)
			result_sales = cipher_suite.encrypt(result_sales.encode())
			info = activation_code.objects.extra(where=['file=%s'], params=[result_sales.decode("utf-8")])


			if info:
				flag = 0
			else:
				flag = 1
		product = districtBangladesh.objects.only('id').get(id=product_name[0])
		if info :
			countData+=1

		else:
			flag = 0
			flag2 = 0
			countInsert+=1
			activation_code.objects.create(product_type=product,file=result_sales.decode("utf-8"))
		
		current_task.update_state(state='PROGRESS',
                                  meta={'current': countInsert, 'total': int(product_number),
                                        'percent': int((float(count) / int(product_number)) * 100)})
		uid_sales = ""
		uid_customer = ""

	return {'current': countInsert, 'total': product_number, 'percent': 100}
