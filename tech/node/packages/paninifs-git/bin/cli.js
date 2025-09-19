#!/usr/bin/env node
import { simpleGit } from 'simple-git';
import { readFile, writeFile } from 'fs/promises';
import { createSemanticFile, Dhatu } from '../dist/types.js';

function parseArgs() {
  const [,, command, ...args] = process.argv;
  return { command: command || 'help', args };
}

async function browseRepo(repoPath) {
  console.log(`🔍 Browsing repository: ${repoPath}`);
  
  const git = simpleGit(repoPath);
  const status = await git.status();
  
  console.log(`📊 Repository status:`);
  console.log(`  Branch: ${status.current}`);
  console.log(`  Files: ${status.files.length} modified`);
  
  // Get recent commits
  const log = await git.log({ maxCount: 5 });
  console.log(`\n📝 Recent commits:`);
  for (const commit of log.all) {
    console.log(`  ${commit.hash.slice(0, 8)} - ${commit.message} (${commit.author_name})`);
  }
  
  // Analyze some files
  console.log(`\n🧬 Dhātu analysis of key files:`);
  const keyFiles = ['README.md', 'package.json', '.gitignore'];
  
  for (const file of keyFiles) {
    try {
      const content = await readFile(`${repoPath}/${file}`);
      const semantic = createSemanticFile(file, content);
      console.log(`  ${file}:`);
      console.log(`    Signature: ${semantic.signature}`);
      console.log(`    Top dhātu: ${semantic.topDhatus.map(d => `${d.dhatu}(${d.weight.toFixed(3)})`).join(', ')}`);
    } catch (e) {
      console.log(`  ${file}: Not found`);
    }
  }
}

async function indexRepo(repoPath, outputPath = 'paninifs-index.json') {
  console.log(`📇 Indexing repository: ${repoPath}`);
  
  const git = simpleGit(repoPath);
  const files = await git.raw(['ls-files']).then(result => 
    result.split('\n').filter(f => f.trim())
  );
  
  const index = {
    version: '0.1.0',
    created: new Date(),
    gitRepo: repoPath,
    files: {},
    bySignature: {},
    byDhatu: {},
    virtualFiles: {}
  };
  
  // Initialize dhatu buckets
  for (const dhatu of Object.values(Dhatu)) {
    index.byDhatu[dhatu] = [];
  }
  
  let processed = 0;
  for (const file of files.slice(0, 20)) { // Limit for demo
    try {
      const content = await readFile(`${repoPath}/${file}`);
      const semantic = createSemanticFile(file, content);
      
      index.files[file] = semantic;
      
      // Index by signature
      if (!index.bySignature[semantic.signature]) {
        index.bySignature[semantic.signature] = [];
      }
      index.bySignature[semantic.signature].push(file);
      
      // Index by primary dhātu
      if (semantic.topDhatus[0]) {
        index.byDhatu[semantic.topDhatus[0].dhatu].push(file);
      }
      
      processed++;
      if (processed % 5 === 0) {
        console.log(`  Processed ${processed}/${Math.min(files.length, 20)} files...`);
      }
    } catch (e) {
      console.log(`  Skipped ${file}: ${e}`);
    }
  }
  
  await writeFile(outputPath, JSON.stringify(index, null, 2));
  console.log(`\n✅ Index written to: ${outputPath}`);
  console.log(`📊 Statistics:`);
  console.log(`  Files indexed: ${Object.keys(index.files).length}`);
  console.log(`  Unique signatures: ${Object.keys(index.bySignature).length}`);
  
  // Show dhātu distribution
  console.log(`\n🧬 Dhātu distribution:`);
  for (const [dhatu, fileList] of Object.entries(index.byDhatu)) {
    if (fileList.length > 0) {
      console.log(`  ${dhatu}: ${fileList.length} files`);
    }
  }
}

function showHelp() {
  console.log(`PaniniFS Git Interface

Usage:
  paninifs-git browse <repo-path>     Browse repository with dhātu analysis
  paninifs-git index <repo-path>      Create semantic index of repository
  paninifs-git help                   Show this help

Examples:
  paninifs-git browse .
  paninifs-git index . my-index.json
`);
}

async function main() {
  const { command, args } = parseArgs();
  
  try {
    switch (command) {
      case 'browse':
        await browseRepo(args[0] || '.');
        break;
      case 'index':
        await indexRepo(args[0] || '.', args[1]);
        break;
      case 'help':
      default:
        showHelp();
        break;
    }
  } catch (error) {
    console.error('❌ Error:', error);
    process.exit(1);
  }
}

main();