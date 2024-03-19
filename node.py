class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.current_term = 0
        self.voted_for = None
        self.log = []
        self.commit_length = 0
        self.current_role = "follower"
        self.current_leader = None
        self.votes_received = set()
        self.other_nodes = [2,3,4,5]

def recover():
    

class RaftService(rat_pb2_grpc.RaftServiceServicer):
    # int node_id = int(input("Enter Node ID: "))
    node1 = Node(1)

    def RequestVote(self, request, context):
        self.current_term = self.current_term + 1
        self.current_role = "candidate"
        self.voted_for = self.node_id
        self.votes_received = self.votes_received.add(self.node_id)

        for nodes in self.other_nodes:
            #send msg
        
        #start election timer

    def giveVote(self, request, context):
        if(request.current_term > self.current_term):
            self.current_term = request.current_term
            self.current_role = "follower"
        
        last_term = 0
        if self.log:
            last_term = self.log[-1].term

        if request.log:
            candidate_log_term = request.log[-1].term

        log_ok = (candidate_log_term > last_term) or (candidate_log_term == last_term and len(request.log) >= len(self.log))

        if request.current_term == self.current_term and log_ok and (self.voted_for in {request.node_id, None}):  #if voted for the candidate in the same term
            self.voted_for = candidate_id
            #send vote

    def CollectVote(self, request, context):
        



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    raft_pb2_grpc.add_RaftServiceServicer_to_server(RaftService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Node1 server started. Listening on port 50051.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
