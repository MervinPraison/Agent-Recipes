# AI Folder Packager

Package folder into distributable archive with manifest and checksums.

## Usage
```bash
praison run ai-folder-packager ./my-project
praison run ai-folder-packager ./my-project --format tar.gz
```

## Output
- `package.zip` - Archive file
- `manifest.json` - File list with hashes
- `checksums.txt` - SHA256 checksums
- `README.txt` - Auto-generated description
