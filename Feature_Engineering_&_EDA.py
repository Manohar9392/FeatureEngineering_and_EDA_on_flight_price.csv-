import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandas.core.computation.ops import isnumeric

from sklearn.preprocessing import OneHotEncoder
# tips=sns.load_dataset("tips")
# # print(tips)
# # print(tips.info())
# sns.heatmap(tips.corr())
# plt.show()

df=pd.read_excel("C:/Udemy_GenAi/Python/EDA_with_red_wine_data/a1_FlightFare_Dataset.xlsx")
# print(df.info())
# print(df.shape)
df.drop_duplicates(inplace=True)
df['Total_Stops']=df['Total_Stops'].replace(np.nan,'0')  #removing null vals

# print(df.head())
df['day']=df['Date_of_Journey'].str.split('/').str[0]
df['month']=df['Date_of_Journey'].str.split('/').str[1]
df['year']=df['Date_of_Journey'].str.split('/').str[2]
df['day']=df['day'].astype(int)
df['month']=df['month'].astype(int)
df['year']=df['year'].astype(int)

df.drop(columns=['Date_of_Journey','Route'],inplace=True)

df['departure_hour']=df['Dep_Time'].str.split(':').str[0]
df['departure_minutes']=df['Dep_Time'].str.split(':').str[1]
df.drop(columns=['Dep_Time'],inplace=True)

print(df['Arrival_Time'].unique())

def arrival(val):
    result=val.split(" ")[0]
    a=result.split(':')[0]
    b=result.split(':')[1]
    return (a,b)
df[['arrival_hour','arrival_min']]=df['Arrival_Time'].map(arrival).apply(pd.Series)


df['departure_hour']=df['departure_hour'].astype(int)
df['departure_minutes']=df['departure_minutes'].astype(int)
df['arrival_hour']=df['arrival_hour'].astype(int)
df['arrival_min']=df['arrival_min'].astype(int)

df.drop(columns=['Arrival_Time'],inplace=True)

def Duration_conversion(value):
    values=value.split(' ')
    result=0
    if len(values)==2:
        hour=int(values[0].split('h')[0])
        min=int(values[1].split('m')[0])
        result=hour*60+min
    elif values[0][-1]=='h':
        hour=int(values[0].split('h')[0])
        result=hour*60
    else:
        min=int(values[0].split('m')[0])
        result=min
    return result
df['Duration_time']=df['Duration'].map(Duration_conversion).apply(pd.Series)
df.drop(columns=['Duration'],inplace=True)

df['Total_Stops']=df['Total_Stops'].map({'non-stop':0,'1 stop':1,'2 stops':2,'3 stops':3,'4 stops':4,'0':0})

encoder=OneHotEncoder()
encoded=pd.DataFrame(encoder.fit_transform(df[['Source','Destination','Airline']]).toarray(),columns=encoder.get_feature_names_out(['Source','Destination','Airline']),index=df.index)  ##df.index used to keep same index as df

# df.drop(columns=['Source','Destination','Airline','Additional_Info'],inplace=True)
df=pd.concat([df,encoded],axis=1)

# print(df.columns)
##shows the relationship between the Features Duration time , total stops and price
# sns.pairplot(df[['Duration_time','Total_Stops','Price']])
# plt.show()



##shows the avg cost for each airline
# vals=df.groupby('Airline')['Price'].mean().reset_index()
# sns.barplot(x='Airline',y='Price',data=vals,color='red')
# plt.title("Average price per Airline")
# plt.xticks(rotation=45)
# plt.show()

##shows correlation between variables
# sns.heatmap(df.iloc[:,0:12].corr(),annot=True)
# plt.title("Correlation between variables")
# plt.show()


##shows most famous airline
# famous_airline=df['Airline'].value_counts().reset_index()
#
# plt.pie(famous_airline['count'],labels=famous_airline['Airline'],autopct='%1.1f%%')
# plt.title("Airlines and their count")
# plt.show()




















