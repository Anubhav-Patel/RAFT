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
            #TODO send msg
        
        #TODO start election timer

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
            #TODO send vote

    def CollectVote(self, request, context):
        if self.current_role == "candidate" and request.term == self.current_term and request.granted:
            self.votes_received.add(request.node_id)
            if len(self.votes_received) >= (len(self.other_nodes) + 1) // 2:
                self.current_role = "leader"
                self.current_leader = self.node_id
                #TODO self.cancel_election_timer()
                for follower_id in self.other_nodes:
                    if follower_id != self.node_id:
                        # self.sent_length[follower_id] = len(self.log)
                        # self.acked_length[follower_id] = 0
                        self.replicate_log(follower_id)
        elif term > self.current_term:
            self.current_term = term
            self.current_role = "follower"
            self.voted_for = None
            #TODO self.cancel_election_timer()

    def broadcast_message(self, request, context):
        if self.current_role == "leader":
            self.log.append({"msg": msg, "term": self.current_term, "index": len(self.log)})
            # self.acked_length[self.node_id] = len(self.log)
            for follower_id in self.other_nodes:
                if follower_id != self.node_id:
                    self.replicate_log(follower_id)
        else:
            if self.current_leader is not None:
                #TODO self.forward_to_leader(msg)

    def replicate_log(follower_id):
        prefix_len = self.sent_length.get(follower_id, 0) 
        suffix = self.log[prefix_len:]
        prefix_term = 0
        if prefix_len > 0:
            prefix_term = self.log[prefix_len - 1]['term']
        #TODO Sending LogRequest message
        log_request_msg = ("LogRequest", self.node_id, self.current_term, prefix_len, prefix_term, self.commit_length, suffix)
        self.send_message(log_request_msg, follower_id)

    def receive_msg(self, request, context):
        if request.term > self.current_term:
            self.current_term = request.term
            self.voted_for = None
            #TODO self.cancel_election_timer()

        if request.term == self.current_term:
            self.current_role = "follower"
            self.current_leader = request.leader_id

        log_ok = (len(self.log) >= prefix_len) and (prefix_len == 0 or self.log[prefix_len - 1]['term'] == prefix_term)

        if request.term == self.current_term and log_ok:
            ack = prefix_len + len(suffix)
            self.AppendEntries(prefix_len, leader_commit, suffix)
            self.send_log_response(leader_id, ack, True)
        else:
            self.send_log_response(leader_id, 0, False)

    def AppendEntries(self, request, context):





def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    raft_pb2_grpc.add_RaftServiceServicer_to_server(RaftService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Node1 server started. Listening on port 50051.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
