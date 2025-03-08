#!/usr/bin/env python3
"""
File Organizer

A simple command-line tool to organize files by extension and name patterns,
and generate reports about file organization.

This script helps users to:
1. Organize files into folders based on file types
2. Organize files by name patterns
3. Generate reports of file structure to identify deletion candidates
4. Perform multiple operations with an interactive menu

Author: [James Patrick De Mesa]
GitHub: [SaucesCode]
License: MIT
"""

import os
import shutil
from pathlib import Path
import time
import re
import argparse
import sys

def organize_files(directory_path, organize_by_name=True):
    """
    Organizes files in the specified directory by their file extensions and/or name patterns.
    Creates folders for each file type and moves files into them.
    
    Args:
        directory_path (str): Path to the directory to organize
        organize_by_name (bool): Whether to also organize by filename patterns
    
    Returns:
        int: Number of files moved
    """
    # Convert to absolute path and ensure the directory exists
    directory = os.path.abspath(directory_path)
    
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return 0
    
    print(f"Starting to organize files in: {directory}")
    
    # Dictionary to map file extensions to folder names
    extension_map = {
        # Documents
        '.doc': 'Documents/Word',
        '.docx': 'Documents/Word',
        '.pdf': 'Documents/PDF',
        '.txt': 'Documents/Text',
        '.rtf': 'Documents/Text',
        '.xlsx': 'Documents/Excel',
        '.xls': 'Documents/Excel',
        '.pptx': 'Documents/PowerPoint',
        '.ppt': 'Documents/PowerPoint',
        
        # Images
        '.jpg': 'Images/JPEG',
        '.jpeg': 'Images/JPEG',
        '.png': 'Images/PNG',
        '.gif': 'Images/GIF',
        '.bmp': 'Images/BMP',
        '.svg': 'Images/SVG',
        
        # Audio
        '.mp3': 'Audio/MP3',
        '.wav': 'Audio/WAV',
        '.flac': 'Audio/FLAC',
        '.aac': 'Audio/AAC',
        
        # Video
        '.mp4': 'Video/MP4',
        '.avi': 'Video/AVI',
        '.mkv': 'Video/MKV',
        '.mov': 'Video/MOV',
        
        # Archives
        '.zip': 'Archives/ZIP',
        '.rar': 'Archives/RAR',
        '.tar': 'Archives/TAR',
        '.gz': 'Archives/GZ',
        
        # Programming
        '.py': 'Programming/Python',
        '.java': 'Programming/Java',
        '.cpp': 'Programming/C++',
        '.c': 'Programming/C',

        # Web development files (grouped together)
        '.html': 'WebDevelopment',
        '.htm': 'WebDevelopment',
        '.css': 'WebDevelopment',
        '.js': 'WebDevelopment',
        '.php': 'WebDevelopment',
        '.jsx': 'WebDevelopment',
        '.ts': 'WebDevelopment',
        '.tsx': 'WebDevelopment',
    }
    
    # Dictionary of name patterns to recognize
    name_patterns = {
        r'backup|bak': 'BackupFiles',
        r'temp|tmp': 'TemporaryFiles',
        r'draft|wip': 'WorkInProgress',
        r'old|outdated|deprecated': 'OldFiles',
        r'screenshot|screen|scrn': 'Screenshots',
        r'report|review': 'Reports',
        r'invoice|receipt|bill': 'FinancialDocs',
        r'log|logs': 'LogFiles',
        r'presentation|slides': 'Presentations',
        r'project|prj': 'ProjectFiles',
        r'data|dataset': 'DataFiles',
        r'test|testing': 'TestFiles',
        r'sample|example': 'SampleFiles',
        r'config|cfg|settings': 'ConfigFiles',
        r'note|notes': 'Notes',
        r'download|dl': 'Downloads',
        r'scan|scanned': 'ScannedDocs',
        r'(20\d{2})[-_]?(0[1-9]|1[0-2])[-_]?(0[1-9]|[12][0-9]|3[01])': 'DateFormattedFiles',
        r'website|site|web': 'WebProjects',
    }
    
    # Create a counter for moved files
    moved_files = 0
    
    # Process each file in the directory
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            # Skip directories
            if os.path.isdir(file_path):
                continue
            
            # Get file extension (lowercase for consistency)
            base_name, extension = os.path.splitext(filename)
            extension = extension.lower()
            
            # Check for name patterns first if enabled
            name_matched = False
            if organize_by_name:
                for pattern, folder in name_patterns.items():
                    if re.search(pattern, filename, re.IGNORECASE):
                        folder_name = folder
                        name_matched = True
                        break
            
            # If no name match or name matching is disabled, use extension
            if not name_matched:
                if extension in extension_map:
                    folder_name = extension_map[extension]
                else:
                    folder_name = f"Other/{extension[1:] if extension else 'No_Extension'}"
            
            # Create target folder path
            target_folder = os.path.join(directory, folder_name)
            
            # Create the folder if it doesn't exist
            os.makedirs(target_folder, exist_ok=True)
            
            # Create target file path
            target_path = os.path.join(target_folder, filename)
            
            # If file with same name exists, add timestamp to filename
            if os.path.exists(target_path):
                name, ext = os.path.splitext(filename)
                timestamp = time.strftime("_%Y%m%d_%H%M%S")
                new_filename = f"{name}{timestamp}{ext}"
                target_path = os.path.join(target_folder, new_filename)
            
            try:
                # Move the file
                shutil.move(file_path, target_path)
                print(f"Moved: {filename} -> {folder_name}/{os.path.basename(target_path)}")
                moved_files += 1
            except Exception as e:
                print(f"Error moving {filename}: {e}")
    except Exception as e:
        print(f"Error while organizing files: {e}")
    
    print(f"\nOrganization complete! {moved_files} files organized.")
    return moved_files

def generate_report(directory_path, report_filename="file_organization_report.txt"):
    """
    Generates a report of the directory structure to help identify files for deletion.
    
    Args:
        directory_path (str): Path to the directory to analyze
        report_filename (str): Name of the report file
    
    Returns:
        str: Path to the generated report
    """
    directory = os.path.abspath(directory_path)
    report_path = os.path.join(directory, report_filename)
    
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return None
    
    print(f"Generating file report for: {directory}")
    print(f"This may take a moment for directories with many files...")
    
    try:
        with open(report_path, "w", encoding="utf-8") as report:
            report.write(f"File Organization Report - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            report.write(f"{'='*50}\n\n")
            report.write(f"Directory: {directory}\n\n")
            
            total_files = 0
            total_size = 0
            potential_deletions = []
            
            # Categories that might be candidates for deletion
            deletion_categories = ["TemporaryFiles", "BackupFiles", "OldFiles", 
                                  "Duplicates", "Downloads", "Cache"]
            
            # Walk through all directories and subdirectories
            for root, dirs, files in os.walk(directory):
                # Skip the report file itself
                files = [f for f in files if f != report_filename]
                
                if files:
                    rel_path = os.path.relpath(root, directory)
                    if rel_path == ".":
                        rel_path = "Root Directory"
                    
                    report.write(f"\n{rel_path} ({len(files)} files):\n")
                    report.write(f"{'-'*50}\n")
                    
                    # Sort files by size for easier identification of large files
                    file_details = []
                    directory_size = 0
                    
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            size = os.path.getsize(file_path)
                            modified = os.path.getmtime(file_path)
                            age_days = (time.time() - modified) / (60 * 60 * 24)
                            
                            file_details.append((file, size, modified, age_days))
                            directory_size += size
                            
                            # Check if file might be a deletion candidate
                            is_candidate = False
                            for category in deletion_categories:
                                if category.lower() in rel_path.lower() or category.lower() in file.lower():
                                    is_candidate = True
                                    break
                            
                            # Add old files (>180 days) as potential candidates
                            if age_days > 180:
                                is_candidate = True
                            
                            if is_candidate:
                                potential_deletions.append((rel_path, file, size, age_days))
                            
                        except Exception as e:
                            file_details.append((file, 0, 0, 0))
                    
                    # Sort by size (largest first)
                    file_details.sort(key=lambda x: x[1], reverse=True)
                    
                    for file, size, modified, age_days in file_details:
                        size_str = format_size(size)
                        date_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(modified))
                        
                        report.write(f"  {file}\n")
                        report.write(f"    Size: {size_str} | Modified: {date_str} | Age: {age_days:.1f} days\n")
                    
                    report.write(f"  Total directory size: {format_size(directory_size)}\n")
                    
                    total_files += len(files)
                    total_size += directory_size
            
            # Write summary information
            report.write(f"\n{'='*50}\n")
            report.write(f"SUMMARY\n")
            report.write(f"{'='*50}\n")
            report.write(f"Total Files: {total_files}\n")
            report.write(f"Total Size: {format_size(total_size)}\n\n")
            
            # Write potential deletion candidates
            if potential_deletions:
                report.write(f"POTENTIAL DELETION CANDIDATES\n")
                report.write(f"{'='*50}\n")
                report.write("The following files might be candidates for deletion:\n\n")
                
                # Sort by size (largest first)
                potential_deletions.sort(key=lambda x: x[2], reverse=True)
                
                for rel_path, file, size, age_days in potential_deletions:
                    full_path = os.path.join(rel_path, file) if rel_path != "Root Directory" else file
                    report.write(f"- {full_path}\n")
                    report.write(f"  Size: {format_size(size)} | Age: {age_days:.1f} days\n")
                
                # Calculate potential space savings
                potential_savings = sum(item[2] for item in potential_deletions)
                report.write(f"\nPotential space savings: {format_size(potential_savings)} ({(potential_savings/total_size*100):.1f}% of total)\n")
        
        print(f"Report generated: {report_path}")
        return report_path
        
    except Exception as e:
        print(f"Error generating report: {e}")
        return None

def format_size(size_bytes):
    """Format file size in human-readable format"""
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes/1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes/(1024*1024):.1f} MB"
    else:
        return f"{size_bytes/(1024*1024*1024):.1f} GB"

def show_menu():
    """Display the main menu and get user choice"""
    print("\n" + "="*50)
    print("FILE ORGANIZER".center(50))
    print("="*50)
    print("1. Organize files by extension")
    print("2. Organize files by extension and name")
    print("3. Generate file report (without organizing)")
    print("4. Organize files and generate report")
    print("5. Exit")
    print("="*50)
    
    while True:
        try:
            choice = input("Enter your choice (1-5): ")
            choice = int(choice)
            if 1 <= choice <= 5:
                return choice
            else:
                print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Please enter a valid number.")

def get_directory_path():
    """Get directory path from user with validation"""

    print("\n📂 **How to Find Your Folder Path in Windows**")
    print("--------------------------------------------------")
    print("1️⃣ Open **File Explorer** and navigate to the folder.")
    print("2️⃣ Click the **address bar** at the top.")
    print("3️⃣ Copy the full folder path (e.g., `C:\\Users\\YourName\\Documents`).")
    print("4️⃣ Paste the copied path below and press **Enter**.")
    print("--------------------------------------------------\n")
    while True:
        directory = input("Enter the path of the directory to process: ")
        directory = os.path.expanduser(directory)  # Expand ~ to user home directory
        
        if os.path.exists(directory) and os.path.isdir(directory):
            return directory
        else:
            print(f"Error: '{directory}' is not a valid directory.")
            retry = input("Would you like to try again? (y/n): ").lower()
            if retry != 'y':
                return None

def main():
    # Check if arguments were provided
    parser = argparse.ArgumentParser(description="File Organizer - Organize files and generate reports")
    parser.add_argument("-d", "--directory", help="Directory path to process")
    parser.add_argument("-m", "--mode", type=int, choices=[1, 2, 3, 4], 
                        help="Mode of operation: 1-Organize by extension, 2-Organize by extension and name, "
                        "3-Generate report only, 4-Organize and generate report")
    parser.add_argument("-r", "--report", help="Name of report file (default: file_organization_report.txt)")
    
    args = parser.parse_args()
    
    # If arguments were provided, run in command line mode
    if args.directory and args.mode:
        directory = os.path.expanduser(args.directory)
        
        if not os.path.exists(directory) or not os.path.isdir(directory):
            print(f"Error: '{directory}' is not a valid directory.")
            return
        
        report_filename = args.report if args.report else "file_organization_report.txt"
        
        if args.mode == 1:
            organize_files(directory, organize_by_name=False)
        elif args.mode == 2:
            organize_files(directory, organize_by_name=True)
        elif args.mode == 3:
            generate_report(directory, report_filename)
        elif args.mode == 4:
            organize_files(directory, organize_by_name=True)
            generate_report(directory, report_filename)
            
    # Otherwise, run in interactive mode
    else:
        try:
            while True:
                choice = show_menu()
                
                if choice == 5:
                    print("Thank you for using File Organizer. Goodbye!")
                    break
                
                directory = get_directory_path()
                if not directory:
                    continue
                
                if choice == 1:
                    organize_files(directory, organize_by_name=False)
                elif choice == 2:
                    organize_files(directory, organize_by_name=True)
                elif choice == 3:
                    generate_report(directory)
                elif choice == 4:
                    organize_files(directory, organize_by_name=True)
                    generate_report(directory)
                
                another = input("\nWould you like to perform another operation? (y/n): ").lower()
                if another != 'y':
                    print("Thank you for using File Organizer. Goodbye!")
                    break
                    
        except KeyboardInterrupt:
            print("\nOperation cancelled by user. Exiting...")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()