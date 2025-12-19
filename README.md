# 🧹 Xcode Cleanup Tool

**An interactive command-line tool to clean Xcode cache files and free up disk space.**

![Platform](https://img.shields.io/badge/platform-macOS-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

Remove gigabytes of Xcode cache files safely and easily with an interactive terminal interface. Perfect for iOS/macOS developers who want to reclaim disk space without risking their projects.

---

## ✨ Features

- 🎯 **Interactive Checkbox Selection** - Choose exactly what to clean
- 🎨 **Beautiful Terminal UI** - Rich colors and formatting
- 📊 **Real-time Storage Calculation** - See how much space each category uses
- ⚡ **Progress Tracking** - Animated progress bar during cleanup
- 🔒 **Safety First** - Multiple confirmations and color-coded warnings
- 🌍 **Clear Explanations** - Detailed English descriptions for every option
- 🚀 **Auto-installation** - Automatically installs required packages
- 💾 **Significant Space Savings** - Typically frees 10-100GB

---


## 🚀 Quick Start

### Prerequisites

- **macOS** (any recent version)
- **Python 3.7 or later** (usually pre-installed on macOS)
- **Xcode** (to have cache files to clean)

### Installation

**1. Clone the repository:**

```bash
git clone https://github.com/OxADD1/Python-CLI-Xcode-Cleanup-Tool.git
```

**2. Navigate to directory:**

```bash
cd Python-CLI-Xcode-Cleanup-Tool
```

**3. Make executable:**

```bash
chmod +x xcode_cleanup.py
```

**4. Run the tool:**

```bash
./xcode_cleanup.py
```

**Alternative:** Run directly with Python (no chmod needed)

```bash
python3 xcode_cleanup.py
```

---

## 📋 What Gets Cleaned?

| Category | Size | Safety | Default | Description |
|----------|------|--------|---------|-------------|
| **Derived Data** | 5-50GB | 🟢 Safe | ✓ | Build artifacts - Xcode will rebuild |
| **Unavailable Simulators** | Varies | 🟢 Safe | ✓ | Old simulator instances |
| **Device Support** | 1-10GB | 🟢 Safe | ✓ | Old iOS version support files |
| **Simulator Caches** | 1-5GB | 🟢 Safe | ✓ | Simulator cache files |
| **Archives** | 1-20GB | 🟡 Caution | ✗ | Old app builds (keep if needed) |
| **Device Logs** | 100MB-1GB | 🟢 Safe | ✓ | Debug logs from devices |
| **Swift PM Cache** | 1-5GB | 🟢 Safe | ✓ | Downloaded Swift packages |
| **Xcode Previews** | 500MB-2GB | 🟢 Safe | ✓ | SwiftUI preview caches |
| **System Caches** | 1-3GB | 🟠 Advanced | ✗ | System-level Xcode caches |

### Safety Levels

- 🟢 **Safe** - Always safe to delete, Xcode will regenerate (selected by default)
- 🟡 **Caution** - Usually safe, but review first (unselected by default)
- 🟠 **Advanced** - For experienced users only (unselected by default)

---

## 💡 Usage

### Basic Usage

Simply run the script and follow the interactive prompts:

```bash
./xcode_cleanup.py
```

**Keyboard Shortcuts for Selection:**
- **↑/↓** - Navigate through items
- **Space** - Toggle individual item on/off
- **a** - Select/deselect all items at once
- **i** - Invert selection
- **Enter** - Confirm selection

### Step-by-Step Flow

1. **View Details** (Optional)
   - Choose whether to see detailed information about all categories

2. **Select Categories**
   - Use keyboard shortcuts above to select items
   - **Space** for individual selection, **a** for all, **i** to invert
   - Press **Enter** to confirm

3. **Confirm Cleanup**
   - Review your selections
   - Confirm the cleanup operation

4. **Watch Progress**
   - See real-time progress bar
   - View each category as it's cleaned

5. **View Results**
   - See what was cleaned
   - Check how much space was freed

6. **Empty Trash** (Optional)
   - Choose whether to empty the macOS Trash

### Example Sessions

**Quick Safe Cleanup:**
```bash
$ ./xcode_cleanup.py

Would you like to see detailed information? (y/N): n
[Keep default selections]
Confirm? (y/N): y

✨ Cleanup Completed!
Freed: 35.7 GB
```

**Full Cleanup with Archives:**
```bash
$ ./xcode_cleanup.py

Would you like to see detailed information? (y/N): y
[Navigate to Archives and press Space to select]
Confirm? (y/N): y

✨ Cleanup Completed!
Freed: 52.3 GB
```

---

## ⚙️ Installation & Setup

### Detailed Setup Instructions

**1. Check Python Version**

```bash
python3 --version
```

Should show Python 3.7 or later. If not installed:
- Download from [python.org](https://www.python.org/downloads/)
- Or install via Homebrew: `brew install python3`

**2. Download the Tool**

Clone the repository:
```bash
git clone https://github.com/OxADD1/Python-CLI-Xcode-Cleanup-Tool.git
```

Navigate to directory:
```bash
cd Python-CLI-Xcode-Cleanup-Tool
```

Make executable:
```bash
chmod +x xcode_cleanup.py
```

**3. Run the Tool**

```bash
./xcode_cleanup.py
```

**4. Install Dependencies**

The tool automatically installs required packages on first run.

**If auto-installation fails** (Homebrew Python users):

```bash
pip3 install --user rich questionary
```

Then run the tool again:

```bash
./xcode_cleanup.py
```

---

## 🛠️ Troubleshooting

### Common Issues

**"Permission Denied"**
```bash
chmod +x xcode_cleanup.py
```

**"python3: command not found"**
- Install Python 3 from [python.org](https://www.python.org/downloads/)
- Or use Homebrew: `brew install python3`

**"No module named 'rich'"**

The script should auto-install, but if it fails:
```bash
pip3 install rich questionary
```

**"No such file or directory"**

Some directories only exist after using Xcode. This is normal - the tool will skip them.

**Cleanup didn't free space**

- Check Trash - deleted files go there first
- Empty Trash to actually free space
- Some directories might be empty already

---

## 🔒 Safety & Privacy

### What's Safe?

- ✅ **Your source code is NEVER touched**
- ✅ **Your Xcode projects remain intact**
- ✅ **Only cache files are removed**
- ✅ **Xcode can regenerate everything we delete**
- ✅ **Multiple confirmations before deletion**

### What We Clean

Only Xcode cache directories:
- `~/Library/Developer/Xcode/DerivedData`
- `~/Library/Developer/Xcode/iOS DeviceSupport`
- `~/Library/Developer/CoreSimulator/Caches`
- `~/Library/Developer/Xcode/Archives` (optional)
- And similar cache locations

### What We Don't Touch

- ❌ Your code/projects
- ❌ Xcode application itself
- ❌ App Store downloads
- ❌ Personal files
- ❌ System files

---

## 📦 Requirements

### System Requirements

- **Operating System:** macOS (any recent version)
- **Python:** 3.7 or later
- **Disk Space:** ~15KB for the script itself
- **Xcode:** Installed (to have files to clean)

### Python Dependencies

Automatically installed on first run:
- [`rich`](https://github.com/Textualize/rich) >= 13.0.0 - Terminal UI
- [`questionary`](https://github.com/tmbo/questionary) >= 2.0.0 - Interactive prompts

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Ideas for Contributions

- [ ] Add command-line arguments (`--auto`, `--safe-only`, etc.)
- [ ] Export results to JSON/CSV
- [ ] Scheduled cleanup (cron job setup)
- [ ] Dry-run mode (preview without deleting)
- [ ] Support for other development tools (Android Studio, etc.)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ❓ FAQ

**Q: Will this delete my Xcode projects?**  
A: No! Only cache files are deleted. Your projects and source code are never touched.

**Q: How much space will I free?**  
A: Typically 10-100GB, depending on how long you've been using Xcode.

**Q: Can I undo the cleanup?**  
A: Deleted files go to Trash first. Don't empty Trash if you want to restore something.

**Q: Is it safe to delete Derived Data?**  
A: Yes! Xcode will rebuild it when you build your projects. This is the safest category.

**Q: Should I delete Archives?**  
A: Only if you don't need old app builds. These are .xcarchive files used for App Store submissions.

**Q: How often should I run this?**  
A: Monthly or when you're low on disk space. Some developers run it weekly.

**Q: Does this work on Linux or Windows?**  
A: No, it's designed for macOS only as Xcode is macOS-exclusive.

**Q: Do I need to install anything?**  
A: Just Python 3.7+. The tool auto-installs its dependencies.

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/OxADD1/Python-CLI-Xcode-Cleanup-Tool/issues)
- **Discussions:** [GitHub Discussions](https://github.com/OxADD1/Python-CLI-Xcode-Cleanup-Tool/discussions)

---

## 🙏 Acknowledgments

- Built with [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- Uses [Questionary](https://github.com/tmbo/questionary) for interactive prompts
- Inspired by the iOS developer community's need for disk space management

---

## 📊 Statistics

- **Lines of Code:** ~450
- **Dependencies:** 2
- **File Size:** ~15KB
- **Typical Space Freed:** 10-100GB
- **Average Runtime:** 1-5 minutes

---

**Made with ❤️ for iOS/macOS developers**

*Star ⭐ this repo if it helped you free up disk space!*
