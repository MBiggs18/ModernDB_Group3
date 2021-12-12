# -*- coding: utf-8 -*-
"""
@author: Mikayla Biggs
"""
import pymongo
import neo4j
from pymongo import MongoClient
from neo4j import GraphDatabase
from models import MongoModel, Neo4jModel

import re #regular expressions
import json
import ssl 

from consolemenu import *
from consolemenu.items import *
from pprint import pprint


mongoUrl = "mongodb+srv://mbiggs:pwd123@cluster0.9uybn.mongodb.net/moderndb?retryWrites=true&w=majority"
neo4jUrl = "neo4j+s://0c0676db.databases.neo4j.io"
neo4jDriver = GraphDatabase.driver(neo4jUrl, auth=('neo4j', 'Xqn4jBlgR_f9x0FVYBGrtPUEX4bp96WkZaf-D5WCeo0'))

mongoDBDatabase = ''
mongoCollection = ''

def menu(driver, client):
    try:
        # Create the menu
        menu = ConsoleMenu("Local Restaurant Recommendation System", "Modern Databases Project - Group #3")
        
        # Queries to Execute, calls a function when selected
        first_query = FunctionItem("Recommend Restaurants from Similar Customers (neo4j)", driver.print_result)
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
        print("Closing database connection...\nGoodbye!")
        driver.close()
        client.close()

if __name__ == "__main__":
    
    neo4jdb = Neo4jModel()
    driver = neo4jdb.neo4jDriver
    
    mongodb = MongoModel()
    client = mongodb.mongoClient

    menu(neo4jdb, mongodb)
