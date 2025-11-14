# Identify-Duplicate-Assets-in-Xcode

🧩 Identify Duplicate Assets in .xcassets (Python Script)

This repository contains a Python script that scans your Xcode project’s .xcassets folders to identify duplicate image assets (even when filenames differ but image content is identical).
It is designed specifically for large iOS projects where multiple modules or teams might contribute duplicate assets, leading to unnecessary app size bloat.

📋 Overview

When working with large iOS codebases containing multiple .xcassets folders, it’s common to encounter identical icons scattered across various modules or frameworks.
This script helps detect such duplicates automatically by comparing image content hashes, not just filenames.

It supports:

✅ .png, .jpg, .jpeg, .heic, .heif, .webp image formats

✅ .pdf, .svg vector assets (hashed as binary)

✅ Nested .xcassets folders across the project

✅ Detection across scales (@1x, @2x, @3x)

✅ CSV output grouped by duplicate sets (with a blank line between groups for readability)

⚙️ How It Works

Recursively scans all .xcassets directories within your specified root project folder.

For each *.imageset, it:

Reads Contents.json to understand asset definitions.

Normalizes the image (via Pillow) and generates a SHA-256 hash of its raw pixel data.

Groups images having identical hashes (i.e., duplicates).

Writes results to a CSV file (e.g., duplicate_assets.csv) containing groups of duplicates separated by a blank line.

🧠 Dependencies

Python ≥ 3.8

Pillow (PIL fork) — used for image normalization

pip install pillow

🚀 Usage
1. Place the script in your desired directory

For example:

/Users/username/Documents/find_xcassets_duplicates_cross_only_collapsed_scales.py

2. Run the script from Terminal
python3 find_xcassets_duplicates_cross_only_collapsed_scales.py

3. When prompted, provide your project path:
Enter the root directory of your Xcode project:
> /Users/username/Projects/MyiOSApp

4.When prompted, Provide location to store output CSV
The script generates a file named:
duplicate_assets.csv

5. View the output CSV

The script generates a file named:

duplicate_assets.csv


Each “Group” represents a set of identical assets, e.g.:

Group 1, a5effda5cd9bec32..., /Assets/Assets.xcassets/Icn_close_refer.imageset
Group 1, a5effda5cd9bec32..., /Icons/Icons.xcassets/Icn_back_copy.imageset

Group 2, 856125a604c0bf46..., /Assets/Assets.xcassets/close_icn_negative_balance.imageset
Group 2, 856125a604c0bf46..., /Assets/Assets.xcassets/Icn_close_refer.imageset

🧼 Tips for Cleanup

Once duplicates are identified:

Choose one canonical image set to keep.

Update references in your Xcode project to point to that image.

Safely remove the redundant .imageset directories.

🧾 Output Format Summary
Column	Description
Group	Duplicate group number
Hash	SHA-256 hash identifying identical images
Path	Folder path of the .imageset containing the image

Blank lines separate groups for readability.
