// Global variables to store results
let comparisonResults = {
    onlyInFile1: new Set(),
    onlyInFile2: new Set(),
    file1Count: 0,
    file2Count: 0,
    commonCount: 0
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    setupDragAndDrop();
});

function setupEventListeners() {
    // File mode radio button listeners
    document.querySelectorAll('input[name="file1-mode"]').forEach(radio => {
        radio.addEventListener('change', () => toggleInputMode('file1'));
    });
    
    document.querySelectorAll('input[name="file2-mode"]').forEach(radio => {
        radio.addEventListener('change', () => toggleInputMode('file2'));
    });

    // File input listeners
    document.getElementById('file1-input').addEventListener('change', (e) => handleFileSelect(e, 'file1'));
    document.getElementById('file2-input').addEventListener('change', (e) => handleFileSelect(e, 'file2'));

    // Textarea listeners for real-time validation
    document.getElementById('file1-textarea').addEventListener('input', validateInputs);
    document.getElementById('file2-textarea').addEventListener('input', validateInputs);
}

function setupDragAndDrop() {
    const fileSections = document.querySelectorAll('.file-section');
    
    fileSections.forEach((section, index) => {
        const fileNum = index === 0 ? 'file1' : 'file2';
        
        section.addEventListener('dragover', (e) => {
            e.preventDefault();
            section.classList.add('dragover');
        });
        
        section.addEventListener('dragleave', () => {
            section.classList.remove('dragover');
        });
        
        section.addEventListener('drop', (e) => {
            e.preventDefault();
            section.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                const fileInput = document.getElementById(`${fileNum}-input`);
                fileInput.files = files;
                handleFileSelect({ target: fileInput }, fileNum);
                
                // Switch to upload mode if in manual mode
                document.getElementById(`${fileNum}-upload`).checked = true;
                toggleInputMode(fileNum);
            }
        });
    });
}

function toggleInputMode(fileNum) {
    const uploadContainer = document.getElementById(`${fileNum}-upload-container`);
    const manualContainer = document.getElementById(`${fileNum}-manual-container`);
    const isUploadMode = document.getElementById(`${fileNum}-upload`).checked;
    
    if (isUploadMode) {
        uploadContainer.style.display = 'block';
        manualContainer.classList.remove('active');
    } else {
        uploadContainer.style.display = 'none';
        manualContainer.classList.add('active');
    }
    
    validateInputs();
}

function handleFileSelect(event, fileNum) {
    const file = event.target.files[0];
    const infoDiv = document.getElementById(`${fileNum}-info`);
    
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const content = e.target.result;
            const lines = content.split('\n').filter(line => line.trim());
            
            infoDiv.innerHTML = `
                <div style="margin-top: 10px; padding: 10px; background: #e8f5e8; border-radius: 4px;">
                    <strong>File loaded:</strong> ${file.name}<br>
                    <strong>Size:</strong> ${(file.size / 1024).toFixed(2)} KB<br>
                    <strong>Lines:</strong> ${lines.length}
                </div>
            `;
        };
        reader.readAsText(file);
        
        showAlert('File loaded successfully!', 'success');
    } else {
        infoDiv.innerHTML = '';
    }
    
    validateInputs();
}

function clearFile(fileNum) {
    document.getElementById(`${fileNum}-input`).value = '';
    document.getElementById(`${fileNum}-info`).innerHTML = '';
    validateInputs();
}

function validateInputs() {
    const compareBtn = document.getElementById('compare-btn');
    let hasFile1 = false;
    let hasFile2 = false;
    
    // Check File 1
    if (document.getElementById('file1-upload').checked) {
        hasFile1 = document.getElementById('file1-input').files.length > 0;
    } else {
        hasFile1 = document.getElementById('file1-textarea').value.trim().length > 0;
    }
    
    // Check File 2
    if (document.getElementById('file2-upload').checked) {
        hasFile2 = document.getElementById('file2-input').files.length > 0;
    } else {
        hasFile2 = document.getElementById('file2-textarea').value.trim().length > 0;
    }
    
    compareBtn.disabled = !(hasFile1 && hasFile2);
}

async function compareFiles() {
    try {
        showLoading(true);
        clearAlerts();
        
        // Get IDs from both sources
        const ids1 = await getIdsFromSource('file1');
        const ids2 = await getIdsFromSource('file2');
        
        if (ids1.size === 0 || ids2.size === 0) {
            throw new Error('One or both files are empty or contain no valid IDs');
        }
        
        // Perform comparison
        const onlyInFile1 = new Set([...ids1].filter(id => !ids2.has(id)));
        const onlyInFile2 = new Set([...ids2].filter(id => !ids1.has(id)));
        const common = new Set([...ids1].filter(id => ids2.has(id)));
        
        // Store results globally
        comparisonResults = {
            onlyInFile1,
            onlyInFile2,
            file1Count: ids1.size,
            file2Count: ids2.size,
            commonCount: common.size
        };
        
        // Display results
        displayResults();
        showAlert(`Comparison completed! Found ${onlyInFile1.size} unique IDs in File 1 and ${onlyInFile2.size} unique IDs in File 2.`, 'success');
        
    } catch (error) {
        showAlert(`Error: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

async function getIdsFromSource(fileNum) {
    const isUploadMode = document.getElementById(`${fileNum}-upload`).checked;
    
    if (isUploadMode) {
        const fileInput = document.getElementById(`${fileNum}-input`);
        if (fileInput.files.length === 0) {
            throw new Error(`Please select ${fileNum}`);
        }
        
        const file = fileInput.files[0];
        const content = await readFileAsync(file);
        return parseIds(content);
    } else {
        const textarea = document.getElementById(`${fileNum}-textarea`);
        const content = textarea.value.trim();
        if (!content) {
            throw new Error(`Please enter content for ${fileNum}`);
        }
        return parseIds(content);
    }
}

function readFileAsync(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = e => resolve(e.target.result);
        reader.onerror = e => reject(new Error('Failed to read file'));
        reader.readAsText(file);
    });
}

function parseIds(content) {
    const lines = content.split('\n');
    const ids = new Set();
    
    lines.forEach(line => {
        const trimmed = line.trim();
        if (trimmed && trimmed.length > 0) {
            ids.add(trimmed);
        }
    });
    
    return ids;
}

function displayResults() {
    // Display results in textareas
    document.getElementById('result1-text').value = 
        comparisonResults.onlyInFile1.size > 0 
            ? [...comparisonResults.onlyInFile1].sort().join('\n')
            : 'No unique IDs found';
            
    document.getElementById('result2-text').value = 
        comparisonResults.onlyInFile2.size > 0 
            ? [...comparisonResults.onlyInFile2].sort().join('\n')
            : 'No unique IDs found';
    
    // Update statistics
    document.getElementById('file1-count').textContent = comparisonResults.file1Count;
    document.getElementById('file2-count').textContent = comparisonResults.file2Count;
    document.getElementById('only-file1-count').textContent = comparisonResults.onlyInFile1.size;
    document.getElementById('only-file2-count').textContent = comparisonResults.onlyInFile2.size;
    document.getElementById('common-count').textContent = comparisonResults.commonCount;
    
    // Show results section
    document.getElementById('results-section').classList.add('active');
    document.getElementById('stats').style.display = 'block';
    
    // Scroll to results
    document.getElementById('results-section').scrollIntoView({ behavior: 'smooth' });
}

function showTab(tabId) {
    // Hide all tab panes
    document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.classList.remove('active');
    });
    
    // Remove active class from all tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Show selected tab pane
    document.getElementById(tabId).classList.add('active');
    
    // Add active class to clicked tab
    event.target.classList.add('active');
}

async function copyResult(textareaId) {
    const textarea = document.getElementById(textareaId);
    const content = textarea.value.trim();
    
    if (!content || content === 'No unique IDs found') {
        showAlert('No data to copy!', 'warning');
        return;
    }
    
    try {
        await navigator.clipboard.writeText(content);
        showAlert('Results copied to clipboard!', 'success');
    } catch (err) {
        // Fallback for older browsers
        textarea.select();
        document.execCommand('copy');
        showAlert('Results copied to clipboard!', 'success');
    }
}

function downloadResults() {
    if (comparisonResults.onlyInFile1.size === 0 && comparisonResults.onlyInFile2.size === 0) {
        showAlert('No results to download!', 'warning');
        return;
    }
    
    // Download file 1 results
    if (comparisonResults.onlyInFile1.size > 0) {
        const content1 = [...comparisonResults.onlyInFile1].sort().join('\n');
        downloadFile(content1, 'only_in_file1.txt');
    }
    
    // Download file 2 results
    if (comparisonResults.onlyInFile2.size > 0) {
        const content2 = [...comparisonResults.onlyInFile2].sort().join('\n');
        downloadFile(content2, 'only_in_file2.txt');
    }
    
    showAlert('Results downloaded successfully!', 'success');
}

function downloadCombined() {
    if (comparisonResults.onlyInFile1.size === 0 && comparisonResults.onlyInFile2.size === 0) {
        showAlert('No results to download!', 'warning');
        return;
    }
    
    let content = '=== Store ID Comparison Results ===\n\n';
    content += `Total IDs in File 1: ${comparisonResults.file1Count}\n`;
    content += `Total IDs in File 2: ${comparisonResults.file2Count}\n`;
    content += `Common IDs: ${comparisonResults.commonCount}\n\n`;
    
    content += '=== Only in File 1 ===\n';
    if (comparisonResults.onlyInFile1.size > 0) {
        content += [...comparisonResults.onlyInFile1].sort().join('\n');
    } else {
        content += 'No unique IDs found';
    }
    
    content += '\n\n=== Only in File 2 ===\n';
    if (comparisonResults.onlyInFile2.size > 0) {
        content += [...comparisonResults.onlyInFile2].sort().join('\n');
    } else {
        content += 'No unique IDs found';
    }
    
    downloadFile(content, 'combined_results.txt');
    showAlert('Combined results downloaded successfully!', 'success');
}

function downloadFile(content, filename) {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

function clearResults() {
    document.getElementById('result1-text').value = '';
    document.getElementById('result2-text').value = '';
    document.getElementById('results-section').classList.remove('active');
    document.getElementById('stats').style.display = 'none';
    
    comparisonResults = {
        onlyInFile1: new Set(),
        onlyInFile2: new Set(),
        file1Count: 0,
        file2Count: 0,
        commonCount: 0
    };
    
    showAlert('Results cleared!', 'success');
}

function showLoading(show) {
    const loading = document.getElementById('loading');
    const compareBtn = document.getElementById('compare-btn');
    
    if (show) {
        loading.classList.add('active');
        compareBtn.disabled = true;
    } else {
        loading.classList.remove('active');
        compareBtn.disabled = false;
        validateInputs(); // Re-validate to set correct button state
    }
}

function showAlert(message, type) {
    const alertsContainer = document.getElementById('alerts');
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    // Add close button
    const closeBtn = document.createElement('span');
    closeBtn.innerHTML = ' ×';
    closeBtn.style.float = 'right';
    closeBtn.style.cursor = 'pointer';
    closeBtn.style.fontSize = '20px';
    closeBtn.style.fontWeight = 'bold';
    closeBtn.onclick = () => alertDiv.remove();
    alertDiv.appendChild(closeBtn);
    
    alertsContainer.appendChild(alertDiv);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

function clearAlerts() {
    const alertsContainer = document.getElementById('alerts');
    alertsContainer.innerHTML = '';
}