import pandas as pd
import matplotlib.pyplot as plt
import missingno as msno
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import mutual_info_regression, SelectKBest




test = pd.read_csv("/Users/kingmopser/PycharmProjects/Housing_Prices_Prediction/assets/test.csv")
train = pd.read_csv("/Users/kingmopser/PycharmProjects/Housing_Prices_Prediction/assets/train.csv")
if __name__ == "__main__":
# overview of dataset
    print(train.head(5))
    print(train.tail(5))
    print(train.info())
    print(train.dtypes)
    print(train.isna().sum())

    # visualizing variance of numerical values
    data=train[train.select_dtypes(exclude=["object"]).columns]
    plt.figure(figsize=(15, 10))
    plt.boxplot(data.values,labels=data.columns, vert=True )
    plt.xticks(rotation=90)
    plt.show()

    data2 = data[data < 100000]
    plt.figure(figsize=(15, 10))
    plt.boxplot(data2.values,labels=data2.columns, vert=True )
    plt.xticks(rotation=90)
    plt.show()

    # visualizing missing data
    train['SalePrice'].value_counts()
    train.isnull().mean().loc[lambda x: x>0 ].sort_values(ascending=False)
    msno.bar(train)
    plt.show()
    msno.matrix(train)
    plt.show()
    msno.heatmap(train)
    plt.show()

# definining  preprocessing function/pipeline
def preprocessing(filePath,name):

    df = pd.read_csv(filePath)
    df.drop(columns="Id", inplace=True)
    num_var = df.select_dtypes(exclude=["object"]).columns
    const_imputer = SimpleImputer(strategy='constant', fill_value="unknown")
    mean_imputer = SimpleImputer(strategy='mean')
    encoder = LabelEncoder()
    col = df.select_dtypes(include=["object"]).columns

    # Imputing NAs
    for i in df.columns :
        if df.dtypes[i] == 'object':
            df[[i]] = const_imputer.fit_transform(df[[i]])
        else:
            df[[i]] =mean_imputer.fit_transform(df[[i]])

    # defining ordered columns via domain knowledge
    ord_mappings = {
        "LotShape": ["IR3","IR2","IR1","Reg"],
        "LandSlope": ["Sev","Mod","Gtl"],
        "ExterQual": ["Po", "Fa", "TA", "Gd", "Ex"],
        "ExterCond": ["Po", "Fa", "TA", "Gd", "Ex"],
        "BsmtQual": ["unknown", "Po", "Fa", "TA", "Gd", "Ex"],
        "BsmtCond": ["unknown", "Po", "Fa", "TA", "Gd", "Ex"],
        "BsmtExposure": ["unknown", "No", "Mn", "Av", "Gd"],
        "BsmtFinType1": ["unknown", "Unf", "LwQ", "Rec", "BLQ", "ALQ", "GLQ"],
        "BsmtFinType2": ["unknown", "Unf", "LwQ", "Rec", "BLQ", "ALQ", "GLQ"],
        "HeatingQC": ["Po", "Fa", "TA", "Gd", "Ex"],
        "KitchenQual": ["Po", "Fa", "TA", "Gd", "Ex"],
        "Functional": ["Sal", "Sev", "Maj2", "Maj1", "Mod", "Min2", "Min1", "Typ"],
        "FireplaceQu": ["unknown", "Po", "Fa", "TA", "Gd", "Ex"],
        "GarageFinish": ["unknown", "Unf", "RFn", "Fin"],
        "GarageQual": ["unknown", "Po", "Fa", "TA", "Gd", "Ex"],
        "GarageCond": ["unknown", "Po", "Fa", "TA", "Gd", "Ex"],
        "PoolQC": ["unknown", "Po", "Fa", "TA", "Gd", "Ex"],
        "Fence": ["unknown", "MnWw", "GdWo", "MnPrv", "GdPrv"]
    }

    #applying order to columns
    for k,v in ord_mappings.items():
        df[k]= pd.Categorical(df[k], categories=v, ordered=True)

    # applying encoding
    df[col] =df[col].apply(encoder.fit_transform)

    # standarizing
    scaler = StandardScaler()
    num_var = num_var[num_var!= "SalePrice"]
    df[num_var] = pd.DataFrame(scaler.fit_transform(df[num_var]), columns=num_var)

    # feature selection
    bestFeatures = SelectKBest(score_func=mutual_info_regression, k=10)
    if name == "train":
        res = bestFeatures.fit_transform(X=df.drop(columns="SalePrice",inplace=False), y=df["SalePrice"])
        fin = pd.DataFrame(res, columns=bestFeatures.get_feature_names_out())
        fin["SalePrice"] = df["SalePrice"]
        return fin

    else:
        return df









