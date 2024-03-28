import grpc
from concurrent import futures
import raft_pb2
import raft_pb2_grpc
import os
import time
import random
import threading
    

class RaftService(raft_pb2_grpc.RaftServiceServicer):
    def __init__(self, node_id):
        self.node_id = node_id
        self.current_term = 0
        self.voted_for = None
        self.log = []
        self.commit_length = 0
        self.current_role = "follower"
        self.current_leader = None
        self.votes_received = set()
        self.other_nodes = [50051, 50052, 50053, 50054, 50055]
        self.address = None
        self.election_timeout = 10
        self.election_period_ms = random.randint(1000, 5000)
        self.sent_length = {1:0, 2:0, 3:0, 4:0, 5:0}
        self.acked_length = {1:0, 2:0, 3:0, 4:0, 5:0}
        thread = threading.Thread(target=self.start_election_timer)
        thread.start()
        # self.start_election_timer()
        
    def start_election_timer(self):
        i = 1
        while(i >= 0):
            if(i == 0):
                self.start_election()
                print(self.current_role)
                i = 1
            time.sleep(1)
            i = i-1


    def start_election(self):
        self.current_term = self.current_term + 1
        self.current_role = "candidate"
        self.voted_for = self.node_id
        self.votes_received.add(self.node_id)
        
        last_term = 0
        if len(self.log) > 0:
            self.last_term = self.log[len(self.log) - 1].term
        
        try:
            for nodes in self.other_nodes:
                if nodes != self.node_id:

                    # print("xxx")
                    channel = grpc.insecure_channel(f'localhost:{nodes}')  
                    stub = raft_pb2_grpc.RaftServiceStub(channel)
                    vote_request = raft_pb2.RequestVoteRequest(term = self.current_term, candidate_id = self.node_id, last_log_index = len(self.log), last_log_term = last_term)
                    response = stub.RequestVote(vote_request)
                    time.sleep(1)
                    print(response.vote_granted)
                    self.CollectVote(response)
                    # if(response.vote_granted == True):
                    #     self.votes_received.add(nodes.node_id)
        except:
            print("Err")
            
        # start_election_timer(self)


    def RequestVote(self, request, context):
        print(request.term)
        print(self.current_term)
        if request.term > self.current_term:
            self.current_term = request.term
            self.voted_for = None
            self.current_role = "Follower"
            self.current_leader = None
        if request.term < self.current_term:
            
            return raft_pb2.RequestVoteResponse(term=self.current_term, vote_granted=False)
        if self.voted_for is None or self.voted_for == request.candidate_id:
            self.voted_for = request.candidate_id
            self.votes_received.add(request.candidate_id)
            return raft_pb2.RequestVoteResponse(term=self.current_term, vote_granted=True)
        return raft_pb2.RequestVoteResponse(term=self.current_term, vote_granted=False)


    def CollectVote(self, response):
        if self.current_role == "candidate" and response.term == self.current_term and response.vote_granted:
            if len(self.votes_received) >= (len(self.other_nodes) + 1) // 2:
                self.current_role = "leader"
                self.current_leader = self.node_id
                # self.cancel_election_timer()
                for follower_id in self.other_nodes:
                    if follower_id != self.node_id:
                        self.sent_length[follower_id] = len(self.log)
                        self.acked_length[follower_id] = 0
                        self.ReplicateLog(follower_id)

        elif response.term > self.current_term:
            self.current_term = response.term
            self.current_role = "follower"
            self.voted_for = None
            # self.cancel_election_timer()


    def broadcast_msg_to_followers(self, request, context):
        if self.current_role == "leader":
            self.log.append({"msg": msg, "term": self.current_term, "index": len(self.log)})
            self.acked_length[self.node_id] = len(self.log)
            for follower_id in self.other_nodes:
                if follower_id != self.node_id:
                    self.ReplicateLog(follower_id)
        # else:
        #     if self.current_leader is not None:
                # self.forward_to_leader(msg)


    def ReplicateLog(self, follower_id):
        previous_len = self.sent_length.get(follower_id, 0) 
        suffix = self.log[previous_len:]
        previous_term = 0
        if previous_len > 0:
            previous_term = self.log[previous_len - 1]['term']
        
        if(len(self.log) == 0):
            last_log_msg = ""
        else:
            last_log_msg = self.log[-1]['msg']
        # log_request_msg = raft_pb2.AppendEntries(term = self.current_term, leader_id = self.node_id, prev_log_index = len(self.log)-1, prev_log_term = previous_term, suffix, leader_commit = self.leader_commit)    
        


    def logRequest(self, request, context):
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


    def AppendEntries(self, request, context):
        suffix = request.suffix
        prefix_len = request.prefix_len
        leader_commit = request.leader_commit

        if suffix and len(self.log) > prefix_len:
            index = min(len(self.log), prefix_len + len(suffix)) - 1
            if self.log[index]['term'] != suffix[index - prefix_len]['term']:
                self.log = self.log[:prefix_len]

        if prefix_len + len(suffix) > len(self.log):
            for i in range(len(self.log) - prefix_len, len(suffix)):
                self.log.append(suffix[i])

        if leader_commit > self.commit_length:
            for i in range(self.commit_length, leader_commit):
                self.deliver_to_application(self.log[i]['msg'])
            self.commit_length = leader_commit


    def ack(self, request, context):
        term = request.term
        ack =request.ack
        success = request.success
        follower = request.follower

        if term == self.current_term and self.current_role == "leader":
            if success and ack >= self.acked_length.get(follower, 0):
                self.sent_length[follower] = ack
                self.acked_length[follower] = ack
                self.commit_log_entries()
            elif self.sent_length.get(follower, 0) > 0:
                self.sent_length[follower] -= 1
                self.ReplicateLog(self.node_id, follower)
        elif term > self.current_term:
            self.current_term = term
            self.current_role = "follower"
            self.voted_for = None
            self.cancel_election_timer()


    def commit(self, request, context):
        term = request.term
        ack =request.ack
        follower = request.follower

        if term == self.current_term and self.current_role == "leader":
            if success and ack >= self.acked_length.get(follower, 0):
                self.sent_length[follower] = ack
                self.acked_length[follower] = ack
                self.commit_log_entries()
            elif self.sent_length.get(follower, 0) > 0:
                self.sent_length[follower] -= 1
                self.ReplicateLog(self.node_id, follower)
        elif term > self.current_term:
            self.current_term = term
            self.current_role = "follower"
            self.voted_for = None
            self.cancel_election_timer()
    

if __name__ == '__main__':
    node_id = int(input("Enter Node ID: "))

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    raft_pb2_grpc.add_RaftServiceServicer_to_server(RaftService(node_id), server)
    server.add_insecure_port(f'[::]:{node_id}')
    server.start()
    print("Node1 server started. Listening on port 50051.")
    server.wait_for_termination()

    # while True:
    #     print(f"Node {node_id} - Role: {raft_node.current_role}, Term: {raft_node.current_term}")
    #     time.sleep(5)