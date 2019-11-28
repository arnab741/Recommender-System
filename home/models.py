from django.db import models

# Create your models here.


class mobiles(models.Model):
	name=models.TextField()
	graph=models.ImageField(upload_to="graph_image",blank=True)
	image=models.ImageField(upload_to="mobile_image",blank=True)

	def __str__(self):
		return str(self.name)

class mobilesAmazon(models.Model):
	mobile=models.ForeignKey('mobiles',on_delete=models.CASCADE,related_name='amazon')
	price=models.IntegerField(default=0)
	review_no=models.IntegerField(default=0)
	rating=models.FloatField(default=0)
	delivery=models.IntegerField(default=0)
	star1=models.IntegerField(default=0)
	star2=models.IntegerField(default=0)
	star3=models.IntegerField(default=0)
	star4=models.IntegerField(default=0)
	star5=models.IntegerField(default=0)
	week_p=models.IntegerField(default=0)
	month_p=models.IntegerField(default=0)
	comments=models.TextField(blank=True)
	
	def __str__(self):
		return str(self.mobile.name)



class mobilesFlipkart(models.Model):
	mobile=models.ForeignKey('mobiles',on_delete=models.CASCADE,related_name='flipkart')
	price=models.IntegerField(default=0)
	review_no=models.IntegerField(default=0)
	rating=models.FloatField(default=0)
	delivery=models.IntegerField(default=0)
	star1=models.IntegerField(default=0)
	star2=models.IntegerField(default=0)
	star3=models.IntegerField(default=0)
	star4=models.IntegerField(default=0)
	star5=models.IntegerField(default=0)
	week_p=models.IntegerField(default=0)
	month_p=models.IntegerField(default=0)
	comments=models.TextField(blank=True)

	def __str__(self):
		return str(self.mobile.name)



class mobilesSnapdeal(models.Model):
	mobile=models.ForeignKey('mobiles',on_delete=models.CASCADE,related_name='snapdeal')
	price=models.IntegerField(default=0)
	review_no=models.IntegerField(default=0)
	rating=models.FloatField(default=0)
	delivery=models.IntegerField(default=0)
	star1=models.IntegerField(default=0)
	star2=models.IntegerField(default=0)
	star3=models.IntegerField(default=0)
	star4=models.IntegerField(default=0)
	star5=models.IntegerField(default=0)
	week_p=models.IntegerField(default=0)
	month_p=models.IntegerField(default=0)
	comments=models.TextField(blank=True)

	def __str__(self):
		return str(self.mobile.name)






