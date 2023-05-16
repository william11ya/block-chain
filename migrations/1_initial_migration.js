const Migrations = artifacts.require("Migrations");

module.exports = function(deployer) {
  deployer.deploy(Migrations);
};

var VotingSystem = artifacts.require("VotingSystem");
 
module.exports = function(deployer) {
    deployer.deploy(VotingSystem);
};
