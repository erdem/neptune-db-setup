import requests
import json
from datetime import datetime

class HttpGremlinClient:
    def __init__(self, url):
        self.url = url.rstrip('/')
        self.session = requests.Session()
    
    def execute(self, gremlin_query):
        """Execute a raw Gremlin query via HTTP"""
        payload = {
            "gremlin": gremlin_query
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        try:
            response = self.session.post(
                f"{self.url}/gremlin",
                json=payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Query execution failed: {e}")
            return None
    
    def clear_graph(self):
        """Clear all vertices and edges"""
        print("Clearing existing data...")
        self.execute("g.V().drop().iterate()")
        self.execute("g.E().drop().iterate()")
    
    def create_user(self, user_id, name, email, age):
        """Create a user vertex"""
        query = f"""
        g.addV('user')
         .property('userId', '{user_id}')
         .property('name', '{name}')
         .property('email', '{email}')
         .property('age', {age})
         .property('createdAt', '{datetime.now().isoformat()}')
        """
        return self.execute(query)
    
    def create_product(self, product_id, name, category, price):
        """Create a product vertex"""
        query = f"""
        g.addV('product')
         .property('productId', '{product_id}')
         .property('name', '{name}')
         .property('category', '{category}')
         .property('price', {price})
         .property('createdAt', '{datetime.now().isoformat()}')
        """
        return self.execute(query)
    
    def create_friendship(self, user_id1, user_id2):
        """Create friendship between two users"""
        query = f"""
        g.V().has('user', 'userId', '{user_id1}').as('u1')
         .V().has('user', 'userId', '{user_id2}').as('u2')
         .addE('friends_with').from('u1').to('u2')
         .property('createdAt', '{datetime.now().isoformat()}')
        """
        return self.execute(query)
    
    def create_purchase(self, user_id, product_id, quantity=1, rating=None):
        """Create purchase relationship"""
        query = f"""
        g.V().has('user', 'userId', '{user_id}').as('u')
         .V().has('product', 'productId', '{product_id}').as('p')
         .addE('purchased').from('u').to('p')
         .property('quantity', {quantity})
         .property('purchaseDate', '{datetime.now().isoformat()}')
        """
        if rating:
            query += f".property('rating', {rating})"
        return self.execute(query)
    
    def create_recommendation(self, user_id, product_id, score):
        """Create recommendation relationship"""
        query = f"""
        g.V().has('user', 'userId', '{user_id}').as('u')
         .V().has('product', 'productId', '{product_id}').as('p')
         .addE('recommended').from('u').to('p')
         .property('score', {score})
         .property('createdAt', '{datetime.now().isoformat()}')
        """
        return self.execute(query)
    
    def get_vertex_count(self):
        """Get total vertex count"""
        result = self.execute("g.V().count()")
        if result and 'result' in result and 'data' in result['result']:
            return result['result']['data'][0]
        return 0

class HttpNeptuneQueries:
    def __init__(self, url="http://localhost:8182"):
        self.client = HttpGremlinClient(url)
        
    def get_all_users(self):
        """Get all users in the graph"""
        print("=== All Users ===")
        result = self.client.execute("g.V().hasLabel('user').valueMap()")
        if result and 'result' in result and 'data' in result['result']:
            users = result['result']['data']
            for user in users:
                print(f"User: {user}")
            return users
        return []
    
    def get_all_products(self):
        """Get all products in the graph"""
        print("=== All Products ===")
        result = self.client.execute("g.V().hasLabel('product').valueMap()")
        if result and 'result' in result and 'data' in result['result']:
            products = result['result']['data']
            for product in products:
                print(f"Product: {product}")
            return products
        return []
    
    def get_user_purchases(self, user_id):
        """Get all products purchased by a specific user"""
        print(f"=== Purchases by User {user_id} ===")
        query = f"""
        g.V().has('user', 'userId', '{user_id}')
         .out('purchased')
         .valueMap('productId', 'name', 'category', 'price')
        """
        result = self.client.execute(query)
        if result and 'result' in result and 'data' in result['result']:
            purchases = result['result']['data']
            for purchase in purchases:
                print(f"Purchased: {purchase}")
            return purchases
        return []
    
    def get_user_friends(self, user_id):
        """Get all friends of a specific user"""
        print(f"=== Friends of User {user_id} ===")
        query = f"""
        g.V().has('user', 'userId', '{user_id}')
         .both('friends_with')
         .valueMap('userId', 'name', 'email')
        """
        result = self.client.execute(query)
        if result and 'result' in result and 'data' in result['result']:
            friends = result['result']['data']
            for friend in friends:
                print(f"Friend: {friend}")
            return friends
        return []
    
    def get_popular_products(self, limit=5):
        """Get most purchased products"""
        print(f"=== Top {limit} Popular Products ===")
        query = f"""
        g.V().hasLabel('product')
         .project('product', 'purchaseCount')
         .by(valueMap('productId', 'name', 'category'))
         .by(__.in('purchased').count())
         .order().by(select('purchaseCount'), desc)
         .limit({limit})
        """
        result = self.client.execute(query)
        if result and 'result' in result and 'data' in result['result']:
            popular = result['result']['data']
            for item in popular:
                print(f"Product: {item}")
            return popular
        return []
    
    def get_recommendations_for_user(self, user_id):
        """Get product recommendations for a user"""
        print(f"=== Recommendations for User {user_id} ===")
        query = f"""
        g.V().has('user', 'userId', '{user_id}')
         .out('recommended')
         .valueMap('productId', 'name', 'category', 'price')
        """
        result = self.client.execute(query)
        if result and 'result' in result and 'data' in result['result']:
            recommendations = result['result']['data']
            for rec in recommendations:
                print(f"Recommended: {rec}")
            return recommendations
        return []
    
    def get_friends_purchases(self, user_id):
        """Get products purchased by friends of a user"""
        print(f"=== What Friends of User {user_id} Bought ===")
        query = f"""
        g.V().has('user', 'userId', '{user_id}')
         .both('friends_with')
         .out('purchased')
         .dedup()
         .valueMap('productId', 'name', 'category', 'price')
        """
        result = self.client.execute(query)
        if result and 'result' in result and 'data' in result['result']:
            friend_purchases = result['result']['data']
            for purchase in friend_purchases:
                print(f"Friend purchased: {purchase}")
            return friend_purchases
        return []
    
    def get_products_by_category(self, category):
        """Get all products in a specific category"""
        print(f"=== Products in {category} Category ===")
        query = f"""
        g.V().hasLabel('product')
         .has('category', '{category}')
         .valueMap('productId', 'name', 'price')
        """
        result = self.client.execute(query)
        if result and 'result' in result and 'data' in result['result']:
            products = result['result']['data']
            for product in products:
                print(f"Product: {product}")
            return products
        return []
    
    def get_high_rated_products(self, min_rating=4):
        """Get products with high ratings"""
        print(f"=== Products with Rating >= {min_rating} ===")
        query = f"""
        g.E().hasLabel('purchased')
         .has('rating', gte({min_rating}))
         .inV()
         .dedup()
         .valueMap('productId', 'name', 'category', 'price')
        """
        result = self.client.execute(query)
        if result and 'result' in result and 'data' in result['result']:
            high_rated = result['result']['data']
            for product in high_rated:
                print(f"High-rated product: {product}")
            return high_rated
        return []
    
    def get_user_network_size(self, user_id):
        """Get the size of a user's network"""
        print(f"=== Network Size for User {user_id} ===")
        
        # Direct friends
        query1 = f"""
        g.V().has('user', 'userId', '{user_id}')
         .both('friends_with')
         .count()
        """
        result1 = self.client.execute(query1)
        direct_friends = 0
        if result1 and 'result' in result1 and 'data' in result1['result']:
            direct_friends = result1['result']['data'][0]
        
        # Friends of friends  
        query2 = f"""
        g.V().has('user', 'userId', '{user_id}')
         .both('friends_with')
         .both('friends_with')
         .where(__.not(__.has('userId', '{user_id}')))
         .dedup()
         .count()
        """
        result2 = self.client.execute(query2)
        friends_of_friends = 0
        if result2 and 'result' in result2 and 'data' in result2['result']:
            friends_of_friends = result2['result']['data'][0]
        
        print(f"Direct friends: {direct_friends}")
        print(f"Extended network: {friends_of_friends}")
        return {'direct_friends': direct_friends, 'extended_network': friends_of_friends}
    
    def get_purchase_analytics(self):
        """Get analytics about purchases"""
        print("=== Purchase Analytics ===")
        
        # Total purchases
        query1 = "g.E().hasLabel('purchased').count()"
        result1 = self.client.execute(query1)
        total_purchases = 0
        if result1 and 'result' in result1 and 'data' in result1['result']:
            total_purchases = result1['result']['data'][0]
        
        # Average rating
        query2 = "g.E().hasLabel('purchased').has('rating').values('rating').mean()"
        result2 = self.client.execute(query2)
        avg_rating = 0.0
        if result2 and 'result' in result2 and 'data' in result2['result']:
            avg_rating = result2['result']['data'][0]
        
        # Most active user
        query3 = """
        g.V().hasLabel('user')
         .project('user', 'purchaseCount')
         .by(values('name'))
         .by(out('purchased').count())
         .order().by(select('purchaseCount'), desc)
         .limit(1)
        """
        result3 = self.client.execute(query3)
        most_active = {}
        if result3 and 'result' in result3 and 'data' in result3['result'] and result3['result']['data']:
            most_active = result3['result']['data'][0]
        
        print(f"Total purchases: {total_purchases}")
        print(f"Average rating: {avg_rating:.2f}")
        print(f"Most active user: {most_active}")
        
        return {
            'total_purchases': total_purchases,
            'average_rating': avg_rating,
            'most_active_user': most_active
        }

def populate_sample_data():
    """Populate the graph with sample data"""
    # Connect to HTTP Gremlin server
    client = HttpGremlinClient("http://localhost:8182")
    
    # Test connection
    try:
        client.get_vertex_count()
        print("Connected to Gremlin server successfully!")
    except Exception as e:
        print(f"Failed to connect to Gremlin server: {e}")
        return
    
    # Clear existing data
    client.clear_graph()
    
    print("Creating sample users...")
    users = [
        ('user1', 'Alice Johnson', 'alice@email.com', 28),
        ('user2', 'Bob Smith', 'bob@email.com', 35),
        ('user3', 'Carol Davis', 'carol@email.com', 42),
        ('user4', 'David Wilson', 'david@email.com', 29),
        ('user5', 'Eve Brown', 'eve@email.com', 33)
    ]
    
    for user_id, name, email, age in users:
        client.create_user(user_id, name, email, age)
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
        client.create_product(product_id, name, category, price)
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
        client.create_friendship(user1, user2)
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
        client.create_purchase(user_id, product_id, quantity, rating)
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
        client.create_recommendation(user_id, product_id, score)
        print(f"Created recommendation: {user_id} -> {product_id} (score: {score})")
    
    # Show final count
    vertex_count = client.get_vertex_count()
    print(f"\nSample data populated successfully! Total vertices: {vertex_count}")

if __name__ == "__main__":
    populate_sample_data()