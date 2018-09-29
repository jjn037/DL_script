# coding: utf-8
import csv, cv2, os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

root = "./idcard"
csv_reader = csv.reader(open("idcard_result(1).csv"))

k = 1
temp = list()
for row in csv_reader:
	# print((row))
	k+=1
	if(k%2):
		temp = ''
		# print("i =: ", i)
		for i in range(1, 9):
			if row[i] != '':
				# temp += 'predict: '+ row[i] + "\n"
				# temp += 'GT: '+ pre[i] + "\n"
				# if(i != 8):
					temp += pre[i] + '\n'
				# else:
				# 	temp += '\n' + row[i] + '\n' + pre[i] + '\n'
			# temp = temp + '\n' + pre
		path = os.path.join(root, row[0])
		img = cv2.imread(path)
		img = cv2.resize(img, (900, 600))
		print(row[0])
		print(temp)
		print("\n")
		# temp = temp.encode('latin-1').decode('unicode_escape')
		imga = cv2.putText(img, temp, (10, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255), 2)
		cv2.imshow('image',imga)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
	else:
		pre = row
		print(row)
	
