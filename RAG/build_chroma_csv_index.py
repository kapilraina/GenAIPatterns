import os, types
import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
import openai
from chromadb.config import Settings
chroma_client = chromadb.PersistentClient(path="/tmp/cdb")
collection = chroma_client.get_or_create_collection("Books_Index002")
embeddingsmodel = SentenceTransformer('all-MiniLM-L6-v2')

OPENAIKEY= os.environ.get('OPENAIKEY')
openai.api_key = OPENAIKEY

df = pd.read_csv('dataset/csv/ds_books_1k.csv')

def prepare_embedding_function(data):
    edict = {
        "title":data[1],
        "series":data[2],
        "author":data[3],
        "rating":data[4],
        "description":data[5],
        "language":data[6],
        "isbn":data[7],
        "genres":data[8],
        "characters":data[9],
        "bookFormat":data[10],
        "edition":data[11],
        "pages":data[12],
        "publisher":data[13],
        "publishDate":data[14],
        "firstPublishDate":data[15],
        "awards":data[16],
        "numRatings":data[17],        
        "ratingsByStars":data[18],
        "likedPercent":data[19],
        "setting":data[20],
        "coverImg":data[21],
        "bbeScore":data[22],
        "bbeVotes":data[23],
        "price":data[24]  
        
        }
    return edict    
def embedding_function(data):
   embeddings = embeddingsmodel.encode(data)
   return embeddings.tolist()

def oai_embedding_function(data):
    #print(embeddingsData)
    response = openai.Embedding.create(
    input=data,
    model="text-embedding-ada-002")
    #print(response)
    embeddings = list(map(lambda row: row.embedding,response.data))
    return embeddings


datalength = len(df)
batchsize = 225
begin = 0
end = batchsize
t_= 0
while True:
    #print("Batch Ranges" , begin,end)
    if begin >= datalength:
        break
    batch = df.iloc[begin:end] 
    #print(batch.count)
    metadata = batch.apply(lambda row: prepare_embedding_function(row), axis=1)   
    embeddable = batch.apply(lambda row: str(prepare_embedding_function(row)), axis=1)   
    #embeddings = embedding_function(embeddable.to_list())
    embeddings = oai_embedding_function(embeddable.to_list())
    ids_ = batch['bookId'].apply(lambda row: str(row))
    #metadata = batch.apply(lambda row: prepare_oai_embedding_function(row), axis=1)
    #data=list(zip(ids_, embeddings,metadata))
    collection.upsert(
        embeddings = embeddings,
        metadatas = metadata.tolist(),
        ids = ids_.tolist()
    )
    t_= t_+ len(batch)
    p_ = str((round(t_/datalength*100,2)))
    print(f"{t_}/{datalength}. {p_}%")
    
    begin = end
    end = end + batchsize
    
print("Chroma Updated")  


