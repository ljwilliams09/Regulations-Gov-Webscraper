import pandas as pd

def parse_comments(comments_file: str, dockets_file: str, output_file: str) -> None:
    chunk_size = 1_000_000
    
    # Load docket IDs
    dockets = pd.read_csv(dockets_file)
    docket_ids = set(dockets["id"])  # e.g., "AMS-2005-0016"
    
    # Add dash so we don't accidentally match substrings (e.g., "AMS-2005-001" vs "AMS-2005-0016")
    docket_prefixes = tuple(d + "-" for d in docket_ids)
    
    first = True
    for chunk in pd.read_csv(comments_file, chunksize=chunk_size):
        # Keep only rows where comment_id starts with a docket prefix
        mask = chunk["comment_id"].str.startswith(docket_prefixes)
        filtered = chunk[mask].copy()
        
        # Extract docket_id as everything up to the last dash (fallback if format changes later)
        filtered["docket_id"] = filtered["comment_id"].str.split("-").str[:3].str.join("-")
        
        # Write results
        filtered.to_csv(output_file, mode="a", index=False, header=first)
        first = False


if __name__ == "__main__":
    parse_comments()
