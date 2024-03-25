import grpc
from concurrent import futures
import raft_pb2
import raft_pb2_grpc
import os
import time

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
        self.other_nodes = {1:0, 2:0, 3:0, 4:0, 5:0}
        self.address = None
        self.election_timeout = 10
        self.election_period_ms = randint(1000, 5000)
        self.sent_length = {1:0, 2:0, 3:0, 4:0, 5:0}
        self.acked_length = {1:0, 2:0, 3:0, 4:0, 5:0}


class RaftService(rat_pb2_grpc.RaftServiceServicer):
    int node_id = int(input("Enter Node ID: "))
    node1 = Node(node_id)

    def recover():
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as log_file:
                pass
        if not os.path.exists(self.meta_file):
            with open(self.meta_file, "w") as meta_file:
                meta_file.write(f"node_id: {self.node_id}\n")
                meta_file.write(f"currTerm: {self.currTerm}\n")
                meta_file.write(f"votedFor: {self.votedFor}\n")
                meta_file.write(f"commitLength: {self.commitLength}\n")

    def start_election_timer(self, request, context):
        while self.election_timeout > 0:
            time.sleep(1)
            self.election_timeout -= 1
            if self.election_timeout <= 0:
                self.start_election()
                break

    def cancel_election_timer():
        self.election_timeout = 0

    def RequestVote(self, request, context):
        self.current_term = self.current_term + 1
        self.current_role = "candidate"
        self.voted_for = self.node_id
        self.votes_received = self.votes_received.add(self.node_id)

        if self.log:
            last_term = self.log[-1]['term']
        else:
            last_term = 0
        
        vote_request_msg = ("VoteRequest", self.node_id, self.current_term, len(self.log), last_term)
        
        for node in self.other_nodes:
            node_pb2.RequestVote(term = self.current_term, candidate_id = self.)

        self.start_election_timer()        



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
                self.cancel_election_timer()
                for follower_id in self.other_nodes:
                    if follower_id != self.node_id:
                        self.sent_length[follower_id] = len(self.log)
                        self.acked_length[follower_id] = 0
                        self.replicate_log(follower_id)

        elif term > self.current_term:
            self.current_term = term
            self.current_role = "follower"
            self.voted_for = None
            self.cancel_election_timer()


    def broadcast_msg_to_followers(self, request, context):
        if self.current_role == "leader":
            self.log.append({"msg": msg, "term": self.current_term, "index": len(self.log)})
            self.acked_length[self.node_id] = len(self.log)
            for follower_id in self.other_nodes:
                if follower_id != self.node_id:
                    self.replicate_log(follower_id)
        else:
            if self.current_leader is not None:
                # self.forward_to_leader(msg)


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
            self.cancel_election_timer()

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
                self.replicate_log(self.node_id, follower)
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
                self.replicate_log(self.node_id, follower)
        elif term > self.current_term:
            self.current_term = term
            self.current_role = "follower"
            self.voted_for = None
            self.cancel_election_timer()





def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    raft_pb2_grpc.add_RaftServiceServicer_to_server(RaftService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Node1 server started. Listening on port 50051.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
