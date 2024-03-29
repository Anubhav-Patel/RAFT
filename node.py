import random as randint
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
class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.current_term = 0
        # self.last_term =0
        self.voted_for = None
        self.log = Log()  #intializing log as an instance of Log
        self.commit_length = 0
        self.current_role = "follower"
        self.current_leader = None
        self.votes_received = set()
        self.other_nodes = [1,2,3,4,5]
        self.address = None
        self.election_timeout = 10
        self.election_period_ms = randint(1000, 5000)
        self.sent_length = {1:0, 2:0, 3:0, 4:0, 5:0}
        self.acked_length = {1:0, 2:0, 3:0, 4:0, 5:0}

    def recover(self):
        #TODO recover
        self.current_leader = "follower"
        self.current_leader = None
        self.votes_received = set()
        self.sent_length = {1:0, 2:0, 3:0, 4:0, 5:0}
        self.acked_length = {1:0, 2:0, 3:0, 4:0, 5:0}

class RaftService(rat_pb2_grpc.RaftServiceServicer):
    node_id = int(input("Enter Node ID: "))
    node1 = Node(node_id)

    def RequestVote(self, request, context):
        self.node1.current_term = self.node1.current_term + 1
        self.node1.current_role = "candidate"
        self.node1.voted_for = self.node1.node_id
        self.node1.votes_received = self.node1.votes_received.add(self.node_id)
        lastTerm =0
        if len(self.node1.log) > 0:
            last_term = self.node1.log.entries[len(self.node1.log.entries)-1].term
        msg = ("VoteRequest", self.node1.node_id, self.node1.current_term, len(self.node1.log.entries), lastTerm)
        for node in self.node1.other_nodes:
            self.
        # for nodes in self.other_nodes:
        #     #TODO send msg
        
        # #TODO start election timer

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
                        self.sent_length[follower_id] = len(self.log)
                        self.acked_length[follower_id] = 0
                        self.replicate_log(follower_id)

        elif term > self.current_term:
            self.current_term = term
            self.current_role = "follower"
            self.voted_for = None
            #TODO self.cancel_election_timer()

    def broadcast_msg_to_followers(self, request, context):
        if self.current_role == "leader":
            self.log.append({"msg": msg, "term": self.current_term, "index": len(self.log)})
            self.acked_length[self.node_id] = len(self.log)
            for follower_id in self.other_nodes:
                if follower_id != self.node_id:
                    self.replicate_log(follower_id)
        # else:
            # if self.current_leader is not None:
            #     #TODO self.forward_to_leader(msg)

    def replicate_log(follower_id):
        previous_len = self.sent_length.get(follower_id, 0) 
        suffix = self.log[previous_len:]
        previous_term = 0
        if previous_len > 0:
            previous_term = self.log[previous_len - 1]['term']
        
        log_request_msg = (self.log['msg'], self.node_id, self.current_term, previous_len, previous_term, self.commit_length, suffix)
        self.send_message(log_request_msg, follower_id)

    def receive_msg(self, request, context):
        if request.term > self.current_term:
            self.current_term = request.term
            self.voted_for = None
            #TODO self.cancel_election_timer()

        if request.term == self.current_term:
            self.current_role = "follower"
            self.current_leader = request.leader_id

        log_ok = (len(self.log) >= previous_len) and (previous_len == 0 or self.log[previous_len - 1]['term'] == previous_term)

        if request.term == self.current_term and log_ok:
            ack = previous_len + len(suffix)
            self.AppendEntries(previous_len, leader_commit, suffix)
            self.send_log_response(leader_id, ack, True)
        else:
            self.send_log_response(leader_id, 0, False)

    # def AppendEntries(self, request, context):





def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    raft_pb2_grpc.add_RaftServiceServicer_to_server(RaftService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Node1 server started. Listening on port 50051.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
