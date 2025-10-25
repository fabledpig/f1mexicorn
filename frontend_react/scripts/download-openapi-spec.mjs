import { spawn } from 'child_process';
import { writeFileSync } from 'fs';
import path from 'path';

function cdToBackendDir() {
  const scriptsDir = import.meta.dirname;
  const backendDir = path.join(scriptsDir, '..', '..', 'backend');
  process.chdir(backendDir);
}

function runBackend() {
  const process = spawn('uvicorn', ['app.main:app', '--reload']);
  process.stdout.on('data', (data) => {
    console.log(`${data}`);
  });

  process.stderr.on('data', (data) => {
    console.log(`${data}`);
  });

  return process;
}

async function tryToDownloadOpenApiConfig() {
  const response = await fetch('http://localhost:8000/openapi.json');
  if (response.status != 200 || !response.body) {
    return null;
  }

  return Buffer.from(await response.arrayBuffer());
}

function saveBufferToFile(buffer, path) {
  writeFileSync(path, buffer);
}

if (process.argv.length < 3) {
  console.error('Missing arguments');
  process.exit(-1);
}

const targetPath = path.resolve(process.argv[2]);

cdToBackendDir();

const backendProcess = runBackend();
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
await sleep(5000);
const buffer = await tryToDownloadOpenApiConfig();

if (!backendProcess.kill()) {
  console.error('Failed to stop backend process');
}

if (!buffer) {
  process.exit(-1);
}

saveBufferToFile(buffer, targetPath);
process.exit(0);
