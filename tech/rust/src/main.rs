use clap::{Parser, Subcommand};
use paninifs_core::{DhatuVector, SemanticFile, SemanticIndex};
use std::fs;
use std::path::Path;
use anyhow::Result;

#[derive(Parser)]
#[command(name = "paninifs")]
#[command(about = "PaniniFS - Semantic filesystem based on dhātu universals")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Analyze a file's semantic content
    Analyze {
        /// File path to analyze
        file: String,
    },
    /// Index a directory
    Index {
        /// Directory to index
        dir: String,
        /// Output index file
        #[arg(short, long, default_value = "paninifs-index.json")]
        output: String,
    },
    /// Mount filesystem (requires FUSE)
    Mount {
        /// Mount point
        mountpoint: String,
        /// Source directory or index
        source: String,
    },
}

fn analyze_file(path: &str) -> Result<()> {
    let content = fs::read(path)?;
    let semantic_file = SemanticFile::from_content(path.to_string(), &content);
    
    println!("{}", serde_json::to_string_pretty(&semantic_file)?);
    Ok(())
}

fn index_directory(dir: &str, output: &str) -> Result<()> {
    let mut index = SemanticIndex::new();
    
    fn visit_dir(dir: &Path, index: &mut SemanticIndex) -> Result<()> {
        if dir.is_dir() {
            for entry in fs::read_dir(dir)? {
                let entry = entry?;
                let path = entry.path();
                if path.is_dir() {
                    visit_dir(&path, index)?;
                } else if let Some(path_str) = path.to_str() {
                    if let Ok(content) = fs::read(&path) {
                        let semantic_file = SemanticFile::from_content(path_str.to_string(), &content);
                        index.add_file(semantic_file);
                        println!("Indexed: {}", path_str);
                    }
                }
            }
        }
        Ok(())
    }
    
    visit_dir(Path::new(dir), &mut index)?;
    
    // Serialize index to JSON
    let index_json = serde_json::to_string_pretty(&index)?;
    fs::write(output, index_json)?;
    
    println!("Index written to: {}", output);
    Ok(())
}

fn main() -> Result<()> {
    tracing_subscriber::init();
    
    let cli = Cli::parse();
    
    match cli.command {
        Commands::Analyze { file } => {
            analyze_file(&file)?;
        }
        Commands::Index { dir, output } => {
            index_directory(&dir, &output)?;
        }
        Commands::Mount { mountpoint: _, source: _ } => {
            println!("FUSE mounting not yet implemented - use analyze/index for now");
            // TODO: Implement FUSE filesystem
        }
    }
    
    Ok(())
}