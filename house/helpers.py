import os, random

def toRupiah(nominal):
	return "Rp.{:,}".format(int(nominal))

def photo_path(instance, filename):
	basefilename, file_extension= os.path.splitext(filename)
	chars= 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
	randomstr= ''.join((random.choice(chars)) for x in range(10))

	return '{folder}/{house_id}-{basename}-{randomstring}{ext}'.format(folder= instance.get_upload_folder(), house_id= instance.house.id, basename= basefilename, randomstring= randomstr, ext= file_extension)
