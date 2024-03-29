# -*- coding: utf-8 -*-
"""
@author: Mikayla Biggs
"""
import pymongo
from models import MongoModel, Neo4jModel

from consolemenu import *
from consolemenu.items import *

def menu(driver, client):
    try:
        # Create the menu
        menu = ConsoleMenu("Local Restaurant Recommendation System", "Modern Databases Project - Group #3")
        
        # Queries to Execute, calls a function when selected
        first_query = FunctionItem("Recommend Restaurants from Similar Customers (neo4j)", driver.print_result, args = [client])
        second_query = FunctionItem('Search Restaurants by Keyword(s) (mongo)', client.printtext)
        third_query = FunctionItem('Search Nearest Vendor by Location (mongo)', client.printloc)
        
        # Create & Order Menu
        menu.append_item(first_query)
        menu.append_item(second_query)
        menu.append_item(third_query)

        # Display ConsoleMenu
        menu.show()
        
    except pymongo.errors.PyMongoError:
        print("Fatal db error... closing menu... \nPlease make sure the input parameters are in the correct format!!")
    
    finally:
        print("Closing database connections...")
        driver.close()
        client.close()
        print("Good-bye!")

if __name__ == "__main__":
    
    neo4jdb = Neo4jModel()
    driver = neo4jdb.neo4jDriver
    
    mongodb = MongoModel()
    client = mongodb.mongoClient

    menu(neo4jdb, mongodb)
    
