// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VotingSystem {

    struct VoteEvent {
        string voteName;
        address owner;
        uint voteEndTime;
        mapping(address => bool) hasVoted;
        Candidate[] candidates;
    }

    struct Candidate {
        string name;
        uint voteCount;
    }

    mapping(uint => VoteEvent) voteEvents; 
    uint index = 0;

    function CreateVote(string memory voteName, string[] memory candidateNames, uint endTime) public returns (uint) {
        require(isVoteExist(voteName) == false, "This vote already exist");

        voteEvents[index].voteEndTime = block.timestamp + endTime;
        voteEvents[index].voteName = voteName;
        voteEvents[index].owner = msg.sender;
        for (uint i = 0; i < candidateNames.length; i++) {
            voteEvents[index].candidates.push(Candidate(candidateNames[i], 0));
        }
        return index++;
    }

    function isVoteExist(string memory voteName) public view returns (bool) {
        bool check = false;
        for (uint i = 0; i < index; i++) 
        {
            if(keccak256(abi.encodePacked(voteEvents[i].voteName)) == keccak256(abi.encodePacked(voteName))){
                check = true;
            }           
        }
        return check;
    }

    function getVoteIndex(string memory voteName) public view returns (int) {
        int a = -1;
        for (uint i = 0; i < index; i++) 
        {
            if(keccak256(abi.encodePacked(voteEvents[i].voteName)) == keccak256(abi.encodePacked(voteName))){
                a = int(i);    
            } 
        }
        return a;
    }

    //測試用fuction，我沒有辦法用js寫加快時間的測試
    function speedTimeForTestingOnly(uint voteId) public {        
        voteEvents[voteId].voteEndTime = 0;
    }

    function vote(uint voteId, uint candidateIndex) public {
        require(voteId <= index - 1, "Vote ID out of range");
        // VoteEvent memory _vt = voteEvents[voteId];
        require(block.timestamp <= voteEvents[voteId].voteEndTime, "Voting has ended.");
        // 验证投票人是否已经投过票
        require(!voteEvents[voteId].hasVoted[msg.sender], "You have already voted.");
        // 验证候选人是否存在
        require(candidateIndex < voteEvents[voteId].candidates.length, "Invalid candidate index.");
        require(voteEvents[voteId].owner != msg.sender, "You are the owner of this vote.");
        // 记录投票人已投票
        voteEvents[voteId].hasVoted[msg.sender] = true;
        // 增加候选人的得票数
        voteEvents[voteId].candidates[candidateIndex].voteCount++;
    }

    function settle(uint voteId) public view returns (string memory) {
        require(voteId <= index - 1, "Vote ID out of range");
        // VoteEvent memory _vt = voteEvent[voteId];
        require(block.timestamp >= voteEvents[voteId].voteEndTime, "Voting is not yet over.");

        // 查找得票数最高的候选人
        uint maxVoteCount = 0;
        uint winningCandidateIndex = 0;
        for (uint i = 0; i < voteEvents[voteId].candidates.length; i++) {
            if (voteEvents[voteId].candidates[i].voteCount > maxVoteCount) {
                maxVoteCount = voteEvents[voteId].candidates[i].voteCount;
                winningCandidateIndex = i;
            }
        }

        // 返回获胜的候选人名称
        return voteEvents[voteId].candidates[winningCandidateIndex].name;
    }

    string[] Tmp;
    function getAllRunningVote() public returns (string[] memory) {
        delete Tmp;
        for (uint i = 0; i < index; i++) 
        {
            if(voteEvents[i].voteEndTime > block.timestamp)
            {
                Tmp.push(voteEvents[i].voteName);
            }
        }
        return Tmp;
    }

    function getAllCandidatesName(uint voteId) public returns (string[] memory) {
        require(voteId <= index - 1, "Vote ID out of range");
        delete Tmp;
        for (uint i = 0; i < voteEvents[voteId].candidates.length; i++) 
        {
            Tmp.push(voteEvents[voteId].candidates[i].name);
        }
        return Tmp;
    }

    function getEndTime(uint voteId) public view returns (uint) {
        require(voteId <= index - 1, "Vote ID out of range");
        return voteEvents[voteId].voteEndTime;
    }
}
