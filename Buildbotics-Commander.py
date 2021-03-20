
#Version_0.2
#Kilian Boell
#03.03.2021
import tailer, re
from datetime import datetime
from time import time


new_entry = []
start = 0
end = 0
directory = ""
project = ""
usage_type = "?"
person = "?"

print("CNC-Commander V0.1")

#Get new entry of bbctrl.log
for new_entry in tailer.follow(open('/var/log/bbctrl.log')):
    try:
        if (new_entry[:5] == "USER:"):
            person = re.split(r'\t+', new_entry.rstrip('\t'))[1]
            usage_type = re.split(r'\t+', new_entry.rstrip('\t'))[2]
        elif (new_entry[:25] == "I:Planner:GCode:./upload/"):
            project = new_entry[25:-4]
        elif (new_entry[:21] == 'I:Planner:Program End' or new_entry[:21] == 'I:Planner:Program Sto'):
            #Get the time
            end = datetime.strptime(new_entry[-26:-7],'%Y-%m-%dT%H:%M:%S').timestamp()
            if (start != 0):
                #Calculate difference
                milling_time = round((end - start)/60,1)
                start = 0
                f=open("/home/bbmc/cnc-commander/user.log",'a+')
                #Save Time: type of usage_type / person / milling time / project / Date to user.log
                print(usage_type + "\t" + person + "\t" + str(milling_time).replace(".",",") + "\t" + project + "\t" + datetime.strptime(new_entry[-26:-7],'%Y-%m-%dT%H:%M:%S').isoformat()[0:10])
                f.write(usage_type + "\t" + person + "\t" + str(milling_time).replace(".",",") + "\t" + project + "\t" + datetime.strptime(new_entry[-26:-7],'%Y-%m-%dT%H:%M:%S').isoformat()[0:10] + "\n")
                f.close()
        elif (new_entry[:21] == 'I:Planner:Program Sta'):
            #Get the times
            start = datetime.strptime(new_entry[-26:-7],'%Y-%m-%dT%H:%M:%S').timestamp()
    except Exception as e:
        #f=open("/home/bbmc/cnc-commander/user.log",'a+')
        print(e)
        #f.write(str(e))
        #f.close()



