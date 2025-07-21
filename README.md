# Neptune Database Demo

A comprehensive Python demo project showcasing AWS Neptune database capabilities using the Gremlin query language. This project demonstrates graph data modeling, complex traversals, and analytics queries that are essential for understanding Neptune.

## 🎯 Project Scope

This demo implements a **social e-commerce graph** with:

- **Users**: People with profiles and friendships
- **Products**: Items with categories and pricing
- **Relationships**: Purchases, friendships, and recommendations
- **Analytics**: Popular products, user networks, and recommendation systems

## 📊 Graph Schema

```
User ──[friends_with]──> User
 │
 ├──[purchased]──> Product
 │
 └──[recommended]──> Product
```

## 🚀 Quick Start

### Option 1: Local TinkerPop Server with Graph Explorer (Recommended)

1. **Start Services**:
   ```bash
   docker-compose up -d
   ```
   This starts both the Gremlin server (port 8182) and Graph Explorer (port 8080).

2. **Install Dependencies**:
   ```bash
   source .venv/bin/activate  # Activate your virtual environment
   pip install -r requirements.txt
   ```

3. **Populate Sample Data**:
   ```bash
   python demo.py
   ```

4. **Access Graph Explorer**:
   Open your browser to `http://localhost:8080/explorer`
   
   **Manual Connection Setup:**
   - Click "Add Connection" or the "+" button
   - Choose "Gremlin" as the graph type
   - Enter these connection details:
     - **Service Type**: `neptune-db`
     - **Connection URL**: `gremlin-server:8182`
     - **Use HTTPS**: `false` (unchecked)
     - **AWS IAM Auth**: `false` (unchecked)
   - Click "Connect" to test the connection
   - Start exploring your graph visually!

### Option 2: AWS Neptune

1. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your Neptune endpoint
   ```

2. **Update config.py**:
   ```python
   g, connection = config.get_connection(use_local=False)
   ```

## 📝 Key Neptune Queries Demonstrated

### Basic Graph Operations
- **Vertex Creation**: `g.addV('user').property('name', 'Alice')`
- **Edge Creation**: `g.V().has('userId', 'user1').addE('purchased').to(V().has('productId', 'prod1'))`
- **Graph Traversal**: `g.V().hasLabel('user').out('purchased')`

### Advanced Patterns
- **Friends of Friends**: `g.V().has('userId', 'user1').both('friends_with').both('friends_with')`
- **Collaborative Filtering**: `g.V().has('userId', 'user1').both('friends_with').out('purchased')`
- **Aggregation**: `g.V().hasLabel('product').group().by('category').by(count())`

### Analytics Queries
- **Popular Products**: Products ordered by purchase count
- **User Network Size**: Direct and extended friend networks
- **High-Rated Items**: Products with ratings above threshold
- **Purchase Analytics**: Total purchases, average ratings, most active users

## 🛠 Interactive Mode

```bash
python demo.py --interactive
```

Available commands:
- `users` - Show all users
- `products` - Show all products  
- `purchases <user_id>` - Show user purchases
- `friends <user_id>` - Show user friends
- `popular` - Show popular products
- `analytics` - Show purchase analytics

## 📁 Project Structure

```
neptune_demo/
├── config.py          # Neptune connection configuration
├── models.py          # Graph data models and operations
├── queries.py         # Comprehensive query examples
├── sample_data.py     # Sample data population
├── demo.py           # Main demonstration script
├── requirements.txt   # Python dependencies
├── docker-compose.yml # Local Gremlin server setup
└── .env.example      # Environment configuration template
```

## 🔍 Learning Objectives

After running this demo, you'll understand:

1. **Graph Modeling**: How to represent real-world entities and relationships
2. **Gremlin Syntax**: Core traversal patterns and query composition
3. **Neptune Operations**: CRUD operations, filtering, and aggregation
4. **Graph Analytics**: Network analysis and recommendation algorithms
5. **Best Practices**: Connection management, error handling, and performance

## 🎨 Graph Explorer Features

### Visual Exploration
- **Interactive Graph**: Click and drag nodes, zoom in/out
- **Custom Styling**: Users (👤 blue), Products (📦 green), different edge colors
- **Search & Filter**: Find specific users or products
- **Query Builder**: Visual query construction without writing Gremlin

### Pre-configured Views
- **User Networks**: See friendship connections
- **Purchase Patterns**: Visualize buying behavior  
- **Recommendations**: View recommendation relationships
- **Category Analysis**: Group products by category

### Useful Graph Explorer Queries
```gremlin
# Show all users and their friends
g.V().hasLabel('user').limit(10)

# Show purchase patterns
g.V().hasLabel('user').out('purchased').limit(20)

# Find popular products
g.V().hasLabel('product').in('purchased').groupCount().order(local).by(values, desc)
```

## 🌟 Next Steps

- **Visual Analysis**: Use Graph Explorer to discover patterns in your data
- **Custom Queries**: Try different Gremlin queries in the Graph Explorer console
- **Schema Evolution**: Modify the graph schema and see changes in real-time
- **Advanced Visualizations**: Explore different layout algorithms
- **Real Neptune**: Connect Graph Explorer to AWS Neptune clusters

## 🔧 Troubleshooting

**Connection Issues**:
- Ensure Docker is running for local setup
- Check Neptune endpoint and security groups for AWS
- Verify network connectivity and authentication

**Query Errors**:
- Check Gremlin syntax in the console output
- Ensure vertices exist before creating edges
- Validate property names and types

This demo provides a solid foundation for understanding Neptune's capabilities and Gremlin query patterns essential for graph database development.