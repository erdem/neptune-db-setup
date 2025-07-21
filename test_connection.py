#!/usr/bin/env python3
"""
Test script to verify Gremlin server connectivity
"""
from config import NeptuneConfig

def test_connection():
    config = NeptuneConfig()
    
    # Test with container hostname
    print("Testing connection to gremlin-server:8182...")
    try:
        # Update config to use container hostname
        config.local_endpoint = 'ws://gremlin-server:8182/gremlin'
        g, connection = config.get_connection()
        if g:
            count = g.V().count().next()
            print(f"✅ Connected successfully! Vertex count: {count}")
            connection.close()
        else:
            print("❌ Failed to connect")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    # Test with localhost
    print("\nTesting connection to localhost:8182...")
    try:
        config.local_endpoint = 'ws://localhost:8182/gremlin'
        g, connection = config.get_connection()
        if g:
            count = g.V().count().next()
            print(f"✅ Connected successfully! Vertex count: {count}")
            connection.close()
        else:
            print("❌ Failed to connect")
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    test_connection()