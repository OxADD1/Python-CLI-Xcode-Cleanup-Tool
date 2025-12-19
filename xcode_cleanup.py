#!/usr/bin/env python3
"""
Xcode Cleanup Tool - Interactive CLI
Removes Xcode cache files and frees up disk space.
"""

import os
import subprocess
import shutil
from pathlib import Path
from typing import List, Dict, Tuple
import sys

try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.panel import Panel
    from rich.table import Table
    from rich import box
    import questionary
    from questionary import Style
except ImportError:
    print("❌ Missing required packages. Installing...")
    print("Note: Installing with --user flag for compatibility with Homebrew Python")
    try:
        # Use --break-system-packages for Python 3.13+ compatibility
        # Safe when combined with --user (installs to user directory only)
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "--user", "--break-system-packages", 
            "rich", "questionary"
        ])
        print("✅ Packages installed successfully!")
        print("Please run the script again: ./xcode_cleanup.py")
        sys.exit(0)
    except subprocess.CalledProcessError:
        print("\n❌ Auto-installation failed. Please install manually:")
        print("\nRecommended command:")
        print("  pip3 install --user --break-system-packages rich questionary")
        print("\nThen run the script again: ./xcode_cleanup.py")
        sys.exit(1)

console = Console()

# Cleanup categories configuration
CATEGORIES = [
    {
        'name': 'Derived Data',
        'path': '~/Library/Developer/Xcode/DerivedData',
        'description': 'Build artifacts and intermediate files. Safe to delete - Xcode will rebuild them.',
        'typical_size': '5-50GB',
        'safety': 'safe',
        'type': 'directory',
        'default': True
    },
    {
        'name': 'Unavailable Simulators',
        'path': 'xcrun simctl delete unavailable',
        'description': 'Removes old iOS Simulator instances that are no longer available.',
        'typical_size': 'Varies',
        'safety': 'safe',
        'type': 'command',
        'default': True
    },
    {
        'name': 'Device Support Files',
        'path': '~/Library/Developer/Xcode/iOS DeviceSupport',
        'description': 'Support files for old iOS versions from connected devices.',
        'typical_size': '1-10GB',
        'safety': 'safe',
        'type': 'directory',
        'default': True
    },
    {
        'name': 'Simulator Caches',
        'path': '~/Library/Developer/CoreSimulator/Caches',
        'description': 'Cache files from iOS Simulators. Safe to delete - simulators will recreate them.',
        'typical_size': '1-5GB',
        'safety': 'safe',
        'type': 'directory',
        'default': True
    },
    {
        'name': 'Archives',
        'path': '~/Library/Developer/Xcode/Archives',
        'description': 'Old app builds (.xcarchive files). Only delete if you don\'t need old builds.',
        'typical_size': '1-20GB',
        'safety': 'caution',
        'type': 'directory',
        'default': False
    },
    {
        'name': 'Device Logs',
        'path': '~/Library/Developer/Xcode/iOS Device Logs',
        'description': 'Debug logs from connected iOS devices. Safe to delete.',
        'typical_size': '100MB-1GB',
        'safety': 'safe',
        'type': 'directory',
        'default': True
    },
    {
        'name': 'Swift Package Manager Cache',
        'path': '~/Library/Caches/org.swift.swiftpm',
        'description': 'Downloaded Swift packages. Safe to delete - they\'ll be re-downloaded when needed.',
        'typical_size': '1-5GB',
        'safety': 'safe',
        'type': 'directory',
        'default': True
    },
    {
        'name': 'Xcode Previews',
        'path': '~/Library/Developer/Xcode/Previews',
        'description': 'SwiftUI Preview cache files. Safe to delete - Xcode will regenerate them.',
        'typical_size': '500MB-2GB',
        'safety': 'safe',
        'type': 'directory',
        'default': True
    },
    {
        'name': 'System Caches',
        'path': '~/Library/Caches/com.apple.dt.Xcode',
        'description': 'Various Xcode-related system caches. Advanced option.',
        'typical_size': '1-3GB',
        'safety': 'advanced',
        'type': 'directory',
        'default': False
    }
]

# Custom style for questionary - neutral green theme
custom_style = Style([
    ('qmark', 'fg:#00aa00 bold'),
    ('question', 'bold'),
    ('answer', 'fg:#00aa00 bold'),
    ('pointer', 'fg:#00aa00 bold'),
    ('highlighted', 'fg:#00aa00'),
    ('selected', 'fg:#00aa00'),
    ('separator', 'fg:#666666'),
    ('instruction', 'fg:#888888'),
    ('text', ''),
])


def get_directory_size(path: str) -> Tuple[str, int]:
    """Get the size of a directory."""
    expanded_path = os.path.expanduser(path)
    
    if not os.path.exists(expanded_path):
        return "Not found", 0
    
    try:
        result = subprocess.run(
            ['du', '-sh', expanded_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            size = result.stdout.split('\t')[0].strip()
            return size, 1  # Return 1 to indicate it exists
        return "Error", 0
    except Exception:
        return "Error", 0


def get_available_space() -> str:
    """Get available disk space."""
    try:
        result = subprocess.run(
            ['df', '-h', '/'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                parts = lines[1].split()
                if len(parts) >= 4:
                    return parts[3]  # Available space
        return "Unknown"
    except Exception:
        return "Unknown"


def show_header():
    """Display the application header."""
    console.clear()
    
    header = Panel.fit(
        "[bold]🧹 Xcode Cleanup Tool[/bold]\n"
        "Free up disk space by removing Xcode cache files"
    )
    console.print(header)
    console.print()
    
    available = get_available_space()
    console.print(f"[bold]Available Disk Space:[/bold] {available}")
    console.print()


def format_category_choice(category: Dict) -> str:
    """Format a category for display in the checkbox list."""
    safety_icons = {
        'safe': '🟢',
        'caution': '🟡',
        'advanced': '🟠'
    }
    
    icon = safety_icons.get(category['safety'], '⚪')
    name = category['name']
    typical = category['typical_size']
    
    return f"{icon} {name} (typically {typical})"


def show_category_details():
    """Show detailed information about all categories."""
    table = Table(title="Cleanup Categories", box=box.ROUNDED)
    
    table.add_column("Category", no_wrap=True)
    table.add_column("Description")
    table.add_column("Size")
    table.add_column("Safety")
    
    for category in CATEGORIES:
        safety_display = {
            'safe': '✓ Safe',
            'caution': '⚠️  Caution',
            'advanced': '⚡ Advanced'
        }
        
        if category['type'] == 'directory':
            size, _ = get_directory_size(category['path'])
        else:
            size = 'N/A'
        
        table.add_row(
            category['name'],
            category['description'],
            size,
            safety_display.get(category['safety'], 'Unknown')
        )
    
    console.print(table)
    console.print()


def select_categories() -> List[Dict]:
    """Interactive category selection."""
    choices = [
        {
            'name': format_category_choice(cat),
            'value': cat,
            'checked': cat['default']
        }
        for cat in CATEGORIES
    ]
    
    console.print("[bold]Select items to clean:[/bold]")
    console.print("Use ↑↓ to navigate, Space to toggle, 'a' to select all, Enter to confirm")
    console.print()
    
    selected = questionary.checkbox(
        '',
        choices=choices,
        style=custom_style
    ).ask()
    
    return selected if selected else []


def clean_directory(path: str) -> Tuple[bool, str, str]:
    """Clean a directory by removing all its contents."""
    expanded_path = os.path.expanduser(path)
    
    if not os.path.exists(expanded_path):
        return True, "Directory not found", "0B"
    
    # Get size before deletion
    size_before, _ = get_directory_size(path)
    
    try:
        # Remove all contents
        for item in os.listdir(expanded_path):
            item_path = os.path.join(expanded_path, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
        
        return True, "Cleaned successfully", size_before
    except Exception as e:
        return False, f"Error: {str(e)}", "0B"


def execute_command(command: str) -> Tuple[bool, str]:
    """Execute a shell command."""
    try:
        result = subprocess.run(
            command.split(),
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return True, "Executed successfully"
        else:
            return True, "No unavailable simulators found"
    except Exception as e:
        return False, f"Error: {str(e)}"


def perform_cleanup(categories: List[Dict]) -> List[Dict]:
    """Perform the cleanup operation."""
    results = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        
        task = progress.add_task("Cleaning...", total=len(categories))
        
        for category in categories:
            progress.update(task, description=f"Cleaning: {category['name']}")
            
            if category['type'] == 'directory':
                success, message, size = clean_directory(category['path'])
                results.append({
                    'name': category['name'],
                    'success': success,
                    'message': message,
                    'size': size
                })
            elif category['type'] == 'command':
                success, message = execute_command(category['path'])
                results.append({
                    'name': category['name'],
                    'success': success,
                    'message': message,
                    'size': 'N/A'
                })
            
            progress.advance(task)
    
    return results


def show_results(results: List[Dict]):
    """Display cleanup results."""
    console.print()
    console.print("[bold]✨ Cleanup Completed![/bold]")
    console.print()
    
    table = Table(title="Results", box=box.ROUNDED)
    table.add_column("Category")
    table.add_column("Status")
    table.add_column("Size Freed")
    
    for result in results:
        status_icon = "✓" if result['success'] else "✗"
        
        table.add_row(
            result['name'],
            f"{status_icon} {result['message']}",
            result['size']
        )
    
    console.print(table)
    console.print()
    
    new_space = get_available_space()
    console.print(f"[bold]New Available Space:[/bold] {new_space}")
    console.print()


def main():
    """Main application flow."""
    try:
        # Show header
        show_header()
        
        # Show category details
        show_details = questionary.confirm(
            "Would you like to see detailed information about all categories?",
            default=False,
            style=custom_style
        ).ask()
        
        if show_details:
            console.print()
            show_category_details()
        
        # Select categories
        selected_categories = select_categories()
        
        if not selected_categories:
            console.print("[yellow]No categories selected. Exiting.[/yellow]")
            return
        
        console.print()
        console.print(f"Selected {len(selected_categories)} categories for cleanup")
        console.print()
        
        # Confirmation
        confirm = questionary.confirm(
            f"⚠️  Delete cache files from {len(selected_categories)} categories? "
            "(Your projects and source code will NOT be affected)",
            default=False,
            style=custom_style
        ).ask()
        
        if not confirm:
            console.print("[yellow]Cleanup cancelled.[/yellow]")
            return
        
        console.print()
        
        # Perform cleanup
        results = perform_cleanup(selected_categories)
        
        # Show results
        show_results(results)
        
        # Optional: Empty trash
        empty_trash = questionary.confirm(
            "Would you like to empty the Trash?",
            default=False,
            style=custom_style
        ).ask()
        
        if empty_trash:
            console.print("Emptying trash...")
            try:
                subprocess.run(
                    ['osascript', '-e', 'tell application "Finder" to empty trash'],
                    capture_output=True,
                    timeout=30
                )
                console.print("✓ Trash emptied")
            except Exception:
                console.print("✗ Failed to empty trash")
        
        console.print()
        console.print("[bold]🎉 All done![/bold]")
        
    except KeyboardInterrupt:
        console.print()
        console.print("Cleanup cancelled by user.")
        sys.exit(0)
    except Exception as e:
        console.print()
        console.print(f"[bold]Error: {str(e)}[/bold]")
        sys.exit(1)


if __name__ == '__main__':
    main()
