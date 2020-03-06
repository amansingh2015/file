library(networkD3)
#simpleNetwork(S8, width = 400, height = 400, linkColour = "red",
              opacity = 0.9, charge = -1000 ,zoom = TRUE)



library(RTextTools)
#Step-1 Training
#Import training data
# Create the document term matrix
dtMatrix <- create_matrix(AnalyzedSVM["Text"])
# Configure the training data
container <- create_container(dtMatrix,AnalyzedSVM$Sentiment, trainSize=1:7144, virgin=FALSE)

# train a SVM Model
model <- train_model(container, "SVM", kernel="linear", cost=1)
#Step-2 Testing
#Import testing data
final_data=data.frame()

for(i in 1:172)
{
  
  predictionData <-unanalyzed$Text[(((i-1)*100)+1):((i*100))]
  
  
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

write.csv(final_data,"C:/Users/ankita2/Desktop/senti9.csv")

