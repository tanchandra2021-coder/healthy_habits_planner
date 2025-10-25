from flask import Flask, render_template_string
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Planner App</title>
    
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-HKCC7BLCC7"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-HKCC7BLCC7');
</script>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--gradient-bg);
            color: var(--text-color);
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
            transition: background 0.3s ease, color 0.3s ease;
        }
        
        /* White theme */
        body.gradient-1 {
            --gradient-bg: #ffffff;
            --text-color: #1f2937;
            --text-secondary: #6b7280;
            --card-bg: rgba(255, 255, 255, 0.95);
            --card-border: rgba(229, 231, 235, 0.8);
            --hover-bg: rgba(243, 244, 246, 0.95);
            --accent-color: #3b82f6;
            --accent-hover: #2563eb;
            --header-text: #1f2937;
            --btn-text: #ffffff;
        }
        
        /* Black theme */
        body.gradient-2 {
            --gradient-bg: #000000;
            --text-color: #f1f5f9;
            --text-secondary: #cbd5e1;
            --card-bg: rgba(30, 30, 30, 0.95);
            --card-border: rgba(60, 60, 60, 0.8);
            --hover-bg: rgba(40, 40, 40, 0.95);
            --accent-color: #3b82f6;
            --accent-hover: #2563eb;
            --header-text: #ffffff;
            --btn-text: #ffffff;
        }
        
        /* Grey theme */
        body.gradient-3 {
            --gradient-bg: #6b7280;
            --text-color: #f9fafb;
            --text-secondary: #e5e7eb;
            --card-bg: rgba(75, 85, 99, 0.95);
            --card-border: rgba(107, 114, 128, 0.8);
            --hover-bg: rgba(55, 65, 81, 0.95);
            --accent-color: #3b82f6;
            --accent-hover: #2563eb;
            --header-text: #ffffff;
            --btn-text: #ffffff;
        }
        
        /* Warm pastel theme */
        body.gradient-4 {
            --gradient-bg: linear-gradient(135deg, #fef3f2 0%, #fef7f6 50%, #fff7ed 100%);
            --text-color: #1f2937;
            --text-secondary: #6b7280;
            --card-bg: rgba(255, 255, 255, 0.95);
            --card-border: rgba(254, 226, 226, 0.6);
            --hover-bg: rgba(254, 243, 242, 0.95);
            --accent-color: #f97316;
            --accent-hover: #ea580c;
            --header-text: #1f2937;
            --btn-text: #ffffff;
        }
        
        /* Cool pastel theme */
        body.gradient-5 {
            --gradient-bg: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #dbeafe 100%);
            --text-color: #1f2937;
            --text-secondary: #6b7280;
            --card-bg: rgba(255, 255, 255, 0.95);
            --card-border: rgba(191, 219, 254, 0.6);
            --hover-bg: rgba(240, 249, 255, 0.95);
            --accent-color: #0284c7;
            --accent-hover: #0369a1;
            --header-text: #1f2937;
            --btn-text: #ffffff;
        }
        
        /* Green pastel theme */
        body.gradient-6 {
            --gradient-bg: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 50%, #d1fae5 100%);
            --text-color: #1f2937;
            --text-secondary: #6b7280;
            --card-bg: rgba(255, 255, 255, 0.95);
            --card-border: rgba(220, 252, 231, 0.6);
            --hover-bg: rgba(240, 253, 244, 0.95);
            --accent-color: #059669;
            --accent-hover: #047857;
            --header-text: #1f2937;
            --btn-text: #ffffff;
        }
        
        body.gradient-1::before,
        body.gradient-2::before,
        body.gradient-3::before {
            display: none;
        }
        
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 20% 50%, rgba(59, 130, 246, 0.1), transparent 50%),
                        radial-gradient(circle at 80% 80%, rgba(59, 130, 246, 0.08), transparent 50%),
                        radial-gradient(circle at 40% 20%, rgba(59, 130, 246, 0.06), transparent 50%);
            pointer-events: none;
            z-index: 0;
        }
        
        .app-bar {
            background: var(--card-bg);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            border-bottom: 1px solid var(--card-border);
            padding: 24px 48px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .app-bar h1 {
            font-size: 32px;
            font-weight: 800;
            color: var(--header-text);
            letter-spacing: -1px;
            background: linear-gradient(135deg, var(--accent-color), var(--accent-hover));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .app-bar-actions {
            display: flex;
            gap: 16px;
            align-items: center;
        }
        
        .btn {
            padding: 14px 28px;
            border: none;
            border-radius: 16px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            font-family: 'Poppins', sans-serif;
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        
        .btn::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }
        
        .btn:hover::before {
            width: 300px;
            height: 300px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, var(--accent-color), var(--accent-hover));
            color: var(--btn-text);
            transform: translateY(0);
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
        }
        
        .btn-secondary {
            background: var(--card-bg);
            color: var(--text-color);
            border: 2px solid var(--card-border);
        }
        
        .btn-secondary:hover {
            background: var(--hover-bg);
            transform: translateY(-2px);
        }
        
        .container {
            max-width: 1400px;
            margin: 40px auto;
            padding: 0 40px;
            position: relative;
            z-index: 1;
        }
        
        .main-grid {
            display: grid;
            grid-template-columns: 350px 1fr;
            gap: 32px;
            margin-top: 32px;
        }
        
        .sidebar {
            display: flex;
            flex-direction: column;
            gap: 24px;
        }
        
        .card {
            background: var(--card-bg);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            border: 1px solid var(--card-border);
            border-radius: 24px;
            padding: 28px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
        }
        
        .card h2 {
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 20px;
            color: var(--text-color);
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .card h2::before {
            content: '';
            width: 4px;
            height: 24px;
            background: linear-gradient(135deg, var(--accent-color), var(--accent-hover));
            border-radius: 4px;
        }
        
        .theme-selector {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
        }
        
        .theme-option {
            width: 100%;
            height: 60px;
            border-radius: 16px;
            border: 3px solid transparent;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .theme-option::after {
            content: '✓';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 24px;
            font-weight: bold;
            color: white;
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        .theme-option.active {
            border-color: var(--accent-color);
            transform: scale(1.05);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
        }
        
        .theme-option.active::after {
            opacity: 1;
        }
        
        .theme-option:hover {
            transform: scale(1.08);
        }
        
        .theme-1 { background: #ffffff; border: 2px solid #e5e7eb; }
        .theme-2 { background: #000000; }
        .theme-3 { background: #6b7280; }
        .theme-4 { background: linear-gradient(135deg, #fef3f2 0%, #fff7ed 100%); }
        .theme-5 { background: linear-gradient(135deg, #f0f9ff 0%, #dbeafe 100%); }
        .theme-6 { background: linear-gradient(135deg, #f0fdf4 0%, #d1fae5 100%); }
        
        .calendar-controls {
            display: flex;
            gap: 12px;
            margin-bottom: 24px;
        }
        
        .view-switcher {
            display: flex;
            background: var(--hover-bg);
            border-radius: 14px;
            padding: 4px;
            gap: 4px;
        }
        
        .view-btn {
            padding: 10px 20px;
            border: none;
            background: transparent;
            color: var(--text-secondary);
            font-size: 14px;
            font-weight: 600;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
            font-family: 'Poppins', sans-serif;
        }
        
        .view-btn.active {
            background: var(--accent-color);
            color: white;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }
        
        .view-btn:hover:not(.active) {
            background: var(--card-bg);
            color: var(--text-color);
        }
        
        .date-navigation {
            display: flex;
            align-items: center;
            gap: 16px;
            background: var(--card-bg);
            padding: 12px 20px;
            border-radius: 14px;
            border: 1px solid var(--card-border);
        }
        
        .date-navigation button {
            background: var(--hover-bg);
            border: none;
            width: 40px;
            height: 40px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 18px;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .date-navigation button:hover {
            background: var(--accent-color);
            color: white;
            transform: scale(1.1);
        }
        
        .current-date {
            font-weight: 600;
            font-size: 16px;
            min-width: 180px;
            text-align: center;
            color: var(--text-color);
        }
        
        .weekly-view {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 16px;
        }
        
        .day-column {
            background: var(--card-bg);
            border-radius: 20px;
            padding: 20px;
            border: 1px solid var(--card-border);
            min-height: 400px;
            transition: all 0.3s;
        }
        
        .day-column:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 28px rgba(0, 0, 0, 0.12);
        }
        
        .day-column.today {
            border: 2px solid var(--accent-color);
            box-shadow: 0 8px 24px rgba(59, 130, 246, 0.2);
        }
        
        .day-header {
            text-align: center;
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 2px solid var(--card-border);
        }
        
        .day-label {
            font-size: 13px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-secondary);
            margin-bottom: 8px;
        }
        
        .day-number {
            font-size: 28px;
            font-weight: 800;
            color: var(--text-color);
        }
        
        .day-column.today .day-number {
            color: var(--accent-color);
        }
        
        .event-card {
            padding: 16px;
            border-radius: 14px;
            margin-bottom: 12px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        
        .event-card:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        }
        
        .event-card.break {
            cursor: default;
            opacity: 0.8;
        }
        
        .event-title {
            font-weight: 700;
            font-size: 15px;
            color: white;
            margin-bottom: 6px;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
        }
        
        .event-time {
            font-size: 13px;
            color: rgba(255, 255, 255, 0.95);
            margin-bottom: 4px;
            font-weight: 500;
        }
        
        .event-duration {
            font-size: 12px;
            color: rgba(255, 255, 255, 0.9);
            font-weight: 500;
        }
        
        .event-class {
            font-size: 11px;
            color: rgba(255, 255, 255, 0.85);
            margin-top: 6px;
            padding: 4px 8px;
            background: rgba(255, 255, 255, 0.15);
            border-radius: 6px;
            display: inline-block;
        }
        
        .no-events {
            text-align: center;
            color: var(--text-secondary);
            font-size: 14px;
            padding: 32px;
            font-style: italic;
        }
        
        .daily-view {
            background: var(--card-bg);
            border-radius: 20px;
            padding: 32px;
            border: 1px solid var(--card-border);
        }
        
        .monthly-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 12px;
        }
        
        .weekday-header {
            text-align: center;
            font-weight: 700;
            font-size: 13px;
            color: var(--text-secondary);
            padding: 16px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .month-day {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 16px;
            min-height: 120px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .month-day:hover {
            background: var(--hover-bg);
            transform: translateY(-4px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        }
        
        .month-day.today {
            border: 2px solid var(--accent-color);
            box-shadow: 0 4px 16px rgba(59, 130, 246, 0.2);
        }
        
        .month-day-number {
            font-size: 18px;
            font-weight: 700;
            color: var(--text-color);
            margin-bottom: 10px;
        }
        
        .month-day.today .month-day-number {
            color: var(--accent-color);
        }
        
        .month-event {
            font-size: 11px;
            padding: 6px 10px;
            border-radius: 8px;
            margin-bottom: 6px;
            color: white;
            font-weight: 600;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(8px);
            z-index: 1000;
            align-items: center;
            justify-content: center;
            animation: fadeIn 0.3s;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .modal.active {
            display: flex;
        }
        
        .modal-content {
            background: var(--card-bg);
            border-radius: 28px;
            padding: 40px;
            max-width: 600px;
            width: 90%;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            animation: slideUp 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid var(--card-border);
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(40px) scale(0.95);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }
        
        .modal-content h2 {
            font-size: 28px;
            font-weight: 800;
            margin-bottom: 28px;
            color: var(--text-color);
        }
        
        .form-group {
            margin-bottom: 24px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 10px;
            font-weight: 600;
            color: var(--text-color);
            font-size: 14px;
        }
        
        .form-group input,
        .form-group select,
        .form-group textarea {
            width: 100%;
            padding: 14px 18px;
            border: 2px solid var(--card-border);
            border-radius: 14px;
            font-size: 15px;
            font-family: 'Poppins', sans-serif;
            background: var(--hover-bg);
            color: var(--text-color);
            transition: all 0.3s;
        }
        
        .form-group input:focus,
        .form-group select:focus,
        .form-group textarea:focus {
            outline: none;
            border-color: var(--accent-color);
            box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
            background: var(--card-bg);
        }
        
        .checkbox-group {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
        }
        
        .checkbox-label {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 10px 16px;
            background: var(--hover-bg);
            border: 2px solid var(--card-border);
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 500;
        }
        
        .checkbox-label:hover {
            background: var(--card-bg);
            border-color: var(--accent-color);
            transform: translateY(-2px);
        }
        
        .checkbox-label input[type="checkbox"] {
            width: auto;
        }
        
        .checkbox-label input[type="checkbox"]:checked + span {
            color: var(--accent-color);
            font-weight: 600;
        }
        
        .modal-actions {
            display: flex;
            gap: 12px;
            margin-top: 32px;
        }
        
        .modal-actions .btn {
            flex: 1;
        }
        
        /* Color Picker Styles - ENHANCED */
        .color-picker-section {
            margin-bottom: 24px;
        }
        
        .preset-colors {
            display: grid;
            grid-template-columns: repeat(8, 1fr);
            gap: 12px;
            margin-bottom: 20px;
        }
        
        .preset-color {
            width: 100%;
            aspect-ratio: 1;
            border-radius: 12px;
            border: 3px solid transparent;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            position: relative;
        }
        
        .preset-color::after {
            content: '✓';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-size: 20px;
            font-weight: bold;
            opacity: 0;
            transition: opacity 0.3s;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .preset-color.selected {
            border-color: white;
            transform: scale(1.15);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
        }
        
        .preset-color.selected::after {
            opacity: 1;
        }
        
        .preset-color:hover {
            transform: scale(1.2);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
        }
        
        .gradient-picker-container {
            margin-bottom: 20px;
        }
        
        .gradient-picker {
            width: 100%;
            height: 60px;
            border-radius: 16px;
            background: linear-gradient(to right, 
                #ef4444, #f59e0b, #eab308, #84cc16, #22c55e, 
                #10b981, #14b8a6, #06b6d4, #0ea5e9, #3b82f6, 
                #6366f1, #8b5cf6, #a855f7, #d946ef, #ec4899, #f43f5e);
            cursor: pointer;
            position: relative;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
            border: 3px solid var(--card-border);
        }
        
        .gradient-picker:hover {
            transform: scale(1.02);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
        }
        
        .gradient-picker-indicator {
            position: absolute;
            top: -8px;
            width: 24px;
            height: 76px;
            border: 4px solid white;
            border-radius: 8px;
            pointer-events: none;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            transform: translateX(-12px);
        }
        
        .hex-input-container {
            display: flex;
            gap: 12px;
            align-items: center;
        }
        
        .color-preview {
            width: 60px;
            height: 60px;
            border-radius: 14px;
            border: 3px solid var(--card-border);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            transition: all 0.3s;
        }
        
        .hex-input {
            flex: 1;
        }
        
        /* Setup Wizard Styles */
        .setup-wizard {
            text-align: center;
        }
        
        .setup-wizard h2 {
            font-size: 36px;
            font-weight: 800;
            margin-bottom: 16px;
            background: linear-gradient(135deg, var(--accent-color), var(--accent-hover));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .setup-wizard p {
            color: var(--text-secondary);
            font-size: 16px;
            margin-bottom: 32px;
        }
        
        .class-list {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 16px;
        }
        
        .class-tag {
            padding: 8px 16px;
            background: linear-gradient(135deg, var(--accent-color), var(--accent-hover));
            color: white;
            border-radius: 10px;
            font-size: 13px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
            transition: all 0.3s;
        }
        
        .class-tag:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
        }
        
        .class-tag button {
            background: rgba(255, 255, 255, 0.2);
            border: none;
            color: white;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s;
        }
        
        .class-tag button:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: rotate(90deg);
        }
        
        /* AI Teacher Button */
        .ai-teacher-btn {
            position: fixed;
            bottom: 32px;
            right: 32px;
            width: 70px;
            height: 70px;
            border-radius: 50%;
            background: linear-gradient(135deg, #8b5cf6, #6366f1);
            border: none;
            cursor: pointer;
            box-shadow: 0 8px 24px rgba(139, 92, 246, 0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            z-index: 999;
        }
        
        .ai-teacher-btn:hover {
            transform: scale(1.1) rotate(10deg);
            box-shadow: 0 12px 32px rgba(139, 92, 246, 0.5);
        }
        
        .ai-teacher-btn:active {
            transform: scale(0.95);
        }
        
        /* AI Chat Styles */
        .ai-chat-container {
            max-height: 400px;
            overflow-y: auto;
            margin-bottom: 20px;
            padding: 20px;
            background: var(--hover-bg);
            border-radius: 16px;
            border: 1px solid var(--card-border);
        }
        
        .ai-message {
            margin-bottom: 16px;
            padding: 16px 20px;
            border-radius: 16px;
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .ai-message.user {
            background: linear-gradient(135deg, var(--accent-color), var(--accent-hover));
            color: white;
            margin-left: 40px;
            border-bottom-right-radius: 4px;
        }
        
        .ai-message.assistant {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            margin-right: 40px;
            border-bottom-left-radius: 4px;
        }
        
        .ai-message-text {
            line-height: 1.6;
            white-space: pre-wrap;
        }
        
        .ai-input-container {
            display: flex;
            gap: 12px;
        }
        
        .ai-input {
            flex: 1;
            padding: 14px 18px;
            border: 2px solid var(--card-border);
            border-radius: 14px;
            font-size: 15px;
            font-family: 'Poppins', sans-serif;
            background: var(--hover-bg);
            color: var(--text-color);
            transition: all 0.3s;
        }
        
        .ai-input:focus {
            outline: none;
            border-color: #8b5cf6;
            box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.1);
        }
        
        .ai-send-btn {
            padding: 14px 24px;
            background: linear-gradient(135deg, #8b5cf6, #6366f1);
            color: white;
            border: none;
            border-radius: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
        }
        
        .ai-send-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(139, 92, 246, 0.4);
        }
        
        .ai-send-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        
        .loading-dots {
            display: inline-block;
        }
        
        .loading-dots::after {
            content: '';
            animation: dots 1.5s steps(4, end) infinite;
        }
        
        @keyframes dots {
            0%, 20% { content: ''; }
            40% { content: '.'; }
            60% { content: '..'; }
            80%, 100% { content: '...'; }
        }
        
        /* Responsive Design */
        @media (max-width: 1200px) {
            .main-grid {
                grid-template-columns: 1fr;
            }
            
            .sidebar {
                order: -1;
            }
            
            .weekly-view {
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            }
        }
        
        @media (max-width: 768px) {
            .app-bar {
                padding: 16px 24px;
            }
            
            .app-bar h1 {
                font-size: 24px;
            }
            
            .container {
                padding: 0 20px;
            }
            
            .monthly-grid {
                gap: 8px;
            }
            
            .weekday-header {
                font-size: 11px;
                padding: 12px 4px;
            }
            
            .month-day {
                padding: 8px;
                min-height: 80px;
            }
            
            .calendar-controls {
                flex-direction: column;
            }
            
            .preset-colors {
                grid-template-columns: repeat(6, 1fr);
            }
            
            .ai-teacher-btn {
                width: 60px;
                height: 60px;
                bottom: 24px;
                right: 24px;
                font-size: 28px;
            }
        }
    </style>
</head>
<body class="gradient-4">
    <div class="app-bar">
        <h1>✨ My Planner</h1>
        <div class="app-bar-actions">
            <span id="userName" style="font-weight: 600; color: var(--text-color);">Welcome!</span>
            <button class="btn btn-secondary" onclick="openSettingsModal()">⚙️ Settings</button>
            <button class="btn btn-primary" onclick="openEventModal()">+ Add Event</button>
        </div>
    </div>

    <div class="container">
        <div class="main-grid">
            <div class="sidebar">
                <div class="card">
                    <h2>🎨 Theme</h2>
                    <div class="theme-selector">
                        <div class="theme-option theme-1" onclick="changeTheme(1)"></div>
                        <div class="theme-option theme-2" onclick="changeTheme(2)"></div>
                        <div class="theme-option theme-3" onclick="changeTheme(3)"></div>
                        <div class="theme-option theme-4 active" onclick="changeTheme(4)"></div>
                        <div class="theme-option theme-5" onclick="changeTheme(5)"></div>
                        <div class="theme-option theme-6" onclick="changeTheme(6)"></div>
                    </div>
                </div>

                <div class="card">
                    <h2>📚 My Classes</h2>
                    <div class="class-list" id="classList"></div>
                    <button class="btn btn-primary" style="width: 100%; margin-top: 16px;" onclick="openAddClassModal()">+ Add Class</button>
                </div>
            </div>

            <div class="main-content">
                <div class="card">
                    <div class="calendar-controls">
                        <div class="view-switcher">
                            <button class="view-btn" onclick="changeView('daily')">Day</button>
                            <button class="view-btn active" onclick="changeView('weekly')">Week</button>
                            <button class="view-btn" onclick="changeView('monthly')">Month</button>
                        </div>
                        <div class="date-navigation">
                            <button onclick="previousPeriod()">‹</button>
                            <span class="current-date" id="currentDate"></span>
                            <button onclick="nextPeriod()">›</button>
                            <button onclick="goToToday()">Today</button>
                        </div>
                    </div>
                    <div id="calendarView"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- AI Teacher Button -->
    <button class="ai-teacher-btn" onclick="openAITeacherModal()" title="AI Teacher">
        🤖
    </button>

    <!-- Setup Modal -->
    <div id="setupModal" class="modal">
        <div class="modal-content">
            <div class="setup-wizard">
                <h2>Welcome! 👋</h2>
                <p>Let's personalize your planning experience</p>
                
                <div class="form-group">
                    <label>What's your name?</label>
                    <input type="text" id="setupName" placeholder="Enter your name">
                </div>

                <div class="form-group">
                    <label>Learning Accommodations (optional)</label>
                    <div class="checkbox-group">
                        <label class="checkbox-label">
                            <input type="checkbox" value="adhd" onchange="updateAccommodations(this)">
                            <span>ADHD</span>
                        </label>
                        <label class="checkbox-label">
                            <input type="checkbox" value="dyslexia" onchange="updateAccommodations(this)">
                            <span>Dyslexia</span>
                        </label>
                        <label class="checkbox-label">
                            <input type="checkbox" value="autism" onchange="updateAccommodations(this)">
                            <span>Autism</span>
                        </label>
                    </div>
                </div>

                <button class="btn btn-primary" style="width: 100%; margin-top: 24px;" onclick="completeSetup()">Get Started! 🚀</button>
            </div>
        </div>
    </div>

    <!-- Event Modal -->
    <div id="eventModal" class="modal">
        <div class="modal-content">
            <h2 id="eventModalTitle">Add Event</h2>
            
            <div class="form-group">
                <label>Event Title</label>
                <input type="text" id="eventTitle" placeholder="e.g., Study Math">
            </div>

            <div class="form-group">
                <label>Event Type</label>
                <select id="eventType" onchange="handleEventTypeChange()">
                    <option value="flexible">Flexible (Auto-scheduled)</option>
                    <option value="fixed">Fixed Time</option>
                </select>
            </div>

            <div class="form-group">
                <label>Date</label>
                <input type="date" id="eventDate">
            </div>

            <div id="fixedTimeFields" style="display: none;">
                <div class="form-group">
                    <label>Start Time</label>
                    <input type="time" id="eventStartTime">
                </div>
            </div>

            <div class="form-group">
                <label>Duration (minutes)</label>
                <input type="number" id="eventDuration" placeholder="60" min="5">
            </div>

            <div class="form-group">
                <label>Class (optional)</label>
                <select id="eventClass">
                    <option value="">None</option>
                </select>
            </div>

            <div class="form-group">
                <label>Description (optional)</label>
                <textarea id="eventDescription" rows="3" placeholder="Add any notes or details..."></textarea>
            </div>

            <div class="form-group color-picker-section">
                <label>Color</label>
                
                <div class="preset-colors">
                    <div class="preset-color" style="background: #ef4444;" onclick="selectPresetColor('#ef4444')"></div>
                    <div class="preset-color" style="background: #f97316;" onclick="selectPresetColor('#f97316')"></div>
                    <div class="preset-color" style="background: #f59e0b;" onclick="selectPresetColor('#f59e0b')"></div>
                    <div class="preset-color" style="background: #eab308;" onclick="selectPresetColor('#eab308')"></div>
                    <div class="preset-color" style="background: #84cc16;" onclick="selectPresetColor('#84cc16')"></div>
                    <div class="preset-color" style="background: #22c55e;" onclick="selectPresetColor('#22c55e')"></div>
                    <div class="preset-color" style="background: #10b981;" onclick="selectPresetColor('#10b981')"></div>
                    <div class="preset-color" style="background: #14b8a6;" onclick="selectPresetColor('#14b8a6')"></div>
                    <div class="preset-color" style="background: #06b6d4;" onclick="selectPresetColor('#06b6d4')"></div>
                    <div class="preset-color" style="background: #0ea5e9;" onclick="selectPresetColor('#0ea5e9')"></div>
                    <div class="preset-color" style="background: #3b82f6;" onclick="selectPresetColor('#3b82f6')"></div>
                    <div class="preset-color" style="background: #6366f1;" onclick="selectPresetColor('#6366f1')"></div>
                    <div class="preset-color" style="background: #8b5cf6;" onclick="selectPresetColor('#8b5cf6')"></div>
                    <div class="preset-color" style="background: #a855f7;" onclick="selectPresetColor('#a855f7')"></div>
                    <div class="preset-color" style="background: #d946ef;" onclick="selectPresetColor('#d946ef')"></div>
                    <div class="preset-color" style="background: #ec4899;" onclick="selectPresetColor('#ec4899')"></div>
                </div>

                <div class="gradient-picker-container">
                    <label style="display: block; margin-bottom: 10px; font-size: 13px; color: var(--text-secondary);">Or tap to pick from gradient:</label>
                    <div class="gradient-picker" id="gradientPicker">
                        <div class="gradient-picker-indicator" id="gradientIndicator"></div>
                    </div>
                </div>

                <div class="hex-input-container">
                    <div class="color-preview" id="colorPreview"></div>
                    <input type="text" class="hex-input" id="eventColor" placeholder="#3b82f6" maxlength="7">
                </div>
            </div>

            <div class="modal-actions">
                <button class="btn btn-secondary" onclick="closeModal('eventModal')">Cancel</button>
                <button class="btn btn-primary" id="saveEventBtn" onclick="saveEvent()">Save Event</button>
            </div>
            
            <button id="deleteEventBtn" class="btn btn-secondary" style="width: 100%; margin-top: 12px; display: none; background: #ef4444; color: white;" onclick="deleteEvent()">Delete Event</button>
        </div>
    </div>

    <!-- Settings Modal -->
    <div id="settingsModal" class="modal">
        <div class="modal-content">
            <h2>⚙️ Settings</h2>
            
            <div class="form-group">
                <label>Your Name</label>
                <input type="text" id="settingsName" placeholder="Enter your name">
            </div>

            <div class="form-group">
                <label>Learning Accommodations</label>
                <div class="checkbox-group" id="accommodationsCheckboxes">
                    <label class="checkbox-label">
                        <input type="checkbox" value="adhd">
                        <span>ADHD</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" value="dyslexia">
                        <span>Dyslexia</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" value="autism">
                        <span>Autism</span>
                    </label>
                </div>
            </div>

            <div class="form-group">
                <label>Daily Start Time</label>
                <input type="time" id="settingsStartTime">
            </div>

            <div class="form-group">
                <label>Daily End Time</label>
                <input type="time" id="settingsEndTime">
            </div>

            <div class="form-group">
                <label>Break Length (minutes)</label>
                <input type="number" id="settingsBreakLength" min="5" placeholder="15">
            </div>

            <div class="form-group">
                <label>Buffer Between Events (minutes)</label>
                <input type="number" id="settingsBuffer" min="0" placeholder="5">
            </div>

            <div class="modal-actions">
                <button class="btn btn-secondary" onclick="closeModal('settingsModal')">Cancel</button>
                <button class="btn btn-primary" onclick="saveSettings()">Save Settings</button>
            </div>
        </div>
    </div>

    <!-- Add Class Modal -->
    <div id="addClassModal" class="modal">
        <div class="modal-content">
            <h2>Add Class</h2>
            
            <div class="form-group">
                <label>Class Name</label>
                <input type="text" id="className" placeholder="e.g., Mathematics">
            </div>

            <div class="modal-actions">
                <button class="btn btn-secondary" onclick="closeModal('addClassModal')">Cancel</button>
                <button class="btn btn-primary" onclick="saveClass()">Add Class</button>
            </div>
        </div>
    </div>

    <!-- AI Teacher Modal -->
    <div id="aiTeacherModal" class="modal">
        <div class="modal-content">
            <h2>🤖 AI Teacher</h2>
            <p style="color: var(--text-secondary); margin-bottom: 20px;">Ask me anything! I'm here to help you learn and understand concepts.</p>
            
            <div class="ai-chat-container" id="aiChatContainer">
                <div class="ai-message assistant">
                    <div class="ai-message-text">Hi! I'm your AI teacher powered by Google Gemini. What would you like to learn about today?</div>
                </div>
            </div>

            <div class="ai-input-container">
                <input type="text" class="ai-input" id="aiInput" placeholder="Ask me anything..." onkeypress="handleAIKeyPress(event)">
                <button class="ai-send-btn" id="aiSendBtn" onclick="sendAIMessage()">Send</button>
            </div>

            <button class="btn btn-secondary" style="width: 100%; margin-top: 16px;" onclick="closeModal('aiTeacherModal')">Close</button>
        </div>
    </div>

    <script>
        // ==================== DATA & STATE ====================
        let userName = '';
        let accommodations = [];
        let events = [];
        let classes = [];
        let selectedDate = new Date();
        let currentView = 'weekly';
        let currentTheme = 4;
        let editingEventId = null;
        let setupComplete = false;
        let durationHistory = {};
        let currentEventColor = '#3b82f6';
        let aiConversation = [];
        
        const GEMINI_API_KEY = 'AIzaSyA_AjHXMJSj7lm4XmxiITqCIZ9-kP7tsXw';
        
        let settings = {
            dailyStartTime: '08:00',
            dailyEndTime: '22:00',
            breakLength: 15,
            bufferBetweenEvents: 5
        };

        // ==================== INITIALIZATION ====================
        window.onload = function() {
            loadData();
            
            if (!setupComplete) {
                openModal('setupModal');
            } else {
                updateDisplay();
            }
            
            changeTheme(currentTheme);
            setupGradientPicker();
            
            // Set default event date to selected date
            const today = new Date();
            document.getElementById('eventDate').value = formatDateForInput(today);
        };

        // ==================== THEME MANAGEMENT ====================
        function changeTheme(themeNumber) {
            currentTheme = themeNumber;
            document.body.className = `gradient-${themeNumber}`;
            
            document.querySelectorAll('.theme-option').forEach(opt => opt.classList.remove('active'));
            document.querySelector(`.theme-${themeNumber}`).classList.add('active');
            
            saveData();
        }

        // ==================== COLOR PICKER ====================
        function setupGradientPicker() {
            const picker = document.getElementById('gradientPicker');
            const indicator = document.getElementById('gradientIndicator');
            
            picker.addEventListener('click', (e) => {
                const rect = picker.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const percentage = x / rect.width;
                
                // Calculate color from gradient
                const colors = [
                    '#ef4444', '#f59e0b', '#eab308', '#84cc16', '#22c55e', 
                    '#10b981', '#14b8a6', '#06b6d4', '#0ea5e9', '#3b82f6', 
                    '#6366f1', '#8b5cf6', '#a855f7', '#d946ef', '#ec4899', '#f43f5e'
                ];
                
                const index = Math.floor(percentage * (colors.length - 1));
                const color = colors[index];
                
                selectColor(color);
                
                // Update indicator position
                indicator.style.left = `${x}px`;
            });
        }

        function selectPresetColor(color) {
            selectColor(color);
            
            // Update visual selection
            document.querySelectorAll('.preset-color').forEach(el => el.classList.remove('selected'));
            event.target.classList.add('selected');
        }

        function selectColor(color) {
            currentEventColor = color;
            document.getElementById('eventColor').value = color;
            document.getElementById('colorPreview').style.background = color;
        }

        // Update color preview when typing
        document.addEventListener('DOMContentLoaded', () => {
            const colorInput = document.getElementById('eventColor');
            if (colorInput) {
                colorInput.addEventListener('input', (e) => {
                    const value = e.target.value;
                    if (/^#[0-9A-Fa-f]{6}$/.test(value)) {
                        selectColor(value);
                    }
                });
            }
        });

        // ==================== SETUP WIZARD ====================
        function updateAccommodations(checkbox) {
            if (checkbox.checked) {
                if (!accommodations.includes(checkbox.value)) {
                    accommodations.push(checkbox.value);
                }
            } else {
                accommodations = accommodations.filter(a => a !== checkbox.value);
            }
        }

        function completeSetup() {
            userName = document.getElementById('setupName').value.trim();
            
            if (!userName) {
                alert('Please enter your name');
                return;
            }
            
            setupComplete = true;
            document.getElementById('userName').textContent = userName;
            closeModal('setupModal');
            saveData();
            updateDisplay();
        }

        // ==================== MODAL MANAGEMENT ====================
        function openModal(modalId) {
            document.getElementById(modalId).classList.add('active');
        }

        function closeModal(modalId) {
            document.getElementById(modalId).classList.remove('active');
        }

        function openEventModal() {
            editingEventId = null;
            document.getElementById('eventModalTitle').textContent = 'Add Event';
            document.getElementById('eventTitle').value = '';
            document.getElementById('eventType').value = 'flexible';
            document.getElementById('eventDate').value = formatDateForInput(selectedDate);
            document.getElementById('eventStartTime').value = '';
            document.getElementById('eventDuration').value = '';
            document.getElementById('eventClass').value = '';
            document.getElementById('eventDescription').value = '';
            document.getElementById('eventColor').value = '#3b82f6';
            document.getElementById('colorPreview').style.background = '#3b82f6';
            document.getElementById('deleteEventBtn').style.display = 'none';
            document.getElementById('fixedTimeFields').style.display = 'none';
            
            updateClassDropdown();
            openModal('eventModal');
        }

        function openEditEventModal(eventId) {
            const event = events.find(e => e.id === eventId);
            if (!event) return;
            
            editingEventId = eventId;
            document.getElementById('eventModalTitle').textContent = 'Edit Event';
            document.getElementById('eventTitle').value = event.title;
            document.getElementById('eventType').value = event.eventType;
            
            // FIX: Format date properly for input
            document.getElementById('eventDate').value = formatDateForInput(new Date(event.date));
            
            document.getElementById('eventStartTime').value = event.startTime || '';
            document.getElementById('eventDuration').value = event.duration;
            document.getElementById('eventClass').value = event.classTag || '';
            document.getElementById('eventDescription').value = event.description || '';
            document.getElementById('eventColor').value = event.color;
            document.getElementById('colorPreview').style.background = event.color;
            document.getElementById('deleteEventBtn').style.display = 'block';
            document.getElementById('fixedTimeFields').style.display = event.eventType === 'fixed' ? 'block' : 'none';
            
            updateClassDropdown();
            openModal('eventModal');
        }

        function openSettingsModal() {
            document.getElementById('settingsName').value = userName;
            document.getElementById('settingsStartTime').value = settings.dailyStartTime;
            document.getElementById('settingsEndTime').value = settings.dailyEndTime;
            document.getElementById('settingsBreakLength').value = settings.breakLength;
            document.getElementById('settingsBuffer').value = settings.bufferBetweenEvents;
            
            document.querySelectorAll('#accommodationsCheckboxes input').forEach(checkbox => {
                checkbox.checked = accommodations.includes(checkbox.value);
            });
            
            openModal('settingsModal');
        }

        function openAddClassModal() {
            document.getElementById('className').value = '';
            openModal('addClassModal');
        }

        function handleEventTypeChange() {
            const eventType = document.getElementById('eventType').value;
            document.getElementById('fixedTimeFields').style.display = eventType === 'fixed' ? 'block' : 'none';
        }

        // ==================== AI TEACHER ====================
        function openAITeacherModal() {
            openModal('aiTeacherModal');
            scrollAIChatToBottom();
        }

        async function sendAIMessage() {
            const input = document.getElementById('aiInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message to chat
            addAIMessage(message, 'user');
            input.value = '';
            
            // Disable send button
            const sendBtn = document.getElementById('aiSendBtn');
            sendBtn.disabled = true;
            sendBtn.innerHTML = '<span class="loading-dots">Thinking</span>';
            
            try {
                const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${GEMINI_API_KEY}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        contents: [{
                            parts: [{
                                text: `You are a helpful AI teacher. Please explain the following in a clear, educational way: ${message}`
                            }]
                        }]
                    })
                });
                
                const data = await response.json();
                
                if (data.candidates && data.candidates[0]?.content?.parts[0]?.text) {
                    const aiResponse = data.candidates[0].content.parts[0].text;
                    addAIMessage(aiResponse, 'assistant');
                } else {
                    addAIMessage('Sorry, I had trouble understanding that. Could you try rephrasing your question?', 'assistant');
                }
            } catch (error) {
                console.error('AI Error:', error);
                addAIMessage('Sorry, I encountered an error. Please try again.', 'assistant');
            } finally {
                sendBtn.disabled = false;
                sendBtn.textContent = 'Send';
            }
        }

        function addAIMessage(text, role) {
            const container = document.getElementById('aiChatContainer');
            const messageDiv = document.createElement('div');
            messageDiv.className = `ai-message ${role}`;
            messageDiv.innerHTML = `<div class="ai-message-text">${text}</div>`;
            container.appendChild(messageDiv);
            scrollAIChatToBottom();
        }

        function scrollAIChatToBottom() {
            const container = document.getElementById('aiChatContainer');
            setTimeout(() => {
                container.scrollTop = container.scrollHeight;
            }, 100);
        }

        function handleAIKeyPress(event) {
            if (event.key === 'Enter') {
                sendAIMessage();
            }
        }

        // ==================== EVENT MANAGEMENT ====================
        function saveEvent() {
            const title = document.getElementById('eventTitle').value.trim();
            const eventType = document.getElementById('eventType').value;
            const dateStr = document.getElementById('eventDate').value;
            const duration = parseInt(document.getElementById('eventDuration').value);
            const classTag = document.getElementById('eventClass').value;
            const description = document.getElementById('eventDescription').value.trim();
            const color = document.getElementById('eventColor').value || '#3b82f6';
            
            if (!title || !dateStr || !duration) {
                alert('Please fill in all required fields');
                return;
            }
            
            // FIX: Create date object properly to avoid timezone issues
            const [year, month, day] = dateStr.split('-').map(Number);
            const eventDate = new Date(year, month - 1, day); // month is 0-indexed
            
            let startTime = null;
            if (eventType === 'fixed') {
                const timeStr = document.getElementById('eventStartTime').value;
                if (!timeStr) {
                    alert('Please specify a start time for fixed events');
                    return;
                }
                startTime = timeStr;
            }
            
            const event = {
                id: editingEventId || Date.now(),
                title,
                eventType,
                date: eventDate.toISOString(),
                startTime,
                duration,
                classTag: classTag || null,
                description: description || null,
                color
            };
            
            if (editingEventId) {
                const index = events.findIndex(e => e.id === editingEventId);
                events[index] = event;
            } else {
                events.push(event);
            }
            
            if (classTag && !durationHistory[classTag]) {
                durationHistory[classTag] = [];
            }
            if (classTag) {
                durationHistory[classTag].push(duration);
                if (durationHistory[classTag].length > 10) {
                    durationHistory[classTag].shift();
                }
            }
            
            saveData();
            closeModal('eventModal');
            updateDisplay();
        }

        function deleteEvent() {
            if (!confirm('Are you sure you want to delete this event?')) return;
            
            events = events.filter(e => e.id !== editingEventId);
            saveData();
            closeModal('eventModal');
            updateDisplay();
        }

        function saveSettings() {
            userName = document.getElementById('settingsName').value.trim();
            settings.dailyStartTime = document.getElementById('settingsStartTime').value;
            settings.dailyEndTime = document.getElementById('settingsEndTime').value;
            settings.breakLength = parseInt(document.getElementById('settingsBreakLength').value);
            settings.bufferBetweenEvents = parseInt(document.getElementById('settingsBuffer').value);
            
            accommodations = [];
            document.querySelectorAll('#accommodationsCheckboxes input:checked').forEach(checkbox => {
                accommodations.push(checkbox.value);
            });
            
            document.getElementById('userName').textContent = userName;
            saveData();
            closeModal('settingsModal');
            updateDisplay();
        }

        function saveClass() {
            const className = document.getElementById('className').value.trim();
            
            if (!className) {
                alert('Please enter a class name');
                return;
            }
            
            if (classes.some(c => c.name.toLowerCase() === className.toLowerCase())) {
                alert('This class already exists');
                return;
            }
            
            classes.push({
                id: Date.now(),
                name: className
            });
            
            saveData();
            updateClassList();
            updateClassDropdown();
            closeModal('addClassModal');
        }

        function deleteClass(classId) {
            if (!confirm('Are you sure? Events linked to this class will remain but lose their class tag.')) return;
            
            classes = classes.filter(c => c.id !== classId);
            saveData();
            updateClassList();
            updateClassDropdown();
        }

        function updateClassList() {
            const container = document.getElementById('classList');
            if (classes.length === 0) {
                container.innerHTML = '<p style="color: var(--text-secondary); font-size: 14px;">No classes yet</p>';
                return;
            }
            
            container.innerHTML = classes.map(c => `
                <div class="class-tag">
                    ${c.name}
                    <button onclick="deleteClass(${c.id})">×</button>
                </div>
            `).join('');
        }

        function updateClassDropdown() {
            const select = document.getElementById('eventClass');
            select.innerHTML = '<option value="">None</option>' + 
                classes.map(c => `<option value="${c.name}">${c.name}</option>`).join('');
        }

        // ==================== CALENDAR NAVIGATION ====================
        function changeView(view) {
            currentView = view;
            document.querySelectorAll('.view-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            updateDisplay();
        }

        function previousPeriod() {
            if (currentView === 'daily') {
                selectedDate.setDate(selectedDate.getDate() - 1);
            } else if (currentView === 'weekly') {
                selectedDate.setDate(selectedDate.getDate() - 7);
            } else if (currentView === 'monthly') {
                selectedDate.setMonth(selectedDate.getMonth() - 1);
            }
            updateDisplay();
        }

        function nextPeriod() {
            if (currentView === 'daily') {
                selectedDate.setDate(selectedDate.getDate() + 1);
            } else if (currentView === 'weekly') {
                selectedDate.setDate(selectedDate.getDate() + 7);
            } else if (currentView === 'monthly') {
                selectedDate.setMonth(selectedDate.getMonth() + 1);
            }
            updateDisplay();
        }

        function goToToday() {
            selectedDate = new Date();
            updateDisplay();
        }

        function updateDisplay() {
            updateDateLabel();
            
            if (currentView === 'daily') {
                renderDailyView();
            } else if (currentView === 'weekly') {
                renderWeeklyView();
            } else if (currentView === 'monthly') {
                renderMonthlyView();
            }
        }

        function updateDateLabel() {
            const label = document.getElementById('currentDate');
            
            if (currentView === 'daily') {
                label.textContent = selectedDate.toLocaleDateString('en-US', { 
                    weekday: 'long', 
                    year: 'numeric', 
                    month: 'long', 
                    day: 'numeric' 
                });
            } else if (currentView === 'weekly') {
                const startOfWeek = getStartOfWeek(selectedDate);
                const endOfWeek = new Date(startOfWeek);
                endOfWeek.setDate(startOfWeek.getDate() + 6);
                
                label.textContent = `${startOfWeek.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })} - ${endOfWeek.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}`;
            } else if (currentView === 'monthly') {
                label.textContent = selectedDate.toLocaleDateString('en-US', { 
                    year: 'numeric', 
                    month: 'long' 
                });
            }
        }

        // ==================== DATE UTILITIES ====================
        function getStartOfWeek(date) {
            const d = new Date(date);
            const day = d.getDay();
            const diff = d.getDate() - day;
            return new Date(d.setDate(diff));
        }

        function isSameDay(date1, date2) {
            return date1.getFullYear() === date2.getFullYear() &&
                   date1.getMonth() === date2.getMonth() &&
                   date1.getDate() === date2.getDate();
        }

        function getDayLabel(dayIndex) {
            const days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];
            return days[dayIndex];
        }

        function formatDateForInput(date) {
            // FIX: Use local date components instead of ISO string to avoid timezone issues
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            return `${year}-${month}-${day}`;
        }

        // ==================== SCHEDULING ALGORITHM ====================
        function generateScheduleForDay(day) {
            const dayEvents = events.filter(e => {
                const eventDate = new Date(e.date);
                return isSameDay(eventDate, day);
            });
            
            const schedule = [];
            
            const fixedEvents = dayEvents.filter(e => e.eventType === 'fixed').map(e => {
                const [hours, minutes] = e.startTime.split(':');
                const startTime = new Date(day);
                startTime.setHours(parseInt(hours), parseInt(minutes), 0, 0);
                const endTime = new Date(startTime.getTime() + e.duration * 60000);
                
                return {
                    ...e,
                    startTime,
                    endTime
                };
            });
            
            schedule.push(...fixedEvents);
            
            const flexibleEvents = dayEvents.filter(e => e.eventType === 'flexible');
            
            const [startHour, startMinute] = settings.dailyStartTime.split(':').map(Number);
            const [endHour, endMinute] = settings.dailyEndTime.split(':').map(Number);
            
            const startTime = new Date(day);
            startTime.setHours(startHour, startMinute, 0, 0);
            
            const endTime = new Date(day);
            endTime.setHours(endHour, endMinute, 0, 0);
            
            let cursor = new Date(startTime);
            
            flexibleEvents.forEach(flex => {
                while (cursor < endTime) {
                    let slotStart = new Date(cursor);
                    let slotEnd = new Date(cursor.getTime() + flex.duration * 60000);
                    
                    let hasConflict = false;
                    for (let fixed of fixedEvents) {
                        if ((slotStart >= fixed.startTime && slotStart < fixed.endTime) ||
                            (slotEnd > fixed.startTime && slotEnd <= fixed.endTime) ||
                            (slotStart <= fixed.startTime && slotEnd >= fixed.endTime)) {
                            hasConflict = true;
                            slotStart = new Date(fixed.endTime.getTime() + settings.bufferBetweenEvents * 60000);
                            break;
                        }
                    }
                    
                    if (!hasConflict && slotEnd <= endTime) {
                        schedule.push({
                            ...flex,
                            startTime: new Date(slotStart),
                            endTime: new Date(slotEnd)
                        });
                        
                        if (accommodations.includes('adhd') || accommodations.includes('dyslexia')) {
                            const breakStart = new Date(slotEnd);
                            const breakEnd = new Date(breakStart.getTime() + settings.breakLength * 60000);
                            if (breakEnd <= endTime) {
                                schedule.push({
                                    id: Date.now() + Math.random(),
                                    title: 'Break',
                                    eventType: 'break',
                                    duration: settings.breakLength,
                                    startTime: breakStart,
                                    endTime: breakEnd,
                                    color: '#10b981'
                                });
                            }
                            cursor = new Date(breakEnd.getTime() + settings.bufferBetweenEvents * 60000);
                        } else {
                            cursor = new Date(slotEnd.getTime() + settings.bufferBetweenEvents * 60000);
                        }
                        break;
                    } else if (hasConflict) {
                        continue;
                    } else {
                        break;
                    }
                }
            });
            
            schedule.sort((a, b) => a.startTime - b.startTime);
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
                                 onclick="${e.eventType !== 'break' ? `openEditEventModal(${e.id})` : ''}">
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
                             onclick="${e.eventType !== 'break' ? `openEditEventModal(${e.id})` : ''}">
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
            
            ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'].forEach(day => {
                html += `<div class="weekday-header">${day}</div>`;
            });
            
            for (let i = 0; i < startWeekday; i++) {
                html += '<div class="month-day"></div>';
            }
            
            for (let day = 1; day <= totalDays; day++) {
                const date = new Date(year, month, day);
                const isToday = isSameDay(date, today);
                const dayEvents = generateScheduleForDay(date).slice(0, 3);
                const extraEvents = generateScheduleForDay(date).length - dayEvents.length;
                
                html += `
                    <div class="month-day ${isToday ? 'today' : ''}" onclick="selectDayAndViewDaily(${year}, ${month}, ${day})">
                        <div class="month-day-number">${day}</div>
                        ${dayEvents.map(e => `
                            <div class="month-event" style="background: ${e.color};">${e.title}</div>
                        `).join('')}
                        ${extraEvents > 0 ? `<div style="font-size: 10px; color: var(--text-secondary);">+${extraEvents} more</div>` : ''}
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

        // ==================== DATA PERSISTENCE ====================
        function saveData() {
            const data = {
                userName,
                accommodations,
                events,
                classes,
                settings,
                durationHistory,
                setupComplete,
                currentTheme
            };
            localStorage.setItem('plannerData', JSON.stringify(data));
        }

        function loadData() {
            const data = localStorage.getItem('plannerData');
            if (data) {
                const parsed = JSON.parse(data);
                userName = parsed.userName || '';
                accommodations = parsed.accommodations || [];
                events = parsed.events || [];
                classes = parsed.classes || [];
                settings = parsed.settings || settings;
                durationHistory = parsed.durationHistory || {};
                setupComplete = parsed.setupComplete || false;
                currentTheme = parsed.currentTheme || 4;
                
                if (userName) {
                    document.getElementById('userName').textContent = userName;
                }
                updateClassList();
            }
        }
    </script>
</body>
</html>'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)
