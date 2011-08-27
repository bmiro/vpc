# -*- coding: utf-8 -*-

from opencv.cv import *
from opencv.highgui import *

threshold = 180 
maxValue = 255 

codiBarres = "codis/Image11.jpg"
rutaPatrons = "patrons/"
patrons = ["0.bmp", "1.bmp", "2.bmp", "3.bmp", "4.bmp", "5.bmp", "6.bmp", "7.bmp", "8.bmp", "9.bmp"]

def cercaContorns(img):

	img_aux = cvCreateImage(cvGetSize(img), IPL_DEPTH_8U, 1)
	mem = cvCreateMemStorage(0)

	cvCopy(img, img_aux)
	n, contours = cvFindContours(img_aux, mem, sizeof_CvContour, CV_RETR_CCOMP, CV_CHAIN_APPROX_SIMPLE, cvPoint (0,0)) 

	return contours

def trataContorns(contours): 
	
	numeros = []
	for c in contours.hrange():
		rect = cvBoundingRect(c, 0)
			
		#TODO Mirar si tenim una imatge mes grosa o una de mes petita es necesari
 		#cercar el ratio

		#si no te el tamany d'un numero no lo cojemos
		if (rect.width > 7 and rect.width < 20 and rect.height > 20 and rect.height < 30):				
			numeros.append(c)	

	#ordenam els numeros trobats aixi com estan a la imagen original
	numeros.sort(comp)

	return numeros

def comp(c1, c2):
	rect_c1 = cvBoundingRect(c1, 0)
	rect_c2 = cvBoundingRect(c2, 0)

	if (rect_c1.x < rect_c2.x): 
		return -1 
	elif (rect_c1.x > rect_c2.x): 
		return 1
	else:
		return 0	

def cercaNumero(img, num): 

	rect = cvBoundingRect(num, 0)

	numCodi = cvCreateImage(cvSize(rect.width, rect.height), IPL_DEPTH_8U, 1)
	numCodi = cvGetSubRect(img, rect)	

	puntuacio = 100000
	for a in range(len(patrons)):
		
		imgNumCodi = cvCreateImage(cvGetSize(imgPatro[a]), IPL_DEPTH_8U,1)
		
		#es redimensiona la imatge perque tengui el mateix tamany que el patro
		cvResize(numCodi, imgNumCodi)
		
		cvXor(imgPatro[a], imgNumCodi, imgNumCodi)
		
		tam = cvGetSize(imgNumCodi)	
		p = float(cvCountNonZero(imgNumCodi)) / float(tam.height*tam.width) 
	
		if p < puntuacio:
			puntuacio = p
			num = a 

	return num

if __name__ == '__main__':
	
	font = cvInitFont(CV_FONT_HERSHEY_SIMPLEX, 1.0, 1.0, 0, 1, CV_AA)	

	#carregam el codigo de barres i el pasam a binari
	img = cvLoadImage(codiBarres, 0)		
	cvShowImage("Codi de barres", img)
	
	imgResultat = cvCreateImage(cvSize(img.width, 50), IPL_DEPTH_8U, 3)
	
	cvAddS(img, cvScalarAll(25), img)
	cvThreshold(img, img, threshold, maxValue, CV_THRESH_BINARY_INV)    

	#carregam els patrons i els pasam a binari 
	imgPatro = []
	i = 0
	for p in patrons: 
		imgPatro.append(cvLoadImage(rutaPatrons + p, 0))
		cvThreshold(imgPatro[i], imgPatro[i], threshold, maxValue, CV_THRESH_BINARY_INV)
		i += 1

	#cercam els contorns que te la imatge original
	contours = cercaContorns(img)		

	#agafam els contorns que tenen aspecte de numero
	numeros = trataContorns(contours)

	#per cada numero trobat, el comparam amb els patrons 
	#i agafam el mes parescut
	punt = cvPoint(45, 35)
	for i in range(len(numeros)):
		num = cercaNumero(img, numeros[i])
		cvPutText(imgResultat, str(num), punt, font, CV_RGB(255, 255, 255))
		punt.x += 20
		
	cvShowImage("Resultat", imgResultat)

	key = -1
	while key == -1:

		key = cvWaitKey(10)


