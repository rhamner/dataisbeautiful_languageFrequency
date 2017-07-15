import praw
import matplotlib.pyplot as plt
import datetime
import numpy as np

reddit = praw.Reddit(client_id='**********',
                     client_secret='**********',
                     password='**********',
                     user_agent='**********',
                     username='**********')

python = 0
excel = 0
matlab = 0
tableau = 0
adobe = 0
javascript = 0
r = 0

numOC = 0					#number of OC posts
numLang = 0					#number of OC posts that specify language
num = 0						#number of posts
textFile = open('C:\Temp\languages.txt', 'w')	#file to dump stats
start=1499990400				#start on July 14th, 2017
while(start > 1436832000):
	stop = start + 86399			#stop at the end of the current day
	for submission in reddit.subreddit('dataisbeautiful').submissions(start, stop):
		num = num + 1
		if(submission.title.find('[OC]') >= 0):
			numOC = numOC + 1
			print(numOC)
			submission.comments.replace_more(limit = 32)	#handle the 'More Comments' problem in reddit
			author = submission.author
			for comment in submission.comments:
				if(comment.author == author):
					try:
						commentText = (comment.body).lower()
						found = 0
						if(commentText.find('python') >= 0):
							python = python + 1							
							textFile.write(str(submission.created) + "\t" + str(submission.score) + "\t" + "python ")
							found = 1
						if(commentText.find('excel') >= 0):
							excel = excel + 1
							textFile.write(str(submission.created) + "\t" + str(submission.score) + "\t" + "excel ")
							found = 1
						if(commentText.find('matlab') >= 0):
							matlab = matlab + 1
							textFile.write(str(submission.created) + "\t" + str(submission.score) + "\t" + "matlab ")
							found = 1
						if(commentText.find('tableau') >= 0):
							tableau = tableau + 1
							textFile.write(str(submission.created) + "\t" + str(submission.score) + "\t" + "tableau ")
							found = 1
						if(commentText.find('adobe') >= 0):
							adobe = adobe + 1
							textFile.write(str(submission.created) + "\t" + str(submission.score) + "\t" + "adobe ")
							found = 1
						if(commentText.find('javascript') >= 0):
							javascript = javascript + 1
							textFile.write(str(submission.created) + "\t" + str(submission.score) + "\t" + "javascript ")
							found = 1
						if((commentText.find(' r,') >= 0) or (commentText.find(' r ') >= 0)):
							r = r + 1
							textFile.write(str(submission.created) + "\t" + str(submission.score) + "\t" + "r ")
							found = 1
						if(found):
							textFile.write("\r\n")
							numLang = numLang + 1
							break
				
					except:
						print('something happened')
		else:
			print('not oc')			
	start = start - 86400			#move to the next day
	print(datetime.datetime.fromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S'))

textFile.close()				#dump data to file

#debug plots
fig = plt.figure(1)
ax = fig.add_subplot(111)
ax.bar(np.arange(7), [100*python/numLang, 100*excel/numLang, 100*tableau/numLang, 100*matlab/numLang, 100*r/numLang, 100*javascript/numLang, 100*adobe/numLang], .75)

# Set the font dictionaries (for plot title and axis titles)
title_font = {'fontname':'Arial', 'size':'30', 'color':'black', 'weight':'normal',
              'verticalalignment':'bottom'} # Bottom vertical alignment for more space
axis_font = {'fontname':'Arial', 'size':'20'}

ax.set_ylabel('%', **axis_font)
ax.set_title('language used in posts that specified language', **title_font)
ax.set_xticks(np.arange(7) + 0.01)
ax.set_xticklabels(['python', 'excel', 'tableau', 'matlab', 'R', 'javascript', 'adobe'])
ax.tick_params(labelsize=16)

fig = plt.figure(2)
ax = fig.add_subplot(111)
ax.bar(np.arange(3), [num, numOC, numLang], .75)

# Set the font dictionaries (for plot title and axis titles)
title_font = {'fontname':'Arial', 'size':'30', 'color':'black', 'weight':'normal',
              'verticalalignment':'bottom'} # Bottom vertical alignment for more space
axis_font = {'fontname':'Arial', 'size':'20'}

ax.set_ylabel('number of posts', **axis_font)
ax.set_title('types of posts', **title_font)
ax.set_xticks(np.arange(3) + 0.01)
ax.set_xticklabels(['total posts', 'OC posts', 'language and OC'])
ax.tick_params(labelsize=16)
plt.show()