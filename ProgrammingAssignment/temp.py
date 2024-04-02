import cv2
videos = ["videos/240p.mp4","videos/720p.mp4","videos/1080p.mp4"]

for video_file in videos:
    vid = cv2.VideoCapture(video_file)

    print(int(vid.get(cv2.CAP_PROP_FRAME_COUNT)))
    
    # ret, frame = vid.read()
    
    # print(ret)
    # print(frame)
    vid.release()