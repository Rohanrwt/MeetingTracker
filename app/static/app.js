// State
let currentFilter = 'all';
let allTasks = [];

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadTasks();
    loadTranscriptHistory();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Transcript form submission
    document.getElementById('transcriptForm').addEventListener('submit', handleTranscriptSubmit);

    // Filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            currentFilter = e.target.dataset.filter;
            
            // Update active state
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            
            // Render tasks with filter
            renderTasks();
        });
    });
}

// Handle transcript submission
async function handleTranscriptSubmit(e) {
    e.preventDefault();
    
    const textarea = document.getElementById('transcriptText');
    const text = textarea.value.trim();
    const resultDiv = document.getElementById('processingResult');
    const btn = document.getElementById('processBtn');
    const btnText = btn.querySelector('.btn-text');
    const btnLoader = btn.querySelector('.btn-loader');

    if (!text) {
        showResult('Please enter a transcript', 'error');
        return;
    }

    // Show loading state
    btn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline';
    resultDiv.style.display = 'none';

    try {
        const response = await fetch('/api/transcripts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to process transcript');
        }

        const data = await response.json();
        
        // Clear form
        textarea.value = '';
        
        // Show success message
        showResult(`Successfully extracted ${data.tasks.length} action item(s)`, 'success');
        
        // Reload tasks and history
        await loadTasks();
        await loadTranscriptHistory();

    } catch (error) {
        showResult(`Error: ${error.message}`, 'error');
    } finally {
        // Reset button state
        btn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

// Show result message
function showResult(message, type) {
    const resultDiv = document.getElementById('processingResult');
    resultDiv.textContent = message;
    resultDiv.className = `result-message ${type}`;
    resultDiv.style.display = 'block';
    
    // Auto-hide success messages after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            resultDiv.style.display = 'none';
        }, 5000);
    }
}

// Load tasks from API
async function loadTasks() {
    try {
        const response = await fetch('/api/tasks');
        if (!response.ok) throw new Error('Failed to load tasks');
        
        allTasks = await response.json();
        renderTasks();
    } catch (error) {
        console.error('Error loading tasks:', error);
        document.getElementById('tasksList').innerHTML = 
            '<p class="empty-state">Error loading tasks. Please refresh the page.</p>';
    }
}

// Render tasks based on current filter
function renderTasks() {
    const container = document.getElementById('tasksList');
    
    // Filter tasks
    let tasks = allTasks;
    if (currentFilter !== 'all') {
        tasks = allTasks.filter(task => task.status === currentFilter);
    }

    if (tasks.length === 0) {
        const emptyMessage = currentFilter === 'all' 
            ? 'No action items yet. Process a transcript to get started.'
            : `No ${currentFilter} tasks.`;
        container.innerHTML = `<p class="empty-state">${emptyMessage}</p>`;
        return;
    }

    container.innerHTML = tasks.map(task => createTaskCard(task)).join('');
}

// Create task card HTML
function createTaskCard(task) {
    const doneClass = task.status === 'done' ? 'done' : '';
    const statusBtn = task.status === 'open' 
        ? `<button class="task-btn complete" onclick="markTaskDone(${task.id})">✓ Done</button>`
        : `<button class="task-btn" onclick="markTaskOpen(${task.id})">Reopen</button>`;

    return `
        <div class="task-card ${doneClass}" id="task-${task.id}">
            <div class="task-header">
                <div class="task-text">${escapeHtml(task.task)}</div>
                <div class="task-actions">
                    ${statusBtn}
                    <button class="task-btn" onclick="toggleEdit(${task.id})">Edit</button>
                    <button class="task-btn delete" onclick="deleteTask(${task.id})">Delete</button>
                </div>
            </div>
            <div class="task-meta">
                ${task.owner ? `<div class="task-meta-item"><strong>Owner:</strong> ${escapeHtml(task.owner)}</div>` : ''}
                ${task.due_date ? `<div class="task-meta-item"><strong>Due:</strong> ${task.due_date}</div>` : ''}
            </div>
            <div id="edit-${task.id}" class="edit-form" style="display: none;">
                <div class="form-group">
                    <label>Task Description</label>
                    <input type="text" id="edit-task-${task.id}" value="${escapeHtml(task.task)}">
                </div>
                <div class="form-group">
                    <label>Owner</label>
                    <input type="text" id="edit-owner-${task.id}" value="${escapeHtml(task.owner || '')}">
                </div>
                <div class="form-group">
                    <label>Due Date</label>
                    <input type="date" id="edit-date-${task.id}" value="${task.due_date || ''}">
                </div>
                <div class="edit-actions">
                    <button onclick="saveEdit(${task.id})">Save</button>
                    <button onclick="toggleEdit(${task.id})" style="background: var(--gray-300); color: var(--gray-700);">Cancel</button>
                </div>
            </div>
        </div>
    `;
}

// Toggle edit form
function toggleEdit(taskId) {
    const editForm = document.getElementById(`edit-${taskId}`);
    editForm.style.display = editForm.style.display === 'none' ? 'block' : 'none';
}

// Save task edit
async function saveEdit(taskId) {
    const task = document.getElementById(`edit-task-${taskId}`).value.trim();
    const owner = document.getElementById(`edit-owner-${taskId}`).value.trim() || null;
    const dueDate = document.getElementById(`edit-date-${taskId}`).value || null;

    if (!task) {
        alert('Task description cannot be empty');
        return;
    }

    try {
        const response = await fetch(`/api/tasks/${taskId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ task, owner, due_date: dueDate })
        });

        if (!response.ok) throw new Error('Failed to update task');

        await loadTasks();
        toggleEdit(taskId);
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

// Mark task as done
async function markTaskDone(taskId) {
    await updateTaskStatus(taskId, 'done');
}

// Mark task as open
async function markTaskOpen(taskId) {
    await updateTaskStatus(taskId, 'open');
}

// Update task status
async function updateTaskStatus(taskId, status) {
    try {
        const response = await fetch(`/api/tasks/${taskId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ status })
        });

        if (!response.ok) throw new Error('Failed to update task');

        await loadTasks();
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

// Delete task
async function deleteTask(taskId) {
    if (!confirm('Are you sure you want to delete this task?')) {
        return;
    }

    try {
        const response = await fetch(`/api/tasks/${taskId}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to delete task');

        await loadTasks();
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

// Load transcript history
async function loadTranscriptHistory() {
    try {
        const response = await fetch('/api/transcripts?limit=5');
        if (!response.ok) throw new Error('Failed to load transcripts');
        
        const transcripts = await response.json();
        renderTranscriptHistory(transcripts);
    } catch (error) {
        console.error('Error loading transcript history:', error);
        document.getElementById('transcriptHistory').innerHTML = 
            '<p class="empty-state">Error loading history.</p>';
    }
}

// Render transcript history
function renderTranscriptHistory(transcripts) {
    const container = document.getElementById('transcriptHistory');

    if (transcripts.length === 0) {
        container.innerHTML = '<p class="empty-state">No transcripts processed yet.</p>';
        return;
    }

    container.innerHTML = transcripts.map(transcript => `
        <div class="history-item">
            <div class="history-meta">
                <span>${formatDate(transcript.created_at)}</span>
                <span class="task-count">${transcript.tasks.length} task(s)</span>
            </div>
            <div class="history-text">${escapeHtml(transcript.text)}</div>
        </div>
    `).join('');
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 60) return `${minutes} minute(s) ago`;
    if (hours < 24) return `${hours} hour(s) ago`;
    if (days < 7) return `${days} day(s) ago`;
    
    return date.toLocaleDateString();
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
