import grpc
import raft_pb2
import raft_pb2_grpc

class LogEntry:
    def __init__(self, term, msg):
        self.term = term
        self.msg = msg

class Log:
    def __init__(self):
        self.entries = []

    def append_entry(self, term, msg):
        self.entries.append(LogEntry(term, msg))

class RaftNode:
    def __init__(self, nodeId, nodes):
        self.nodeId = nodeId
        self.nodes = nodes
        self.currentTerm = 0
        self.votedFor = None
        self.log = Log()
        self.commitLength = 0
        self.currentRole = "follower"
        self.currentLeader = None
        self.votesReceived = {}
        self.sentLength = len(self.log.entries)
        self.ackedLength = len(self.log.entries)

        # Connect to other nodes using gRPC channel
        self.grpc_channels = {}
        for node_id, node_address in self.nodes.items():
            if node_id != self.nodeId:  # Skip connecting to itself
                self.grpc_channels[node_id] = grpc.insecure_channel(node_address)

    def append_to_log(self, msg, term):
        self.log.append_entry(term, msg)

    def send_msg(self, msg, receiver):
        # Create gRPC stub for the receiver node
        stub = raft_pb2_grpc.RaftNodeStub(self.grpc_channels[receiver])

        # Convert message to gRPC format
        grpc_msg = raft_pb2.Message(
            msg_type=msg[0],
            sender=self.nodeId,
            term=self.currentTerm,
            log_length=len(self.log.entries),
            last_log_term=self.log.entries[-1].term if self.log.entries else 0
        )

        # Send message using gRPC
        response = stub.ReceiveMessage(grpc_msg)

    def start_leader_election(self):
        self.currentTerm += 1
        self.currentRole = "candidate"
        self.votedFor = self.nodeId
        self.votesReceived = {self.nodeId}
        lastTerm = 0
        if len(self.log.entries) >0:
            lastTerm = self.log.entries[len(self.log.entries)-1].term
        msg = ("VoteRequest", self.nodeId, self.currentTerm, len(self.log.entries), lastTerm)
        for node in self.nodes:
            self.send_msg(msg, node)
        self.start_election_timer()

    def on_receive_vote_request(self, cId, cTerm, cLogLength, cLogTerm):
        if cTerm > self.currentTerm:
            self.currentTerm = cTerm
            self.currentRole = "follower"
            self.votedFor = None

        lastTerm = 0
        if len(self.log.entries) >0:
            lastTerm = self.log.entries[len(self.log.entries)-1].term

        logOk = (cLogTerm > lastTerm) or (cLogTerm == lastTerm and cLogLength >= len(self.log.entries))

        if cTerm == self.currentTerm and logOk and self.votedFor in {cId, None}:
            self.votedFor = cId
            self.send_msg(("VoteResponse", self.nodeId, self.currentTerm, True), cId)
        else:
            self.send_msg(("VoteResponse", self.nodeId, self.currentTerm, False), cId)

    def on_leader_election_timeout(self):
        if self.currentRole == "follower":
            self.start_leader_election()

    def start_election_timer(self):
        pass  # Placeholder for starting the election timer

    def recover_from_crash(self):
        self.currentRole = "follower"
        self.currentLeader = None
        self.votesReceived = {}
        self.sentLength = len(self.log.entries)
        self.ackedLength = len(self.log.entries)

    def on_receive_vote_request(self, cId, cTerm, cLogLength, cLogTerm):
        if cTerm > self.currentTerm:
            self.currentTerm = cTerm
            self.currentRole = "follower"
            self.votedFor = None

        lastTerm = 0
        if self.log.entries:
            lastTerm = self.log.entries[-1].term

        logOk = (cLogTerm > lastTerm) or (cLogTerm == lastTerm and cLogLength >= len(self.log.entries))

        if cTerm == self.currentTerm and logOk and self.votedFor in {cId, None}:
            self.votedFor = cId
            self.send_msg(("VoteResponse", self.nodeId, self.currentTerm, True), cId)
        else:
            self.send_msg(("VoteResponse", self.nodeId, self.currentTerm, False), cId)

    def on_receive_vote_response(self, voterId, term, voteGranted):
        if term == self.currentTerm and voteGranted:
            self.votesReceived.add(voterId)
            if len(self.votesReceived) > len(self.nodes) // 2:
                self.currentRole = "leader"
                self.currentLeader = self.nodeId

# Define nodes and their addresses
nodes = {
    "node1": "localhost:50051",
    "node2": "localhost:50052",
    "node3": "localhost:50053",
    "node4": "localhost:50054",
    "node5": "localhost:50055"
}

# Create Raft nodes
raft_nodes = {}
for node_id, node_address in nodes.items():
    raft_nodes[node_id] = RaftNode(node_id, nodes)
