const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  // Deploy contract
  const Voting = await hre.ethers.getContractFactory("Voting");
  const voting = await Voting.deploy();
  await voting.waitForDeployment();
  const address = await voting.getAddress();

  // Paths configuration
  const artifactsDir = path.join(__dirname, "../artifacts/contracts");
  const reactContractsDir = path.join(__dirname, "../../election_frontend/src/contracts");
  const djangoContractsDir = path.join(__dirname, "../../election_system/contracts");

  // 1. Get existing ABI from artifacts
  const artifact = JSON.parse(
    fs.readFileSync(`${artifactsDir}/Voting.sol/Voting.json`)
  );

  // 2. Save to React (Vite)
  if (!fs.existsSync(reactContractsDir)) fs.mkdirSync(reactContractsDir, { recursive: true });
  fs.writeFileSync(
    `${reactContractsDir}/contract-address.json`,
    JSON.stringify({ Voting: address }, null, 2)
  );
  fs.writeFileSync(
    `${reactContractsDir}/Voting.json`,
    JSON.stringify(artifact, null, 2)
  );

  // 3. Save to Django
  if (!fs.existsSync(djangoContractsDir)) fs.mkdirSync(djangoContractsDir, { recursive: true });
  fs.writeFileSync(
    `${djangoContractsDir}/contract-address.json`,
    JSON.stringify({ VOTING_CONTRACT_ADDRESS: address }, null, 2)
  );
  fs.writeFileSync(
    `${djangoContractsDir}/Voting.json`,
    JSON.stringify(artifact, null, 2)
  );

  console.log(`
  ============================================
  Contract deployed to: ${address}
  Config files updated in:
  - Frontend: ${reactContractsDir}
  - Backend: ${djangoContractsDir}
  ============================================
  `);
}

main().catch(console.error);

