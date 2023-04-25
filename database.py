from pymongo import MongoClient


cluster = MongoClient("mongodb+srv://tuan816:Copybox2023@cluster0.pzaped9.mongodb.net/?retryWrites=true&w=majority")
db = cluster["todo-demo"]
# db = cluster.get_database()
collection_user = db["user"]
collection_todo = db["todo"]
# collection_todo = db.get_collection()
