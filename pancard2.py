#importing necessary packages
from skimage.metrics import structural_similarity
import imutils
import cv2
from PIL import Image
import requests


#scraping original and tampered pancards from different sources
#original = Image.open(requests.get('https://www.thestatesman.com/wp-content/uploads/2019/07/pan-card.jpg', stream=True).raw)
#tampered = Image.open(requests.get('https://assets1.cleartax-cdn.com/s/img/20170526124335/Pan4.png', stream=True).raw)
pancard1 = cv2.imread("D:/pancard1.png")
pancard2 = cv2.imread("D:/pancard2.png")

pancard1_gray = cv2.cvtColor(pancard1, cv2.COLOR_BGR2GRAY)
pancard2_gray = cv2.cvtColor(pancard2, cv2.COLOR_BGR2GRAY)

#the file format of source file
#print("pancard1 image format:", pancard1.format)
#print("pancard2 image format:", pancard2.format)
#print("pancard1 image size :", pancard1.size)
#print("pancard2 image size :", pancard2.size)

#resize image
pancard1 = pancard1.resize((250, 160))
#print("pancard1 image size:",pancard1.size)
pancard1.save('D:pan1.png')
pancard2 = pancard2.resize((250, 160))
#print("pancard2 image size",pancard2.size)
pancard2.save('D:/pan2.png')

#change image type if required from png to jpg
#pancard2 = Image.open('C:/pan_card_tampering/image/pancard2.png')
#pancard2.save('C:/pan_card_tampering/image/pancard2.png')

#reading images using opencv
#pancard1 = cv2.imread("C:/pan_card_tampering/image/pancard1.png")
#pancard2 = cv2.imread("C:/pan_card_tampering/image/pancard2.png")
#convert images to grayscale
#pancard1_gray = cv2.cvtColor(pancard1, cv2.COLOR_BGR2GRAY)
#pancard2_gray = cv2.cvtColor(pancard2, cv2.COLOR_BGR2GRAY)

#applying structural similarity index
(score, diff) = structural_similarity(pancard1_gray, pancard2_gray, full=True)
diff = (diff*255).astype("uint8")
print("SSIM Score is:{}".format(score*100))
if score >= 80:
    print("The given pan card is original")
else:
    print("the given pan card is tampered")

#calculating threshold and contours
thresh= cv2.threshold(diff,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cnts= cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts= imutils.grab_contours(cnts)
#creating bounding boxes(contours)
for c in cnts:
    #applying contours on images
    (x, y, w, h)=cv2.boundingRect(c)
    cv2.rectangle(original, (x, y), (x + w, y + h), (0, 0, 255),6)
    cv2.rectangle(tampered, (x, y), (x + w, y + h), (0, 0, 255),6)
#display original image with contours
print("pancard1 image")
original_contour=Image.fromarray(pancard1)
original_contour.save("C:/pan_card_tampering/image/pancard1_contour_image.png")
original_contour
#display tamperred image with contour
print("pancard2 image")
tampered_contour=Image.fromarray(pancard2)
tampered_contour.save("C:/pan_card_tampering/image/tampered_contour_image.png")
tampered_contour

#display difference image with black
print("different image")
difference_image = Image.fromarray(diff)
difference_image.save('C:/pan_card_tampering/image/difference_image.png')
difference_image

#dispaly threshold image with white
print('Threshold Image')
threshold_image = Image.fromarray(thresh)
threshold_image.save('C:/pan_card_tampering/image/threshold_image.png')
