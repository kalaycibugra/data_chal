import datetime
import os
import random
import operator
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt

def random_date(start_date,end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days+1
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date

def precision_calculate(df,label,num):
    tp=len(df.query("Correct_Answer_{}_Label == '{}' and Rater_Answer_{}_Label == '{}'".format(num,label,num,label)))
    fp=len(df.query("Correct_Answer_{}_Label != '{}' and Rater_Answer_{}_Label == '{}'".format(num,label,num,label)))
    return tp/(tp+fp)

def recall_calculate(df,label,num):
    tp=len(df.query("Correct_Answer_{}_Label == '{}' and Rater_Answer_{}_Label == '{}'".format(num,label,num,label)))
    fn=len(df.query("Correct_Answer_{}_Label == '{}' and Rater_Answer_{}_Label != '{}'".format(num,label,num,label)))
    return tp/(tp+fn)

##############################################################################################
class obj:
    def __init__(self, task_id,date, rater,cor_a_3,cor_a_5,rate_a_3,rate_a_5,agreement_3=None,agreement_5=None):
        self.task_id=task_id
        self.date=date
        self.rater=rater
        self.cor_a_3=cor_a_3
        self.cor_a_5=cor_a_5
        self.rate_a_3=rate_a_3
        self.rate_a_5=rate_a_5
        self.agreement_3=None
        self.agreement_5=None
    def print_obj(self):
        print ("Task ID : ",self.task_id)
        print ("Date : ",self.date)
        print ("Rater : ",self.rater)
        print ("Correct Answer 3 : ",self.cor_a_3)
        print ("Correct Answer 5 : ",self.cor_a_5)
        print ("Rater Answer 3 : ",self.rate_a_3)
        print ("Rater Answer 5 : ",self.rate_a_5)
        print ("Agreement_3 : ",self.agreement_3)
        print ("Agreement_5 : ",self.agreement_5)

##############################################################################################
rater_a=["A", "B", "C", "D", "E"]
cor_a_3=["Low","Average","High"]
cor_a_5=["Bad", "Okay", "Intermediate", "Great","Exceptional"]
rate_a_3=["Low","Average","High"]
rate_a_5=["Bad", "Okay", "Intermediate", "Great","Exceptional"]
array=[]
start=datetime.date(2005, 10, 1)
end=datetime.date(2005, 10, 30)

##############################################################################################

for i in range(0,10000):
    
    date1=random_date(start,end)
    rat=random.choice(rater_a)
    c1=random.choice(cor_a_3)
    c2=random.choice(cor_a_5)
    r1=random.choice(rate_a_3)
    r2=random.choice(rate_a_5)
    task=i
    ob1=obj(task,date1,rat,c1,c2,r1,r2)
    array.append(ob1)

##############################################################################################
for i in array:
    if i.cor_a_3==i.rate_a_3:
        i.agreement_3=True 
    else :
        i.agreement_3=False
    if i.cor_a_5==i.rate_a_5: 
        i.agreement_5=True 
    else :
        i.agreement_5=False

##############################################################################################
task_ids=[]
dates=[]
raters=[]
cor3s=[]
cor5s=[]
rat3s=[]
rat5s=[]
ag3s=[]
ag5s=[]
for i in array:
    task_ids.append(i.task_id)
    dates.append(i.date)
    raters.append(i.rater)
    cor3s.append(i.cor_a_3)
    cor5s.append(i.cor_a_5)
    rat3s.append(i.rate_a_3)
    rat5s.append(i.rate_a_5)
    ag3s.append(i.agreement_3)
    ag5s.append(i.agreement_5)
data={'Task id':task_ids,
    'Date':dates,'Rater':raters,'Correct_Answer_3_Label':cor3s,
    'Correct_Answer_5_Label':cor5s,'Rater_Answer_3_Label':rat3s,
    'Rater_Answer_5_Label':rat5s,'Agreement_3':ag3s,'Agreement_5':ag5s}
df = pd.DataFrame.from_dict(data)

##############################################################################################



##############################################################################################
print("------------------------------------------------------------------------------------------")
print("What is the agreement rate between the engineer and all the raters for each day?")
print("------------------------------------------------------------------------------------------")
print("\n")    
weeks={}
temp=[]
delta = datetime.timedelta(days=1)
count=0
week_count=1
day_dict={}
while start<= end:
    sub4=df[df["Date"]==start]
    a=sub4[sub4["Agreement_3"]==True]
    b=sub4[sub4["Agreement_5"]==True]
    c=(a.count()[1]+b.count()[1])
    e=sub4.count()[1]
    print(start,":",c/(e*2))
    day_dict[start]=c/(e*2)
    temp.append(start)
    start += delta
    count+=1
    if count%7==0:
        weeks[week_count]=temp
        temp=[]
        week_count+=1
    
weeks[week_count]=temp
print("\n")

#-----------------------------------Plotting -----------------------------------

x,y = zip(*sorted(day_dict.items()))
plt.title("rate between the engineer and all the raters for each day")
plt.plot(x,y)
plt.show()

##############################################################################################    
print("------------------------------------------------------------------------------------------")
print("What is the agreement rate between the engineer and all the raters for each week?")
print("------------------------------------------------------------------------------------------")
print("\n")

week_dict={}
for i in weeks:
    total_true=0
    total=0
    frames=[]
    for k in weeks[i]:
        frames.append(df[df["Date"]==k])
    res=pd.concat(frames)
    a=res[res["Agreement_3"]==True]
    b=res[res["Agreement_5"]==True]
    c=(a.count()[1]+b.count()[1])
    print("Week",i,":",c/(len(res)*2))
    week_dict["Week {}".format(i)]=c/(len(res)*2)
    print("\n")    

#-----------------------------------Plotting -----------------------------------

x,y = zip(*sorted(week_dict.items()))
plt.title("rate between the engineer and all the raters for each week")
plt.plot(x,y)
plt.show()

##############################################################################################
dic1={}
dic2={}

for i in rater_a:
    sub5=df[df["Rater"]==i]
    a=sub5[sub5["Agreement_3"]==True]
    b=sub5[sub5["Agreement_5"]==True]
    c=(a.count()[1])
    d=(b.count()[1])
    e=sub5.count()[1]
    dic1[i]=c/e
    dic2[i]=d/e
print("------------------------------------------------------------------------------------------")
print("Identify raters that have the highest agreement rates with the engineer.")
print("------------------------------------------------------------------------------------------")
print("\n")    
max_value1=max(dic1.values()) 
max_keys1 = [k for k, v in dic1.items() if v == max_value1]
max_value2=max(dic2.values()) 
max_keys2 = [k for k, v in dic2.items() if v == max_value2]

print("For aggreement 3 :",max_keys1[0])
print("For aggreement 5 :",max_keys2[0])

print("\n")

##############################################################################################
print("------------------------------------------------------------------------------------------")
print("Identify raters that have the lowest agreement rates with the engineer.")
print("------------------------------------------------------------------------------------------")
print("\n")
min_value1=min(dic1.values()) 
min_keys1 = [k for k, v in dic1.items() if v == min_value1]
min_value2=min(dic2.values()) 
min_keys2 = [k for k, v in dic2.items() if v == min_value2]
print("For aggreement 3 :",min_keys1[0])
print("For aggreement 5 :",min_keys2[0])

#-----------------------------------Plotting -----------------------------------

x,y = zip(*sorted(dic1.items()))
plt.title("Raters agreement 3 rates")
plt.plot(x,y)
plt.show()
x,y = zip(*sorted(dic2.items()))
plt.title("Raters agreement 5 rates")
plt.plot(x,y)
plt.show()

##############################################################################################

print("\n")    
print("------------------------------------------------------------------------------------------")
print("Identify raters that have completed the most Task IDs.")
print("------------------------------------------------------------------------------------------")
print("\n")    
maxo=df['Rater'].value_counts().idxmax()
print(maxo," :",df['Rater'].value_counts().max())

##############################################################################################

print("\n")    
print("------------------------------------------------------------------------------------------")
print("Identify raters that have completed the least Task IDs.")
print("------------------------------------------------------------------------------------------")
print("\n")    
mino=df['Rater'].value_counts().idxmin()
print(mino," :",df['Rater'].value_counts().min())
print("\n")

#-----------------------------------Plotting -----------------------------------
s=df['Rater'].value_counts()
s.plot(kind='bar')
plt.title("Raters/Total tasks")
plt.show()

##############################################################################################
print("--------------------------------------------------------------------------------------------------")
print("What is the precision for each of the 3 labels? and What is the recall for each of the 3 labels?")
print("--------------------------------------------------------------------------------------------------")
this_dict1={}
this_dict2={}
for i in rate_a_3:
    print("Precision for {} : ".format(i),precision_calculate(df,i,len(rate_a_3)))

    print("Recall for {} : ".format(i),recall_calculate(df,i,len(rate_a_3)))

    this_dict1[i]=precision_calculate(df,i,len(rate_a_3))
    this_dict2[i]=recall_calculate(df,i,len(rate_a_3))
    print("\n")

#-----------------------------------Plotting -----------------------------------

plt.bar(range(len(this_dict1)), list(this_dict1.values()), align='center')
plt.xticks(range(len(this_dict1)), list(this_dict1.keys()))
plt.title("Precision for each 3 labels")
plt.show()
plt.bar(range(len(this_dict2)), list(this_dict2.values()), align='center')
plt.xticks(range(len(this_dict2)), list(this_dict2.keys()))
plt.title("Recall for each 3 labels")
plt.show()

##############################################################################################
print("--------------------------------------------------------------------------------------------------")
print("What is the precision for each of the 5 labels? and What is the recall for each of the 5 labels?")
print("--------------------------------------------------------------------------------------------------")
this_dict1={}
this_dict2={}
for i in rate_a_5:
    print("Precision for {} : ".format(i),precision_calculate(df,i,len(rate_a_5)))
    print("Recall for {} : ".format(i),recall_calculate(df,i,len(rate_a_5)))
    print("\n")
    this_dict1[i]=precision_calculate(df,i,len(rate_a_5))
    this_dict2[i]=recall_calculate(df,i,len(rate_a_5))

#-----------------------------------Plotting -----------------------------------

plt.bar(range(len(this_dict1)), list(this_dict1.values()), align='center')
plt.xticks(range(len(this_dict1)), list(this_dict1.keys()))
plt.title("Precision for each 5 labels")
plt.show()
plt.bar(range(len(this_dict2)), list(this_dict2.values()), align='center')
plt.xticks(range(len(this_dict2)), list(this_dict2.keys()))
plt.title("Recall for each 5 labels")
plt.show()
##############################################################################################
print("------------------------------------------------------------------------------------------------------")
print("""What is the overall agreement rate considering that the raters have to be in agreement with both the
engineer's 3-label answer and the engineer's 5-label answer.""")
print("------------------------------------------------------------------------------------------------------")
print("")    

sub=df[df["Agreement_3"]==True]
sub2=df[df["Agreement_5"]==True]
print((sub.count()[1]+sub2.count()[1])/20000)
##############################################################################################

