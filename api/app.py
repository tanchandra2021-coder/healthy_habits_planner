from flask import Flask, render_template_string, request, jsonify, session
from datetime import datetime, timedelta
import json
import os
from collections import defaultdict

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# In-memory storage (replace with database in production)
users_data = {}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Planner App</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8f9fa;
            color: #2c3e50;
            min-height: 100vh;
        }
        
        .app-bar {
            background: #ffffff;
            padding: 16px 32px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .app-bar h1 {
            font-size: 22px;
            font-weight: 600;
            color: #2c3e50;
            letter-spacing: -0.5px;
        }
        
        .app-bar-actions {
            display: flex;
            gap: 12px;
            align-items: center;
        }
        
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            font-family: 'Inter', sans-serif;
        }
        
        .btn-primary {
            background: #714B67;
            color: white;
        }
        
        .btn-primary:hover {
            background: #5d3e56;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(113, 75, 103, 0.3);
        }
        
        .btn-secondary {
            background: #f0f0f0;
            color: #2c3e50;
        }
        
        .btn-secondary:hover {
            background: #e0e0e0;
        }
        
        .btn-icon {
            background: transparent;
            padding: 8px;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            min-width: 36px;
            height: 36px;
        }
        
        .btn-icon:hover {
            background: #f0f0f0;
        }
        
        .btn-icon.active {
            background: #714B67;
            color: white;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 32px;
        }
        
        .view-tabs {
            display: flex;
            gap: 8px;
            margin-bottom: 24px;
            border-bottom: 2px solid #e9ecef;
            padding-bottom: 0;
        }
        
        .view-tab {
            padding: 12px 24px;
            background: transparent;
            border: none;
            font-size: 15px;
            font-weight: 500;
            color: #6c757d;
            cursor: pointer;
            border-bottom: 3px solid transparent;
            transition: all 0.2s;
            font-family: 'Inter', sans-serif;
            margin-bottom: -2px;
        }
        
        .view-tab:hover {
            color: #714B67;
        }
        
        .view-tab.active {
            color: #714B67;
            border-bottom-color: #714B67;
        }
        
        .calendar-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            padding: 16px 24px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        }
        
        .calendar-nav {
            display: flex;
            gap: 16px;
            align-items: center;
        }
        
        .calendar-nav h2 {
            font-size: 20px;
            font-weight: 600;
            color: #2c3e50;
            min-width: 200px;
            text-align: center;
        }
        
        .weekly-view {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 16px;
        }
        
        .day-column {
            background: white;
            border-radius: 8px;
            padding: 16px;
            min-height: 500px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        }
        
        .day-column.today {
            box-shadow: 0 0 0 2px #714B67;
        }
        
        .day-header {
            text-align: center;
            padding-bottom: 12px;
            border-bottom: 2px solid #f0f0f0;
            margin-bottom: 16px;
        }
        
        .day-label {
            font-size: 13px;
            font-weight: 600;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .day-number {
            font-size: 24px;
            font-weight: 600;
            color: #2c3e50;
            margin-top: 4px;
        }
        
        .day-column.today .day-number {
            color: #714B67;
        }
        
        .event-card {
            background: #714B67;
            border-radius: 6px;
            padding: 12px;
            margin-bottom: 8px;
            cursor: pointer;
            transition: all 0.2s;
            border-left: 4px solid rgba(255,255,255,0.3);
        }
        
        .event-card:hover {
            transform: translateX(4px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .event-title {
            font-size: 14px;
            font-weight: 600;
            color: white;
            margin-bottom: 6px;
        }
        
        .event-time {
            font-size: 12px;
            color: rgba(255,255,255,0.85);
            margin-bottom: 4px;
        }
        
        .event-duration {
            font-size: 11px;
            color: rgba(255,255,255,0.7);
        }
        
        .event-class {
            font-size: 11px;
            color: rgba(255,255,255,0.9);
            margin-top: 4px;
            font-weight: 500;
        }
        
        .event-card.break {
            background: #28a745;
        }
        
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }
        
        .modal.active {
            display: flex;
        }
        
        .modal-content {
            background: white;
            border-radius: 12px;
            padding: 32px;
            max-width: 600px;
            width: 90%;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
        }
        
        .modal-header h2 {
            font-size: 24px;
            font-weight: 600;
            color: #2c3e50;
        }
        
        .close-btn {
            background: transparent;
            border: none;
            font-size: 28px;
            color: #6c757d;
            cursor: pointer;
            padding: 0;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 4px;
        }
        
        .close-btn:hover {
            background: #f0f0f0;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-size: 14px;
            font-weight: 500;
            color: #2c3e50;
        }
        
        .form-group input,
        .form-group select,
        .form-group textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e9ecef;
            border-radius: 6px;
            font-size: 14px;
            font-family: 'Inter', sans-serif;
            transition: border-color 0.2s;
        }
        
        .form-group input:focus,
        .form-group select:focus,
        .form-group textarea:focus {
            outline: none;
            border-color: #714B67;
        }
        
        .form-actions {
            display: flex;
            gap: 12px;
            justify-content: flex-end;
            margin-top: 24px;
        }
        
        .drawer {
            position: fixed;
            left: -300px;
            top: 0;
            width: 300px;
            height: 100%;
            background: white;
            box-shadow: 2px 0 8px rgba(0,0,0,0.1);
            transition: left 0.3s;
            z-index: 999;
            overflow-y: auto;
        }
        
        .drawer.open {
            left: 0;
        }
        
        .drawer-header {
            background: #714B67;
            color: white;
            padding: 24px;
            font-size: 20px;
            font-weight: 600;
        }
        
        .drawer-content {
            padding: 16px;
        }
        
        .class-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 8px;
        }
        
        .class-item:hover {
            background: #f8f9fa;
        }
        
        .class-color {
            width: 24px;
            height: 24px;
            border-radius: 50%;
        }
        
        .monthly-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 8px;
            background: white;
            padding: 24px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        }
        
        .weekday-header {
            text-align: center;
            font-size: 13px;
            font-weight: 600;
            color: #6c757d;
            padding: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .month-day {
            min-height: 120px;
            padding: 8px;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .month-day:hover {
            border-color: #714B67;
            box-shadow: 0 2px 8px rgba(113, 75, 103, 0.15);
        }
        
        .month-day.today {
            border-color: #714B67;
            background: #f8f5f7;
        }
        
        .month-day-number {
            font-size: 16px;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 8px;
        }
        
        .month-day.today .month-day-number {
            color: #714B67;
        }
        
        .month-event {
            font-size: 11px;
            padding: 4px 6px;
            border-radius: 3px;
            margin-bottom: 4px;
            color: white;
            font-weight: 500;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        
        .fab {
            position: fixed;
            bottom: 32px;
            right: 32px;
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: #714B67;
            color: white;
            border: none;
            font-size: 24px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(113, 75, 103, 0.4);
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .fab:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 20px rgba(113, 75, 103, 0.5);
        }
        
        .daily-view {
            background: white;
            border-radius: 8px;
            padding: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        }
        
        .no-events {
            text-align: center;
            padding: 48px;
            color: #6c757d;
            font-size: 15px;
        }
        
        .menu-btn {
            background: transparent;
            border: none;
            font-size: 24px;
            cursor: pointer;
            padding: 8px;
            color: #2c3e50;
        }
        
        @media (max-width: 1200px) {
            .weekly-view {
                grid-template-columns: repeat(3, 1fr);
            }
        }
        
        @media (max-width: 768px) {
            .weekly-view {
                grid-template-columns: 1fr;
            }
            
            .container {
                padding: 16px;
            }
            
            .modal-content {
                padding: 24px;
            }
        }
    </style>
</head>
<body>
    <div class="app-bar">
        <div style="display: flex; align-items: center; gap: 16px;">
            <button class="menu-btn" onclick="toggleDrawer()">☰</button>
            <h1><span id="userName">My</span>'s Planner</h1>
        </div>
        <div class="app-bar-actions">
            <button class="btn-icon" onclick="changeView('weekly')" id="weeklyBtn">📅</button>
            <button class="btn-icon" onclick="changeView('daily')" id="dailyBtn">📆</button>
            <button class="btn-icon" onclick="changeView('monthly')" id="monthlyBtn">🗓️</button>
            <button class="btn-secondary btn" onclick="openSettings()">⚙️ Settings</button>
        </div>
    </div>
    
    <div class="drawer" id="drawer">
        <div class="drawer-header">Classes & Commitments</div>
        <div class="drawer-content">
            <button class="btn btn-primary" style="width: 100%; margin-bottom: 16px;" onclick="openAddClassModal()">+ Add New Class</button>
            <div id="classList"></div>
        </div>
    </div>
    
    <div class="container">
        <div class="calendar-header">
            <div class="calendar-nav">
                <button class="btn-icon" onclick="navigateDate(-1)">◀</button>
                <h2 id="currentDateLabel"></h2>
                <button class="btn-icon" onclick="navigateDate(1)">▶</button>
            </div>
        </div>
        
        <div id="calendarView"></div>
    </div>
    
    <button class="fab" onclick="openAddEventModal()">+</button>
    
    <!-- Add Event Modal -->
    <div class="modal" id="addEventModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Add Event</h2>
                <button class="close-btn" onclick="closeModal('addEventModal')">&times;</button>
            </div>
            <form id="addEventForm">
                <div class="form-group">
                    <label>Title</label>
                    <input type="text" id="eventTitle" required>
                </div>
                <div class="form-group">
                    <label>Event Type</label>
                    <select id="eventType" onchange="toggleFixedFields()">
                        <option value="flexible">Flexible</option>
                        <option value="fixed">Fixed</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Duration (minutes)</label>
                    <input type="number" id="eventDuration" value="30" min="1">
                </div>
                <div class="form-group">
                    <label>Priority (1=highest, 5=lowest)</label>
                    <select id="eventPriority">
                        <option value="1">1 - Highest</option>
                        <option value="2">2</option>
                        <option value="3" selected>3 - Medium</option>
                        <option value="4">4</option>
                        <option value="5">5 - Lowest</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Recurrence</label>
                    <select id="eventRecurrence">
                        <option value="none">None</option>
                        <option value="daily">Daily</option>
                        <option value="weekly">Weekly</option>
                        <option value="monthly">Monthly</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Class / Commitment (optional)</label>
                    <select id="eventClass">
                        <option value="">None</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Event Date</label>
                    <input type="date" id="eventDate" required>
                </div>
                <div class="form-group" id="fixedTimeGroup" style="display: none;">
                    <label>Start Time (for fixed events)</label>
                    <input type="time" id="eventStartTime">
                </div>
                <div class="form-actions">
                    <button type="button" class="btn btn-secondary" onclick="closeModal('addEventModal')">Cancel</button>
                    <button type="submit" class="btn btn-primary">Add Event</button>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Edit Event Modal -->
    <div class="modal" id="editEventModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Edit Event</h2>
                <button class="close-btn" onclick="closeModal('editEventModal')">&times;</button>
            </div>
            <form id="editEventForm">
                <input type="hidden" id="editEventId">
                <div class="form-group">
                    <label>Title</label>
                    <input type="text" id="editEventTitle" required>
                </div>
                <div class="form-group">
                    <label>Event Type</label>
                    <select id="editEventType" onchange="toggleEditFixedFields()">
                        <option value="flexible">Flexible</option>
                        <option value="fixed">Fixed</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Duration (minutes)</label>
                    <input type="number" id="editEventDuration" value="30" min="1">
                </div>
                <div class="form-group">
                    <label>Priority (1=highest, 5=lowest)</label>
                    <select id="editEventPriority">
                        <option value="1">1 - Highest</option>
                        <option value="2">2</option>
                        <option value="3">3 - Medium</option>
                        <option value="4">4</option>
                        <option value="5">5 - Lowest</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Recurrence</label>
                    <select id="editEventRecurrence">
                        <option value="none">None</option>
                        <option value="daily">Daily</option>
                        <option value="weekly">Weekly</option>
                        <option value="monthly">Monthly</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Class / Commitment (optional)</label>
                    <select id="editEventClass">
                        <option value="">None</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Event Date</label>
                    <input type="date" id="editEventDate" required>
                </div>
                <div class="form-group" id="editFixedTimeGroup" style="display: none;">
                    <label>Start Time (for fixed events)</label>
                    <input type="time" id="editEventStartTime">
                </div>
                <div class="form-actions">
                    <button type="button" class="btn btn-secondary" onclick="deleteEvent()">Delete</button>
                    <button type="button" class="btn btn-secondary" onclick="closeModal('editEventModal')">Cancel</button>
                    <button type="submit" class="btn btn-primary">Save Changes</button>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Settings Modal -->
    <div class="modal" id="settingsModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Settings</h2>
                <button class="close-btn" onclick="closeModal('settingsModal')">&times;</button>
            </div>
            <form id="settingsForm">
                <div class="form-group">
                    <label>Break Length (minutes)</label>
                    <input type="number" id="settingsBreakLength" value="10" min="1">
                </div>
                <div class="form-group">
                    <label>Shower Length (minutes)</label>
                    <input type="number" id="settingsShowerLength" value="15" min="1">
                </div>
                <div class="form-group">
                    <label>Meal Length (minutes)</label>
                    <input type="number" id="settingsMealLength" value="30" min="1">
                </div>
                <div class="form-group">
                    <label>Buffer Between Events (minutes)</label>
                    <input type="number" id="settingsBuffer" value="5" min="0">
                </div>
                <div class="form-group">
                    <label>Work Chunk Length (minutes)</label>
                    <input type="number" id="settingsWorkChunk" value="50" min="1">
                </div>
                <div class="form-group">
                    <label>Work Start Time</label>
                    <input type="time" id="settingsWorkStart" value="16:00">
                </div>
                <div class="form-group">
                    <label>Work End Time</label>
                    <input type="time" id="settingsWorkEnd" value="22:00">
                </div>
                <div class="form-actions">
                    <button type="button" class="btn btn-secondary" onclick="closeModal('settingsModal')">Cancel</button>
                    <button type="submit" class="btn btn-primary">Save Settings</button>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Add Class Modal -->
    <div class="modal" id="addClassModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Add Class / Commitment</h2>
                <button class="close-btn" onclick="closeModal('addClassModal')">&times;</button>
            </div>
            <form id="addClassForm">
                <div class="form-group">
                    <label>Name</label>
                    <input type="text" id="className" required>
                </div>
                <div class="form-group">
                    <label>Color (hex code)</label>
                    <input type="text" id="classColor" value="#714B67" placeholder="#714B67">
                </div>
                <div class="form-actions">
                    <button type="button" class="btn btn-secondary" onclick="closeModal('addClassModal')">Cancel</button>
                    <button type="submit" class="btn btn-primary">Add Class</button>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Name Prompt Modal -->
    <div class="modal active" id="nameModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Welcome!</h2>
            </div>
            <form id="nameForm">
                <div class="form-group">
                    <label>What's your name?</label>
                    <input type="text" id="userNameInput" required>
                </div>
                <div class="form-actions">
                    <button type="submit" class="btn btn-primary">Get Started</button>
                </div>
            </form>
        </div>
    </div>

    <script>
        // State management
        let currentView = 'weekly';
        let selectedDate = new Date();
        let events = [];
        let classes = [];
        let settings = {
            breakLength: 10,
            showerLength: 15,
            mealLength: 30,
            bufferBetweenEvents: 5,
            workChunkLength: 50,
            workStart: '16:00',
            workEnd: '22:00'
        };
        let durationHistory = {};
        let userName = '';
        let currentEditingEventId = null;
        
        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            loadData();
            if (userName) {
                document.getElementById('nameModal').classList.remove('active');
            }
            setTodayDate();
            updateView();
            updateClassDropdowns();
        });
        
        // Name form
        document.getElementById('nameForm').addEventListener('submit', (e) => {
            e.preventDefault();
            userName = document.getElementById('userNameInput').value.trim() || 'My';
            document.getElementById('userName').textContent = userName;
            closeModal('nameModal');
            saveData();
        });
        
        // Add Event form
        document.getElementById('addEventForm').addEventListener('submit', (e) => {
            e.preventDefault();
            const event = {
                id: Date.now(),
                title: document.getElementById('eventTitle').value,
                eventType: document.getElementById('eventType').value,
                duration: parseInt(document.getElementById('eventDuration').value),
                priority: parseInt(document.getElementById('eventPriority').value),
                recurrence: document.getElementById('eventRecurrence').value,
                classTag: document.getElementById('eventClass').value || null,
                eventDate: document.getElementById('eventDate').value,
                startTime: document.getElementById('eventType').value === 'fixed' ? document.getElementById('eventStartTime').value : null,
                color: getEventColor(document.getElementById('eventClass').value, parseInt(document.getElementById('eventPriority').value))
            };
            events.push(event);
            saveData();
            closeModal('addEventModal');
            updateView();
            document.getElementById('addEventForm').reset();
        });
        
        // Edit Event form
        document.getElementById('editEventForm').addEventListener('submit', (e) => {
            e.preventDefault();
            const eventId = parseInt(document.getElementById('editEventId').value);
            const eventIndex = events.findIndex(e => e.id === eventId);
            if (eventIndex !== -1) {
                events[eventIndex] = {
                    ...events[eventIndex],
                    title: document.getElementById('editEventTitle').value,
                    eventType: document.getElementById('editEventType').value,
                    duration: parseInt(document.getElementById('editEventDuration').value),
                    priority: parseInt(document.getElementById('editEventPriority').value),
                    recurrence: document.getElementById('editEventRecurrence').value,
                    classTag: document.getElementById('editEventClass').value || null,
                    eventDate: document.getElementById('editEventDate').value,
                    startTime: document.getElementById('editEventType').value === 'fixed' ? document.getElementById('editEventStartTime').value : null,
                    color: getEventColor(document.getElementById('editEventClass').value, parseInt(document.getElementById('editEventPriority').value))
                };
                saveData();
                closeModal('editEventModal');
                updateView();
            }
        });
        
        // Settings form
        document.getElementById('settingsForm').addEventListener('submit', (e) => {
            e.preventDefault();
            settings = {
                breakLength: parseInt(document.getElementById('settingsBreakLength').value),
                showerLength: parseInt(document.getElementById('settingsShowerLength').value),
                mealLength: parseInt(document.getElementById('settingsMealLength').value),
                bufferBetweenEvents: parseInt(document.getElementById('settingsBuffer').value),
                workChunkLength: parseInt(document.getElementById('settingsWorkChunk').value),
                workStart: document.getElementById('settingsWorkStart').value,
                workEnd: document.getElementById('settingsWorkEnd').value
            };
            saveData();
            closeModal('settingsModal');
            updateView();
        });
        
        // Add Class form
        document.getElementById('addClassForm').addEventListener('submit', (e) => {
            e.preventDefault();
            const newClass = {
                id: Date.now(),
                name: document.getElementById('className').value,
                color: document.getElementById('classColor').value || '#714B67'
            };
            classes.push(newClass);
            saveData();
            closeModal('addClassModal');
            updateClassList();
            updateClassDropdowns();
            document.getElementById('addClassForm').reset();
        });
        
        // Helper functions
        function toggleDrawer() {
            document.getElementById('drawer').classList.toggle('open');
        }
        
        function closeModal(modalId) {
            document.getElementById(modalId).classList.remove('active');
        }
        
        function openAddEventModal() {
            setTodayDate();
            closeModal('editEventModal');
            document.getElementById('addEventModal').classList.add('active');
        }
        
        function openAddClassModal() {
            document.getElementById('addClassModal').classList.add('active');
        }
        
        function openSettings() {
            document.getElementById('settingsBreakLength').value = settings.breakLength;
            document.getElementById('settingsShowerLength').value = settings.showerLength;
            document.getElementById('settingsMealLength').value = settings.mealLength;
            document.getElementById('settingsBuffer').value = settings.bufferBetweenEvents;
            document.getElementById('settingsWorkChunk').value = settings.workChunkLength;
            document.getElementById('settingsWorkStart').value = settings.workStart;
            document.getElementById('settingsWorkEnd').value = settings.workEnd;
            document.getElementById('settingsModal').classList.add('active');
        }
        
        function toggleFixedFields() {
            const eventType = document.getElementById('eventType').value;
            document.getElementById('fixedTimeGroup').style.display = eventType === 'fixed' ? 'block' : 'none';
        }
        
        function toggleEditFixedFields() {
            const eventType = document.getElementById('editEventType').value;
            document.getElementById('editFixedTimeGroup').style.display = eventType === 'fixed' ? 'block' : 'none';
        }
        
        function setTodayDate() {
            const today = new Date().toISOString().split('T')[0];
            if (document.getElementById('eventDate')) {
                document.getElementById('eventDate').value = today;
            }
        }
        
        function changeView(view) {
            currentView = view;
            document.querySelectorAll('.btn-icon').forEach(btn => btn.classList.remove('active'));
            document.getElementById(view + 'Btn').classList.add('active');
            updateView();
        }
        
        function navigateDate(direction) {
            if (currentView === 'weekly') {
                selectedDate.setDate(selectedDate.getDate() + (direction * 7));
            } else if (currentView === 'daily') {
                selectedDate.setDate(selectedDate.getDate() + direction);
            } else if (currentView === 'monthly') {
                selectedDate.setMonth(selectedDate.getMonth() + direction);
            }
            updateView();
        }
        
        function updateView() {
            updateDateLabel();
            if (currentView === 'weekly') {
                renderWeeklyView();
            } else if (currentView === 'daily') {
                renderDailyView();
            } else if (currentView === 'monthly') {
                renderMonthlyView();
            }
        }
        
        function updateDateLabel() {
            const label = document.getElementById('currentDateLabel');
            if (currentView === 'weekly') {
                const startOfWeek = getStartOfWeek(selectedDate);
                label.textContent = `Week of ${formatDate(startOfWeek)}`;
            } else if (currentView === 'daily') {
                label.textContent = formatDate(selectedDate);
            } else if (currentView === 'monthly') {
                label.textContent = `${getMonthName(selectedDate.getMonth())} ${selectedDate.getFullYear()}`;
            }
        }
        
        function getStartOfWeek(date) {
            const d = new Date(date);
            const day = d.getDay();
            const diff = d.getDate() - day + (day === 0 ? -6 : 1);
            return new Date(d.setDate(diff));
        }
        
        function formatDate(date) {
            return date.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' });
        }
        
        function getMonthName(month) {
            const names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
            return names[month];
        }
        
        function getDayLabel(weekday) {
            const labels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
            return labels[weekday];
        }
        
        function isSameDay(d1, d2) {
            return d1.getFullYear() === d2.getFullYear() &&
                   d1.getMonth() === d2.getMonth() &&
                   d1.getDate() === d2.getDate();
        }
        
        function getEventColor(classTag, priority) {
            if (classTag) {
                const cls = classes.find(c => c.name === classTag);
                if (cls) return cls.color;
            }
            const colors = ['#1e3a8a', '#1e40af', '#3b82f6', '#60a5fa', '#93c5fd'];
            return colors[priority - 1] || '#714B67';
        }
        
        function updateClassList() {
            const list = document.getElementById('classList');
            list.innerHTML = classes.map(c => `
                <div class="class-item">
                    <div class="class-color" style="background: ${c.color};"></div>
                    <span>${c.name}</span>
                </div>
            `).join('');
        }
        
        function updateClassDropdowns() {
            const options = classes.map(c => `<option value="${c.name}">${c.name}</option>`).join('');
            document.getElementById('eventClass').innerHTML = '<option value="">None</option>' + options;
            document.getElementById('editEventClass').innerHTML = '<option value="">None</option>' + options;
        }
        
        function openEditEventModal(eventId) {
            const event = events.find(e => e.id === eventId);
            if (!event) return;
            
            currentEditingEventId = eventId;
            document.getElementById('editEventId').value = event.id;
            document.getElementById('editEventTitle').value = event.title;
            document.getElementById('editEventType').value = event.eventType;
            document.getElementById('editEventDuration').value = event.duration;
            document.getElementById('editEventPriority').value = event.priority;
            document.getElementById('editEventRecurrence').value = event.recurrence;
            document.getElementById('editEventClass').value = event.classTag || '';
            document.getElementById('editEventDate').value = event.eventDate;
            document.getElementById('editEventStartTime').value = event.startTime || '';
            toggleEditFixedFields();
            document.getElementById('editEventModal').classList.add('active');
        }
        
        function deleteEvent() {
            if (confirm('Are you sure you want to delete this event?')) {
                events = events.filter(e => e.id !== currentEditingEventId);
                saveData();
                closeModal('editEventModal');
                updateView();
            }
        }
        
        function occursOnDay(event, day) {
            const eventDate = new Date(event.eventDate);
            
            if (event.eventType === 'fixed' && event.startTime) {
                const fixedDate = new Date(event.eventDate + 'T' + event.startTime);
                return isSameDay(fixedDate, day);
            }
            
            if (isSameDay(eventDate, day)) return true;
            
            if (event.recurrence === 'none') return false;
            if (day < eventDate) return false;
            
            if (event.recurrence === 'daily') return true;
            if (event.recurrence === 'weekly') return day.getDay() === eventDate.getDay();
            if (event.recurrence === 'monthly') return day.getDate() === eventDate.getDate();
            
            return false;
        }
        
        function generateScheduleForDay(day) {
            const schedule = [];
            
            // Get fixed events
            const fixedEvents = events.filter(e => e.eventType === 'fixed' && occursOnDay(e, day));
            fixedEvents.forEach(e => {
                const startTime = new Date(e.eventDate + 'T' + e.startTime);
                const endTime = new Date(startTime.getTime() + e.duration * 60000);
                schedule.push({
                    ...e,
                    startTime: startTime,
                    endTime: endTime,
                    scheduled: true
                });
            });
            
            // Get flexible events
            const flexibleEvents = events.filter(e => e.eventType === 'flexible' && occursOnDay(e, day));
            
            if (flexibleEvents.length === 0) {
                schedule.sort((a, b) => a.startTime - b.startTime);
                return schedule;
            }
            
            // Auto-prioritize
            flexibleEvents.forEach(e => {
                if (e.deadline) {
                    const deadline = new Date(e.deadline);
                    const minutesLeft = (deadline - day) / 60000;
                    if (minutesLeft <= 0) e.priority = Math.max(1, e.priority - 2);
                    else if (minutesLeft <= 1440) e.priority = Math.max(1, e.priority - 1);
                }
            });
            
            // Calculate available time
            const [startHour, startMin] = settings.workStart.split(':').map(Number);
            const [endHour, endMin] = settings.workEnd.split(':').map(Number);
            let cursor = new Date(day);
            cursor.setHours(startHour, startMin, 0, 0);
            const cutoff = new Date(day);
            cutoff.setHours(endHour, endMin, 0, 0);
            
            let totalAvailable = (cutoff - cursor) / 60000;
            
            // Subtract fixed event time
            fixedEvents.forEach(fe => {
                totalAvailable -= fe.duration + settings.bufferBetweenEvents;
            });
            
            let totalTaskTime = flexibleEvents.reduce((sum, e) => sum + e.duration, 0);
            
            // Reduction algorithm (same as Flutter version)
            if (totalTaskTime > totalAvailable) {
                const mutable = flexibleEvents.map(e => ({ event: e, remaining: e.duration, removed: false }));
                
                // Step 1: Halve priority 5
                mutable.forEach(m => {
                    if (!m.removed && m.event.priority === 5) {
                        const old = m.remaining;
                        m.remaining = Math.ceil(m.remaining / 2);
                        totalTaskTime -= (old - m.remaining);
                    }
                });
                
                if (totalTaskTime > totalAvailable) {
                    // Step 2: Halve priority 4
                    mutable.forEach(m => {
                        if (!m.removed && m.event.priority === 4) {
                            const old = m.remaining;
                            m.remaining = Math.ceil(m.remaining / 2);
                            totalTaskTime -= (old - m.remaining);
                        }
                    });
                }
                
                if (totalTaskTime > totalAvailable) {
                    // Step 3: Remove priority 5
                    mutable.forEach(m => {
                        if (!m.removed && m.event.priority === 5) {
                            m.removed = true;
                            totalTaskTime -= m.remaining;
                        }
                    });
                }
                
                if (totalTaskTime > totalAvailable) {
                    // Step 4: Remove priority 4
                    mutable.forEach(m => {
                        if (!m.removed && m.event.priority === 4) {
                            m.removed = true;
                            totalTaskTime -= m.remaining;
                        }
                    });
                }
                
                if (totalTaskTime > totalAvailable) {
                    // Step 6: Halve priority 3
                    mutable.forEach(m => {
                        if (!m.removed && m.event.priority === 3) {
                            const old = m.remaining;
                            m.remaining = Math.ceil(m.remaining / 2);
                            totalTaskTime -= (old - m.remaining);
                        }
                    });
                }
                
                if (totalTaskTime > totalAvailable) {
                    // Step 7: Remove priority 3
                    mutable.forEach(m => {
                        if (!m.removed && m.event.priority === 3) {
                            m.removed = true;
                            totalTaskTime -= m.remaining;
                        }
                    });
                }
                
                if (totalTaskTime > totalAvailable) {
                    // Step 8: Halve priority 2
                    mutable.forEach(m => {
                        if (!m.removed && m.event.priority === 2) {
                            const old = m.remaining;
                            m.remaining = Math.ceil(m.remaining / 2);
                            totalTaskTime -= (old - m.remaining);
                        }
                    });
                }
                
                if (totalTaskTime > totalAvailable) {
                    // Step 9: Remove priority 2
                    mutable.forEach(m => {
                        if (!m.removed && m.event.priority === 2) {
                            m.removed = true;
                            totalTaskTime -= m.remaining;
                        }
                    });
                }
                
                if (totalTaskTime > totalAvailable) {
                    // Step 10: Halve priority 1
                    mutable.forEach(m => {
                        if (!m.removed && m.event.priority === 1) {
                            const old = m.remaining;
                            m.remaining = Math.ceil(m.remaining / 2);
                            totalTaskTime -= (old - m.remaining);
                        }
                    });
                }
                
                // Allocate remaining tasks
                const remainingTasks = mutable.filter(m => !m.removed && m.remaining > 0);
                remainingTasks.sort((a, b) => a.event.priority - b.event.priority);
                
                const sortedFixed = [...fixedEvents].sort((a, b) => a.startTime - b.startTime);
                let fixedIdx = 0;
                let continuousWork = 0;
                
                remainingTasks.forEach(task => {
                    let remaining = task.remaining;
                    
                    while (remaining > 0 && cursor < cutoff) {
                        // Skip over fixed events
                        while (fixedIdx < sortedFixed.length && cursor >= sortedFixed[fixedIdx].startTime) {
                            if (cursor < sortedFixed[fixedIdx].endTime) {
                                cursor = new Date(sortedFixed[fixedIdx].endTime.getTime() + settings.bufferBetweenEvents * 60000);
                                continuousWork = 0;
                            }
                            fixedIdx++;
                        }
                        
                        const nextFixed = fixedIdx < sortedFixed.length ? sortedFixed[fixedIdx].startTime : cutoff;
                        const freeMinutes = (nextFixed - cursor) / 60000;
                        
                        if (freeMinutes <= 0) break;
                        
                        const chunk = Math.min(remaining, settings.workChunkLength, freeMinutes);
                        const end = new Date(cursor.getTime() + chunk * 60000);
                        
                        schedule.push({
                            ...task.event,
                            duration: chunk,
                            startTime: new Date(cursor),
                            endTime: end,
                            scheduled: true,
                            title: remaining === task.remaining ? task.event.title : task.event.title + ' (cont)'
                        });
                        
                        cursor = end;
                        remaining -= chunk;
                        continuousWork += chunk;
                        
                        // Adaptive breaks
                        let breakDuration = settings.breakLength;
                        if (continuousWork >= 120) breakDuration = Math.ceil(settings.breakLength * 1.5);
                        else if (continuousWork >= 60) breakDuration = Math.ceil(settings.breakLength * 1.25);
                        
                        const breakEnd = new Date(cursor.getTime() + breakDuration * 60000);
                        if (breakEnd < nextFixed && breakEnd < cutoff) {
                            schedule.push({
                                id: Date.now() + Math.random(),
                                title: 'Break',
                                eventType: 'break',
                                duration: breakDuration,
                                startTime: new Date(cursor),
                                endTime: breakEnd,
                                color: '#28a745',
                                scheduled: true
                            });
                            cursor = breakEnd;
                            continuousWork = Math.max(0, continuousWork - breakDuration);
                        }
                    }
                    
                    if (remaining > 0) {
                        schedule.push({
                            ...task.event,
                            duration: remaining,
                            startTime: null,
                            endTime: null,
                            scheduled: false,
                            title: task.event.title + ' (pushed)'
                        });
                    }
                });
            } else {
                // All tasks fit - simple allocation
                const sortedTasks = [...flexibleEvents].sort((a, b) => a.priority - b.priority);
                const sortedFixed = [...fixedEvents].sort((a, b) => a.startTime - b.startTime);
                let fixedIdx = 0;
                let continuousWork = 0;
                
                sortedTasks.forEach(task => {
                    let remaining = task.duration;
                    
                    while (remaining > 0 && cursor < cutoff) {
                        while (fixedIdx < sortedFixed.length && cursor >= sortedFixed[fixedIdx].startTime) {
                            if (cursor < sortedFixed[fixedIdx].endTime) {
                                cursor = new Date(sortedFixed[fixedIdx].endTime.getTime() + settings.bufferBetweenEvents * 60000);
                                continuousWork = 0;
                            }
                            fixedIdx++;
                        }
                        
                        const nextFixed = fixedIdx < sortedFixed.length ? sortedFixed[fixedIdx].startTime : cutoff;
                        const freeMinutes = (nextFixed - cursor) / 60000;
                        
                        if (freeMinutes <= 0) break;
                        
                        const chunk = Math.min(remaining, settings.workChunkLength, freeMinutes);
                        const end = new Date(cursor.getTime() + chunk * 60000);
                        
                        schedule.push({
                            ...task,
                            duration: chunk,
                            startTime: new Date(cursor),
                            endTime: end,
                            scheduled: true
                        });
                        
                        cursor = end;
                        remaining -= chunk;
                        continuousWork += chunk;
                        
                        let breakDuration = settings.breakLength;
                        if (continuousWork >= 120) breakDuration = Math.ceil(settings.breakLength * 1.5);
                        else if (continuousWork >= 60) breakDuration = Math.ceil(settings.breakLength * 1.25);
                        
                        const breakEnd = new Date(cursor.getTime() + breakDuration * 60000);
                        if (breakEnd < nextFixed && breakEnd < cutoff) {
                            schedule.push({
                                id: Date.now() + Math.random(),
                                title: 'Break',
                                eventType: 'break',
                                duration: breakDuration,
                                startTime: new Date(cursor),
                                endTime: breakEnd,
                                color: '#28a745',
                                scheduled: true
                            });
                            cursor = breakEnd;
                            continuousWork = Math.max(0, continuousWork - breakDuration);
                        }
                    }
                });
            }
            
            schedule.sort((a, b) => {
                if (!a.startTime) return 1;
                if (!b.startTime) return -1;
                return a.startTime - b.startTime;
            });
            
            return schedule;
        }
        
        function renderWeeklyView() {
            const container = document.getElementById('calendarView');
            const startOfWeek = getStartOfWeek(selectedDate);
            const today = new Date();
            
            let html = '<div class="weekly-view">';
            for (let i = 0; i < 7; i++) {
                const day = new Date(startOfWeek);
                day.setDate(startOfWeek.getDate() + i);
                const isToday = isSameDay(day, today);
                const dayEvents = generateScheduleForDay(day);
                
                html += `
                    <div class="day-column ${isToday ? 'today' : ''}">
                        <div class="day-header">
                            <div class="day-label">${getDayLabel(day.getDay())}</div>
                            <div class="day-number">${day.getDate()}</div>
                        </div>
                        ${dayEvents.length === 0 ? '<div class="no-events">No events</div>' : ''}
                        ${dayEvents.map(e => `
                            <div class="event-card ${e.eventType === 'break' ? 'break' : ''}" 
                                 style="background: ${e.color};" 
                                 onclick="openEditEventModal(${e.id})">
                                <div class="event-title">${e.title}</div>
                                ${e.startTime && e.endTime ? `
                                    <div class="event-time">${formatTime(e.startTime)} - ${formatTime(e.endTime)}</div>
                                ` : ''}
                                <div class="event-duration">${e.duration} min</div>
                                ${e.classTag ? `<div class="event-class">${e.classTag}</div>` : ''}
                            </div>
                        `).join('')}
                    </div>
                `;
            }
            html += '</div>';
            container.innerHTML = html;
        }
        
        function renderDailyView() {
            const container = document.getElementById('calendarView');
            const dayEvents = generateScheduleForDay(selectedDate);
            
            let html = '<div class="daily-view">';
            if (dayEvents.length === 0) {
                html += '<div class="no-events">No events scheduled for this day</div>';
            } else {
                dayEvents.forEach(e => {
                    html += `
                        <div class="event-card ${e.eventType === 'break' ? 'break' : ''}" 
                             style="background: ${e.color}; margin-bottom: 12px;" 
                             onclick="openEditEventModal(${e.id})">
                            <div class="event-title">${e.title}</div>
                            ${e.startTime && e.endTime ? `
                                <div class="event-time">${formatTime(e.startTime)} - ${formatTime(e.endTime)}</div>
                            ` : ''}
                            <div class="event-duration">Duration: ${e.duration} min</div>
                            ${e.classTag ? `<div class="event-class">Class: ${e.classTag}</div>` : ''}
                        </div>
                    `;
                });
            }
            html += '</div>';
            container.innerHTML = html;
        }
        
        function renderMonthlyView() {
            const container = document.getElementById('calendarView');
            const year = selectedDate.getFullYear();
            const month = selectedDate.getMonth();
            const firstDay = new Date(year, month, 1);
            const lastDay = new Date(year, month + 1, 0);
            const startWeekday = firstDay.getDay();
            const totalDays = lastDay.getDate();
            const today = new Date();
            
            let html = '<div class="monthly-grid">';
            
            // Weekday headers
            ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].forEach(day => {
                html += `<div class="weekday-header">${day}</div>`;
            });
            
            // Empty cells before first day
            for (let i = 0; i < startWeekday; i++) {
                html += '<div class="month-day"></div>';
            }
            
            // Days of month
            for (let day = 1; day <= totalDays; day++) {
                const date = new Date(year, month, day);
                const isToday = isSameDay(date, today);
                const dayEvents = generateScheduleForDay(date).slice(0, 2);
                const extraEvents = generateScheduleForDay(date).length - dayEvents.length;
                
                html += `
                    <div class="month-day ${isToday ? 'today' : ''}" onclick="selectDayAndViewDaily(${year}, ${month}, ${day})">
                        <div class="month-day-number">${day}</div>
                        ${dayEvents.map(e => `
                            <div class="month-event" style="background: ${e.color};">${e.title}</div>
                        `).join('')}
                        ${extraEvents > 0 ? `<div style="font-size: 10px; color: #6c757d;">+${extraEvents} more</div>` : ''}
                    </div>
                `;
            }
            
            html += '</div>';
            container.innerHTML = html;
        }
        
        function selectDayAndViewDaily(year, month, day) {
            selectedDate = new Date(year, month, day);
            changeView('daily');
        }
        
        function formatTime(date) {
            const hours = date.getHours().toString().padStart(2, '0');
            const minutes = date.getMinutes().toString().padStart(2, '0');
            return `${hours}:${minutes}`;
        }
        
        function saveData() {
            const data = {
                userName,
                events,
                classes,
                settings,
                durationHistory
            };
            localStorage.setItem('plannerData', JSON.stringify(data));
        }
        
        function loadData() {
            const data = localStorage.getItem('plannerData');
            if (data) {
                const parsed = JSON.parse(data);
                userName = parsed.userName || '';
                events = parsed.events || [];
                classes = parsed.classes || [];
                settings = parsed.settings || settings;
                durationHistory = parsed.durationHistory || {};
                
                if (userName) {
                    document.getElementById('userName').textContent = userName;
                }
                updateClassList();
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)


