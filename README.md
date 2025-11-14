# 🧩 Identify Duplicate Assets in `.xcassets`

This Python script scans `.xcassets` folders inside your iOS project to identify duplicate image assets — even when filenames differ but image contents are identical.  
It’s perfect for large Xcode projects where redundant icons and images increase app size.

---

## 🚀 Getting Started

### Prerequisites

To run the Duplicate Asset Finder, you need:

- **Python 3.8+** installed on your system  
- **Pillow** library for image normalization  

Install Pillow using pip:

```bash
pip install pillow
```
<br>

### How to Use

Clone the repository Or download .py file:

```bash
git clone https://github.com/yourusername/xcassets-duplicate-finder.git
```


<br>

Run the script:

```bash
python3 find_xcassets_duplicates_cross_only_collapsed_scales.py
```

<br>


When you run the script, you’ll be prompted for two inputs:

```bash
Enter the root directory of your Xcode project (if you dont want to give entire repo access - club
all .xcassets folder to new folder and give access of new folder):
> /Users/username/Projects/MyiOSApp
```




```bash
Enter the directory path where you want to save duplicate_assets.csv:
> /Users/username/Desktop
```

<br>

The script will then:

- Scan all .xcassets folders recursively
- Compare normalized image hashes (pixel-by-pixel)
- Output a grouped CSV file listing duplicates

<br>

🧼 Tips for Cleanup

- Once duplicates are identified:
- Choose one canonical image set to keep.
- Update references in your Xcode project to point to that image.
- Safely remove the redundant .imageset directories.
