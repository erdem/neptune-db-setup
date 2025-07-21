# Neptune Local Playground Setup

This project provides a local setup for AWS Neptune graph database playground. It includes a containerized Gremlin server, Python client libraries, sample data, and the AWS Graph Explorer UI for visual graph exploration.

## Project Overview

The stack includes:

- **Social E-commerce Graph Model**: Users, products, and their relationships (purchases, friendships, recommendations)
- **Local Gremlin Server**: TinkerPop server configured for HTTP connectivity  
- **AWS Graph Explorer**: Visual interface for interactive graph exploration tool

## 📊 Graph Schema

```
User ──[friends_with]──> User
 │
 ├──[purchased]──> Product
 │
 └──[recommended]──> Product
```

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ with virtual environment support

### Quick Setup

1. **Start the Stack**:
   ```bash
   docker-compose up -d
   ```
   This launches the Gremlin server (port 8182) and Graph Explorer (port 8080).

2. **Setup Python Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run Interactive Demo**:
   ```bash
   python demo.py
   ```
   
4. **Explore Visually**:
   Open `http://localhost:8080/explorer` in your browser to see the graph visualization.

### What is Gremlin?

Gremlin is a graph traversal language - like SQL for relational databases. Neptune is compatible with Apache TinkerPop and Gremlin, so you can connect to Neptune and use Gremlin to query your graphs.

### Why HTTP Instead of WebSocket?

The local setup uses HTTP instead of WebSocket because AWS Graph Explorer visual tool supports HTTP only. The Docker Compose Gremlin server is configured with `HttpChannelizer` rather than the default `WebSocketChannelizer`. This makes the local environment fully compatible with Graph Explorer while maintaining all Gremlin functionality. For production Neptune work, you'd typically use secure WebSocket connections.

## Working with Real Neptune

To connect this demo to an actual AWS Neptune cluster:

1. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your Neptune cluster details
   ```

2. **Update Connection**:
   The Python client supports both HTTP (local) and WebSocket (Neptune) connections. For Neptune, it automatically uses WebSocket with proper authentication.

## Graph Queries and Patterns

```gremlin
// Create vertices and edges
g.addV('user').property('name', 'Alice')
g.V().has('userId', 'user1').addE('purchased').to(V().has('productId', 'prod1'))

// Basic traversals
g.V().hasLabel('user').out('purchased')
g.V().has('userId', 'user1').both('friends_with')
```

```gremlin
// Friends of friends (social network expansion)
g.V().has('userId', 'user1').both('friends_with').both('friends_with').dedup()

// Collaborative filtering (recommendation basis)
g.V().has('userId', 'user1').both('friends_with').out('purchased').dedup()

// Popular products by purchase count
g.V().hasLabel('product').project('product', 'count')
  .by(valueMap('name', 'category'))
  .by(__.in('purchased').count())
  .order().by(select('count'), desc)
```

## Project Structure

```
neptune_demo/
├── demo.py                  # Interactive demo and query runner
├── sample_data.py           # HTTP client, queries, and data population
├── config.py                # Connection configuration (for Neptune)
├── docker-compose.yml       # Container orchestration
├── sample/conf/             # Gremlin server HTTP configuration
└── graph-explorer-config/   # Graph Explorer workspace settings
```
