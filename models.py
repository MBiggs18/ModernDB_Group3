from pymongo import MongoClient
import pymongo
from neo4j import GraphDatabase
import redis


class Neo4jModel:
    def __init__(self, url='neo4j+s://0c0676db.databases.neo4j.io', user='neo4j', password='Xqn4jBlgR_f9x0FVYBGrtPUEX4bp96WkZaf-D5WCeo0'):
        self.neo4jUrl = url;
        self.neo4jDriver = GraphDatabase.driver(url, auth=(user, password))
        print("Connected to {0} Neo4j Database...".format(url))

    def close(self):
        self.neo4jDriver.close()
        print("Closing Neo4j Database...")
        
        
    def print_result1(self):
        with self.neo4jDriver.session() as session:
            greeting = session.write_transaction(self.query1)
            print(greeting)

    
    def query1(self, tx):
        # result = tx.run("MATCH (c:Customer) "
        #                 "RETURN c.customerId LIMIT 1  ")
        # return result.single()[0]
    
        X = input("Please enter your userId (0-7455):\n")
        
        while(int(X) not in range(0,601)):
            X = input("User Id must be between 0-7455, try again:")
        
        result = tx.run('''WITH %s as X
                        CALL { 
                             WITH X
                             MATCH(c:Customer {customerId:X})-[r:RATED]-(v:Vendor)
                             RETURN DISTINCT v.vendorId as ids
                        }
                        WITH X, ids
                        MATCH(c:Customer {customerId:X})-[r:RATED]-(v:Vendor)-[i:IN_TAG]-(t:Tag)
                        WHERE v.vendorId in ids
                        RETURN t.name;'''.format(X))
        for record in result:
            self.username=record.get('n.name')
            self.userid=record.get('n.customerId')
       
        if self.userid != None:
            if self.username != None:
                return "Welcome back, " + str(self.username) + "!" 
            
            self.username=input("Welcome user {0}, please enter a user name:\n".format(self.userid))
            result = tx.run("MATCH(n:User) WHERE n.userId={0} SET n.name='{1}' RETURN n.userId, n.name".format(str(self.userid),str(self.username)))
            
            for record in result:
                self.username=record.get('n.name')
                self.userid=record.get('n.userId')
            return "Welcome {0}".format(self.username)
        
        return "No user {} found...".format(X)


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

