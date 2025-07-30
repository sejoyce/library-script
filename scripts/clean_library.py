import pandas as pd

def clean_text(text):
    if pd.isna(text):
        return ""
    return str(text).encode("ascii", "ignore").decode("utf-8").strip()

# Load Goodreads export
input_path = "files/goodreads_library_export.csv"
df = pd.read_csv(input_path)

# Filter only 'to-read' shelf
to_read_df = df[df['Exclusive Shelf'] == 'to-read'].copy()

# Extract relevant columns
to_read_df = to_read_df[['Title', 'Author', 'ISBN', 'ISBN13', 'Number of Pages']].copy()

# Clean columns
for column in ['Title', 'Author', 'ISBN', 'ISBN13']:
    to_read_df[column] = to_read_df[column].apply(clean_text)

# Use ISBN13 if ISBN is missing
to_read_df['ISBN'] = to_read_df['ISBN'].fillna(to_read_df['ISBN13'])

# Drop entries without any ISBN
to_read_df = to_read_df.dropna(subset=['ISBN'])

# Reset index
to_read_df = to_read_df.reset_index(drop=True)

# Add placeholder columns for enrichment
to_read_df['Available Formats'] = ''

# Save cleaned CSV
output_path = "files/cleaned_to_read_list.csv"
to_read_df.to_csv(output_path, index=False)

print(f"Cleaned file saved to: {output_path}")