from gremlin_python.process.graph_traversal import __
from gremlin_python.process.traversal import T, Order, P
from config import NeptuneConfig

class NeptuneQueries:
    def __init__(self):
        self.config = NeptuneConfig()
        self.g, self.connection = self.config.get_connection()
        
    def close_connection(self):
        if self.connection:
            self.connection.close()
    
    def get_all_users(self):
        """Get all users in the graph"""
        print("=== All Users ===")
        users = self.g.V().hasLabel('user').valueMap().toList()
        for user in users:
            print(f"User: {user}")
        return users
    
    def get_all_products(self):
        """Get all products in the graph"""
        print("=== All Products ===")
        products = self.g.V().hasLabel('product').valueMap().toList()
        for product in products:
            print(f"Product: {product}")
        return products
    
    def get_user_purchases(self, user_id):
        """Get all products purchased by a specific user"""
        print(f"=== Purchases by User {user_id} ===")
        purchases = (self.g.V().has('user', 'userId', user_id)
                    .out('purchased')
                    .valueMap('productId', 'name', 'category', 'price')
                    .toList())
        for purchase in purchases:
            print(f"Purchased: {purchase}")
        return purchases
    
    def get_user_friends(self, user_id):
        """Get all friends of a specific user"""
        print(f"=== Friends of User {user_id} ===")
        friends = (self.g.V().has('user', 'userId', user_id)
                  .both('friends_with')
                  .valueMap('userId', 'name', 'email')
                  .toList())
        for friend in friends:
            print(f"Friend: {friend}")
        return friends
    
    def get_popular_products(self, limit=5):
        """Get most purchased products"""
        print(f"=== Top {limit} Popular Products ===")
        popular = (self.g.V().hasLabel('product')
                  .project('product', 'purchaseCount')
                  .by(__.valueMap('productId', 'name', 'category'))
                  .by(__.in_('purchased').count())
                  .order().by(__.select('purchaseCount'), Order.desc)
                  .limit(limit)
                  .toList())
        for item in popular:
            print(f"Product: {item}")
        return popular
    
    def get_recommendations_for_user(self, user_id):
        """Get product recommendations for a user"""
        print(f"=== Recommendations for User {user_id} ===")
        recommendations = (self.g.V().has('user', 'userId', user_id)
                          .out('recommended')
                          .valueMap('productId', 'name', 'category', 'price')
                          .toList())
        for rec in recommendations:
            print(f"Recommended: {rec}")
        return recommendations
    
    def get_friends_purchases(self, user_id):
        """Get products purchased by friends of a user (collaborative filtering basis)"""
        print(f"=== What Friends of User {user_id} Bought ===")
        friend_purchases = (self.g.V().has('user', 'userId', user_id)
                           .both('friends_with')
                           .out('purchased')
                           .dedup()
                           .valueMap('productId', 'name', 'category', 'price')
                           .toList())
        for purchase in friend_purchases:
            print(f"Friend purchased: {purchase}")
        return friend_purchases
    
    def get_products_by_category(self, category):
        """Get all products in a specific category"""
        print(f"=== Products in {category} Category ===")
        products = (self.g.V().hasLabel('product')
                   .has('category', category)
                   .valueMap('productId', 'name', 'price')
                   .toList())
        for product in products:
            print(f"Product: {product}")
        return products
    
    def get_high_rated_products(self, min_rating=4):
        """Get products with high ratings"""
        print(f"=== Products with Rating >= {min_rating} ===")
        high_rated = (self.g.E().hasLabel('purchased')
                     .has('rating', P.gte(min_rating))
                     .inV()
                     .dedup()
                     .valueMap('productId', 'name', 'category', 'price')
                     .toList())
        for product in high_rated:
            print(f"High-rated product: {product}")
        return high_rated
    
    def get_user_network_size(self, user_id):
        """Get the size of a user's network (friends + friends of friends)"""
        print(f"=== Network Size for User {user_id} ===")
        
        # Direct friends
        direct_friends = (self.g.V().has('user', 'userId', user_id)
                         .both('friends_with')
                         .count()
                         .next())
        
        # Friends of friends (excluding self and direct friends)
        friends_of_friends = (self.g.V().has('user', 'userId', user_id)
                             .both('friends_with')
                             .both('friends_with')
                             .where(__.not_(__.has('userId', user_id)))
                             .dedup()
                             .count()
                             .next())
        
        print(f"Direct friends: {direct_friends}")
        print(f"Extended network: {friends_of_friends}")
        return {'direct_friends': direct_friends, 'extended_network': friends_of_friends}
    
    def get_purchase_analytics(self):
        """Get analytics about purchases"""
        print("=== Purchase Analytics ===")
        
        # Total purchases
        total_purchases = self.g.E().hasLabel('purchased').count().next()
        
        # Average rating
        avg_rating = (self.g.E().hasLabel('purchased')
                     .has('rating')
                     .values('rating')
                     .mean()
                     .next())
        
        # Most active user
        most_active = (self.g.V().hasLabel('user')
                      .project('user', 'purchaseCount')
                      .by(__.values('name'))
                      .by(__.out('purchased').count())
                      .order().by(__.select('purchaseCount'), Order.desc)
                      .limit(1)
                      .next())
        
        print(f"Total purchases: {total_purchases}")
        print(f"Average rating: {avg_rating:.2f}")
        print(f"Most active user: {most_active}")
        
        return {
            'total_purchases': total_purchases,
            'average_rating': avg_rating,
            'most_active_user': most_active
        }