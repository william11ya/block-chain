const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("VotingSystem", function () {
  let VotingSystem;
  let votingSystem;
  let owner;
  let addr1;
  let addr2;
  let addr3;
  let candidateNames1;
  let candidateNames2;
  let v1
  let v2

  beforeEach(async function () {
    VotingSystem = await ethers.getContractFactory("VotingSystem");
    [owner, addr1, addr2, addr3] = await ethers.getSigners();
    candidateNames1 = ["Alice", "Bob", "Charlie"];
    candidateNames2 = ["Paul", "Stephen", "Samuel"];
    v1 = "vote one"
    v2 = "vote two"

    votingSystem = await VotingSystem.deploy();
    await votingSystem.deployed();
    await votingSystem.connect(owner).CreateVote(v1,candidateNames1, 1000);
    await votingSystem.connect(owner).CreateVote(v2,candidateNames2, 1000);
  });

  it("Get vote index currect", async function () {
      let num1 = await votingSystem.connect(owner).getVoteIndex(v1);
      let num2 = await votingSystem.connect(owner).getVoteIndex(v2);
      expect(num1).to.equal("0x00");
      expect(num2).to.equal("0x01");
  });

  it("Get vote index -no vote", async function () {
      let num = await votingSystem.connect(owner).getVoteIndex("77777");
      await expect(num).to.equal("-0x01");
  });

  it("Owner should not vote", async function () {
      await expect(votingSystem.connect(owner).vote(1,0)).to.be.revertedWith("You are the owner of this vote.");
  });

  it("Voting time haven't ended yet", async function () {
      await votingSystem.connect(addr1).vote(1, 0);
      await votingSystem.connect(addr2).vote(1, 0);
      await votingSystem.connect(addr3).vote(1, 1);
      await expect(votingSystem.settle(1)).to.be.revertedWith("Voting is not yet over.");
  });

  it("Voting time has ended", async function () {
      await votingSystem.connect(owner).speedTimeForTestingOnly(1);
      await expect(votingSystem.connect(addr1).vote(1, 0)).to.be.revertedWith("Voting has ended.");
  });


  // it("Should set candidates correctly", async function () {
  //   console.log(candidate);
  //   for (let i = 0; i < candidateNames1.length; i++) {
      
  //     expect(candidate.name).to.equal(candidateNames1[i]);
  //     expect(candidate.voteCount).to.equal(0);
  //   }
  // });

  it("Should allow users to vote and not vote twice", async function () {
    await votingSystem.connect(addr1).vote(1, 0);
    await expect(votingSystem.connect(addr1).vote(1, 1)).to.be.revertedWith("You have already voted.");
    await votingSystem.connect(owner).speedTimeForTestingOnly(1);
    expect(await votingSystem.settle(1)).to.equal("Paul");
  });

  it("Should not allow voting for invalid candidate index", async function () {
    await expect(votingSystem.connect(addr1).vote(1, 3)).to.be.revertedWith("Invalid candidate index.");
  });

  it("Should correctly settle the election", async function () {
    await votingSystem.connect(addr1).vote(1, 0);
    await votingSystem.connect(addr2).vote(1, 0);
    await votingSystem.connect(addr3).vote(1, 1);

    await votingSystem.connect(owner).speedTimeForTestingOnly(1);

    const winner = await votingSystem.settle(1);
    expect(winner).to.equal("Paul");
  });
});
