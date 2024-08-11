import re
import numpy as np

def analyze_data_blocks(data_blocks):
    winrates = []
    big_wins = []
    big_losses = []

    for block in data_blocks:
        win_count = np.sum(np.array(block) > 0)
        loss_count = np.sum(np.array(block) < 0)
        winrate = win_count / (win_count + loss_count)
        winrates.append(winrate)

    return winrates

def extract_data_blocks(section_content):
    # Find all data blocks using regex
    blocks = re.findall(r"All:\s*\[([^\]]+)\]", section_content)
    
    data_blocks = []
    for block in blocks:
        # Convert the block of string numbers into a list of integers
        data_blocks.append(list(map(int, block.split(','))))
    
    return data_blocks

def process_section(section_content):
    # Extract data blocks
    data_blocks = extract_data_blocks(section_content)

    # Analyze data blocks
    winrates = analyze_data_blocks(data_blocks)

    # Calculate overall mean and winrate for the section
    block_means = [np.mean(block) for block in data_blocks]
    overall_mean = np.mean(block_means)
    overall_winrate = np.mean(winrates)

    # Count occurrences of +3 in each block
    count_of_3 = sum(block.count(3) for block in data_blocks)

    return overall_mean, overall_winrate, count_of_3

def compare_sections(file_content):
    # Split the file content into sections based on the delimiter
    sections = file_content.split('==========================')

    section_stats = []

    for section in sections:
        if section.strip():  # Skip any empty sections
            # Extract the section name
            section_name_match = re.search(r'Combination: ([^\n]+)', section)
            if section_name_match:
                section_name = section_name_match.group(1)
            else:
                section_name = "Unnamed Section"

            overall_mean, overall_winrate, count_of_3 = process_section(section)
            combined_metric = (overall_mean + overall_winrate) / 2
            section_stats.append((section_name, overall_mean, overall_winrate, count_of_3, combined_metric))

    # Determine the best sections based on different criteria
    best_by_mean = max(section_stats, key=lambda x: x[1])
    best_by_winrate = max(section_stats, key=lambda x: x[2])
    best_by_combined = max(section_stats, key=lambda x: x[4])
    best_by_highest_3 = max(section_stats, key=lambda x: x[3])
    best_by_lowest_3 = min(section_stats, key=lambda x: x[3])

    return best_by_mean, best_by_winrate, best_by_combined, best_by_highest_3, best_by_lowest_3, section_stats

def analyze_differences(section_stats):
    means = [stat[1] for stat in section_stats]
    winrates = [stat[2] for stat in section_stats]
    counts_of_3 = [stat[3] for stat in section_stats]

    # Compute variances to see how much the sections differ
    mean_variance = np.var(means)
    winrate_variance = np.var(winrates)
    count_of_3_variance = np.var(counts_of_3)

    return mean_variance, winrate_variance, count_of_3_variance

# Read the entire file content
file_path = 'schnapsenExperiment/tournament_results.txt'
with open(file_path, 'r') as file:
    file_content = file.read()

# Compare sections
best_mean_section, best_winrate_section, best_combined_section, best_highest_3_section, best_lowest_3_section, section_stats = compare_sections(file_content)

print(f"Section with highest mean: {best_mean_section[0]}, Mean: {best_mean_section[1]:.4f}")
print(f"Section with highest winrate: {best_winrate_section[0]}, Winrate: {best_winrate_section[2]:.4f}")
print(f"Section with highest combined mean and winrate: {best_combined_section[0]}, Combined: {best_combined_section[4]:.4f}")
print(f"Section with highest count of +3: {best_highest_3_section[0]}, Count of +3: {best_highest_3_section[3]}")
print(f"Section with lowest count of +3: {best_lowest_3_section[0]}, Count of +3: {best_lowest_3_section[3]}")

# Analyze differences between sections
mean_var, winrate_var, count_3_var = analyze_differences(section_stats)

print(f"\nVariance in Mean across sections: {mean_var:.4f}")
print(f"Variance in Winrate across sections: {winrate_var:.4f}")
print(f"Variance in Count of +3 across sections: {count_3_var:.4f}")
