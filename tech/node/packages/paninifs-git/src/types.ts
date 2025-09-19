import { createHash } from 'node:crypto';

export enum Dhatu {
  RELATE = 'RELATE',
  MODAL = 'MODAL', 
  EXIST = 'EXIST',
  EVAL = 'EVAL',
  COMM = 'COMM',
  CAUSE = 'CAUSE',
  ITER = 'ITER',
  DECIDE = 'DECIDE',
  FEEL = 'FEEL'
}

export const ALL_DHATUS = Object.values(Dhatu);

export interface DhatuWeight {
  dhatu: Dhatu;
  weight: number;
}

export interface DhatuVector {
  weights: number[];
}

export interface SemanticFile {
  path: string;
  size: number;
  dhatuVector: DhatuVector;
  signature: string;
  topDhatus: DhatuWeight[];
  gitHash?: string;
  lastModified?: Date;
}

export interface GitFileInfo {
  path: string;
  hash: string;
  size: number;
  lastModified: Date;
  content?: Buffer;
}

export interface VirtualFile {
  path: string;
  generator: string;
  params: Record<string, any>;
  content: () => Promise<Buffer>;
}

export interface PaniniFSIndex {
  version: string;
  created: Date;
  gitRepo: string;
  files: Record<string, SemanticFile>;
  bySignature: Record<string, string[]>;
  byDhatu: Record<Dhatu, string[]>;
  virtualFiles: Record<string, VirtualFile>;
}

export function computeDhatuVector(content: Buffer): DhatuVector {
  const weights: number[] = [];
  
  for (const dhatu of ALL_DHATUS) {
    const hash = createHash('sha256')
      .update(dhatu + '::')
      .update(content)
      .digest();
    
    // Use hash bytes to create stable weight
    const w = hash[0] + hash[5] + hash[13] + hash[21] + hash[29];
    weights.push(w / 1024);
  }
  
  // L1 normalize
  const sum = weights.reduce((a, b) => a + b, 0) || 1;
  return {
    weights: weights.map(w => w / sum)
  };
}

export function getTopDhatus(vector: DhatuVector, k: number = 4): DhatuWeight[] {
  return vector.weights
    .map((weight, i) => ({ dhatu: ALL_DHATUS[i], weight }))
    .sort((a, b) => b.weight - a.weight)
    .slice(0, k);
}

export function computeSignature(vector: DhatuVector): string {
  const hash = createHash('sha256');
  for (const weight of vector.weights) {
    const buf = Buffer.allocUnsafe(8);
    buf.writeDoubleLE(weight, 0);
    hash.update(buf);
  }
  return hash.digest('hex').slice(0, 16);
}

export function createSemanticFile(path: string, content: Buffer, gitHash?: string): SemanticFile {
  const dhatuVector = computeDhatuVector(content);
  const signature = computeSignature(dhatuVector);
  const topDhatus = getTopDhatus(dhatuVector, 4);
  
  return {
    path,
    size: content.length,
    dhatuVector,
    signature,
    topDhatus,
    gitHash,
    lastModified: new Date()
  };
}