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


mongoUrl = "mongodb://localhost:27017/"
neo4jUrl = "bolt://localhost:7687"
neo4jDriver = GraphDatabase.driver(neo4jUrl, auth=('neo4j', 'moderndb'))

mongoDBDatabase = ''
mongoCollection = ''

def menu(driver, client):
    try:
        # Create the menu
        menu = ConsoleMenu("New Guinea Restaurant Recommendations", "Modern Databases Project - Group #3")
        
        # Queries to Execute, calls a function when selected
        first_query = FunctionItem("Test Query 1", driver.print_result1)
        second_query = FunctionItem('Test Query 1', driver.print_result1)
        third_query = FunctionItem('Test Query 1', driver.print_result1)
        fourth_query = FunctionItem('Test Query 1', driver.print_result1)
        
        # Can create sub menus for more specific queries
        s_menu = SelectionMenu([])
        s_menu.append_item(first_query)
        s_menu.append_item(second_query)        
        submenu = SubmenuItem("Test Submenu", s_menu , menu)

        # Create & Order Menu
        menu.append_item(first_query)
        menu.append_item(second_query)
        menu.append_item(third_query)
        menu.append_item(fourth_query)
        menu.append_item(submenu)

        
        # Display ConsoleMenu
        menu.show()
        
    except pymongo.errors.PyMongoError:
        print("Fatal db error... closing menu... \nPlease make sure the input parameters are in the correct format!!")
    
    finally:
        print("Closing database connection...\nGoodbye!")
        driver.close()

if __name__ == "__main__":
    neo4jdb = Neo4jModel()
    driver = neo4jdb.neo4jDriver
    
    mongodb = MongoModel()
    client = mongodb.mongoClient
    mongoDBDatabase = client['moderndb']
    # mongoCollection = dbname.? # replace ? with collection name
        
    menu(neo4jdb, client)
    
    neo4jdb.close()
    mongodb.close()

