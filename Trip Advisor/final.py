from bs4 import BeautifulSoup
from datetime import datetime
from calendar import monthrange
import csv
import glob
    
#generates a list of filenames of .html extension in current dir        
files = glob.glob('*.html')
    
    
titles = ['<---COMMENT TITLE--->','<---COMMENT TEXT--->','<---DATE--->','<---RATINGS--->','<---STAYED TIME--->']
i = 0

#used to create details1.csv,details2.csv and so on
x = 1 

for file in files:
    print(file)
    with open(file,'r+') as f:
        soup = BeautifulSoup(f)
        with open('details'+str(x)+'.csv','w+') as csv_file:
            #incrementing file no.
            x += 1
            writer = csv.writer(csv_file)
            
            #comment title
            writer.writerow([titles[i]])
            comment_title = soup.find('div',attrs={'class':'quote'})
            writer.writerow([comment_title.text.strip()])
            
            #comment text
            writer.writerow([titles[i+1]])
            find_comment = soup.find('span',attrs = {'class':'fullText'})
            writer.writerow([find_comment.text.strip()])
            
            #comment date
            writer.writerow([titles[i+2]])
            find_date = soup.find('span',attrs = {'class':'ratingDate'})
            writer.writerow([find_date.text.strip()])
            #print(find_date.text.strip())
            
            #stayed time
            writer.writerow([titles[i+4]])
            dates = soup.find_all('div',attrs = {'class':'picker-body'})
            #print(dates[0])
            #print(dates[1])
            
            
            if(dates is not None and len(dates) > 0):
                inText = dates[0].text.strip()
                #contains the check-in date
                checkIn = []
                for char in inText:
                    if(char == ','):
                        pass
                    if(char.isalpha()):
                        pass
                    if(char.isnumeric()):
                        checkIn.append(char)
            
                outText = dates[1].text.strip()
                #contains the check-out date
                checkOut = []
                for char in outText:    
                    if(char == ','):
                        pass
                    if(char.isalpha()):
                        pass
                    if(char.isnumeric()):
                        checkOut.append(char)
            
                #converting the lists to int
                checkIn = [int(x) for x in checkIn]
                checkIn = ''.join(map(str,checkIn))
    
                checkOut = [int(x) for x in checkOut]
                checkOut = ''.join(map(str,checkOut))
                #print(checkIn)
           
           
                #checking if same month(if so, then direct difference of each list[:2] will do it)
                #stayed time is in days
                if(checkIn[2:4] == checkOut[2:4]):
                    stayedTime = int(checkOut[:2]) - int(checkIn[:2])
                
                else:  
                    d_in = monthrange((int('20')+int(checkIn[4:])),int(checkIn[2:4]))
                
                    #contains the number of days in the checkin month
                    days_in_month_in = d_in[1] 
                
                    stayedTime = ((days_in_month_in - int(checkIn[:2]) + 1) + (int(checkOut[:2])))
                writer.writerow(['The customer stayed for %d days.'%(stayedTime)])
                