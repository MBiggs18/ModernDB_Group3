from pymongo import MongoClient
from neo4j import GraphDatabase
import pandas as pd
pd.set_option('display.max_columns', 500)

class Neo4jModel:
    def __init__(self, url='neo4j+s://0c0676db.databases.neo4j.io', user='neo4j', password='Xqn4jBlgR_f9x0FVYBGrtPUEX4bp96WkZaf-D5WCeo0'):
        self.neo4jUrl = url
        self.neo4jDriver = GraphDatabase.driver(url, auth=(user, password))
        self.customerId = ''
        self.topvendors = list()
        self.tags = list()
        self.usratings = list()
        print("Connected to {0} Neo4j Database...".format(url))

    def close(self):
        self.neo4jDriver.close()
        print("Closing Neo4j Database...")
        
        
    def print_result(self, client):
        with self.neo4jDriver.session() as session:
            top_vendors = session.write_transaction(self.get_user_rec_vendors)
            if isinstance(top_vendors, str):
                greeting = "Wrong Username, please enter again!"
                print(greeting)
            else:
                vendor_info = client.vendordetails(top_vendors['vendor'].tolist())
                greeting = pd.concat([top_vendors, vendor_info], axis=1)
                print(greeting)

    
    def get_user_rec_vendors(self, tx):   
        X = input("Please enter your customerId (7 character code):\n")
        

        result = tx.run("OPTIONAL MATCH (n:Customer) WHERE n.customerId='{0}' RETURN n.customerId".format(X))
        
            
        for record in result:
            self.customerId=record.get('n.customerId')
            
        print(self.customerId)
       
        if(self.customerId == None):
            return "No results matching your search, sorry!"
        
        print("User {0} found!".format(self.customerId))
        query = ''' MATCH (c1:Customer{customerId:'%s'})-[s:SIMILARITY]->(c2:Customer)
                    WHERE c1<>c2
                    WITH s.score as score, collect(c2.customerId) as top_user ORDER BY s.score
                    MATCH(c:Customer)-[r:RATED]-(v:Vendor)
                    WHERE c.customerId IN top_user
                    WITH c, r, v, top_user, score
                    ORDER BY r.rating DESC
                    WITH c, collect(r.rating) AS rating, collect(v.vendorId) as ids, score
                    UNWIND rating[0] AS rated
                    UNWIND ids[0] as vendor
                    RETURN c.customerId as customer, rated, vendor, score ORDER BY score DESC LIMIT 5;''' % (str(self.customerId))
            
        result = tx.run(query)
        top_vendors = pd.DataFrame([dict(record) for record in result])
        if top_vendors.empty:
            return "No results matching your search, sorry!"

        return top_vendors
        

class MongoModel:
    def __init__(self, url="mongodb+srv://mbiggs:pwd123@cluster0.9uybn.mongodb.net/moderndb?retryWrites=true&w=majority"):
        self.mongoUrl = url
        #self.mongoClient = MongoClient(url)
        self.mongoClient = MongoClient(port=27017)
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
        {"_id": 0, "vendor_tag_name": 1, "vendor_rating": 1, "OpeningTime": 1, "preparation_time": 1, "is_akeed_delivering": 1, 
        "score": {"$meta": "textScore"}}).limit(5)
        myquery.sort([('score', {'$meta': 'textScore'})])
        
        print("RESULTS:")
        top_vendors = pd.DataFrame([dict(record) for record in myquery])
        if top_vendors.empty:
            return "No results matching your search, sorry!"
        return top_vendors
    
    def printtext(self):
        greeting = self.searchtext()
        print(greeting)

    
    #Search for top 5 vendors based on keywords
    def searchvendor(self):
        client = self.mongoClient
        db = client.trydb
        long = float(input("Please enter your longitude: \n"))
        lat = float(input("Please enter your latitude: \n"))
        myquery = db.vendors.find({"geoloc": 
            {"$near": {"$geometry": {"type": "Point", "coordinates": [long, lat]}}}},
            {"_id": 0, "vendor_tag_name": 1, "vendor_rating": 1, "OpeningTime": 1, "preparation_time": 1, "is_akeed_delivering": 1}).limit(5)
        
        print("RESULTS:")
        top_vendors = pd.DataFrame([dict(record) for record in myquery])
        if top_vendors.empty:
            return "No results matching your search, sorry!"
        return top_vendors
     

    #retrieve vendor details
    def vendordetails(self, vendor_info):
        client = self.mongoClient
        db = client.trydb
       	myquery = db.vendors.aggregate([{"$match": {"id": {"$in": vendor_info}}},
                                        {"$project": {"_id": 0, "vendor_tags": "$vendor_tag_name", "rating": "$vendor_rating", "OpeningTime": "$OpeningTime",
                                                      "preparation_time": "$preparation_time", "delivery": "$is_akeed_delivering"}}])
       
        print("RESULTS:")
        vendor_info = pd.DataFrame([dict(record) for record in myquery])
        if vendor_info.empty:
            return "No results matching your search, sorry!"
        print(vendor_info)
        return vendor_info
        
    def printloc(self):
        greeting = self.searchvendor()
        print(greeting)

