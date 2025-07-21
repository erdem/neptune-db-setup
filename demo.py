#!/usr/bin/env python3
"""
Neptune Database Demo

This demo showcases various Neptune/Gremlin operations including:
- Graph data modeling (users, products, relationships)
- Basic CRUD operations
- Complex graph traversals
- Analytics queries
- Recommendation systems basics

Usage:
1. Set up local TinkerPop server or configure Neptune endpoint in .env
2. Install dependencies: pip install -r requirements.txt
3. Run: python demo.py
"""

import sys
from sample_data import populate_sample_data
from queries import NeptuneQueries

def run_demo():
    print("🚀 Neptune Database Demo")
    print("=" * 50)
    
    # Populate sample data
    print("\n📊 Setting up sample data...")
    try:
        populate_sample_data()
    except Exception as e:
        print(f"❌ Failed to populate data: {e}")
        print("Make sure you have a Gremlin server running locally or Neptune configured.")
        return
    
    # Initialize queries
    queries = NeptuneQueries()
    
    if not queries.g:
        print("❌ Failed to connect to Neptune/Gremlin server")
        return
    
    print("\n🔍 Running demonstration queries...")
    print("=" * 50)
    
    try:
        # Basic queries
        queries.get_all_users()
        print()
        
        queries.get_all_products()
        print()
        
        # User-specific queries
        queries.get_user_purchases('user1')
        print()
        
        queries.get_user_friends('user1')
        print()
        
        # Recommendation queries
        queries.get_recommendations_for_user('user1')
        print()
        
        queries.get_friends_purchases('user1')
        print()
        
        # Analytics queries
        queries.get_popular_products(3)
        print()
        
        queries.get_products_by_category('Electronics')
        print()
        
        queries.get_high_rated_products(4)
        print()
        
        # Network analysis
        queries.get_user_network_size('user1')
        print()
        
        # Purchase analytics
        queries.get_purchase_analytics()
        print()
        
        print("✅ Demo completed successfully!")
        print("\n📝 Key Gremlin Concepts Demonstrated:")
        print("- Vertex creation and properties: addV(), property()")
        print("- Edge creation: addE().from().to()")
        print("- Graph traversal: V(), out(), in(), both()")
        print("- Filtering: has(), where()")
        print("- Aggregation: count(), mean(), dedup()")
        print("- Projection: project(), by()")
        print("- Ordering: order(), limit()")
        print("- Complex patterns: friends-of-friends, collaborative filtering")
        
    except Exception as e:
        print(f"❌ Query execution failed: {e}")
    finally:
        queries.close_connection()

def interactive_mode():
    """Simple interactive mode for running custom queries"""
    print("\n🔧 Interactive Mode")
    print("=" * 30)
    print("Available commands:")
    print("1. users - Show all users")
    print("2. products - Show all products")
    print("3. purchases <user_id> - Show user purchases")
    print("4. friends <user_id> - Show user friends")
    print("5. popular - Show popular products")
    print("6. analytics - Show purchase analytics")
    print("7. quit - Exit")
    
    queries = NeptuneQueries()
    
    if not queries.g:
        print("❌ Failed to connect to Neptune/Gremlin server")
        return
    
    try:
        while True:
            command = input("\n> ").strip().split()
            
            if not command:
                continue
            
            cmd = command[0].lower()
            
            if cmd == 'quit':
                break
            elif cmd == 'users':
                queries.get_all_users()
            elif cmd == 'products':
                queries.get_all_products()
            elif cmd == 'purchases' and len(command) > 1:
                queries.get_user_purchases(command[1])
            elif cmd == 'friends' and len(command) > 1:
                queries.get_user_friends(command[1])
            elif cmd == 'popular':
                queries.get_popular_products()
            elif cmd == 'analytics':
                queries.get_purchase_analytics()
            else:
                print("❌ Invalid command or missing parameters")
                
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    finally:
        queries.close_connection()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        interactive_mode()
    else:
        run_demo()