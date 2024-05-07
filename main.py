import psycopg2

class NetworkSimulator:
    def __init__(self):
        # Establishing connection to PostgreSQL database
        self.conn = psycopg2.connect(
            dbname="network_simulation",
            user="aihcon",
            password="27673855",
            host="localhost"
        )
        self.cur = self.conn.cursor()

    def add_node(self, node_id, description, location):
        # Adding a node to the network
        self.cur.execute("INSERT INTO NodeDetails (node_id, description, location) VALUES (%s, %s, %s)", (node_id, description, location))
        self.conn.commit()

    def add_edge(self, source, destination, weight):
        # Adding an edge (connection) between nodes with a certain weight
        self.cur.execute("INSERT INTO NetworkEvents (event_type, event_description) VALUES (%s, %s)", ("DataTransmission", f"Sending data from {source} to {destination} with weight {weight}"))
        self.conn.commit()

    def create_topology(self):
        # Displaying the network topology
        self.cur.execute("SELECT node_id, ARRAY(SELECT node_id FROM NodeDetails WHERE node_id != n.node_id) as neighbors FROM NodeDetails n")
        rows = self.cur.fetchall()
        print("Network Topology:")
        for row in rows:
            print(f"Node {row[0]} is connected to: {', '.join(map(str, row[1]))}")

    def simulate_network(self):
        # Simulating network behavior by retrieving and displaying network events
        self.cur.execute("SELECT event_description FROM NetworkEvents WHERE event_type = 'DataTransmission'")
        rows = self.cur.fetchall()
        print("Simulating network behavior...")
        for row in rows:
            print(row[0])

    def close_connection(self):
        # Closing the database connection
        self.cur.close()
        self.conn.close()

# Instantiate the network simulator
simulator = NetworkSimulator()

# Add nodes and edges
simulator.add_node(1, 'Main server node', 'Data center A')
simulator.add_node(2, 'Backup server node', 'Data center B')
simulator.add_edge(1, 2, 5)
simulator.add_edge(2, 3, 3)

# Create and simulate network
simulator.create_topology()
simulator.simulate_network()

# Close the connection
simulator.close_connection()
