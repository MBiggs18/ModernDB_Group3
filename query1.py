#search for vendors based on location
def searchvendor ():
    db = client.trydb
    long = float(input("Please enter your longitude: \n"))
    lat = float(input("Please enter your latitude: \n"))
    myquery = db.vendors.find({"location": 
        {"$near": {"$geometry": {"type": "Point", "coordinates": [long, lat]}}}},
        {'_id': 0, "name": 1, "address": 1, "city": 1, "state": 1, "stars": 1, "categories": 1, "review_count": 1}).limit(3)
    for doc in myquery:
        print("\n")
        print(doc)
        print("\n")
        
    return()
