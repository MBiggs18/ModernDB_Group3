from pymongo import MongoClient
from neo4j import GraphDatabase
import redis


class Neo4jModel:
    def __init__(self, url='bolt://localhost:7687', user='neo4j', password='moderndb'):
        self.neo4jUrl = url;
        self.neo4jDriver = GraphDatabase.driver(url, auth=(user, password))

    def close(self):
        self.neo4jDriver.close()
        
    def query1(self, tx):
        X = input("Please enter your userId (0-600):\n")
        
        # while(int(X) not in range(0,601)):
        #     X = input("User Id must be between 0-600, try again:")
        
        # result = tx.run("Match (n:User) WHERE n.userId={0} RETURN n.userId, n.name".format(X))
        # for record in result:
        #     self.username=record.get('n.name')
        #     self.userid=record.get('n.userId')
       
        # if self.userid != None:
        #     if self.username != None:
        #         return "Welcome back, " + str(self.username) + "!" 
            
        #     self.username=input("Welcome user {0}, please enter a user name:\n".format(self.userid))
        #     # result = tx.run("MATCH(n:User) WHERE n.userId={0} SET n.name='{1}' RETURN n.userId, n.name".format(str(self.userid),str(self.username)))
            
        #     for record in result:
        #         self.username=record.get('n.name')
        #         self.userid=record.get('n.userId')
        #     return "Welcome {0}".format(self.username)
        
        return "user {}...".format(X)
        
    def print_result1(self):
        with self.neo4jDriver.session() as session:
            greeting = session.write_transaction(self.query1)
            print(greeting)


class MongoModel:
    def __init__(self, url='mongodb://localhost:27017/pokemon'):
        self.mongoUrl = url
        self.mongoClient = MongoClient(url)

    def close(self):
        self.mongoClient.close()
        
    def query1(self):
        lat = input("Please enter latitude:\n").strip()
        long = input("Please enter longitude:\n").strip()
        coords = [float(long), float(lat)]
        print("Coordinated entered:",coords)
        # pipeline = [{ '$geoNear': { 'near': { '$geometry': { 'type': "Point", 'coordinates': coords }} , 'distanceField': "distance", 'key': "location" } }, { "$limit": 3 }, {'$project':{'_id':0, 'name':1, 'distance':1, 'address':1, 'city':1, 'state':1, 'stars':1, 'categories':1, 'review_count':1}}]
        # query = self.businesses.aggregate(pipeline)
        # print("Results:")
        # pprint(list(query))
        return
    
    def query2(db):
        terms = input("Please enter search terms separated by a space\n")
        print("Search terms entered: ",terms)
        # pipeline = [{'$match': {'$text': {'$search': terms}}},{'$group':{'_id':{'name':"$name",'city':"$city",'state':"$state",'categories':"$categories", 'stars':"$stars", 'review_count':'$review_count','score':{'$meta':"textScore"}}}}, {'$sort': {"_id.score":-1}},{'$limit':5}]
        # query = self.businesses.aggregate(pipeline)
        # print("Results:")
        # pprint(list(query))
        return

