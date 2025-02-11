# -*- coding: utf-8 -*-
"""makreting.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZVHMFgn7swHDbMBn-EShUmtOEnPlAPDP

## About Dataset


### Problem Statement

Customer Personality Analysis is a detailed analysis of a company’s ideal customers. It helps a business to better understand its customers and makes it easier for them to modify products according to the specific needs, behaviors and concerns of different types of customers.

Customer personality analysis helps a business to modify its product based on its target customers from different types of customer segments. For example, instead of spending money to market a new product to every customer in the company’s database, a company can analyze which customer segment is most likely to buy the product and then market the product only on that particular segment.

### Column Information

#### People

ID: Customer's unique identifier

Year_Birth: Customer's birth year

Education: Customer's education level

Marital_Status: Customer's marital status

Income: Customer's yearly household income

Kidhome: Number of children in customer's household

Teenhome: Number of teenagers in customer's household

Dt_Customer: Date of customer's enrollment with the company

Recency: Number of days since customer's last purchase

Complain: 1 if the customer complained in the last 2 years, 0 otherwise

### Products

MntWines: Amount spent on wine in last 2 years

MntFruits: Amount spent on fruits in last 2 years

MntMeatProducts: Amount spent on meat in last 2 years

MntFishProducts: Amount spent on fish in last 2 years

MntSweetProducts: Amount spent on sweets in last 2 years

MntGoldProds: Amount spent on gold in last 2 years

### Promotion

NumDealsPurchases: Number of purchases made with a discount

AcceptedCmp1: 1 if customer accepted the offer in the 1st campaign, 0 otherwise

AcceptedCmp2: 1 if customer accepted the offer in the 2nd campaign, 0 otherwise

AcceptedCmp3: 1 if customer accepted the offer in the 3rd campaign, 0 otherwise

AcceptedCmp4: 1 if customer accepted the offer in the 4th campaign, 0 otherwise

AcceptedCmp5: 1 if customer accepted the offer in the 5th campaign, 0 otherwise

Response: 1 if customer accepted the offer in the last campaign, 0 otherwise

### Place

NumWebPurchases: Number of purchases made through the company’s website

NumCatalogPurchases: Number of purchases made using a catalogue

NumStorePurchases: Number of purchases made directly in stores

NumWebVisitsMonth: Number of visits to company’s website in the last month

### Target

Need to perform clustering to summarize customer segments.
"""

import datetime
from datetime import date

import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

import warnings
warnings.filterwarnings("ignore")

#from google.colab import drive

#drive.mount('/content/drive/')

#READ THE DATASET...
#df = pd.read_csv("/content/drive/MyDrive/CLOUDY_ML/Customer_seg/marketing_campaign.csv", sep="\t")

#READ THE DATASET...
df = pd.read_csv("marketing_campaign.csv", sep="\t")

df.head()

df.columns

df.shape

df.info()

df.describe().T

df.isna().sum()

"""since there are some missing values in Income we will check that column and replace missing values with mean or median"""

sns.distplot(df['Income'])
plt.show()

"""since the data is left skewed we will replace the missing values with median"""

#FILL THE MISSING VALUES WITH THE MEDIAN VALUES..
df['Income']=df['Income'].fillna(df['Income'].median())

df[df.duplicated()]

#FINDING THE NUMBER OF UNIQUE VALUES PRESENT IN EACH COLUMN...
df.nunique()

"""Note:-In above cell "Z_CostContact" and "Z_Revenue" have same value in all the rows that's why , they are not going to contribute anything in the model building. So we can drop them."""

df=df.drop(columns=["Z_CostContact", "Z_Revenue"],axis=1)

"""### Univariate Analysis :-

1.Analysis on Year_Birth Variable.
"""

#CHECKING NUMBER OF UNIQUE CATEGORIES PRESENT IN THE "Year_Birth"
print("Unique categories present in the Year_Birth:",df["Year_Birth"].value_counts())

def uni_V(col):
    plt.figure(figsize=(20,8))
    sns.countplot(df[col])

    plt.xticks(rotation=90)
    plt.show()

uni_V('Year_Birth')

"""Data points in year birth are uniformly distributed

2.Analysis On Education Variable.
"""

df['Education'].unique()

#CHANGING CATEGORY INTO "UG" AND "PG" ONLY....
df['Education'] = df['Education'].replace(['PhD','2n Cycle','Graduation', 'Master'],'Post Graduate')
df['Education'] = df['Education'].replace(['Basic'], 'Under Graduate')

uni_V('Education')

"""We observed that most of the data points here are post-Graduated

3.Analysis On Marital_Status Variable.
"""

df['Marital_Status'].unique()

#REPLACING THE CONFLICT VALUES IN Marital_status..
df['Marital_Status'] = df['Marital_Status'].replace(['Married', 'Together'],'Relationship')
df['Marital_Status'] = df['Marital_Status'].replace(['Divorced', 'Widow', 'Alone', 'YOLO', 'Absurd'],'Single')

uni_V('Marital_Status')

"""64.46% of Customers in the dataset are in "Relationship".
35.53% of Customers in the dataset are "Single".

4.Analysis On Income Variable.
"""

df['Income'].describe()

plt.figure(figsize=(12,5))
sns.distplot(df["Income"],color = 'turquoise')
plt.show()
df["Income"].plot.box(figsize=(12,5),color = 'turquoise')
plt.show()

"""The income column is left skewed as we saw earrlier but it has some outliers that we will treat it in later stage while model building

5.Analysis On "Kidhome,Teenhome" Variable.
"""

df['Teenhome'].unique()

df['Kidhome'].unique()

# Combining different dataframe into a single column to reduce the number of dimension

df['Kids'] = df['Kidhome'] + df['Teenhome']

uni_V('Kids')

"""50.35% of Customers in the dataset have 1 kid.
28.48% of Customers in the dataset have no kids.
18.79% of Customers in the dataset have 2 kids.
2.36% of Customers in the dataset have 3 kids.

6.Analysis On "MntWines,MntMeatProducts,MntFishProducts,MntSweetProducts,MntGoldProds" Variable.
"""

df[['MntFruits','MntMeatProducts']].head()

df['MntFishProducts'].nunique()

df['MntFruits'].nunique()

# Combining different dataframe into a single column to reduce the number of dimension

df['Expenses'] = df['MntWines'] + df['MntFruits'] + df['MntMeatProducts'] + df['MntFishProducts'] + df['MntSweetProducts'] + df['MntGoldProds']
df['Expenses'].head(10)

df['Expenses'].describe()

plt.figure(figsize=(12,5))
sns.distplot(df["Expenses"],color = 'turquoise')
plt.show()
df["Expenses"].plot.box(figsize=(12,5),color='turquoise')
plt.show()

"""The distribution of expenses is uniform

7.Analysis on "AcceptedCmp1,AcceptedCmp2,AcceptedCmp3,AcceptedCmp4,AcceptedCmp5" Variable.
"""

df['AcceptedCmp1'].unique()

df['AcceptedCmp2'].unique()

df['TotalAcceptedCmp'] = df['AcceptedCmp1'] + df['AcceptedCmp2'] + df['AcceptedCmp3'] + df['AcceptedCmp4'] + df['AcceptedCmp5']

#CHECKING NUMBER OF UNIQUE CATEGORIES PRESENT IN THE "TotalAcceptedCmp"
print("Unique categories present in the TotalAcceptedCmp:",df['TotalAcceptedCmp'].value_counts())
print("\n")

#VISUALIZING THE "TotalAcceptedCmp"


plt.figure(figsize=(8,8))
df['TotalAcceptedCmp'].value_counts().plot(kind='bar',color = 'turquoise',edgecolor = "black",linewidth = 3)
plt.title("Frequency Of Each Category in the TotalAcceptedCmp Variable \n",fontsize=24)
plt.show()

"""79.33% of Customers accepted the offer in the campaign are "0".
14.50% of Customers accepted the offer in the campaign are "1".
3.70% of Customers accepted the offer in the campaign are "2".
1.96% of Customers accepted the offer in the campaign are "3".
0.49% of Customers accepted the offer in the campaign are "4".

8.Analysis on "NumWebPurchases,NumCatalogPurchases,NumStorePurchases,NumDealsPurchases" Variable.
"""

df['NumWebPurchases'].unique()

df['NumCatalogPurchases'].unique()

df['NumStorePurchases'].unique()

df['NumTotalPurchases'] = df['NumWebPurchases'] + df['NumCatalogPurchases'] + df['NumStorePurchases'] + df['NumDealsPurchases']
df['NumTotalPurchases'].unique()

df[['NumTotalPurchases']]

df['NumTotalPurchases'].describe()

uni_V('NumTotalPurchases')

df.head()

"""9. Converting the Year_Birth to customer_Age"""

#ADDING A COLUMN "customer_Age" IN THE DATAFRAME....
df['Customer_Age'] = (pd.Timestamp('now').year) - df['Year_Birth']
df.head()

plt.figure(figsize=(12,5))
sns.distplot(df["Customer_Age"],color = 'turquoise')
plt.show()

"""Most of the cutomers we have are in middle age i.e between 35-55"""

# Deleting some column to reduce dimension and complexity of model

col_del = ["Year_Birth","ID","AcceptedCmp1" , "AcceptedCmp2", "AcceptedCmp3" , "AcceptedCmp4","AcceptedCmp5","NumWebVisitsMonth", "NumWebPurchases","NumCatalogPurchases","NumStorePurchases","NumDealsPurchases" , "Kidhome", "Teenhome","MntWines", "MntFruits", "MntMeatProducts", "MntFishProducts", "MntSweetProducts", "MntGoldProds"]
df=df.drop(columns=col_del,axis=1)

df.head()

df.head()

df.info()

"""In the next step, I am going to create a feature out of "Dt_Customer" that indicates the number of days a customer is registered in the firm's database. However, in order to keep it simple, I am taking this value relative to the most recent customer in the record.

Thus to get the values I must check the newest and oldest recorded dates.
"""

df["Dt_Customer"] = pd.to_datetime(df["Dt_Customer"])
dates = []
for i in df["Dt_Customer"]:
    i = i.date()
    dates.append(i)
#Dates of the newest and oldest recorded customer
print("The newest customer's enrolment date in therecords:",max(dates))
print("The oldest customer's enrolment date in the records:",min(dates))

"""Creating a feature ("Customer_For") of the number of days the customers started to shop in the store relative to the last recorded date"""

#Created a feature "Customer_For"
days = []
d1 = max(dates) #taking it to be the newest customer
for i in dates:
    delta = d1 - i
    days.append(delta)
df["Customer_For"] = days
df['Customer_For'] = df['Customer_For'].apply(lambda x:x.days)

df.head()

df['Customer_For'].describe()

df.drop(['Dt_Customer','Recency','Complain','Response'],axis=1,inplace=True)

df.head()

plt.figure(figsize=(12,5))

sns.distplot(df["Customer_For"],color = 'turquoise')
plt.show()

"""Most of the customers are regular to the campaign for 200-850 days"""

df.head()

df.shape

"""## Bivariate Analysis :-

1.Education vs Expenses
"""

sns.set_theme(style="white")
plt.figure(figsize=(8,8))
plt.title("How Education impacts on Expenses?",fontsize=24)
ax = sns.barplot(x="Education", y="Expenses", data=df,palette="rainbow")

"""We observe that the post graduated people spends more than the UG people

2.Marital status vs Expenses
"""

sns.set_theme(style="white")
plt.figure(figsize=(8,8))
plt.title("How Marital_Status impacts on Expenses?",fontsize=24)
ax = sns.barplot(x="Marital_Status", y="Expenses", data=df,palette="rainbow")

"""We observe that single and married people have the same spendings

3.Kids vs Expenses
"""

sns.set_theme(style="white")
plt.figure(figsize=(8,8))
plt.title("How Kids impacts on Expenses?",fontsize=24)
ax = sns.barplot(x="Kids", y="Expenses", data=df,palette="rainbow")

"""Here we observe some thing different that parents with 1 kid spends more than the parents who are having 2 or 3 kids

4.TotalAcceptedCmp vs Expenses
"""

sns.set_theme(style="white")
plt.figure(figsize=(8,8))
plt.title("How TotalAcceptedCmp impacts on Expenses?",fontsize=24)
ax = sns.barplot(x="TotalAcceptedCmp", y="Expenses", data=df,palette="rainbow")

"""those who accepeted more campaign have more expenses

5.NumTotalPurchases vs Expenses
"""

sns.set_theme(style="white")
plt.figure(figsize=(8,8))
plt.title("How NumTotalPurchases impacts on Expenses?",fontsize=24)
plt.xticks(rotation=90)
ax = sns.barplot(x="NumTotalPurchases", y="Expenses", data=df,palette="rainbow")

"""Those who have more purchases have more expenses

6.Day engaged vs Expenses
"""

df.columns

sns.set_theme(style="white")
plt.figure(figsize=(20,8))
plt.title("How Days Engaged impacts on Expenses?",fontsize=24)
plt.xticks(rotation=90)
ax = sns.lineplot(x="Customer_For", y="Expenses", data=df,palette="rainbow")

sns.scatterplot(df['Customer_For'],df['Expenses'])

plt.show()

"""No relationship between days enagaged vs expenses

7.Customer Age vs Expenses
"""

sns.set_theme(style="white")
plt.figure(figsize=(15,8))
plt.title("How Age impacts on Expenses?",fontsize=24)
plt.xticks(rotation=90)
ax = sns.barplot(x="Customer_Age", y="Expenses", data=df,palette="rainbow")

plt.show()

"""People who are in middle age have less expenses than others

### Remove some outliers present in age and income
"""

df['Income'].describe()

df['Customer_For'].describe()

df.shape

df = df[df['Customer_Age'] < 90]
df = df[df['Income'] < 300000]

df.shape

df.head()

"""### Finding the correlation:-"""

plt.figure(figsize=(10,8))
sns.heatmap(df.corr(), annot=True,cmap = 'Greys',linewidths=1)

"""Income is more positively correlated to Expenses and Number of purchases

Expenses is positively correlated to Income and Number of pur chases and negitively correlated with Kids
"""

# Import label encoder
from sklearn import preprocessing

# label_encoder object knows
# how to understand word labels.
label_encoder = preprocessing.LabelEncoder()


df['Education'] = label_encoder.fit_transform(df['Education'])
df['Marital_Status'] = label_encoder.fit_transform(df['Marital_Status'])

df.columns

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
col_scale = ['Income', 'Kids', 'Expenses',
       'TotalAcceptedCmp', 'NumTotalPurchases', 'Customer_Age', 'Customer_For']

df[col_scale] = scaler.fit_transform(df[col_scale])

df.head()

"""# Model Building

### K-Means
"""

X_0 = df.copy()

from sklearn.cluster import KMeans

wcss=[]
for i in range (1,11):
    kmeans=KMeans(n_clusters=i,init='k-means++',random_state=42)
    kmeans.fit(X_0)
    wcss.append(kmeans.inertia_)
plt.figure(figsize=(16,8))
plt.plot(range(1,11),wcss, 'bx-')
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

"""We can understand from the plot that cluster = 2 is the best..."""

# Training a predicting using K-Means Algorithm.

kmeans=KMeans(n_clusters=2, random_state=42).fit(X_0)
pred=kmeans.predict(X_0)


# Appending those cluster value into main dataframe (without standard-scalar)

X_0['cluster_Kmeans'] = pred + 1

X_0.head()

sns.countplot(x=X_0["cluster_Kmeans"])
plt.title("Distribution Of The Clusters")
plt.show()

sns.scatterplot(X_0['Expenses'],X_0['Income'],hue=X_0['cluster_Kmeans'])

"""### pca with Agglomerative clustering"""

df.head()

X_1 = df.copy()

X_1.head()

from sklearn.decomposition import PCA
#Initiating PCA to reduce dimentions aka features to 3
pca = PCA(n_components=3)
pca.fit(X_1)
PCA_ds = pd.DataFrame(pca.transform(X_1), columns=(["col1","col2", "col3"]))
PCA_ds.describe().T

#A 3D Projection Of Data In The Reduced Dimension
x =PCA_ds["col1"]
y =PCA_ds["col2"]
z =PCA_ds["col3"]

#To plot
fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111, projection="3d")
ax.scatter(x,y,z, c="maroon", marker="o" )
ax.set_title("A 3D Projection Of Data In The Reduced Dimension")

plt.show()

from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA

wcss=[]
for i in range (1,11):
    kmeans=KMeans(n_clusters=i,init='k-means++',random_state=42)
    kmeans.fit(PCA_ds)
    wcss.append(kmeans.inertia_)
plt.figure(figsize=(16,8))
plt.plot(range(1,11),wcss, 'bx-')
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

"""WCSS is the sum of the squared distance between each point and the centroid in a cluster.

wcss values is more less for k=2 here...so we take k=2
"""

#Initiating the Agglomerative Clustering model
AC = AgglomerativeClustering(n_clusters=2)

# fit model and predict clusters
yhat_AC = AC.fit_predict(PCA_ds)
PCA_ds["Clusters"] = yhat_AC

#Adding the Clusters feature to the orignal dataframe.
X_1["Cluster_Agglo"]= yhat_AC + 1

sns.scatterplot(X_1['Expenses'],X_1['Income'],hue=X_1['Cluster_Agglo'])

sns.scatterplot(X_1['Kids'],X_1['Income'],hue=X_1['Cluster_Agglo'])

sns.scatterplot(X_1['Marital_Status'],X_1['Income'],hue=X_1['Cluster_Agglo'])

sns.scatterplot(X_1['Marital_Status'],X_1['Expenses'],hue=X_1['Cluster_Agglo'])

sns.scatterplot(X_1['Income'],X_1['Customer_Age'],hue=X_1['Cluster_Agglo'])

sns.countplot(x=X_1["Cluster_Agglo"])
plt.title("Distribution Of The Clusters")
plt.show()

#Plotting the clusters
fig = plt.figure(figsize=(16,14))
ax = plt.subplot(111, projection='3d', label="bla")

ax.scatter(x, y, z, s=40, c=PCA_ds["Clusters"], marker='o')
ax.set_title("The Plot Of The Clusters")

plt.show()

"""## Conclusions:

### Cluster 1:
People with less expenses

people who are married and parents of more than 3 kids

people which low income


-------------------------------------------------------------------------
-------------------------------------------------------------------------

### Cluster 2:
people with more expenses

people who are single or parents who have less than 3 kids

people with high income

Age is not the criteria but it is observed to some extent that people who are older fall in this group

So, the customers falling in cluster 2 likes to spend more...so the Firm's can target people falling in cluster 2 for the sale of their Products....

# Thanks you!!!!
"""





