use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::collections::HashMap;

/// Core dhātu universals from Panini's linguistic theory
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum Dhatu {
    RELATE,
    MODAL,
    EXIST,
    EVAL,
    COMM,
    CAUSE,
    ITER,
    DECIDE,
    FEEL,
}

impl Dhatu {
    pub const ALL: [Dhatu; 9] = [
        Dhatu::RELATE, Dhatu::MODAL, Dhatu::EXIST, Dhatu::EVAL, Dhatu::COMM,
        Dhatu::CAUSE, Dhatu::ITER, Dhatu::DECIDE, Dhatu::FEEL,
    ];
    
    pub fn as_str(&self) -> &'static str {
        match self {
            Dhatu::RELATE => "RELATE",
            Dhatu::MODAL => "MODAL",
            Dhatu::EXIST => "EXIST",
            Dhatu::EVAL => "EVAL",
            Dhatu::COMM => "COMM",
            Dhatu::CAUSE => "CAUSE",
            Dhatu::ITER => "ITER",
            Dhatu::DECIDE => "DECIDE",
            Dhatu::FEEL => "FEEL",
        }
    }
}

/// Semantic vector representation of content
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DhatuVector {
    pub weights: [f64; 9],
}

impl DhatuVector {
    pub fn from_content(content: &[u8]) -> Self {
        let mut weights = [0.0; 9];
        
        for (i, dhatu) in Dhatu::ALL.iter().enumerate() {
            let mut hasher = Sha256::new();
            hasher.update(dhatu.as_str().as_bytes());
            hasher.update(b"::");
            hasher.update(content);
            let hash = hasher.finalize();
            
            // Use hash bytes to create stable weight
            let w = hash[0] as u32 + hash[5] as u32 + hash[13] as u32 + hash[21] as u32 + hash[29] as u32;
            weights[i] = w as f64 / 1024.0;
        }
        
        // L1 normalize
        let sum: f64 = weights.iter().sum();
        if sum > 0.0 {
            for weight in &mut weights {
                *weight /= sum;
            }
        }
        
        Self { weights }
    }
    
    pub fn top_dhatus(&self, k: usize) -> Vec<(Dhatu, f64)> {
        let mut pairs: Vec<_> = Dhatu::ALL.iter()
            .zip(self.weights.iter())
            .map(|(dhatu, weight)| (*dhatu, *weight))
            .collect();
        
        pairs.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
        pairs.truncate(k);
        pairs
    }
    
    pub fn signature(&self) -> String {
        let mut hasher = Sha256::new();
        for weight in &self.weights {
            hasher.update(&weight.to_le_bytes());
        }
        let hash = hasher.finalize();
        format!("{:x}", &hash[..8])
    }
}

/// File metadata with semantic information
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SemanticFile {
    pub path: String,
    pub size: u64,
    pub dhatu_vector: DhatuVector,
    pub signature: String,
    pub top_dhatus: Vec<(Dhatu, f64)>,
}

impl SemanticFile {
    pub fn from_content(path: String, content: &[u8]) -> Self {
        let dhatu_vector = DhatuVector::from_content(content);
        let signature = dhatu_vector.signature();
        let top_dhatus = dhatu_vector.top_dhatus(4);
        
        Self {
            path,
            size: content.len() as u64,
            dhatu_vector,
            signature,
            top_dhatus,
        }
    }
}

/// In-memory semantic index
#[derive(Debug, Default)]
pub struct SemanticIndex {
    files: HashMap<String, SemanticFile>,
    by_signature: HashMap<String, Vec<String>>,
    by_dhatu: HashMap<Dhatu, Vec<String>>,
}

impl SemanticIndex {
    pub fn new() -> Self {
        Self::default()
    }
    
    pub fn add_file(&mut self, file: SemanticFile) {
        let path = file.path.clone();
        let signature = file.signature.clone();
        
        // Index by primary dhatu
        if let Some((primary_dhatu, _)) = file.top_dhatus.first() {
            self.by_dhatu.entry(*primary_dhatu).or_default().push(path.clone());
        }
        
        // Index by signature
        self.by_signature.entry(signature).or_default().push(path.clone());
        
        // Store file
        self.files.insert(path, file);
    }
    
    pub fn find_by_dhatu(&self, dhatu: Dhatu) -> Vec<&SemanticFile> {
        self.by_dhatu.get(&dhatu)
            .map(|paths| paths.iter().filter_map(|p| self.files.get(p)).collect())
            .unwrap_or_default()
    }
    
    pub fn find_by_signature(&self, signature: &str) -> Vec<&SemanticFile> {
        self.by_signature.get(signature)
            .map(|paths| paths.iter().filter_map(|p| self.files.get(p)).collect())
            .unwrap_or_default()
    }
    
    pub fn get_file(&self, path: &str) -> Option<&SemanticFile> {
        self.files.get(path)
    }
}