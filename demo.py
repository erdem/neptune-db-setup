from sample_data import populate_sample_data, HttpNeptuneQueries


def interactive_mode():
    """Interactive mode for running custom queries"""
    print("Neptune Interactive Demo")
    print("=" * 30)
    print("Available commands:")
    print("1. users - Show all users")
    print("2. products - Show all products")
    print("3. purchases <user_id> - Show user purchases")
    print("4. friends <user_id> - Show user friends")  
    print("5. popular - Show popular products")
    print("6. analytics - Show purchase analytics")
    print("7. demo - Run full demo")
    print("8. quit - Exit")
    
    queries = HttpNeptuneQueries("http://localhost:8182")
    
    # Test connection
    try:
        queries.client.get_vertex_count()
        print("Connected to HTTP Gremlin server successfully!")
    except Exception as e:
        print(f"Failed to connect to HTTP Gremlin server: {e}")
        return
    
    try:
        while True:
            try:
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
                elif cmd == 'demo':
                    run_demo()
                else:
                    print("Invalid command or missing parameters")
                    
            except EOFError:
                print("\nGoodbye!")
                break
                
    except KeyboardInterrupt:
        print("\nGoodbye!")

if __name__ == "__main__":
    populate_sample_data()
    interactive_mode()