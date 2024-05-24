from peewee import *
import xml.etree.ElementTree as ET
from datetime import datetime as dt
from datetime import timedelta as td
# Instantiates a database file with the given name. Variable will be passed into most of the functions defined below.
# Main flow should probably only include this as a text, other functions can be imported.

productsDB = SqliteDatabase("assets/productsDB.db")
# Table and column definition class

class Product(Model):
    shop = TextField()
    date = DateField()
    product_name = TextField()
    price = FloatField()
    
    class Meta:
        database = productsDB


# Function to see if given table exists in DB or not, will return boolean for if clause usage
def existingTable(model):
    return productsDB.table_exists(model._meta.table_name)


def connectToDB():
    try:
        productsDB.connect()
        print("Successfully connected to database.")
    except OperationalError as failed:
        print("Failed to connect.")


def closeConnection():
    try:
        productsDB.close()
        print("Connection succesfully closed.")
    except OperationalError as failed:
        print("Failed to close connection.")


# Will search for a perfect match in the database, returns a "None" valued "product" variable if fails to find so. 
def dbSearch(product_entry):
    try:
        product = Product.get(Product.shop == product_entry["shop"], Product.date == product_entry["date"], Product.product_name == product_entry["product_name"], Product.price == product_entry["price"])
    except Product.DoesNotExist:
        product = None
    return product
# Checking uniqueness of given product_entry, is used in Insertion method.
def checkUniqueness(product_entry):
    product = dbSearch(product_entry)
    if (product != None):
        return False
    else:
        return True

# Will insert all the product dictionary entries in the list but will roll back if even a single one fails.
def dbInsert(products_list):
    error_str = ""
    try: 
        with productsDB.atomic():
            for product_entry in products_list:
                    if(checkUniqueness(product_entry)):
                       Product.create(**product_entry)
                    else:
                        error_str += product_entry["product_name"] + "\n"
        return error_str
    except IntegrityError as fail:
        print(f"Insertion failed: {fail}")

# Will delete given dictionary entry, prints deleted rows count if successful, returns None if fails.
def dbDelete(product_entry):
    doesExist = dbSearch(product_entry)
    if(doesExist):
        deletionQuery = Product.delete().where(Product.shop == product_entry["shop"], Product.date == product_entry["date"], Product.product_name == product_entry["product_name"], Product.price == product_entry["price"])
        deleteInfo = deletionQuery.execute()
        print(f"Count of rows deleted: {deleteInfo}")
    else:
        print("Given product does not exist, thus cannot be deleted.")
        return None


def dbUpdate(product_entry, shop = None, date = None, product_name = None, price = None):
    argumentsList = locals()
    isEmpty = all(value is None for value in argumentsList.values())
    if(isEmpty):
        print("To update a row, you need to give at least 1 parameter.")
    else:
        updateDict = {key: product_entry[key] if value is None and key in product_entry else value for key, value in argumentsList.items()}
        Product.update(shop = updateDict["shop"], date = updateDict["date"], product_name = updateDict["product_name"], price = updateDict["price"]).where(Product.shop == product_entry["shop"], Product.date == product_entry["date"], Product.product_name == product_entry["product_name"], Product.price == product_entry["price"]).execute()
        print("Data successfully updated.")


def dbCompare(product_entry1, product_entry2):
    product1 = dbSearch(product_entry1)
    product2 = dbSearch(product_entry2)
    
    if(product1 == None or product2 == None):
        print("Either one or both of the products don't exist.")
    else:
        print("1st product is more expensive." if product1.price > product2.price else "1st product is cheaper.")
        if(product1["product_name"] == product2["product_name"] and product1["date"] != product2["date"]):
            product1_date = dt.strptime(product1["date"], "%d/%m/%y")
            product2_date = dt.strptime(product2["date"], "%d/%m/%y")
           
           valChange = (abs(product1["price"] - product2["price"]) / product2["price"]) * 100.0 if product1_date > product2_date else (abs(product2["price"] - product1["price"]) / product1["price"]) * 100.0
            timeDiff = product1_date - timedelta(product2_date) if product1_date > product2_date else product2_date - timedelta(product1_date)
            return valChange, timeDiff



def dbGetAll():
    products_list = [product for product in Product.select().dicts()]
    return products_list

def cheapestPrice(product_name):
    queryRes = Product.select(Product.shop, Product.price).where(Product.product_name == product_name)
    productTuple = [(values.shop, values.price) for values in queryRes]
    if(productTuple == []):
        print("This product doesn't exist.")
    else:
        cheapestPrice = productTuple[0][1]
        shopName = productTuple[0][0]
        for shop, price in productTuple:
            if price < cheapestPrice:
                cheapestPrice = price
                shopName = shop
        print(f"Cheapest price for this product is in {shopName} market and costs {cheapestPrice}")



def exportXML(products_list):
    xmlRoot = ET.Element('Products')

    for product in products_list:
        product_element = ET.SubElement(xmlRoot, 'Product')
        
        shop_element = ET.SubElement(product_element, 'Shop')
        shop_element.text = product["shop"]

        date_element = ET.SubElement(product_element, 'Date')
        date_element.text = str(product["date"])

        name_element = ET.SubElement(product_element, 'ProductName')
        name_element.text = product["product_name"]

        price_element = ET.SubElement(product_element, 'Price')
        price_element.text = str(product["price"])

    outPath = "assets/products.xml" 
    xmlTree = ET.ElementTree(xmlRoot)
    xmlTree.write(outPath, encoding = "utf-8", xml_declaration = True)
