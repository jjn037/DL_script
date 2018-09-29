import cv2

image=cv2.imread('hs.jpg')
res=cv2.resize(image,(77, 88),interpolation=cv2.INTER_CUBIC)
cv2.imshow('iker',res)
cv2.imshow('image',image)
cv2.imwrite('litt.jpg', res)
cv2.waitKey(0)
cv2.destoryAllWindows()