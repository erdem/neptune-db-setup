from gremlin_python.process.graph_traversal import __
from gremlin_python.process.traversal import T
from datetime import datetime

class GraphModel:
    def __init__(self, g):
        self.g = g
        
    def create_user(self, user_id, name, email, age):
        """Create a user vertex"""
        return (self.g.addV('user')
                .property('userId', user_id)
                .property('name', name)
                .property('email', email)
                .property('age', age)
                .property('createdAt', datetime.now().isoformat())
                .next())
    
    def create_product(self, product_id, name, category, price):
        """Create a product vertex"""
        return (self.g.addV('product')
                .property('productId', product_id)
                .property('name', name)
                .property('category', category)
                .property('price', price)
                .property('createdAt', datetime.now().isoformat())
                .next())
    
    def create_purchase(self, user_id, product_id, quantity=1, rating=None):
        """Create a purchase relationship between user and product"""
        edge = (self.g.V().has('user', 'userId', user_id).as_('u')
                .V().has('product', 'productId', product_id).as_('p')
                .addE('purchased').from_('u').to('p')
                .property('quantity', quantity)
                .property('purchaseDate', datetime.now().isoformat()))
        
        if rating:
            edge = edge.property('rating', rating)
            
        return edge.next()
    
    def create_friendship(self, user_id1, user_id2):
        """Create a friendship relationship between two users"""
        return (self.g.V().has('user', 'userId', user_id1).as_('u1')
                .V().has('user', 'userId', user_id2).as_('u2')
                .addE('friends_with').from_('u1').to('u2')
                .property('createdAt', datetime.now().isoformat())
                .next())
    
    def create_recommendation(self, user_id, product_id, score):
        """Create a recommendation relationship"""
        return (self.g.V().has('user', 'userId', user_id).as_('u')
                .V().has('product', 'productId', product_id).as_('p')
                .addE('recommended').from_('u').to('p')
                .property('score', score)
                .property('createdAt', datetime.now().isoformat())
                .next())