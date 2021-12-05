#Search for vendors based on keywords
def searchtext ():
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

