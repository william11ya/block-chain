const Migrations = artifacts.require("Migrations");

module.exports = function(deployer) {
  deployer.deploy(Migrations);
};

var gfg = artifacts.require("gfg");
 
module.exports = function(deployer) {
    deployer.deploy(gfg);
};