import glob, os, shutil


s_path = '/Users/didi/Desktop/pop-up/s5'
i=19145
for video_path in glob.glob(os.path.join(s_path, '*')):
    # print(video_path.split('/')[-1])
    # if video_path.split('/')[-1] not in s5:
    #     print(video_path)
    fpath, fname = os.path.split(video_path)
    # t = fname.split('.')
    print()
    # i+=1
    # print("video_path", fname)
    if "png" in fname:
    	new_name = fpath + '/' + "%05d"%(i) + ".png"
    else:
    	new_name = fpath + '/' + "%05d"%(i) + ".jpg"
    print("new_name", new_name)
    os.rename(video_path, new_name)
    # print (new_name)
    i+=1
