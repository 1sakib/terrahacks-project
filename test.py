import re

def format_title(title):
    # Remove leading non-capital alphabetical characters
    title = re.sub(r'^[^A-Z]+', '', title)
    # Capitalize the first letter of the title
    title = title.capitalize()
    return title

def extract_titles_and_values(arr):
    # Regex pattern to match the format title : value
    pattern = r'([^:]+?) : ([\d.]+|yes|no|none|)'
    
    result = []
    
    for item in arr:
        matches = re.findall(pattern, item, re.IGNORECASE)
        for match in matches:
            title = match[0].strip()
            value = match[1].strip().lower()  # Convert to lowercase for consistency

            # Format the title
            title = format_title(title)
            
            # Default empty value to 'yes' for "Most Efficient"
            if title.lower() == 'most efficient' and value == '':
                value = 'yes'
            elif value == '':
                value = 'yes'
            else:
                # Try to convert value to float if possible, otherwise keep as string
                try:
                    value = float(value)
                except ValueError:
                    if value not in ['yes', 'no', 'none']:
                        value = value  # Keep as string if it's not "yes", "no", or "none"
                    
            result.append([title, value])
    
    return result

def filter_titles(data, titles_to_include):
    filtered_data = []
    title_map = {title.lower(): title for title in titles_to_include}

    # Process each item to match the titles we're interested in
    for item in data:
        title, value = item
        title_lower = title.lower()
        if title_lower in title_map:
            filtered_data.append([title_map[title_lower], str(value)])
    
    # Ensure that all desired titles are included, even if they are missing
    for title in titles_to_include:
        if not any(item[0] == title for item in filtered_data):
            filtered_data.append([title, 'yes'])

    return filtered_data

def split_and_process_array(array):
    # Split the array into two based on the presence of certain keywords
    # Here, we will split based on whether the string contains "Features" or not
    split_index = next((i for i, s in enumerate(array) if 'Features' in s), len(array))
    array1 = array[:split_index]
    array2 = array[split_index:]
    
    # Process both arrays
    processed_data1 = extract_titles_and_values(array1)
    processed_data2 = extract_titles_and_values(array2)
    
    # Modify the first entry of processed_data1 to omit the first word of its title
    if processed_data1:
        first_entry = processed_data1[0]
        title = first_entry[0].split(' ', 1)[-1]  # Omit the first word
        processed_data1[0] = [title, first_entry[1]]
    
    # Filter the second array to include only specific titles
    titles_to_include = ["Most Efficient", "ENERGY STAR Certified"]
    processed_data2 = filter_titles(processed_data2, titles_to_include)
    
    return processed_data1, processed_data2

# Sample array
array = ['Efficiency Annual Energy Use (kWh/yr) : 633 US Federal Standard (kWh/yr) : 731', 'Features Connected Functionality : No ENERGY STAR Certified : Yes Most Efficient : No']

# Process the array
processed_data1, processed_data2 = split_and_process_array(array)

# Print the results
print("Processed Data 1:")
for item in processed_data1:
    print(item)

print("\nProcessed Data 2:")
for item in processed_data2:
    print(item)
