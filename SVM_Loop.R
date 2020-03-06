library(SparseM)
library(RTextTools)
library(openxlsx)
#install.packages("openxlsx")
library("openxlsx")
rm(list=ls())
#Step-1 Training
#Import training data
YT_TG_test<-read.xlsx("C:/Users/mukul.gupta/Documents/Python Scripts/Training Stuff/R/SVM _Classifier/YT_TG_test.xlsx")
YT_SVM_trai<-read.xlsx("C:/Users/mukul.gupta/Documents/Python Scripts/Training Stuff/R/SVM _Classifier/YT_SVM_trai.xlsx")
# Create the document term matrix

YT_TG_test=rbind.data.frame(YT_TG_test)


dtMatrix <- create_matrix(YT_SVM_trai$Text)
# Configure the training data
container <- create_container(dtMatrix, YT_SVM_trai$Topic1, trainSize=1:2737, virgin=FALSE)

# train a SVM Model
model <- train_model(container, "SVM", kernel="linear", cost=1)
#Step-2 Testing
#Import testing data#
#Test_data=rbind.data.frame(Test_data,Test_data[0:124,])

final_data=data.frame()
for(i in 1:179)
{
  
  predictionData <- YT_TG_test$Text[(((i-1)*100)+1):((i*100))]
  #predictionData <- Samsung_POS$Text[i]
  
  # create a prediction document term matrix
  predMatrix <- create_matrix(predictionData, originalMatrix=dtMatrix)
  #if error occured
  #trace("create_matrix",edit=T)
  
  predSize = length(predictionData);
  # create the corresponding container
  predictionContainer <- create_container(predMatrix, labels=rep(0,predSize), testSize=1:predSize, virgin=FALSE)
  # Results
  result <- classify_model(predictionContainer, model)
  final_data=rbind.data.frame(final_data,result)
  
}


YT_TG_test$Topic1=final_data$SVM_LABEL

#Synthesio_conversations$Sentiment_New = final_data$SVM_LABEL

#write.csv(YT_TG_test,"yt_analyzed.csv")


write.xlsx(YT_TG_test, "yt_analyzed.xlsx")

getwd()

setwd("C:/Users/mukul.gupta/Documents/Python Scripts/Training Stuff/R/SVM _Classifier")
