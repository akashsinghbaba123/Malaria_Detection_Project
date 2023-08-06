# -*- coding: utf-8 -*-
"""Untitled17 (1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UhyWIkhFNlL15WZIwPrRurjlD_J4jeQG
"""

#Installing pyspark
!pip install pyspark

# importing the required libraries for in pyspark
from pyspark.sql import SparkSession
import pyspark.sql.types as tp
from pyspark.sql import functions as F

# creating the  spark session object
spark = SparkSession.builder.getOrCreate()

# reading the train data
train_data = spark.read.csv("/content/train.csv",inferSchema=True, header=True)
# reading the test data
test_data  = spark.read.csv("/content/test.csv", inferSchema=True, header=True)

# data type of the columns
train_data.printSchema()

#1. Average Purchase amount?
train_data_avg=train_data.agg(F.avg("Purchase").alias("average amount"))
train_data_avg.show()

#total rows
train_data_count=train_data.agg(F.count('User_ID')).show()
test_data_count=test_data.agg(F.count('User_ID')).show()

#2. Counting and Removing null values
# null values in each column
#train
for n in train_data.columns:
  # defining  the condition
  missing_values = F.isnull(n)

  # filter the data with condition and count the number of data points
  missing_values = train_data.filter(missing_values).count()

  # print the result
  print(n, missing_values)
#test
for n in test_data.columns:
  # defining  the condition
  missing_values = F.isnull(n)

  # filter the data with condition and count the number of data points
  missing_values = test_data.filter(missing_values).count()

  # print the result
  print(n, missing_values)

"""We can see Product_Category_2 have null values approx 30% and Product_Category_3 have null values 70% so , we can drop the column Product_Category_3 for datasets.

"""

# droping the Product_Category_3
train_data=train_data.drop('Product_Category_3')
test_data=test_data.drop('Product_Category_3')

#filling the null values in column Product_Category_2 with mode value
train_data_mode=train_data.agg(F.mode('Product_Category_2'))
value=train_data_mode.show()
value
train_data=train_data.fillna(8)

test_data_mode=test_data.agg(F.mode('Product_Category_2'))
value=test_data_mode.show()
value
test_data=test_data.fillna(8)

#3. How many distinct values per column?
# distinct values in each column
train_data.agg(*(F.countDistinct(F.col(c)).alias(c) for c in train_data.columns)).show()

# 4. Count category values within each of the following column:
# ● Gender
# ● Age
# ● City_Category
# ● Stay_In_Current_City_Years
# ● Marital_Status

#Gender
train_data_cols_gender=train_data.groupby('Gender').agg(F.count('Gender'))
train_data_cols_gender.show()

#Age
train_data_cols_age=train_data.groupby('Age').agg(F.count('Age'))
train_data_cols_age.show()

#City Category
train_data_cols_City_Category=train_data.groupby('City_Category').agg(F.count('City_Category'))
train_data_cols_City_Category.show()

#Stay_In_Current_City_Years
train_data_cols_Stay_In_Current_City_Years=train_data.groupby('Stay_In_Current_City_Years').agg(F.count('Stay_In_Current_City_Years'))
train_data_cols_Stay_In_Current_City_Years.show()
#Marital_Status
train_data_cols_Marital_Status=train_data.groupby('Marital_Status').agg(F.count('Marital_Status'))
train_data_cols_Marital_Status.show()

#5. Calculate average Purchase for each of the following columns:
# ● Gender
# ● Age
# ● City_Category
# ● Stay_In_Current_City_Years
# ● Marital_Status

train_data_cols_gender=train_data.groupby('Gender').agg(F.round(F.avg('Purchase')))
train_data_cols_gender.show()

train_data_cols_age=train_data.groupby('Age').agg(F.round(F.avg('Purchase')))
train_data_cols_age.show()
train_data_cols_City_Category=train_data.groupby('City_Category').agg(F.round(F.avg('Purchase')))
train_data_cols_City_Category.show()

train_data_cols_Stay_In_Current_City_Years=train_data.groupby('Stay_In_Current_City_Years').agg(F.round(F.avg('Purchase')))
train_data_cols_Stay_In_Current_City_Years.show()

train_data_cols_Marital_Status=train_data.groupby('Marital_Status').agg(F.round(F.avg('Purchase')))
train_data_cols_Marital_Status.show()

#6. Label encode the following columns:
# ● Age
# ● Gender
# ● Stay_In_Current_City_Years
# ● City_Category

# importing some more library for encoding
from pyspark.ml.feature import StringIndexer

# label encode using StringIndexer
le_age = StringIndexer(inputCol= "Age", outputCol= "Age1" , handleInvalid="skip")
le_Gender = StringIndexer(inputCol= "Gender", outputCol= "Gender1" , handleInvalid="skip")
le_current_city = StringIndexer(inputCol= "Stay_In_Current_City_Years", outputCol= "Stay_In_Current_City_Years1" , handleInvalid="skip")
le_city_cat = StringIndexer(inputCol= "City_Category", outputCol= "City_Category1" , handleInvalid="skip")

#train data object
le_age_obj = le_age.fit(train_data)
le_Gender_obj=le_Gender.fit(train_data)
le_current_city_obj=le_current_city.fit(train_data)
le_city_cat_obj=le_city_cat.fit(train_data)
#test data object
le_age_obj = le_age.fit(test_data)
le_Gender_obj=le_Gender.fit(test_data)
le_current_city_obj=le_current_city.fit(test_data)
le_city_cat_obj=le_city_cat.fit(test_data)

#train data transformation
train_data_encoded=le_age_obj.transform(train_data)
train_data_encoded=le_Gender_obj.transform(train_data_encoded)
train_data_encoded=le_current_city_obj.transform(train_data_encoded)
train_data_encoded=le_city_cat_obj.transform(train_data_encoded)
#test data transformation
test_data_encoded=le_age_obj.transform(test_data)
test_data_encoded=le_Gender_obj.transform(test_data_encoded)
test_data_encoded=le_current_city_obj.transform(test_data_encoded)
test_data_encoded=le_city_cat_obj.transform(test_data_encoded)



#train data encoded columns list
train_data_encoded.columns

#test data encoded columns list
test_data_encoded.columns

test_data_encoded.show()
train_data_encoded.show()

#library for one hot encoder
from pyspark.ml.feature import OneHotEncoder

# 7. One-Hot encode following columns:
# ● Gender
# ● City_Category
# ● Occupation
OHE_train = OneHotEncoder(inputCols=[
                                         "Gender1",

                                              "City_Category1",
                                         "Occupation"],
                                  outputCols=[
                                              "Gender1_ohe",

                                              "City_Category1_ohe",
                                              "Occupation_ohe"
                                              ])

# OHE object
OHE_Obj = OHE_train.fit(train_data_encoded)
OHE_Obj_test=OHE_train.fit(test_data_encoded)

# Transform train data
train_data_encoded = OHE_Obj.transform(train_data_encoded)
test_data_encoded=OHE_Obj.transform(test_data_encoded)

# view the one hot encoded data
train_data_encoded.select(
                                              "Gender1_ohe",
                                              "City_Category1_ohe",
                                              "Occupation_ohe"
                           ).show()
#view the one hot encoded data
test_data_encoded.select(
                                              "Gender1_ohe",
                                              "City_Category1_ohe",
                                              "Occupation_ohe"
                           ).show()

#8. Build a baseline model using any of the ML algorithms.
# import the library
from pyspark.ml.feature import VectorAssembler

# create feature vector
feature_vector = VectorAssembler(inputCols= ['Age1',
                                             'Gender1_ohe',
                                             'Stay_In_Current_City_Years1',
                                             'City_Category1_ohe',
                                             'Occupation_ohe',
                                             'Product_Category_1',
                                             'Product_Category_2'


                                             ],
                                outputCol= 'feature_vector')

# transform the feature vector
train_data_encoded = feature_vector.transform(train_data_encoded)
test_data_encoded= feature_vector.transform(test_data_encoded)

# view the feature vector
train_data_encoded.select("feature_vector").show(15)
test_data_encoded.select("feature_vector").show(15)

#we can see that the data type of the `feature_vector` is vector
train_data_encoded.printSchema()
test_data_encoded.printSchema()

# Importing the libraries
from pyspark.ml import regression
from pyspark.ml.evaluation import RegressionEvaluator

#liearregression model
model_LR = regression.LinearRegression(featuresCol='feature_vector', labelCol="Purchase")

#fitting the train data encoded into model
model_LR = model_LR.fit(train_data_encoded)

# Evaluate training data
evaluator = RegressionEvaluator(labelCol="Purchase", metricName="rmse")
evaluator.evaluate(model_LR.transform(train_data_encoded))

#evaluating on mean absolute error
evaluator = RegressionEvaluator(labelCol="Purchase", metricName="mae")
evaluator.evaluate(model_LR.transform(train_data_encoded))

#evaluating on root mean square error
evaluator = RegressionEvaluator(labelCol="Purchase", metricName="rmse")
evaluator.evaluate(model_LR.transform(train_data_encoded))

#prediction on test data
model_predict=model_LR.transform(test_data_encoded)

#predicted values of test data
model_predict.select("prediction").show()

#9. Model improvement with Grid-Search CV
# import the CrossValidator and ParamGridBuilder
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

# create the object of the Logistic Regression Model
model_LR_CV = regression.LinearRegression(featuresCol= "feature_vector",  labelCol="Purchase")

# create parameter builder

updated_params = ParamGridBuilder() \
                .addGrid(model_LR_CV.regParam, [0.01, 0.005, 0.0001]) \
                .addGrid(model_LR_CV.elasticNetParam, [0.1, 0.001]) \
                .build()

# create object of the Cross Calidator with 3 folds
cv = CrossValidator(estimator=model_LR_CV,
                    estimatorParamMaps=updated_params,
                    evaluator=evaluator,
                    numFolds=3,
                    seed=27)

# fit the model
grid_model = cv.fit(train_data_encoded)

# evaluate the model
evaluator = RegressionEvaluator(labelCol="Purchase",metricName="rmse")
evaluator.evaluate(grid_model.transform(train_data_encoded))

#10. Create a Spark ML Pipeline for the final model.
## Import the Required Libraries
from pyspark.ml import Pipeline
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.ml import Transformer
from pyspark.ml.param.shared import HasInputCol, HasOutputCol, Param
from pyspark.ml import regression

#loading the data
train_data_pipeline = spark.read.csv("/content/train.csv", inferSchema=True, header=True)
test_data_pipeline = spark.read.csv("/content/test.csv", inferSchema=True, header=True)

# #filling the null values in column Product_Category_2 with mode value
# train_data_mode=train_data.agg(F.mode('Product_Category_2'))
# value=train_data_mode.show()
# value
# train_data=train_data.fillna(8)

class nullValuestransformer(Transformer):

  def __init__(self,dataframe= None):
    self.dataframe=dataframe

  def _transform(self,dataframe):
    dataframe=dataframe.fillna({'Product_Category_2':8})

    return dataframe



#creating stages for pipeline
stage1=nullValuestransformer()
stage2 = StringIndexer(inputCol= "Age", outputCol= "Age1" , handleInvalid="skip")
stage3 = StringIndexer(inputCol= "Gender", outputCol= "Gender1" , handleInvalid="skip")
stage4 = StringIndexer(inputCol= "Stay_In_Current_City_Years", outputCol= "Stay_In_Current_City_Years1" , handleInvalid="skip")
stage5= StringIndexer(inputCol= "City_Category", outputCol= "City_Category1" , handleInvalid="skip")
stage6 = OneHotEncoder(inputCols=[
                                         "Gender1",

                                              "City_Category1",
                                         "Occupation"],
                                  outputCols=[
                                              "Gender1_ohe",

                                              "City_Category1_ohe",
                                              "Occupation_ohe"
                                              ])
stage7 = VectorAssembler(inputCols= ['Age1',
                                             'Gender1_ohe',
                                             'Stay_In_Current_City_Years1',
                                             'City_Category1_ohe',
                                             'Occupation_ohe',
                                             'Product_Category_1',
                                             'Product_Category_2'


                                             ],
                                outputCol= 'feature_vector')
stage8=regression.LinearRegression(featuresCol='feature_vector',labelCol='Purchase')

#defining pipline
pipline=Pipeline(stages=[stage1,stage2,stage3,stage4,stage5,stage6,stage7,stage8])

# fit the pipeline with the training data
pipeline_model = pipline.fit(train_data_pipeline)

# transform data
final_data = pipeline_model.transform(train_data_pipeline)

final_data.select('Age1','Gender1','Prediction').show()

