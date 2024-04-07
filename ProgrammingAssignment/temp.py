import os

VIDEO_DIR = "videos/"

nfiles = 0
for f in os.listdir(VIDEO_DIR):
    if(f.endswith('mp4')):
        nfiles+=1
  
video_list = [[] for i in range(nfiles//3)]
video_files = [[] for i in range(nfiles//3)]  

for f in os.listdir(VIDEO_DIR):
    if(f.endswith('mp4')):
        print(f)
        i = int(f[5])
        video_files[i-1].append(VIDEO_DIR + f)
        video_list[i-1].append(f)

print(video_files)
print(video_list)