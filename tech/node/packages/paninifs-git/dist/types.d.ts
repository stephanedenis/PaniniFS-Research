export declare enum Dhatu {
    RELATE = "RELATE",
    MODAL = "MODAL",
    EXIST = "EXIST",
    EVAL = "EVAL",
    COMM = "COMM",
    CAUSE = "CAUSE",
    ITER = "ITER",
    DECIDE = "DECIDE",
    FEEL = "FEEL"
}
export declare const ALL_DHATUS: Dhatu[];
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
export declare function computeDhatuVector(content: Buffer): DhatuVector;
export declare function getTopDhatus(vector: DhatuVector, k?: number): DhatuWeight[];
export declare function computeSignature(vector: DhatuVector): string;
export declare function createSemanticFile(path: string, content: Buffer, gitHash?: string): SemanticFile;
//# sourceMappingURL=types.d.ts.map