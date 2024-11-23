"""
Leipzig Programming project
Book Inventory Management task 1
A list of dictionaries in Python to store book details. They should then create functions to:
• Add a book to the inventory
• Retrieve the entire inventory
• Filter and display books by a specific author
"""
class Books:

    def __init__(this,titles,authors,prices):
            
        this.titles = titles
        this.authors = authors
        this.prices = prices

class InventoryManagement: 
    #Book records are stored into a hashmap
    bookRecords = {}
    
    def addBook():
        #This one should be a user input 
        books = Books("Mario's life","Mario","100$")
        InventoryManagement.bookRecords[books.titles] = {books.authors,books.prices} 
    def retrieveBook():
        return InventoryManagement.bookRecords.get("Mario's life")
    def retrieveInventory():
        #Full inventory
        inventory = []
        for keys,values in InventoryManagement.bookRecords.items():
            inventory.append([keys,values])
        return inventory


#class Main:
    #if __name__=="__main__":
InventoryManagement.addBook()
print(InventoryManagement.retrieveBook())
print(InventoryManagement.retrieveInventory())

    

        
        
        
        
    
    


