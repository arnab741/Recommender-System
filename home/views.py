from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import mobiles,mobilesAmazon,mobilesFlipkart,mobilesSnapdeal
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.naive_bayes import GaussianNB

# Create your views here.

def scrape_amazon(search_term):
	headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
	search_term="+".join(search_term.split(" "))
	website="https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords="+search_term+"&&qid=1700000000&sr=8-1"+"&keywords="+search_term

	code=0
	while code!=200:
	    page=requests.get(website,headers)
	    code=page.status_code
	    

	bs_page=BeautifulSoup(page.text,"lxml")

	products=bs_page.select('a.a-link-normal.s-access-detail-page.s-color-twister-title-link.a-text-normal')
	first_link=products[0].get("href")

	detail_page=requests.get(first_link)

	bs_detail_page=BeautifulSoup(detail_page.text,"lxml")
	name=bs_detail_page.find('span',{'id':'productTitle'}).text
	name=name.strip()

	rating=bs_detail_page.find('span',{'id':"acrPopover"}).get("title")
	review=bs_detail_page.find('span',{'id':"acrCustomerReviewText"}).text

	ans=bs_detail_page.select("a.askATFLink")[0].findChild().text.strip()
	price=bs_detail_page.find('span',{'id':"priceblock_ourprice"}).text.strip()
	delivery=bs_detail_page.find('span',{'id':"ourprice_shippingmessage"}).findChild().findChild().text.strip()

	html_description=str(bs_detail_page.find('div',{'class':"pdTab"}))

	star5=bs_detail_page.find('div',{'class':"a-meter 5star"}).get('aria-label')
	star4=bs_detail_page.find('div',{'class':"a-meter 4star"}).get('aria-label')
	star3=bs_detail_page.find('div',{'class':"a-meter 3star"}).get('aria-label')
	star2=bs_detail_page.find('div',{'class':"a-meter 2star"}).get('aria-label')
	star1=bs_detail_page.find('div',{'class':"a-meter 1star"}).get('aria-label')


	response={'name':name,'rating':rating,'review':review,'answers':ans,
	          'price':price,'delivery':delivery,'html_description':html_description,
	          'star5':star5,'star4':star4,'star3':star3,'star2':star2,
	          'star1':star1}

	print(response)
	return(response)



def show(request,search):
	amazon=scrape_amazon(search)
	return render(request,"compare.html",amazon)

def home(request):
	return render(request,template_name="home/index.html")


def classify_comments(comments):
	from sklearn.feature_extraction.text import CountVectorizer
	cv = CountVectorizer(max_features = 1500)
	X = cv.fit_transform(corpus).toarray()
	y = dataset.iloc[:, 1].values
	
	classifier = GaussianNB()
	classifier.fit(X, y)

	y_pred = classifier.predict(sen)
	print(y_pred)




	pos=0
	neg=0
	for i in comments:
		review = re.sub('[^a-zA-Z]', ' ', i)
		review = review.lower()
		review = review.split()
		ps = PorterStemmer()
		review = [ps.stem(word) for word in review]
		review = ' '.join(review)
		sen=cv.transform([review]).toarray()
		y_pred=classifier.predict(sen)
		if y_pred[0]==1:
			pos=pos+1
		else:
			neg=neg+1

	return pos,neg



def proba_order(amazon,flipkart,snapdeal):
	coef_=np.array([1.20034,70.3456,-0.005,-21.9594,4.5,3.0,1.00023,-2.87951,-4.45567])
	score_amazon=np.sum(coef_*amazon)
	score_flipkart=np.sum(coef_*flipkart)
	score_snapdeal=np.sum(coef_*snapdeal)
	s=score_amazon+score_flipkart+score_snapdeal
	print(s)
	score_array=np.array([score_amazon/s,score_flipkart/s,score_snapdeal/s])
	return score_array







def showdata(request):

	search=request.POST['search']
	mobile=mobiles.objects.filter(name=search)

	if len(mobile):
		mobile=mobile[0]
		mobile_name=mobile.name
		mobile_image=mobile.image
		amazon=mobilesAmazon.objects.filter(mobile=mobile)[0]
		flipkart=mobilesFlipkart.objects.filter(mobile=mobile)[0]
		snapdeal=mobilesSnapdeal.objects.filter(mobile=mobile)[0]
		amazon_data=np.array([amazon.price,amazon.delivery,amazon.review_no,amazon.rating,amazon.star1,amazon.star2,amazon.star3,amazon.star4,amazon.star5])
		flipkart_data=np.array([flipkart.price,flipkart.delivery,flipkart.review_no,flipkart.rating,flipkart.star1,flipkart.star2,flipkart.star3,flipkart.star4,flipkart.star5])
		snapdeal_data=np.array([snapdeal.price,snapdeal.delivery,snapdeal.review_no,snapdeal.rating,snapdeal.star1,snapdeal.star2,snapdeal.star3,snapdeal.star4,snapdeal.star5])
		order=proba_order(amazon_data,flipkart_data,snapdeal_data)
		print(order)
		order=np.argsort(order)
		order=list(order)
		order_1=order.index(0)+1
		order_2=order.index(1)+1
		order_3=order.index(2)+1
		context={'amazon':amazon,'flipkart':flipkart,'snapdeal':snapdeal,'mobile':mobile,'order_1':order_1,'order_2':order_2,'order_3':order_3}
		print(context)
	else:
		context={'mobile.name':'No Mobile Found'}


	return render(request,"showdata.html",context)
