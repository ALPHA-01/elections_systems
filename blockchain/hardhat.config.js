// require("@nomicfoundation/hardhat-toolbox");
// require("dotenv").config();

// /** @type import('hardhat/config').HardhatUserConfig */
// module.exports = {
//   solidity: "0.8.19",
//   networks: {
//     hardhat: {
//       chainId: 1337, // Local development network
//     },
//     // For testnet (Sepolia for example)
//     sepolia: {
//       url: process.env.SEPOLIA_URL || "",
//       accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
//     },
//     // For mainnet when ready for production
//     mainnet: {
//       url: process.env.MAINNET_URL || "",
//       accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
//     }
//   },
//   paths: {
//    artifacts: "../election_frontend/src/contracts",
//     cache: "./cache",
//     sources: "./contracts",
//     tests: "./test",
//   },
// };

require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: "0.8.19",
  networks: {
    localhost: {
      url: "http://127.0.0.1:8545"
    }
  }
};