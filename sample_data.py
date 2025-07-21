from config import NeptuneConfig
from models import GraphModel

def populate_sample_data():
    """Populate the graph with sample data"""
    config = NeptuneConfig()
    g, connection = config.get_connection()
    
    if not g:
        print("Failed to connect to Neptune")
        return
    
    model = GraphModel(g)
    
    print("Clearing existing data...")
    g.V().drop().iterate()
    g.E().drop().iterate()
    
    print("Creating sample users...")
    users = [
        ('user1', 'Alice Johnson', 'alice@email.com', 28),
        ('user2', 'Bob Smith', 'bob@email.com', 35),
        ('user3', 'Carol Davis', 'carol@email.com', 42),
        ('user4', 'David Wilson', 'david@email.com', 29),
        ('user5', 'Eve Brown', 'eve@email.com', 33)
    ]
    
    for user_id, name, email, age in users:
        model.create_user(user_id, name, email, age)
        print(f"Created user: {name}")
    
    print("\nCreating sample products...")
    products = [
        ('prod1', 'Laptop', 'Electronics', 999.99),
        ('prod2', 'Coffee Maker', 'Appliances', 79.99),
        ('prod3', 'Python Book', 'Books', 29.99),
        ('prod4', 'Wireless Headphones', 'Electronics', 149.99),
        ('prod5', 'Desk Chair', 'Furniture', 199.99),
        ('prod6', 'Smartphone', 'Electronics', 699.99)
    ]
    
    for product_id, name, category, price in products:
        model.create_product(product_id, name, category, price)
        print(f"Created product: {name}")
    
    print("\nCreating friendships...")
    friendships = [
        ('user1', 'user2'),
        ('user1', 'user3'),
        ('user2', 'user4'),
        ('user3', 'user4'),
        ('user4', 'user5')
    ]
    
    for user1, user2 in friendships:
        model.create_friendship(user1, user2)
        print(f"Created friendship: {user1} <-> {user2}")
    
    print("\nCreating purchases...")
    purchases = [
        ('user1', 'prod1', 1, 5),
        ('user1', 'prod3', 2, 4),
        ('user2', 'prod2', 1, 5),
        ('user2', 'prod4', 1, 4),
        ('user3', 'prod1', 1, 5),
        ('user3', 'prod5', 1, 3),
        ('user4', 'prod6', 1, 5),
        ('user4', 'prod3', 1, 4),
        ('user5', 'prod2', 1, 4),
        ('user5', 'prod4', 1, 5)
    ]
    
    for user_id, product_id, quantity, rating in purchases:
        model.create_purchase(user_id, product_id, quantity, rating)
        print(f"Created purchase: {user_id} bought {product_id}")
    
    print("\nCreating recommendations...")
    recommendations = [
        ('user1', 'prod4', 0.85),
        ('user2', 'prod3', 0.72),
        ('user3', 'prod6', 0.91),
        ('user4', 'prod2', 0.68),
        ('user5', 'prod1', 0.89)
    ]
    
    for user_id, product_id, score in recommendations:
        model.create_recommendation(user_id, product_id, score)
        print(f"Created recommendation: {user_id} -> {product_id} (score: {score})")
    
    print("\nSample data populated successfully!")
    
    if connection:
        connection.close()

if __name__ == "__main__":
    populate_sample_data()