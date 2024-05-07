# Network Simulator 

In computer network research, network simulation is a technique whereby a software program replicates the behavior of a real network. 

### Prerequisites

- Python 3.6 or higher
- `git` installed on your machine


## Installation

Install Aihcon Patients Service Project

Step 1: Clone the Repository
```shell
git clone https://github.com/aihcon-jahid/network-simulator.git
```

Step 2: Navigate to the Project Directory
```shell
cd network-simulator
```

Step 3: Create a Virtual Environment
```shell
python -m venv .venv
```

Step 4: Activate the Virtual Environment

- On Windows:
```shell
.venv\Scripts\activate
```

Step 5: Install Dependencies
```shell
pip install -r requirements.txt
```


Step 6: Executing the Program
```shell
python main.py
```


## Python Scripts

```shell
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

```




## PostgreSQL Scripts

```shell
-- Create a table to store additional information about nodes
CREATE TABLE IF NOT EXISTS NodeDetails (
    id SERIAL PRIMARY KEY,
    node_id INT NOT NULL,
    description TEXT,
    location VARCHAR(255),
    FOREIGN KEY (node_id) REFERENCES Nodes(id)
);

-- Create a table to store network events
CREATE TABLE IF NOT EXISTS NetworkEvents (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(255) NOT NULL,
    event_description TEXT,
    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data into NodeDetails table
INSERT INTO NodeDetails (node_id, description, location) VALUES (1, 'Main server node', 'Data center A');
INSERT INTO NodeDetails (node_id, description, location) VALUES (2, 'Backup server node', 'Data center B');

-- Insert sample data into NetworkEvents table
INSERT INTO NetworkEvents (event_type, event_description) VALUES ('NodeFailure', 'Node1 is down');
INSERT INTO NetworkEvents (event_type, event_description) VALUES ('NodeRecovery', 'Node1 is back up');

```



