"""
Government Scheme AI Assistant - Streamlit Application
Main application file for the AI assistant
"""

import streamlit as st
import streamlit.components.v1 as components
import os
from vector_db import get_vector_db
from qa_logic import get_qa_system

# Lucide Icons as inline SVG - Direct and reliable for Streamlit
LUCIDE_ICONS = {
    'bank': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" x2="21" y1="21" y2="21"/><line x1="3" x2="21" y1="10" y2="10"/><path d="M5 6l7-3 7 3"/><path d="M5 21V10"/><path d="M19 21V10"/><path d="M9 21V10"/><path d="M15 21V10"/></svg>''',
    'building-2': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12h16"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/></svg>''',
    'lightbulb': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/></svg>''',
    'info': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>''',
    'file-check': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="m9 15 2 2 4-4"/></svg>''',
    'file-text': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/></svg>''',
    'search': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>''',
    'message-circle': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/></svg>''',
    'edit': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.12 2.12 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>''',
    'pen-tool': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 19 7-7 3 3-7 7-3-3z"/><path d="m18 13-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/><path d="m2 2 7.586 7.586"/><circle cx="11" cy="11" r="2"/></svg>''',
    'help-circle': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/></svg>''',
    'sparkles': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/><path d="M5 3v4"/><path d="M19 17v4"/><path d="M3 5h4"/><path d="M17 19h4"/></svg>''',
    'wallet': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/></svg>''',
    'shield-check': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/></svg>''',
    'users': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>''',
    'clipboard-list': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M12 11h4"/><path d="M12 16h4"/><path d="M8 11h.01"/><path d="M8 16h.01"/></svg>''',
    'check-circle': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>''',
    'link': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>''',
    'globe': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>'''
}

def get_icon(icon_name, size="1.2em", color="#4CAF50"):
    """Get inline SVG icon with proper styling"""
    if icon_name not in LUCIDE_ICONS:
        return ""
    svg = LUCIDE_ICONS[icon_name]
    # Replace stroke color and add size
    svg = svg.replace('width="24"', f'width="{size}"')
    svg = svg.replace('height="24"', f'height="{size}"')
    svg = svg.replace('stroke="currentColor"', f'stroke="{color}"')
    return f'<span class="lucide-icon" style="display:inline-block;vertical-align:middle;margin-right:0.5rem;color:{color};">{svg}</span>'

def replace_emojis_with_icons(text: str) -> str:
    """Replace emojis in output with Lucide icons"""
    import re
    
    # Emoji to icon mapping
    emoji_icon_map = {
        '📋': ('clipboard-list', '#4CAF50'),  # Details
        '💰': ('wallet', '#FFC107'),  # Benefits
        '✅': ('shield-check', '#4CAF50'),  # Eligibility
        '📝': ('pen-tool', '#4CAF50'),  # Application Process
        '📄': ('file-text', '#2196F3'),  # Documents Required
        '🔗': ('link', '#4CAF50'),  # Official Website
        '🌐': ('globe', '#4CAF50'),  # Scheme Name
    }
    
    # Replace emojis in section labels with icons (markdown format)
    for emoji, (icon_name, color) in emoji_icon_map.items():
        # Pattern: **📋 Details** - replace with icon HTML
        pattern = rf'\*\*{re.escape(emoji)}\s*([^*]+?)\*\*'
        def replace_func(match):
            section_name = match.group(1).strip()
            icon_html = get_icon(icon_name, "1.2em", color)
            # Return HTML directly (not in markdown bold, as HTML is already formatted)
            return f'**{icon_html} {section_name}**'
        
        text = re.sub(pattern, replace_func, text)
        
        # Also handle emojis in headings (### 🌐 Scheme Name)
        pattern_heading = rf'###\s*{re.escape(emoji)}\s*([^\n]+)'
        def replace_func_heading(match):
            section_name = match.group(1).strip()
            icon_html = get_icon(icon_name, "1.2em", color)
            return f'### {icon_html} {section_name}'
        
        text = re.sub(pattern_heading, replace_func_heading, text)
    
    return text

def format_answer_md(user_query: str, raw_text: str) -> str:
    """Format LLM answer into clean, well-structured markdown with proper formatting."""
    import re
    if not raw_text:
        return "I don't have that information right now."

    # Step 1: Basic cleanup
    text = raw_text.replace('\r\n', '\n').replace('\r', '\n').strip()
    
    # Step 1a: ULTIMATE GLOBAL FIX - Replace ALL double colons (::) with single colon (:) in ENTIRE text
    # This removes ALL double colons from everywhere, not just section labels
    while '::' in text:
        text = text.replace('::', ':')
    
    # Step 2: Remove excessive asterisks (***) - this is a common LLM mistake
    # Replace triple asterisks with single dash for bullets
    text = re.sub(r'\*{3,}', '-', text)
    # Remove any double asterisks that aren't part of markdown bold
    text = re.sub(r'(?<!\*)\*{2}(?!\*)', '', text)
    # Fix cases where we have "* * *" with spaces
    text = re.sub(r'\*\s+\*\s+\*', '-', text)
    
    # Step 3: Fix scheme name headings (use h3 instead of h2 for smaller size)
    text = re.sub(r'^#+\s*🌐\s*(.+?)(\s*\(Maharashtra\))?\s*$', r'### 🌐 \1', text, flags=re.MULTILINE)
    text = re.sub(r'^🌐\s*Scheme\s+Name:?\s*(.+)$', r'### 🌐 \1', text, flags=re.MULTILINE)
    text = re.sub(r'^🌐\s*([^:\n]+)$', r'### 🌐 \1', text, flags=re.MULTILINE)
    
    # Step 4: Normalize section labels - be very careful here
    # First, remove any existing bold formatting around emojis (NO COLON)
    text = re.sub(r'\*\*?([📋💰✅📝📄🔗])\s*([^:*]+?)\s*\*\*?', r'**\1 \2**', text)
    
    # Then standardize each section (NO COLON in headings)
    section_patterns = [
        (r'📋\s*Details:?\s*', '**📋 Details**'),
        (r'💰\s*Benefits:?\s*', '**💰 Benefits**'),
        (r'✅\s*Eligibility:?\s*', '**✅ Eligibility**'),
        (r'📝\s*Application\s+Process:?\s*', '**📝 Application Process**'),
        (r'📄\s*Documents\s+Required:?\s*', '**📄 Documents Required**'),
        (r'🔗\s*Official\s+Website[^:]*:?\s*', '**🔗 Official Website**'),
    ]
    
    for pattern, replacement in section_patterns:
        # Only replace if not already properly formatted (no ** before or after)
        text = re.sub(rf'(?<!\*\*){pattern}(?!\*\*)', replacement + ' ', text, flags=re.IGNORECASE)
        # Also handle if already has ** but wrong format
        text = re.sub(rf'\*\*?{pattern}\*\*?', replacement + ' ', text, flags=re.IGNORECASE)
    
    # Step 4a: Remove ALL colons from section labels (NO COLON in headings)
    # Remove single colon (:) from section labels
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        # If line contains section label emoji, remove colon from it
        if re.search(r'[📋💰✅📝📄🔗]', line):
            # Remove colon if it appears right after the section label (before or after **)
            # Pattern: **📄 Documents Required:** → **📄 Documents Required**
            line = re.sub(r'(\*\*[📋💰✅📝📄🔗][^*]+?):(\*\*)', r'\1\2', line)  # Colon inside bold
            line = re.sub(r'(\*\*[📋💰✅📝📄🔗][^*]+?\*\*):', r'\1', line)  # Colon outside bold
        cleaned_lines.append(line)
    text = '\n'.join(cleaned_lines)
    
    # Step 4b: GLOBAL FIX - Remove ALL double colons (::) from ENTIRE text
    # Simple global replacement after pattern replacement
    while '::' in text:
        text = text.replace('::', ':')
    
    # Step 5: Ensure section labels are on their own lines with proper spacing
    text = re.sub(r'([^\n])(\*\*[📋💰✅📝📄🔗])', r'\1\n\n\2', text)
    
    # Step 5a: Handle Online/Offline in Application Process - add to heading in brackets
    # Detect if "Online" or "Offline" appears right after Application Process heading
    lines = text.split('\n')
    cleaned_lines = []
    skip_indices = set()
    
    for i in range(len(lines)):
        if i in skip_indices:
            continue
            
        line = lines[i]
        # Check if this is Application Process heading
        if re.search(r'\*\*📝\s*Application\s+Process', line, re.IGNORECASE):
            # Check if already has brackets with Online/Offline
            if re.search(r'\(Online|Offline\)', line, re.IGNORECASE):
                cleaned_lines.append(line)
                continue
                
            # Check next few lines for "Online" or "Offline"
            mode = None
            for j in range(i + 1, min(i + 6, len(lines))):
                if j in skip_indices:
                    continue
                next_line = lines[j].strip()
                
                # Check if line starts with "Online" or "Offline" (may have dash, hyphen, or other formatting)
                if re.match(r'^(Online|Offline)\b', next_line, re.IGNORECASE):
                    match = re.match(r'^(Online|Offline)\b', next_line, re.IGNORECASE)
                    if match:
                        mode = match.group(1)  # Get "Online" or "Offline" (preserve case)
                        # If the line is just "Online" or "Offline" or starts with it followed by dash/hyphen, skip it
                        if re.match(r'^(Online|Offline)\s*[-–—:]?\s*$', next_line, re.IGNORECASE):
                            skip_indices.add(j)  # Mark this line to be skipped
                        # If "Online - Step 1:" format, remove "Online -" part and keep the step
                        elif re.match(r'^(Online|Offline)\s*[-–—]\s*Step', next_line, re.IGNORECASE):
                            # Remove "Online -" or "Offline -" from the line
                            cleaned_step = re.sub(r'^(Online|Offline)\s*[-–—]\s*', '', next_line, flags=re.IGNORECASE).strip()
                            if cleaned_step:
                                # Update the line in place - we'll process it later as a normal line
                                lines[j] = cleaned_step  # Update for later iteration
                                # Don't skip it - we want to process the cleaned step
                            else:
                                skip_indices.add(j)  # Only skip if nothing left after cleaning
                        break
                # Also check if line contains "Online" or "Offline" as standalone word
                elif re.match(r'^\s*(Online|Offline)\s*$', next_line, re.IGNORECASE):
                    match = re.match(r'^\s*(Online|Offline)\s*$', next_line, re.IGNORECASE)
                    if match:
                        mode = match.group(1)
                        skip_indices.add(j)
                        break
                # If we hit a bullet point or section heading, stop looking
                if re.match(r'^[-*]|^\*\*[📋💰✅📝📄🔗]|^#+', next_line):
                    break
            
            # Add mode to heading if found
            if mode:
                # Format: **📝 Application Process (Online)**
                # More flexible pattern - handle any spacing
                if re.search(r'\*\*📝\s*Application\s+Process\s*\*\*', line, re.IGNORECASE):
                    line = re.sub(r'(\*\*📝\s*Application\s+Process\s*)(\*\*)', rf'\1({mode})\2', line, flags=re.IGNORECASE)
                # Also handle if it's already formatted differently
                elif re.search(r'\*\*📝\s*Application\s+Process', line, re.IGNORECASE):
                    line = re.sub(r'(\*\*📝\s*Application\s+Process)(\s*\*\*)', rf'\1 ({mode})\2', line, flags=re.IGNORECASE)
        
        cleaned_lines.append(line)
    
    text = '\n'.join(cleaned_lines)
    
    # Step 5b: Fix section labels that have bullet points on the same line (NO COLON)
    # Pattern: **✅ Eligibility** - Point 1  should become:
    # **✅ Eligibility**
    # - Point 1
    text = re.sub(r'(\*\*[📋💰✅📝📄🔗][^*]+?\*\*)\s*:?\s*-\s+', r'\1\n\n- ', text)
    text = re.sub(r'(\*\*[📋💰✅📝📄🔗][^*]+?\*\*)\s*:?\s*-\s+', r'\1\n\n- ', text)  # Run twice to catch nested patterns
    
    # Step 6: Clean up bullet points
    # Remove any asterisks at start of lines that aren't part of bold formatting
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        # Check if section label has bullet point on same line (NO COLON in section label)
        # Patterns: **✅ Eligibility** - Point 1  or  **✅ Eligibility**- Point 1  or  **✅ Eligibility** -Point 1
        section_with_bullet = re.match(r'^(\s*\*\*[📋💰✅📝📄🔗][^*]+?\*\*)\s*:?\s*-\s*(.+)$', line)
        if section_with_bullet:
            # Split into separate lines (NO COLON in section label)
            section_label = section_with_bullet.group(1)
            bullet_content = section_with_bullet.group(2).strip()
            # Remove any colon from section label
            section_label = re.sub(r':(\*\*)$', r'\1', section_label)  # Remove colon before closing **
            section_label = re.sub(r'(\*\*)$', r'\1', section_label) if section_label.endswith(':**') else section_label
            section_label = section_label.rstrip(':')  # Remove trailing colon
            cleaned_lines.append(section_label)
            cleaned_lines.append('- ' + bullet_content)
            continue
        
        # Also handle case where section label ends without colon but has bullet on same line
        section_with_bullet_no_colon = re.match(r'^(\s*\*\*[📋💰✅📝📄🔗][^*]+?\*\*)\s+-\s+(.+)$', line)
        if section_with_bullet_no_colon:
            section_label = section_with_bullet_no_colon.group(1)
            bullet_content = section_with_bullet_no_colon.group(2).strip()
            # Remove any colon from section label
            section_label = section_label.rstrip(':')
            cleaned_lines.append(section_label)
            cleaned_lines.append('- ' + bullet_content)
            continue
        
        # Don't modify lines that are section headers (have **emoji)
        if re.match(r'^\s*\*\*[📋💰✅📝📄🔗]', line):
            # Remove ALL colons from section headers (NO COLON in headings)
            line = re.sub(r'(\*\*[📋💰✅📝📄🔗][^*]+?):(\*\*)', r'\1\2', line)  # Colon inside bold
            line = re.sub(r'(\*\*[📋💰✅📝📄🔗][^*]+?\*\*):', r'\1', line)  # Colon outside bold
            # Also remove double colons
            while '::' in line:
                line = line.replace('::', ':')
            cleaned_lines.append(line)
            continue
        
        # Don't modify lines that are headings
        if re.match(r'^#+\s', line):
            cleaned_lines.append(line)
            continue
        
        # Remove triple or more asterisks at start
        line = re.sub(r'^(\s*)\*{3,}\s*', r'\1- ', line)
        # Convert single asterisk at start to dash (if not part of bold)
        line = re.sub(r'^(\s*)\*(?!\*)\s+', r'\1- ', line)
        # Convert various bullet characters to dash
        line = re.sub(r'^(\s*)[•▪▫‣⁃]\s+', r'\1- ', line)
        # Convert numbered lists to bullets
        line = re.sub(r'^(\s*)\d+[.)]\s+', r'\1- ', line)
        
        cleaned_lines.append(line)
    
    text = '\n'.join(cleaned_lines)
    
    # Step 6a: GLOBAL FIX - Remove ALL double colons (::) from ENTIRE text
    # Simple global replacement
    while '::' in text:
        text = text.replace('::', ':')
    
    # Step 7: Fix step formatting - ensure all steps in Application Process are bullet points
    # First, convert all "Step X:" patterns to bullet format
    text = re.sub(r'^(\s*)Step\s+(\d+)[:.)]\s*', r'\1- Step \2: ', text, flags=re.IGNORECASE | re.MULTILINE)
    # Also handle steps that might be on lines without proper formatting
    text = re.sub(r'(\n)(\s*)Step\s+(\d+)[:.)]\s*', r'\1\2- Step \3: ', text, flags=re.IGNORECASE)
    
    # Step 8: Expand inline (a)(b) style lists
    def expand_inline_lists(content):
        lines = content.split('\n')
        result = []
        for line in lines:
            # Skip section headers and headings
            if re.match(r'^\s*(\*\*[📋💰✅📝📄🔗]|#+)', line):
                result.append(line)
                continue
            
            # Check for inline (a)(b) pattern
            if re.search(r':\s*\([a-z]\)', line, re.IGNORECASE):
                match = re.match(r'^(.+?):\s*(.+)$', line)
                if match:
                    head, tail = match.groups()
                    items = re.findall(r'\(([a-z])\)\s*([^(]+?)(?=\([a-z]\)|$)', tail, re.IGNORECASE)
                    if items:
                        result.append(head + ':')
                        for label, item_text in items:
                            result.append(f"  - ({label}) {item_text.strip()}")
                        continue
            result.append(line)
        return '\n'.join(result)
    
    text = expand_inline_lists(text)
    
    # Step 9: Remove duplicate section labels
    text = re.sub(r'(\*\*[📋💰✅📝📄🔗][^*]+?\*\*)[:\s]+\1', r'\1', text, flags=re.IGNORECASE)
    
    # Step 10: Ensure proper spacing around headings
    text = re.sub(r'\n(##\s+[^\n]+)\n([^\n#*])', r'\n\n\1\n\n\2', text)
    
    # Step 11: Clean up excessive blank lines
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    
    # Step 12: Remove trailing whitespace from each line
    lines = [line.rstrip() for line in text.split('\n')]
    text = '\n'.join(lines)
    
    # Step 13: Ensure section labels have content after them (remove empty sections)
    lines = text.split('\n')
    final_lines = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        # If this is a section label, check if next line is also a section label or empty
        if re.match(r'^\*\*[📋💰✅📝📄🔗]', stripped):
            # Look ahead to see if there's content
            has_content = False
            for j in range(i + 1, min(i + 3, len(lines))):
                next_line = lines[j].strip()
                if next_line and not re.match(r'^(\*\*[📋💰✅📝📄🔗]|#+)', next_line):
                    has_content = True
                    break
            if has_content:
                final_lines.append(line)
        else:
            final_lines.append(line)
    
    text = '\n'.join(final_lines)
    
    # Step 13a: Remove empty bullet points immediately after section labels
    lines = text.split('\n')
    cleaned_lines = []
    skip_next = False
    for i, line in enumerate(lines):
        if skip_next:
            skip_next = False
            continue
        
        stripped = line.strip()
        # Check if this is a section label
        if re.match(r'^\*\*[📋💰✅📝📄🔗]', stripped):
            cleaned_lines.append(line)
            # Check if next line is an empty bullet point
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                # If next line is just a dash or empty bullet, skip it
                if re.match(r'^-\s*$', next_line) or next_line == '-':
                    skip_next = True  # Skip adding the empty bullet line
                    continue
        else:
            cleaned_lines.append(line)
    
    text = '\n'.join(cleaned_lines)
    
    # Step 14: Final cleanup - remove triple or more consecutive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    
    # Step 15: Add intro if needed
    lines = text.split('\n')
    has_intro = False
    for line in lines[:3]:
        if line.strip() and not re.match(r'^(#+|\*\*[📋💰✅📝📄🔗])', line.strip()):
            if len(line.strip()) > 15:
                has_intro = True
                break
    
    if not has_intro:
        intro_text = f"Here's information about {user_query}:\n\n"
        text = intro_text + text
    
    # Step 16: FINAL GLOBAL FIX - Remove ALL double colons (::) from ENTIRE text
    # Simple global replacement - replace ALL :: with : everywhere
    while '::' in text:
        text = text.replace('::', ':')
    
    # Step 17: Remove duplicate bullet points (especially in Application Process)
    # This step removes consecutive duplicate bullet points
    lines = text.split('\n')
    cleaned_lines = []
    prev_line = None
    
    for line in lines:
        stripped = line.strip()
        # Check if this is a bullet point
        if stripped.startswith('- '):
            # If previous line is the same bullet point, skip it
            if prev_line and prev_line.strip() == stripped:
                continue
            prev_line = line
        else:
            prev_line = None
        cleaned_lines.append(line)
    
    text = '\n'.join(cleaned_lines)
    
    # Step 17.5: Ensure links in Application Process section are properly formatted
    # If there's a URL in the Application Process section, ensure it's displayed as "Link: [URL]" at the end
    lines = text.split('\n')
    formatted_lines = []
    in_application_process = False
    application_process_end = -1
    
    for i, line in enumerate(lines):
        # Check if this is the Application Process section heading
        if re.search(r'\*\*📝\s*Application\s+Process', line, re.IGNORECASE):
            in_application_process = True
            application_process_end = -1
            formatted_lines.append(line)
            continue
        
        # Check if we've moved to a new section
        if in_application_process and re.match(r'^\*\*[📋💰✅📄🔗]', line.strip()):
            # We've reached the end of Application Process section
            in_application_process = False
            # Check if there was a URL that needs to be formatted
            if application_process_end > 0:
                # Look for URL in the last few lines of Application Process
                for j in range(max(0, application_process_end - 5), application_process_end):
                    if j < len(formatted_lines):
                        url_match = re.search(r'(https?://[^\s]+)', formatted_lines[j])
                        if url_match:
                            url = url_match.group(1)
                            # Check if it's not already formatted as "Link:"
                            if not re.search(r'Link:\s*', formatted_lines[j], re.IGNORECASE):
                                # Always put link on new line
                                # Remove URL from current line
                                line_without_url = re.sub(r'https?://[^\s]+', '', formatted_lines[j]).strip()
                                # If line has content other than URL, keep it and add link on new line
                                if line_without_url:
                                    formatted_lines[j] = f"{line_without_url}\nLink: {url}"
                                else:
                                    # If line was just the URL, make it "Link: URL" on its own line
                                    formatted_lines[j] = f"Link: {url}"
        
        formatted_lines.append(line)
        
        # Track the end of Application Process section
        if in_application_process:
            application_process_end = len(formatted_lines)
    
    # Final pass: ensure URLs in Application Process are formatted as "Link: [URL]"
    final_lines = []
    for i, line in enumerate(formatted_lines):
        # Check if this line is in Application Process section and contains a URL
        # Look backwards to see if we're in Application Process section
        is_in_app_process = False
        for j in range(max(0, i - 20), i):
            if j < len(formatted_lines):
                if re.search(r'\*\*📝\s*Application\s+Process', formatted_lines[j], re.IGNORECASE):
                    is_in_app_process = True
                    break
                # Check if we've hit another section
                if re.match(r'^\*\*[📋💰✅📄🔗]', formatted_lines[j].strip()):
                    is_in_app_process = False
                    break
        
        if is_in_app_process:
            # Check if line contains a URL but not formatted as "Link:"
            url_match = re.search(r'https?://[^\s]+', line)
            if url_match and not re.search(r'Link:\s*', line, re.IGNORECASE):
                url = url_match.group(0)
                # Always put link on new line
                # Remove URL from current line
                line_without_url = re.sub(r'https?://[^\s]+', '', line).strip()
                # If line has content other than URL, keep it and add link on new line
                if line_without_url:
                    line = f"{line_without_url}\nLink: {url}"
                else:
                    # If line was just the URL, make it "Link: URL" on its own line
                    line = f"Link: {url}"
        
        final_lines.append(line)
    
    text = '\n'.join(final_lines)
    
    # Step 17.6: Ensure all steps in Application Process section are bullet points
    lines = text.split('\n')
    final_formatted_lines = []
    in_app_process = False
    
    for i, line in enumerate(lines):
        # Check if we're entering Application Process section
        if re.search(r'\*\*📝\s*Application\s+Process', line, re.IGNORECASE):
            in_app_process = True
            final_formatted_lines.append(line)
            continue
        
        # Check if we've left Application Process section
        if in_app_process and re.match(r'^\*\*[📋💰✅📄🔗]', line.strip()):
            in_app_process = False
            final_formatted_lines.append(line)
            continue
        
        # If in Application Process section and line starts with "Step" (without bullet), add bullet
        if in_app_process:
            stripped = line.strip()
            # Check if line starts with "Step X:" or "Step X." but doesn't have bullet point
            if re.match(r'^Step\s+\d+[:.]', stripped, re.IGNORECASE) and not stripped.startswith('- '):
                # Add bullet point at the beginning, preserving indentation
                indent = len(line) - len(line.lstrip())
                # Format as "- Step X:"
                formatted_step = re.sub(r'^(Step\s+\d+)[:.]', r'- \1: ', stripped, flags=re.IGNORECASE)
                final_formatted_lines.append(' ' * indent + formatted_step)
                continue
            # Also handle "Step X" without colon/dot
            elif re.match(r'^Step\s+\d+\s', stripped, re.IGNORECASE) and not stripped.startswith('- '):
                indent = len(line) - len(line.lstrip())
                final_formatted_lines.append(' ' * indent + '- ' + stripped)
                continue
        
        final_formatted_lines.append(line)
    
    text = '\n'.join(final_formatted_lines)
    
    # Step 18: Replace emojis with icons in output
    text = replace_emojis_with_icons(text)
    
    return text.strip()

def get_icon(icon_name, size="1.2em", color="#4CAF50"):
    """Get inline SVG icon with proper styling"""
    if icon_name not in LUCIDE_ICONS:
        return ""
    svg = LUCIDE_ICONS[icon_name]
    # Replace stroke color and add size
    svg = svg.replace('width="24"', f'width="{size}"')
    svg = svg.replace('height="24"', f'height="{size}"')
    svg = svg.replace('stroke="currentColor"', f'stroke="{color}"')
    return f'<span class="lucide-icon" style="display:inline-block;vertical-align:middle;margin-right:0.5rem;color:{color};">{svg}</span>'

# Page configuration - Set title and icon
try:
    # Try to load logo as favicon
    import base64
    import os
    from PIL import Image
    
    logo_file = None
    if os.path.exists("LOGO.png"):
        logo_file = "LOGO.png"
    elif os.path.exists("LOGO.PNG"):
        logo_file = "LOGO.PNG"
    elif os.path.exists("LOGO.jpg"):
        logo_file = "LOGO.jpg"
    elif os.path.exists("LOGO.JPG"):
        logo_file = "LOGO.JPG"
    
    if logo_file:
        # Use logo as page icon
        page_icon = Image.open(logo_file)
    else:
        page_icon = "🇮🇳"
except Exception as e:
    page_icon = "🇮🇳"

st.set_page_config(
    page_title="Yojana Mitra",
    page_icon=page_icon,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Suvidha Portal Theme - Friendly & Citizen-Focused

# Add favicon to HTML head via JavaScript
try:
    import base64
    import os
    
    logo_file = None
    logo_format = None
    if os.path.exists("LOGO.png"):
        logo_file = "LOGO.png"
        logo_format = "png"
    elif os.path.exists("LOGO.PNG"):
        logo_file = "LOGO.PNG"
        logo_format = "png"
    elif os.path.exists("LOGO.jpg"):
        logo_file = "LOGO.jpg"
        logo_format = "jpeg"
    elif os.path.exists("LOGO.JPG"):
        logo_file = "LOGO.JPG"
        logo_format = "jpeg"
    
    favicon_script = ""
    if logo_file:
        with open(logo_file, "rb") as f:
            logo_data = base64.b64encode(f.read()).decode()
        favicon_script = f"""
        <script>
        (function() {{
            const link = document.createElement('link');
            link.rel = 'icon';
            link.type = 'image/{logo_format}';
            link.href = 'data:image/{logo_format};base64,{logo_data}';
            document.head.appendChild(link);
            // Also update title
            document.title = 'Yojana Mitra';
        }})();
        </script>
        """
except Exception as e:
    favicon_script = ""

# Add favicon script if available
if favicon_script:
    st.markdown(favicon_script, unsafe_allow_html=True)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Global Reset & Base Styles */
    * {
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    
    /* Suvidha Portal Background - Warm & Welcoming with Glass Effect Support */
    .stApp {
        background: linear-gradient(135deg, #FFF9E6 0%, #ffffff 50%, #FFF9E6 100%);
        background-size: 400% 400%;
        animation: gentleShift 20s ease infinite;
        position: relative;
        min-height: 100vh;
    }
    
    /* Add animated glass pattern overlay for moving glass effect - Lighter - No Horizontal Movement */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 200%;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(76, 175, 80, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255, 193, 7, 0.06) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(76, 175, 80, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 60% 60%, rgba(255, 193, 7, 0.04) 0%, transparent 45%),
            radial-gradient(circle at 30% 70%, rgba(76, 175, 80, 0.03) 0%, transparent 55%);
        background-size: 100% 100%;
        animation: glassMove 15s ease-in-out infinite, glassFloat 20s ease-in-out infinite;
        pointer-events: none;
        z-index: 0;
        transform-origin: center center;
        opacity: 0.6;
        overflow: hidden;
    }
    
    /* Prevent horizontal scrolling */
    html, body {
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }
    
    .stApp {
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }
    
    @keyframes glassMove {
        0% {
            transform: translateY(0%) scale(1);
            opacity: 0.5;
        }
        25% {
            transform: translateY(-5%) scale(1.1);
            opacity: 0.7;
        }
        50% {
            transform: translateY(-10%) scale(1.05);
            opacity: 0.6;
        }
        75% {
            transform: translateY(-15%) scale(1.08);
            opacity: 0.7;
        }
        100% {
            transform: translateY(0%) scale(1);
            opacity: 0.5;
        }
    }
    
    @keyframes glassFloat {
        0%, 100% {
            transform: translateY(0%) rotate(0deg);
        }
        33% {
            transform: translateY(-8%) rotate(2deg);
        }
        66% {
            transform: translateY(8%) rotate(-2deg);
        }
    }
    
    @keyframes gentleShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Main Content Container - Glassmorphism Effect with Enhanced 3D Animation - More Visible */
    .main .block-container,
    [data-testid="stAppViewContainer"] .main .block-container,
    .main .block-container {
        max-width: 1200px !important;
        background: rgba(255, 255, 255, 0.75) !important;
        backdrop-filter: blur(30px) saturate(200%) !important;
        -webkit-backdrop-filter: blur(30px) saturate(200%) !important;
        border-radius: 30px !important;
        box-shadow: 0 8px 32px rgba(76, 175, 80, 0.4),
                    0 0 0 2px rgba(255, 255, 255, 0.8) inset,
                    0 0 100px rgba(76, 175, 80, 0.25),
                    0 0 150px rgba(255, 193, 7, 0.2) !important;
        border: 3px solid rgba(255, 249, 230, 0.9) !important;
        margin: 0rem auto !important;
        padding: 0rem 2rem 0.5rem 2rem !important;
        animation: fadeInUp 0.6s ease-out, glassFloatRotate 10s ease-in-out infinite, glassShimmer 8s ease-in-out infinite !important;
        position: relative !important;
        overflow: hidden !important;
        transform-style: preserve-3d !important;
        transform-origin: center center;
        perspective: 1000px !important;
    }
    
    /* Float & Rotate: Container gently floats with slight 3D rotation effect */
    @keyframes glassFloatRotate {
        0%, 100% {
            transform: translateY(0px) rotateX(0deg) rotateY(0deg) scale(1);
        }
        25% {
            transform: translateY(-8px) rotateX(1deg) rotateY(-0.5deg) scale(1.002);
        }
        50% {
            transform: translateY(-12px) rotateX(0deg) rotateY(0.5deg) scale(1.003);
        }
        75% {
            transform: translateY(-8px) rotateX(-1deg) rotateY(-0.3deg) scale(1.002);
        }
    }
    
    /* Glassmorphism Shimmer Animation - Continuous shimmer effect - More Visible */
    .main .block-container::before,
    [data-testid="stAppViewContainer"] .main .block-container::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -150% !important;
        width: 150% !important;
        height: 100% !important;
        background: linear-gradient(
            90deg,
            transparent 0%,
            rgba(255, 255, 255, 0.9) 15%,
            rgba(76, 175, 80, 0.5) 30%,
            rgba(255, 193, 7, 0.45) 50%,
            rgba(76, 175, 80, 0.5) 70%,
            rgba(255, 255, 255, 0.9) 85%,
            transparent 100%
        ) !important;
        transform: skewX(-25deg) !important;
        animation: glassShine 4s ease-in-out infinite, shimmerPulse 3s ease-in-out infinite !important;
        pointer-events: none !important;
        z-index: 0 !important;
    }
    
    @keyframes shimmerPulse {
        0%, 100% {
            opacity: 0.9;
            filter: brightness(1.1);
        }
        50% {
            opacity: 1;
            filter: brightness(1.5);
        }
    }
    
    /* Glassmorphism Border Glow Animation - Beautiful glowing animation - More Visible */
    .main .block-container::after,
    [data-testid="stAppViewContainer"] .main .block-container::after {
        content: '' !important;
        position: absolute !important;
        top: -5px !important;
        left: -5px !important;
        right: -5px !important;
        bottom: -5px !important;
        border-radius: 35px !important;
        background: linear-gradient(
            135deg,
            rgba(76, 175, 80, 0.8),
            rgba(255, 193, 7, 0.7),
            rgba(76, 175, 80, 0.8),
            rgba(255, 193, 7, 0.7),
            rgba(76, 175, 80, 0.8)
        ) !important;
        background-size: 400% 400% !important;
        animation: borderGlow 4s ease-in-out infinite, borderPulse 2s ease-in-out infinite !important;
        z-index: -1 !important;
        opacity: 1 !important;
        filter: blur(1.5px);
        box-shadow: 0 0 30px rgba(76, 175, 80, 0.5), 0 0 60px rgba(255, 193, 7, 0.4) !important;
    }
    
    @keyframes borderPulse {
        0%, 100% {
            opacity: 0.9;
            box-shadow: 0 0 25px rgba(76, 175, 80, 0.5), 0 0 50px rgba(255, 193, 7, 0.4);
        }
        50% {
            opacity: 1;
            box-shadow: 0 0 40px rgba(76, 175, 80, 0.7), 0 0 80px rgba(255, 193, 7, 0.6);
        }
    }
    
    /* Ensure content is above glass effects */
    .main .block-container > *,
    [data-testid="stAppViewContainer"] .main .block-container > * {
        position: relative !important;
        z-index: 1 !important;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes glassShimmer {
        0%, 100% {
            box-shadow: 0 8px 32px rgba(76, 175, 80, 0.4),
                        0 0 0 1px rgba(255, 255, 255, 0.7) inset,
                        0 0 100px rgba(76, 175, 80, 0.25),
                        0 0 150px rgba(255, 193, 7, 0.2);
        }
        50% {
            box-shadow: 0 12px 48px rgba(76, 175, 80, 0.5),
                        0 0 0 2px rgba(255, 255, 255, 0.9) inset,
                        0 0 120px rgba(76, 175, 80, 0.35),
                        0 0 180px rgba(255, 193, 7, 0.25);
        }
    }
    
    @keyframes glassShine {
        0% {
            left: -150%;
            opacity: 0.3;
            transform: skewX(-25deg) translateY(0);
        }
        20% {
            opacity: 1;
            transform: skewX(-25deg) translateY(-5px);
        }
        50% {
            opacity: 1;
            transform: skewX(-25deg) translateY(0);
        }
        80% {
            opacity: 1;
            transform: skewX(-25deg) translateY(5px);
        }
        100% {
            left: 250%;
            opacity: 0.3;
            transform: skewX(-25deg) translateY(0);
        }
    }
    
    @keyframes borderGlow {
        0% {
            background-position: 0% 0%;
        }
        25% {
            background-position: 100% 0%;
        }
        50% {
            background-position: 100% 100%;
        }
        75% {
            background-position: 0% 100%;
        }
        100% {
            background-position: 0% 0%;
        }
    }
    
    /* Lucide Icons Styling - Inline SVG */
    .lucide-icon {
        display: inline-block;
        vertical-align: middle;
        margin-right: 0.5rem;
    }
    
    .lucide-icon svg {
        display: block;
        width: 100%;
        height: 100%;
    }
    
    /* Friendly Header - Leaf Green - Visible Size */
    .main-header {
        font-size: 1.5rem !important;
        font-weight: 800;
        text-align: center;
        padding: 0rem 0 0.1rem 0 !important;
        margin-top: -1.5rem !important;
        margin-bottom: 0.1rem;
        letter-spacing: -0.3px;
        position: relative;
        white-space: nowrap;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        flex-wrap: wrap;
        /* Animated gradient text - green variations only */
        background: linear-gradient(90deg, #2E7D32, #4CAF50, #66BB6A, #2E7D32);
        background-size: 200% 100%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 2px 6px rgba(76, 175, 80, 0.25));
        animation: titleGradient 6s linear infinite, titleReveal 0.7s ease-out;
    }
    
    .main-header img {
        height: 5rem !important;
        width: auto;
        vertical-align: middle;
        display: inline-block;
        flex-shrink: 0;
        mix-blend-mode: multiply;
        background: transparent;
        /* Remove white background - use multiply blend mode to make white transparent */
        filter: contrast(1.1) brightness(1.05);
        margin-right: 1rem;
    }

    /* Glassy sheen sweeping across the title */
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -20%;
        width: 20%;
        height: 100%;
        background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,0.5), rgba(255,255,255,0));
        transform: skewX(-20deg);
        filter: blur(1px);
        mix-blend-mode: screen;
        pointer-events: none;
        animation: headerShine 3.5s ease-in-out infinite;
    }
    
    .main-header .lucide-icon {
        margin-right: 0.75rem;
    }
    
    .main-header .lucide-icon svg {
        width: 2.2rem;
        height: 2.2rem;
        animation: iconFloat 3s ease-in-out infinite;
    }
    
    .main-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 120px;
        height: 5px;
        background: linear-gradient(90deg, #4CAF50, #FFC107);
        border-radius: 10px;
        animation: warmGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes warmGlow {
        from { box-shadow: 0 0 15px rgba(76, 175, 80, 0.4); }
        to { box-shadow: 0 0 25px rgba(76, 175, 80, 0.6); }
    }

    /* Header animations */
    @keyframes titleGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes titleReveal {
        0% { opacity: 0; transform: translateY(-8px) scale(0.98); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
    }
    @keyframes headerShine {
        0% { left: -30%; opacity: 0.0; }
        10% { opacity: 0.6; }
        50% { left: 110%; opacity: 0.0; }
        100% { left: 110%; opacity: 0.0; }
    }
    @keyframes iconFloat {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-4px); }
    }
    
    .subtitle {
        font-size: 1.05rem;
        text-align: center;
        color: #37474F;
        padding-bottom: 0.25rem;
        padding-top: 0rem !important;
        margin-top: -0.3rem !important;
        margin-bottom: 0rem;
        font-weight: 500;
        letter-spacing: 0.3px;
    }
    
    /* Friendly Sidebar - Cream White - Curvy Glassy Border with Animation */
    [data-testid="stSidebar"] {
        background: rgba(255, 249, 230, 0.85) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border-right: none !important;
        border-radius: 0 30px 30px 0 !important;
        box-shadow: 4px 0 24px rgba(76, 175, 80, 0.15),
                    0 0 0 2px rgba(76, 175, 80, 0.3) inset,
                    0 0 40px rgba(76, 175, 80, 0.1) !important;
        animation: slideInSidebar 0.5s ease-out, sidebarGlow 3s ease-in-out infinite !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    /* Animated glassy border effect for sidebar */
    [data-testid="stSidebar"]::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        right: 0 !important;
        width: 4px !important;
        height: 100% !important;
        background: linear-gradient(
            180deg,
            rgba(76, 175, 80, 0.8),
            rgba(255, 193, 7, 0.6),
            rgba(76, 175, 80, 0.8),
            rgba(255, 193, 7, 0.6),
            rgba(76, 175, 80, 0.8)
        ) !important;
        background-size: 100% 200% !important;
        animation: sidebarBorderGlow 3s ease-in-out infinite !important;
        border-radius: 0 30px 30px 0 !important;
        z-index: 1 !important;
        box-shadow: 0 0 20px rgba(76, 175, 80, 0.5), 0 0 40px rgba(255, 193, 7, 0.3) !important;
    }
    
    /* Shimmer effect on sidebar */
    [data-testid="stSidebar"]::after {
        content: '' !important;
        position: absolute !important;
        top: -50% !important;
        right: 0 !important;
        width: 100% !important;
        height: 200% !important;
        background: linear-gradient(
            180deg,
            transparent 0%,
            rgba(255, 255, 255, 0.3) 30%,
            rgba(76, 175, 80, 0.1) 50%,
            rgba(255, 255, 255, 0.3) 70%,
            transparent 100%
        ) !important;
        animation: sidebarShimmer 4s ease-in-out infinite !important;
        pointer-events: none !important;
        z-index: 0 !important;
    }
    
    @keyframes sidebarGlow {
        0%, 100% {
            box-shadow: 4px 0 24px rgba(76, 175, 80, 0.15),
                        0 0 0 2px rgba(76, 175, 80, 0.3) inset,
                        0 0 40px rgba(76, 175, 80, 0.1);
        }
        50% {
            box-shadow: 4px 0 32px rgba(76, 175, 80, 0.25),
                        0 0 0 3px rgba(76, 175, 80, 0.4) inset,
                        0 0 60px rgba(76, 175, 80, 0.2);
        }
    }
    
    @keyframes sidebarBorderGlow {
        0% {
            background-position: 0% 0%;
            opacity: 0.8;
        }
        50% {
            background-position: 0% 100%;
            opacity: 1;
        }
        100% {
            background-position: 0% 0%;
            opacity: 0.8;
        }
    }
    
    @keyframes sidebarShimmer {
        0% {
            transform: translateY(-100%) translateX(0);
            opacity: 0;
        }
        50% {
            opacity: 0.6;
        }
        100% {
            transform: translateY(100%) translateX(0);
            opacity: 0;
        }
    }
    
    /* Main content area - Independent Scrolling */
    [data-testid="stAppViewContainer"] {
        overflow: hidden !important;
        height: 100vh !important;
    }
    
    [data-testid="stAppViewContainer"] .main {
        overflow-y: auto !important;
        overflow-x: hidden !important;
        height: 100vh !important;
        padding-top: 0 !important;
    }
    
    /* Ensure sidebar content scrolls independently */
    [data-testid="stSidebar"] > div {
        overflow-y: auto !important;
        overflow-x: hidden !important;
        height: 100% !important;
    }
    
    @keyframes slideInSidebar {
        from {
            transform: translateX(-100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        padding: 0.5rem 0.75rem;
        padding-top: 0.3rem;
    }
    
    /* Sidebar Text Styling */
    [data-testid="stSidebar"] h3 {
        color: #4CAF50;
        font-weight: 700;
        margin-bottom: 0.3rem;
        margin-top: 0.4rem;
        font-size: 1.4rem;
        line-height: 1.3;
        animation: fadeInDown 0.6s ease-out;
        animation-fill-mode: both;
    }
    
    [data-testid="stSidebar"] h3:first-child {
        margin-top: 0.1rem;
        animation-delay: 0s;
        font-size: 1.5rem;
        color: #FFC107;
        text-shadow: 0 2px 8px rgba(255, 193, 7, 0.3);
        animation: fadeInDownOrange 0.8s ease-out, glowOrange 2s ease-in-out infinite;
        animation-fill-mode: both;
        position: relative;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        display: flex;
        align-items: center;
        flex-wrap: nowrap;
    }
    
    [data-testid="stSidebar"] h3:first-child::before {
        content: '';
        position: absolute;
        left: -10px;
        top: 50%;
        transform: translateY(-50%);
        width: 4px;
        height: 80%;
        background: linear-gradient(180deg, #FFC107, #FF9800);
        border-radius: 2px;
        animation: slideInLeftBar 0.8s ease-out;
    }
    
    @keyframes fadeInDownOrange {
        from {
            opacity: 0;
            transform: translateY(-15px) scale(0.9);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    @keyframes glowOrange {
        0%, 100% {
            text-shadow: 0 2px 8px rgba(255, 193, 7, 0.3), 0 0 20px rgba(255, 193, 7, 0.2);
        }
        50% {
            text-shadow: 0 2px 12px rgba(255, 193, 7, 0.5), 0 0 30px rgba(255, 193, 7, 0.4);
        }
    }
    
    @keyframes slideInLeftBar {
        from {
            width: 0;
            opacity: 0;
        }
        to {
            width: 4px;
            opacity: 1;
        }
    }
    
    [data-testid="stSidebar"] h3:nth-child(2) {
        animation-delay: 0.2s;
        margin-bottom: 0;
    }
    
    /* Tips heading specific styling */
    [data-testid="stSidebar"] h3:has(+ div) {
        margin-bottom: 0 !important;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    [data-testid="stSidebar"] h3 .lucide-icon svg {
        width: 1.4rem;
        height: 1.4rem;
    }
    
    [data-testid="stSidebar"] h3:first-child .lucide-icon svg {
        width: 1.6rem;
        height: 1.6rem;
        color: #FFC107;
        animation: iconPulse 2s ease-in-out infinite;
        filter: drop-shadow(0 2px 4px rgba(255, 193, 7, 0.4));
    }
    
    @keyframes iconPulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.1);
        }
    }
    
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] div {
        color: #37474F;
        font-weight: 500;
        margin-bottom: 0.2rem;
        margin-top: 0.1rem;
        line-height: 1.4;
    }
    
    [data-testid="stSidebar"] hr {
        margin: 0.1rem 0;
        border: none;
        border-top: 1px solid #e0e0e0;
    }
    
    [data-testid="stSidebar"] strong {
        color: #4CAF50;
        font-weight: 700;
        margin-bottom: 0.3rem;
        display: block;
        line-height: 1.3;
        font-size: 1.1rem;
        animation: fadeIn 0.5s ease-out;
        transition: transform 0.3s ease;
    }
    
    [data-testid="stSidebar"] strong:hover {
        transform: translateX(5px);
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    [data-testid="stSidebar"] strong .lucide-icon svg {
        width: 1.1rem;
        height: 1.1rem;
    }
    
    [data-testid="stSidebar"] .lucide-icon svg {
        width: 1.2rem;
        height: 1.2rem;
    }
    
    /* Friendly Sidebar Buttons - Rounded & Warm */
    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        background: #ffffff;
        border: 2px solid #4CAF50;
        border-radius: 20px;
        padding: 0.5rem 0.75rem;
        margin-bottom: 0.2rem;
        margin-top: 0.1rem;
        font-size: 0.9rem;
        font-weight: 600;
        color: #37474F;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.15);
        text-align: left;
        position: relative;
        overflow: hidden;
        line-height: 1.3;
        animation: slideInLeft 0.5s ease-out;
        animation-fill-mode: both;
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Stagger animation for buttons */
    [data-testid="stSidebar"] .stButton:nth-child(1) > button {
        animation-delay: 0.1s;
    }
    [data-testid="stSidebar"] .stButton:nth-child(2) > button {
        animation-delay: 0.2s;
    }
    [data-testid="stSidebar"] .stButton:nth-child(3) > button {
        animation-delay: 0.3s;
    }
    [data-testid="stSidebar"] .stButton:nth-child(4) > button {
        animation-delay: 0.4s;
    }
    
    /* Reduce spacing between button containers */
    [data-testid="stSidebar"] .stButton {
        margin-bottom: 0.1rem;
    }
    
    [data-testid="stSidebar"] .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #4CAF50 0%, #FFC107 100%);
        transition: left 0.3s ease;
        z-index: -1;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover::before {
        left: 0;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        color: white;
        transform: translateX(8px) scale(1.02);
        box-shadow: 0 8px 24px rgba(76, 175, 80, 0.3);
        border-color: transparent;
        animation: pulse 0.6s ease-in-out;
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: translateX(8px) scale(1.02);
        }
        50% {
            transform: translateX(8px) scale(1.05);
        }
    }
    
    /* Chat Bubble Style Input Field - Text Area (Expandable) */
    .stTextArea > div > div > textarea {
        border-radius: 25px;
        border: 2px solid #4CAF50;
        padding: 1.25rem 2rem;
        font-size: 1rem;
        font-weight: 400;
        background: #ffffff;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 16px rgba(76, 175, 80, 0.15);
        resize: vertical;
        min-height: 100px;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #FFC107;
        box-shadow: 0 0 0 4px rgba(255, 193, 7, 0.2), 0 6px 24px rgba(76, 175, 80, 0.25);
        background: #ffffff;
        outline: none;
        transform: translateY(-2px);
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: #9E9E9E;
        font-weight: 400;
    }
    
    /* Also style regular text input for consistency */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #4CAF50;
        padding: 1.25rem 2rem;
        font-size: 1rem;
        font-weight: 400;
        background: #ffffff;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 16px rgba(76, 175, 80, 0.15);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #FFC107;
        box-shadow: 0 0 0 4px rgba(255, 193, 7, 0.2), 0 6px 24px rgba(76, 175, 80, 0.25);
        background: #ffffff;
        outline: none;
        transform: translateY(-2px);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #9E9E9E;
        font-weight: 400;
    }
    
    /* Friendly Search Button - Leaf Green - Minimal Padding */
    .stButton > button {
        border-radius: 25px;
        background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem !important;
        font-weight: 700;
        font-size: 0.95rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.3);
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    /* Ripple effect for all buttons using ::before */
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
        z-index: 0;
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    /* Search icon styling - Applied via JavaScript */
    button.search-icon-added {
        padding-left: 1.8rem !important;
        padding-right: 1rem !important;
        position: relative !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 10px 32px rgba(76, 175, 80, 0.4);
        background: linear-gradient(135deg, #66BB6A 0%, #4CAF50 100%);
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(0.98);
    }
    
    /* Friendly Answer Container */
    .answer-container {
        background: #ffffff;
        padding: 2.5rem;
        border-radius: 25px;
        border: 2px solid #4CAF50;
        box-shadow: 0 8px 32px rgba(76, 175, 80, 0.15);
        margin: 2rem 0;
        position: relative;
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .answer-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background: linear-gradient(180deg, #4CAF50 0%, #FFC107 100%);
        border-radius: 25px 0 0 25px;
    }
    
    /* Friendly Scheme Cards */
    .scheme-card {
        background: #FFF9E6;
        padding: 1.5rem;
        border-radius: 20px;
        border: 2px solid #4CAF50;
        margin-bottom: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.15);
        position: relative;
        overflow: hidden;
    }
    
    .scheme-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background: linear-gradient(180deg, #4CAF50, #FFC107);
        transform: scaleY(0);
        transition: transform 0.3s ease;
    }
    
    .scheme-card:hover {
        box-shadow: 0 12px 32px rgba(76, 175, 80, 0.25);
        transform: translateY(-4px);
        border-color: #FFC107;
        background: #ffffff;
    }
    
    .scheme-card:hover::before {
        transform: scaleY(1);
    }
    
    /* Friendly Status Messages */
    .stSuccess {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        border-left: 5px solid #4CAF50;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 4px 16px rgba(76, 175, 80, 0.2);
    }
    
    .stInfo {
        background: linear-gradient(135deg, #FFF9E6 0%, #FFECB3 100%);
        border-left: 5px solid #FFC107;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 4px 16px rgba(255, 193, 7, 0.2);
    }
    
    .stError {
        background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%);
        border-left: 5px solid #F44336;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 4px 16px rgba(244, 67, 54, 0.2);
    }
    
    .stWarning {
        background: linear-gradient(135deg, #FFF9E6 0%, #FFECB3 100%);
        border-left: 5px solid #FFC107;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 4px 16px rgba(255, 193, 7, 0.2);
    }
    
    /* Friendly Expander */
    .streamlit-expanderHeader {
        background: #FFF9E6;
        border-radius: 20px;
        padding: 1.25rem 1.5rem;
        font-weight: 600;
        border: 2px solid #4CAF50;
        transition: all 0.3s ease;
        color: #37474F;
    }
    
    .streamlit-expanderHeader:hover {
        background: #ffffff;
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.2);
        border-color: #FFC107;
    }
    
    /* Section Headers - Keep original size for UI headers */
    .main h3:has(.lucide-icon) {
        color: #4CAF50;
        font-weight: 700;
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }
    
    /* Scheme Name Headings in Markdown - Make smaller */
    h2, 
    .stMarkdown h2, 
    .stMarkdown h3,
    [data-testid="stMarkdownContainer"] h2, 
    [data-testid="stMarkdownContainer"] h3 {
        font-size: 1.15rem !important;
        font-weight: 600;
        margin-bottom: 0.5rem;
        margin-top: 0.5rem;
        line-height: 1.4;
    }
    
    h3 .lucide-icon svg {
        width: 1.3rem;
        height: 1.3rem;
    }
    
    /* Button Icon Styling */
    .stButton > button .lucide-icon {
        margin-right: 0.5rem;
    }
    
    /* Main Content Text */
    .main {
        color: #37474F;
        position: relative;
        z-index: 1;
    }
    
    /* Additional glass effect wrapper for entire main area */
    [data-testid="stAppViewContainer"] {
        position: relative;
    }
    
    /* Ensure glass effect is visible on main content wrapper */
    [data-baseweb="modal"] {
        backdrop-filter: none !important;
    }
    
    /* Smooth Scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* Loading Spinner Enhancement */
    .stSpinner > div {
        border-color: #4CAF50 transparent transparent transparent;
        border-width: 3px;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.3rem;
        }
        
        .main .block-container {
            padding: 1.5rem;
            margin: 1rem;
            border-radius: 25px;
        }
        
        .stTextInput > div > div > input {
            padding: 1rem 1.5rem;
        }
        
        .stTextArea > div > div > textarea {
            padding: 1rem 1.5rem;
            min-height: 80px;
        }
    }
    
    /* Accessibility - Hidden Labels */
    label {
        visibility: hidden;
        height: 0;
        margin: 0;
        padding: 0;
    }
</style>
<script>
// Add search icon to Search button
(function() {
    function addSearchIcon() {
        const buttons = document.querySelectorAll('button[data-baseweb="button"]');
        buttons.forEach(function(btn) {
            const text = btn.textContent.trim();
            if (text === 'Search' && !btn.classList.contains('search-icon-added')) {
                btn.classList.add('search-icon-added');
                btn.style.paddingLeft = '1.8rem';
                btn.style.paddingRight = '1rem';
                btn.style.position = 'relative';
                
                // Create icon element
                const icon = document.createElement('span');
                icon.style.position = 'absolute';
                icon.style.left = '0.6rem';
                icon.style.top = '50%';
                icon.style.transform = 'translateY(-50%)';
                icon.style.width = '1.2rem';
                icon.style.height = '1.2rem';
                icon.style.backgroundImage = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='11' cy='11' r='8'/%3E%3Cpath d='m21 21-4.3-4.3'/%3E%3C/svg%3E\")";
                icon.style.backgroundSize = 'contain';
                icon.style.backgroundRepeat = 'no-repeat';
                icon.style.backgroundPosition = 'center';
                icon.style.zIndex = '2';
                icon.style.pointerEvents = 'none';
                btn.appendChild(icon);
            }
        });
    }
    
    // Run immediately and after DOM updates
    addSearchIcon();
    setTimeout(addSearchIcon, 100);
    setTimeout(addSearchIcon, 500);
    
    // Watch for new buttons
    const observer = new MutationObserver(addSearchIcon);
    observer.observe(document.body, { childList: true, subtree: true });
})();
</script>
""", unsafe_allow_html=True)


@st.cache_resource
def load_vector_database():
    """Load and cache the vector database"""
    try:
        db = get_vector_db()
        return db
    except Exception as e:
        st.error(f"Error loading vector database: {e}")
        return None


def load_qa_system():
    """Load the QA system"""
    # Get API key from environment or use the provided key
    api_key = os.getenv("GEMINI_API_KEY", "AIzaSyAkKlo45wq1v8HNBd_Fw1naw27JYltsDPI")
    
    if not api_key:
        st.error("Gemini API key not found. Please set GEMINI_API_KEY environment variable.")
        return None
    
    try:
        return get_qa_system(api_key)
    except Exception as e:
        st.error(f"Error initializing QA system: {e}")
        return None


def main():
    """Main application function"""
    
    # Header Section with Logo inline
    try:
        # Read logo image and convert to base64 for inline display
        import base64
        import os
        
        # Try PNG first, then JPG
        logo_file = None
        logo_format = None
        
        if os.path.exists("LOGO.png"):
            logo_file = "LOGO.png"
            logo_format = "png"
        elif os.path.exists("LOGO.jpg"):
            logo_file = "LOGO.jpg"
            logo_format = "jpeg"
        elif os.path.exists("LOGO.JPG"):
            logo_file = "LOGO.JPG"
            logo_format = "jpeg"
        elif os.path.exists("LOGO.PNG"):
            logo_file = "LOGO.PNG"
            logo_format = "png"
        
        if logo_file:
            with open(logo_file, "rb") as f:
                logo_data = base64.b64encode(f.read()).decode()
            logo_html = f'<img src="data:image/{logo_format};base64,{logo_data}" style="height: 5.5rem; width: auto; vertical-align: middle; margin-right: 1rem; display: inline-block; mix-blend-mode: multiply; background: transparent; object-fit: contain;" />'
        else:
            logo_html = ""
    except Exception as e:
        logo_html = ""  # If logo not found, no logo
    
    # Header with gradient - Logo inline with text - Positioned at top (higher and larger)
    st.markdown(f'<div class="main-header" style="display: flex; align-items: center; justify-content: center; margin-top: -1.5rem !important; padding-top: 0 !important;">{logo_html} Yojana Mitra: Your Smart Assistant for Maharashtra Government Schemes</div>', 
                unsafe_allow_html=True)
    
    # Initialize systems
    with st.spinner("Loading scheme database..."):
        db = load_vector_database()
    
    if db is None:
        st.error("Failed to load the database. Please check if the CSV file exists.")
        return
    
    # Initialize QA system
    qa_system = load_qa_system()
    if qa_system is None:
        st.error("Failed to initialize the AI system. Please check your API key.")
        return
    
    # Sidebar with examples
    with st.sidebar:
        st.markdown(f"### {get_icon('lightbulb', '1.2rem', '#4CAF50')} Quick Examples", unsafe_allow_html=True)
        st.markdown("Click any example below to get started:")
        # Categorized example queries
        st.markdown(f"**{get_icon('info', '1rem', '#4CAF50')} Scheme Information**", unsafe_allow_html=True)
        example_queries_info = [
            "Tell me about LIDCOM Margin Money Loan scheme",
            "What benefits does Ramai Awas Gharkul Scheme provide?",
            "What are the education assistance schemes?"
        ]
        
        for idx, query in enumerate(example_queries_info):
            if st.button(query, key=f"info_{idx}", use_container_width=True):
                st.session_state['query'] = query
        
        st.markdown("---")
        st.markdown(f"**{get_icon('file-check', '1rem', '#4CAF50')} Eligibility & Application**", unsafe_allow_html=True)
        example_queries_process = [
            "What is the eligibility for Indira Gandhi National Widow Pension Scheme?",
            "How to apply for Mahila Samridhi Yojana?",
            "What documents are needed for LIDCOM Training Scheme?"
        ]
        
        for idx, query in enumerate(example_queries_process):
            if st.button(query, key=f"process_{idx}", use_container_width=True):
                st.session_state['query'] = query
        
        st.markdown("---")
        st.markdown(f"**{get_icon('search', '1rem', '#4CAF50')} Category Search**", unsafe_allow_html=True)
        example_queries_category = [
            "List schemes for disabled persons",
            "Tell me about agricultural schemes",
            "What are the pension schemes?"
        ]
        
        for idx, query in enumerate(example_queries_category):
            if st.button(query, key=f"category_{idx}", use_container_width=True):
                st.session_state['query'] = query
        
        st.markdown(f"<h3 style='margin-bottom:0; margin-top:0.2rem'>{get_icon('lightbulb', '1.2rem', '#4CAF50')} Tips</h3>", unsafe_allow_html=True)
        tips_html = f"""
        <div style="background-color: #E8F5E9; padding: 0.75rem; border-radius: 8px; border-left: 4px solid #4CAF50; margin-top: 0;">
            <p style="margin: 0; color: #37474F; line-height: 1.4;">{get_icon('message-circle', '1rem', '#37474F')} Ask in natural language</p>
            <p style="margin: 0.3rem 0 0 0; color: #37474F; line-height: 1.4;">{get_icon('edit', '1rem', '#37474F')} Be specific for better results</p>
            <p style="margin: 0.3rem 0 0 0; color: #37474F; line-height: 1.4;">{get_icon('search', '1rem', '#37474F')} Try different phrasings if needed</p>
        </div>
        """
        st.markdown(tips_html, unsafe_allow_html=True)
    
    # Main query input section (pushed further down)
    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
    st.markdown(f"### {get_icon('help-circle', '1.3rem', '#4CAF50')} Find Scheme Information", unsafe_allow_html=True)
    
    # Create a container for better visual grouping
    user_query = st.text_area(
            "Query",
        value=st.session_state.get('query', ''),
            placeholder="Example: 'What is the eligibility for Indira Gandhi National Widow Pension Scheme?' or 'How to apply for Mahila Samridhi Yojana?'",
            key="main_query",
            label_visibility="collapsed",
            height=100
    )
    
    # Button below text area - with spacing
    st.markdown("<div style='margin-top: 0.5rem; margin-bottom: 1rem;'></div>", unsafe_allow_html=True)
    submit_button = st.button("Search", type="primary", use_container_width=False, key="search_btn")
    
    # Clear session state query after using it
    if 'query' in st.session_state and not submit_button:
        del st.session_state['query']
    
    # Process query
    if submit_button or user_query:
        if not user_query.strip():
            st.warning("Please enter a question to get started.")
        else:
            try:
                # Show loading spinner
                with st.spinner("Finding relevant schemes for you..."):
                    # Search for relevant schemes - increased top_k for better matching
                    retrieved_schemes = db.search_schemes(user_query, top_k=8)
                
                if not retrieved_schemes:
                    st.error("I couldn't find relevant information for your query. Please try rephrasing or asking about a different scheme.")
                else:
                    # Generate answer
                    with st.spinner("Getting your information ready..."):
                        answer = qa_system.generate_answer(user_query, retrieved_schemes)
                    
                    # Display answer (formatted)
                    st.markdown("---")
                    st.markdown(f"### {get_icon('sparkles', '1.3rem', '#4CAF50')} Scheme Information", unsafe_allow_html=True)
                    formatted_answer = format_answer_md(user_query, answer)
                    # EXTRA SAFETY NET: Remove colons from section labels and double colons right before display
                    import re
                    lines = formatted_answer.split('\n')
                    final_lines = []
                    for line in lines:
                        # If line is a section label (with emoji or icon), remove colon from it
                        # Check for both emojis and icons (HTML span with lucide-icon class)
                        if re.match(r'^\s*\*\*[📋💰✅📝📄🔗]', line) or re.search(r'<span class="lucide-icon"', line):
                            # Remove colon from section label
                            line = re.sub(r'(\*\*[📋💰✅📝📄🔗][^*]+?):(\*\*)', r'\1\2', line)  # Colon inside bold
                            line = re.sub(r'(\*\*[📋💰✅📝📄🔗][^*]+?\*\*):', r'\1', line)  # Colon outside bold
                            # Also handle icons - remove colon after icon HTML
                            line = re.sub(r'(<span class="lucide-icon"[^>]*></span>)\s*([^:]+?):', r'\1 \2', line)
                            line = line.rstrip(':')  # Remove any trailing colon
                        # Also remove double colons
                        while '::' in line:
                            line = line.replace('::', ':')
                        final_lines.append(line)
                    formatted_answer = '\n'.join(final_lines)
                    # Use unsafe_allow_html=True to render HTML icons
                    st.markdown(formatted_answer, unsafe_allow_html=True)
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Please try again with a different query or check your connection.")
    


if __name__ == "__main__":
    main()

