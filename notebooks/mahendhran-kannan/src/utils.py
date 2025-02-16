def extract_section(recipe_content, section):    
    # Split the contents to lines    
    lines = recipe_content.split("\n")

    section_content = []
    section_start = False

    valid_sections = ["Title", "Ingredients", "Instructions", "Summary"]
 
    # Loop thru lines   
    for line in lines:   
        line = line.strip() 
        if line.startswith(f"{section}:"):  
            section_start = True
            section_content.append(line.replace(f"{section}:","").strip())
            continue
        elif any(line.startswith(f"{s}:") for s in valid_sections) and section_start:
            break

        # Add the content
        if section_start:
            section_content.append(line)            

    # convert the list to single string
    return "\n".join([line for line in section_content if line]).strip()