# Store ID Comparator - Web Application

This is a web-based version of the Store ID Comparator that allows you to compare two lists of store IDs and find the differences between them.

## Features

- **Dual Input Methods**: Support for both file upload and manual text entry
- **Drag & Drop**: Simply drag and drop files onto the upload areas
- **Real-time Validation**: Buttons are enabled/disabled based on input availability
- **Detailed Statistics**: View comprehensive statistics about your comparison
- **Multiple Export Options**: Copy results to clipboard or download as files
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Tab-based Results**: View results in organized tabs

## How to Use

### 1. Start the Application

#### Option A: Simple HTTP Server (Recommended)
```bash
# Navigate to the project directory
cd path/to/compare_2_id_lists

# Start a simple HTTP server
python -m http.server 8080

# Open your browser and go to: http://localhost:8080
```

#### Option B: Direct File Opening
Simply open the `index.html` file in your web browser (some features may be limited due to browser security restrictions).

### 2. Input Your Data

**For each file, you can choose between two input methods:**

#### Method 1: File Upload
- Click the "Upload from file" radio button
- Click "Choose File" or drag and drop a text file into the upload area
- Supported formats: .txt, .csv (one ID per line)

#### Method 2: Manual Entry
- Click the "Enter manually" radio button
- Type or paste your store IDs into the text area (one per line)

### 3. Compare the Files

- Once both files have data, the "Compare Files" button will become active
- Click "Compare Files" to start the comparison
- Wait for the results to appear

### 4. View Results

The results are displayed in two tabs:
- **Only in File 1**: IDs that exist only in the first file
- **Only in File 2**: IDs that exist only in the second file

### 5. Statistics

The application provides comprehensive statistics:
- Total IDs in each file
- Number of unique IDs in each file
- Number of common IDs between files

### 6. Export Results

**Copy to Clipboard:**
- Click "Copy Result 1" or "Copy Result 2" to copy specific results
- Paste the results anywhere you need them

**Download Files:**
- Click "Download Results" to download separate files for each result set
- Click "Download Combined" to download a single file with all results and statistics

**Clear Results:**
- Click "Clear Results" to reset the application for a new comparison

## File Format

Your input files should contain one store ID per line:
```
123
456
789
ABC123
DEF456
```

## Browser Compatibility

- Chrome 60+
- Firefox 60+
- Safari 12+
- Edge 79+

## Features Comparison with Python GUI

| Feature | Python GUI | Web App |
|---------|------------|---------|
| File Upload | ✅ | ✅ |
| Manual Input | ✅ | ✅ |
| Drag & Drop | ❌ | ✅ |
| Copy to Clipboard | ✅ | ✅ |
| Save Results | ✅ | ✅ |
| Statistics | ✅ | ✅ |
| Cross-platform | ❌ | ✅ |
| No Installation | ❌ | ✅ |
| Mobile Support | ❌ | ✅ |

## Troubleshooting

**Problem**: The "Compare Files" button is disabled
**Solution**: Make sure both files have data (either uploaded files or manual text entry)

**Problem**: Copy to clipboard doesn't work
**Solution**: Some browsers require HTTPS for clipboard access. Use the download feature instead, or run the app over HTTPS

**Problem**: File upload doesn't work
**Solution**: Make sure you're accessing the app via HTTP server, not by opening the HTML file directly

**Problem**: Results don't display
**Solution**: Check the browser console for errors and ensure your input files contain valid data

## Technical Details

- **Frontend**: Pure HTML5, CSS3, and JavaScript (ES6+)
- **No Dependencies**: No external libraries required
- **File Processing**: Client-side processing using File API
- **Browser Storage**: Results stored in memory (cleared on page refresh)

## Security Notes

- All processing is done client-side in your browser
- No data is sent to any external servers
- Files are processed locally and never uploaded anywhere
- Your data remains completely private and secure