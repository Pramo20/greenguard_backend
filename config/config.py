from pymongo import MongoClient

uri = "mongodb+srv://admin:greenguardapp@cluster0.glmkok5.mongodb.net/"
client = MongoClient(uri)
try:
    client.admin.command('ping')
    print('pinged your deployment. You successfully connected to MongoDB Atlas')
except Exception as e:
    print(e)
    print('failed to connect to MongoDB Atlas. Check your connection: ', uri)

