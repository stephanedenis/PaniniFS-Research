import { createHash } from 'node:crypto';
export var Dhatu;
(function (Dhatu) {
    Dhatu["RELATE"] = "RELATE";
    Dhatu["MODAL"] = "MODAL";
    Dhatu["EXIST"] = "EXIST";
    Dhatu["EVAL"] = "EVAL";
    Dhatu["COMM"] = "COMM";
    Dhatu["CAUSE"] = "CAUSE";
    Dhatu["ITER"] = "ITER";
    Dhatu["DECIDE"] = "DECIDE";
    Dhatu["FEEL"] = "FEEL";
})(Dhatu || (Dhatu = {}));
export const ALL_DHATUS = Object.values(Dhatu);
export function computeDhatuVector(content) {
    const weights = [];
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
export function getTopDhatus(vector, k = 4) {
    return vector.weights
        .map((weight, i) => ({ dhatu: ALL_DHATUS[i], weight }))
        .sort((a, b) => b.weight - a.weight)
        .slice(0, k);
}
export function computeSignature(vector) {
    const hash = createHash('sha256');
    for (const weight of vector.weights) {
        const buf = Buffer.allocUnsafe(8);
        buf.writeDoubleLE(weight, 0);
        hash.update(buf);
    }
    return hash.digest('hex').slice(0, 16);
}
export function createSemanticFile(path, content, gitHash) {
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
//# sourceMappingURL=types.js.map