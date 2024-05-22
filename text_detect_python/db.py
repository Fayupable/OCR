from peewee import *

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
    except OperationalError as failed:
        print("Failed to connect.")


def closeConnection():
    try:
        productsDB.close()
    except OperationalError as failed:
        print("Failed to connect.")


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
    try: 
        with productsDB.atomic():
            for product_entry in products_list:
                    if(checkUniqueness(product_entry)):
                       Product.create(**product_entry)
                    else:
                        print("Insertion failed.")
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



