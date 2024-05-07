def toRupiah(nominal):
	return "Rp. {:,}".format(int(nominal))

def resize_image(image):
	import sys
	from PIL import Image
	from io import BytesIO
	from django.core.files.uploadedfile import InMemoryUploadedFile

	im = Image.open(image)
	basewidth = 200
	wpercent = basewidth/float(im.size[0])
	hsize = im.size[1]*wpercent
	size_f = (basewidth, int(hsize))
	im = im.resize(size_f, Image.NEAREST)
	im = im.convert('RGB')

	output = BytesIO()
	im.save(fp=output, format='JPEG', quality=90)

	return InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)
