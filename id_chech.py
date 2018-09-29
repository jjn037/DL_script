import csv, cv2, os

root = "./bankcard"
csv_reader = csv.reader(open("bankcard-test(1).csv"))

error_file = open('id_error.txt', 'w+')

for row in csv_reader:
     
	path = os.path.join(root, row[0])
	try:
		img = cv2.imread(path)
		img = cv2.resize(img, (1000, 600))

		# if(len(row)<2):
		# 	print("empty", path)
		# 	continue
		# print(row[1])
		print path
		imga = cv2.putText(img, str(row[1]), (10, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255), 2)
		cv2.imshow('image',imga)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
	except:


		print(path)
		error_file.write(path+'\n')
error_file.close()

