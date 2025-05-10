const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Helper function to start a process
function startProcess(command, args, options) {
  const proc = spawn(command, args, {
    ...options,
    stdio: 'inherit'
  });
  
  proc.on('error', (error) => {
    console.error(`Error starting ${command}:`, error);
  });
  
  return proc;
}

// Start the Hardhat node
console.log('Starting local Hardhat node...');
const hardhatProc = startProcess(
  'npx', 
  ['hardhat', 'node'], 
  { cwd: path.join(__dirname, 'blockchain') }
);

// Wait a bit for the node to initialize
setTimeout(() => {
  // Deploy contracts to local node
  console.log('Deploying contracts to local node...');
  const deployProc = spawn(
    'npx', 
    ['hardhat', 'run', 'scripts/deploy.js', '--network', 'localhost'], 
    { 
      cwd: path.join(__dirname, 'blockchain'),
      stdio: 'inherit'
    }
  );
  
  deployProc.on('close', (code) => {
    if (code !== 0) {
      console.error('Contract deployment failed');
      return;
    }
    
    console.log('Contracts deployed successfully!');
    
    // Start Django development server
    console.log('Starting Django server...');
    const djangoProc = startProcess(
      'python', 
      ['manage.py', 'runserver'], 
      { cwd: path.join(__dirname, 'backend') }
    );
    
    // Start Vite development server
    console.log('Starting Vite development server...');
    const viteProc = startProcess(
      'npm', 
      ['run', 'dev'], 
      { cwd: path.join(__dirname, 'frontend') }
    );
    
    // Handle process termination
    const cleanup = () => {
      console.log('Shutting down all services...');
      hardhatProc.kill();
      djangoProc.kill();
      viteProc.kill();
      process.exit(0);
    };
    
    process.on('SIGINT', cleanup);
    process.on('SIGTERM', cleanup);
  });
}, 5000);

console.log('Starting development environment...');