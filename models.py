from pymongo import MongoClient
import pymongo
from neo4j import GraphDatabase
import redis


class Neo4jModel:
    def __init__(self, url='neo4j+s://0c0676db.databases.neo4j.io', user='neo4j', password='Xqn4jBlgR_f9x0FVYBGrtPUEX4bp96WkZaf-D5WCeo0'):
        self.neo4jUrl = url;
        self.neo4jDriver = GraphDatabase.driver(url, auth=(user, password))
        self.customerId = ''
        self.tags = list()
        print("Connected to {0} Neo4j Database...".format(url))

    def close(self):
        self.neo4jDriver.close()
        print("Closing Neo4j Database...")
        
        
    def print_result1(self):
        with self.neo4jDriver.session() as session:
            greeting = session.write_transaction(self.query1)
            print(greeting)

    
    def query1(self, tx):   
        X = input("Please enter your customerId (7 character code):\n")
        result = tx.run("MATCH (n:Customer) WHERE n.customerId='{0}' RETURN n.customerId LIMIT 25".format(X))
        
        for record in result:
            self.customerId=record.get('n.customerId')
       
        if(self.customerId==''):
            return "No user found, try again."
        
        print("User {0} found!".format(self.customerId))
        query = '''WITH '%s' as X
                    CALL { 
                         WITH X
                         MATCH(c:Customer {customerId:X})-[r:RATED]-(v:Vendor)
                         RETURN DISTINCT v.vendorId as ids
                    }
                    WITH X, ids
                    MATCH(c:Customer {customerId:X})-[r:RATED]-(v:Vendor)-[i:IN_TAG]-(t:Tag)
                    WHERE v.vendorId in ids
                    RETURN X, t.name;''' % (str(self.customerId))
            
        result = tx.run(query)
        for record in result:
            self.username=record.get('X')
            self.tags.append(record.get('t.name'))
            
        return "Welcome {0}, you rated these tags: {1}".format(self.username, self.tags)
    

class MongoModel:
    def __init__(self, url="mongodb+srv://mbiggs:pwd123@cluster0.9uybn.mongodb.net/moderndb?retryWrites=true&w=majority"):
        self.mongoUrl = url
        self.mongoClient = MongoClient(url)
        print("Connected to {0} Mongo Database...".format(self.mongoClient['moderndb'].name))

    def close(self):
        self.mongoClient.close()
        print("Closing Mongo Database...")
        
    #Search for top 5 vendors based on keywords
    def searchtext (self):
        client = self.mongoClient
        db = client.trydb
        userinput = input("Please enter the terms you would like to search with: \n")
    
        myquery = db.vendors.find({"$text": {"$search": userinput}},
        {"_id": 0, "vendor_tag_name": 1, "vendor_rating": 1, "OpeningTime": 1, "preparation_time": 1,
        "is_akeed_delivering": 1, 
        "categories": 1, "review_count": 1, "score": {"$meta": "textScore"}}).sort("score", pymongo.ASCENDING).limit(5) 
    
        for doc in myquery:
            print("\n")
            print(doc)
            print("\n")
        
        return()
    
    #Search for top 5 vendors based on keywords
    def searchvendor(self):
        client = self.mongoClient
        db = client.trydb
        long = float(input("Please enter your longitude: \n"))
        lat = float(input("Please enter your latitude: \n"))
        myquery = db.vendors.find({"geoloc": 
            {"$near": {"$geometry": {"type": "Point", "coordinates": [long, lat]}}}},
            {'_id': 0, "name": 1, "address": 1, "city": 1, "state": 1, "stars": 1, "categories": 1, "review_count": 1}).limit(5)
        for doc in myquery:
            print("\n")
            print(doc)
            print("\n")
        
        return()

