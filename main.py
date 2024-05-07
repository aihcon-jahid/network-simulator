import psycopg2

class NetworkSimulator:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, edge):
        self.edges.append(edge)

    def create_topology(self):
        topology = {}
        for node in self.nodes:
            topology[node] = []
        for edge in self.edges:
            source, destination = edge
            topology[source].append(destination)
            topology[destination].append(source)
        print("Network Topology:")
        for node, neighbors in topology.items():
            print(f"Node {node} is connected to: {', '.join(neighbors)}")

    def simulate_network(self):
        print("Simulating network behavior...")
        for node in self.nodes:
            neighbors = self.get_neighbors(node)
            print(f"Node {node} is connected to: {', '.join(neighbors)}")

    def get_neighbors(self, node):
        return [edge[1] for edge in self.edges if edge[0] == node or edge[1] == node]


# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname="network_simulation",
    user="khadiza",
    password="12345678",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Create table for NodeDetails if not exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS NodeDetails (
        id SERIAL PRIMARY KEY,
        node_id INT NOT NULL,
        description TEXT,
        location VARCHAR(255)
    );
""")

# Create table for NetworkEvents if not exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS NetworkEvents (
        id SERIAL PRIMARY KEY,
        event_type VARCHAR(255) NOT NULL,
        event_description TEXT,
        event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")

# Insert data into NodeDetails
node_data = [
    (1, 'Main server node', 'Data center A'),
    (2, 'Backup server node', 'Data center B')
]
cur.executemany("INSERT INTO NodeDetails (node_id, description, location) VALUES (%s, %s, %s)", node_data)

# Insert data into NetworkEvents
event_data = [
    ('NodeFailure', 'Node1 is down'),
    ('NodeRecovery', 'Node1 is back up')
]
cur.executemany("INSERT INTO NetworkEvents (event_type, event_description) VALUES (%s, %s)", event_data)

# Commit changes to the database
conn.commit()
cur.close()
conn.close()

# Create NetworkSimulator instance
simulator = NetworkSimulator()
simulator.add_node("Node1")
simulator.add_node("Node2")
simulator.add_node("Node3")
simulator.add_edge(("Node1", "Node2"))
simulator.add_edge(("Node2", "Node3"))
simulator.create_topology()
simulator.simulate_network()
