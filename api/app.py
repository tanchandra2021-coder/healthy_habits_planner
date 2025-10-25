from flask import Flask, render_template_string
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', '')

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
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
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
        
        /* Purple pastel theme */
        body.gradient-7 {
            --gradient-bg: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 50%, #e9d5ff 100%);
            --text-color: #1f2937;
            --text-secondary: #6b7280;
            --card-bg: rgba(255, 255, 255, 0.95);
            --card-border: rgba(233, 213, 255, 0.6);
            --hover-bg: rgba(250, 245, 255, 0.95);
            --accent-color: #9333ea;
            --accent-hover: #7e22ce;
            --header-text: #1f2937;
            --btn-text: #ffffff;
        }
        
        /* Pink pastel theme */
        body.gradient-8 {
            --gradient-bg: linear-gradient(135deg, #fef1f7 0%, #fce7f3 50%, #fbcfe8 100%);
            --text-color: #1f2937;
            --text-secondary: #6b7280;
            --card-bg: rgba(255, 255, 255, 0.95);
            --card-border: rgba(251, 207, 232, 0.6);
            --hover-bg: rgba(254, 241, 247, 0.95);
            --accent-color: #ec4899;
            --accent-hover: #db2777;
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
            padding: 20px 40px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .app-bar h1 {
            font-size: 28px;
            font-weight: 700;
            color: var(--header-text);
            letter-spacing: -0.5px;
        }
        
        .app-bar-actions {
            display: flex;
            gap: 12px;
            align-items: center;
        }
        
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 14px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            font-family: 'Poppins', sans-serif;
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
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
            background: var(--accent-color);
            color: var(--btn-text);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            border: 1px solid var(--accent-color);
        }
        
        .btn-primary:hover {
            background: var(--accent-hover);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        .btn-secondary {
            background: var(--card-bg);
            color: var(--text-color);
            border: 1px solid var(--card-border);
            backdrop-filter: blur(10px);
        }
        
        .btn-secondary:hover {
            background: var(--hover-bg);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        
        .btn-icon {
            background: var(--card-bg);
            padding: 10px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            min-width: 44px;
            height: 44px;
            border: 1px solid var(--card-border);
            backdrop-filter: blur(10px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            color: var(--text-color);
        }
        
        .btn-icon:hover {
            background: var(--hover-bg);
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        
        .btn-icon.active {
            background: var(--accent-color);
            color: var(--btn-text);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            border: 1px solid var(--accent-color);
        }
        
        .container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 40px;
            position: relative;
            z-index: 1;
        }
        
        .calendar-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 32px;
            padding: 24px 32px;
            background: var(--card-bg);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            border-radius: 24px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            border: 1px solid var(--card-border);
            animation: slideDown 0.6s ease;
        }
        
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .calendar-nav {
            display: flex;
            gap: 24px;
            align-items: center;
        }
        
        .calendar-nav h2 {
            font-size: 24px;
            font-weight: 700;
            color: var(--text-color);
            min-width: 280px;
            text-align: center;
        }
        
        .weekly-view {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 20px;
            animation: fadeIn 0.8s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .day-column {
            background: var(--card-bg);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            border-radius: 20px;
            padding: 20px;
            min-height: 500px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            border: 1px solid var(--card-border);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .day-column::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, var(--accent-color) 0%, transparent 70%);
            opacity: 0;
            transition: opacity 0.4s;
        }
        
        .day-column:hover::before {
            opacity: 0.05;
        }
        
        .day-column:hover {
            transform: translateY(-8px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
            border: 1px solid var(--accent-color);
        }
        
        .day-column.today {
            background: var(--card-bg);
            border: 2px solid var(--accent-color);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        }
        
        .day-header {
            text-align: center;
            padding-bottom: 16px;
            border-bottom: 2px solid var(--card-border);
            margin-bottom: 20px;
        }
        
        .day-label {
            font-size: 12px;
            font-weight: 700;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }
        
        .day-number {
            font-size: 32px;
            font-weight: 800;
            color: var(--text-color);
            margin-top: 8px;
        }
        
        .day-column.today .day-number {
            color: var(--accent-color);
        }
        
        .event-card {
            background: var(--accent-color);
            border-radius: 16px;
            padding: 16px;
            margin-bottom: 12px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid transparent;
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
            color: var(--btn-text);
        }
        
        .event-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s;
        }
        
        .event-card:hover::before {
            left: 100%;
        }
        
        .event-card:hover {
            transform: translateX(4px) scale(1.02);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        
        .event-title {
            font-size: 15px;
            font-weight: 700;
            color: var(--btn-text);
            margin-bottom: 8px;
        }
        
        .event-time {
            font-size: 13px;
            color: var(--btn-text);
            margin-bottom: 6px;
            font-weight: 500;
            opacity: 0.95;
        }
        
        .event-duration {
            font-size: 12px;
            color: var(--btn-text);
            font-weight: 500;
            opacity: 0.9;
        }
        
        .event-class {
            font-size: 11px;
            color: var(--btn-text);
            margin-top: 6px;
            font-weight: 600;
            background: rgba(255, 255, 255, 0.2);
            display: inline-block;
            padding: 4px 10px;
            border-radius: 8px;
        }
        
        .event-card.break {
            background: #10b981;
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
            animation: fadeInModal 0.3s ease;
        }
        
        @keyframes fadeInModal {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .modal.active {
            display: flex;
        }
        
        .modal-content {
            background: var(--card-bg);
            backdrop-filter: blur(40px) saturate(180%);
            -webkit-backdrop-filter: blur(40px) saturate(180%);
            border-radius: 28px;
            padding: 40px;
            max-width: 600px;
            width: 90%;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
            border: 1px solid var(--card-border);
            animation: slideUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(40px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 32px;
        }
        
        .modal-header h2 {
            font-size: 28px;
            font-weight: 800;
            color: var(--text-color);
        }
        
        .close-btn {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            font-size: 24px;
            color: var(--text-color);
            cursor: pointer;
            padding: 0;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 12px;
            transition: all 0.3s;
            backdrop-filter: blur(10px);
        }
        
        .close-btn:hover {
            background: var(--hover-bg);
            transform: rotate(90deg);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        
        .form-group {
            margin-bottom: 24px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 10px;
            font-size: 14px;
            font-weight: 600;
            color: var(--text-color);
        }
        
        .form-group input,
        .form-group select,
        .form-group textarea {
            width: 100%;
            padding: 14px 18px;
            border: 2px solid var(--card-border);
            border-radius: 14px;
            font-size: 14px;
            font-family: 'Poppins', sans-serif;
            transition: all 0.3s;
            background: var(--card-bg);
            color: var(--text-color);
            backdrop-filter: blur(10px);
            font-weight: 500;
        }
        
        .form-group input::placeholder,
        .form-group textarea::placeholder {
            color: var(--text-secondary);
        }
        
        .form-group input:focus,
        .form-group select:focus,
        .form-group textarea:focus {
            outline: none;
            border-color: var(--accent-color);
            background: var(--card-bg);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            transform: translateY(-2px);
        }
        
        .form-group select {
            cursor: pointer;
        }
        
        .form-group select option {
            background: var(--card-bg);
            color: var(--text-color);
        }
        
        .form-actions {
            display: flex;
            gap: 12px;
            justify-content: flex-end;
            margin-top: 24px;
        }
        
        .checkbox-group {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        
        .checkbox-item {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            padding: 12px;
            border-radius: 12px;
            background: var(--hover-bg);
            border: 2px solid var(--card-border);
            transition: all 0.3s;
            cursor: pointer;
        }
        
        .checkbox-item:hover {
            background: var(--card-bg);
            border-color: var(--accent-color);
        }
        
        .checkbox-item input[type="checkbox"] {
            width: 20px;
            height: 20px;
            cursor: pointer;
            flex-shrink: 0;
            margin-top: 2px;
        }
        
        .checkbox-label {
            flex: 1;
        }
        
        .checkbox-label strong {
            display: block;
            margin-bottom: 4px;
            color: var(--text-color);
        }
        
        .checkbox-label span {
            font-size: 13px;
            color: var(--text-secondary);
        }
        
        .drawer {
            position: fixed;
            left: -350px;
            top: 0;
            width: 350px;
            height: 100%;
            background: var(--card-bg);
            backdrop-filter: blur(40px) saturate(180%);
            -webkit-backdrop-filter: blur(40px) saturate(180%);
            box-shadow: 4px 0 24px rgba(0, 0, 0, 0.15);
            transition: left 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            z-index: 999;
            overflow-y: auto;
            border-right: 1px solid var(--card-border);
        }
        
        .drawer.open {
            left: 0;
        }
        
        .drawer-header {
            background: var(--accent-color);
            color: var(--btn-text);
            padding: 32px 24px;
            font-size: 22px;
            font-weight: 800;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .drawer-close {
            background: rgba(255, 255, 255, 0.2);
            border: none;
            color: var(--btn-text);
            font-size: 24px;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s;
        }
        
        .drawer-close:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: rotate(90deg);
        }
        
        .drawer-content {
            padding: 24px;
        }
        
        .class-item {
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 16px;
            border-radius: 14px;
            margin-bottom: 12px;
            background: var(--hover-bg);
            border: 1px solid var(--card-border);
            transition: all 0.3s;
            backdrop-filter: blur(10px);
        }
        
        .class-item:hover {
            background: var(--card-bg);
            transform: translateX(8px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        
        .class-item:hover .class-delete {
            opacity: 1;
        }
        
        .class-color {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            border: 2px solid var(--card-border);
        }
        
        .class-item span {
            color: var(--text-color);
            font-weight: 600;
            flex: 1;
        }
        
        .class-delete {
            background: rgba(239, 68, 68, 0.8);
            border: none;
            color: white;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s;
            opacity: 0;
        }
        
        .class-delete:hover {
            background: rgba(239, 68, 68, 1);
            transform: scale(1.1);
        }
        
        /* ENHANCED COLOR PICKER */
        .color-picker-enhanced {
            margin-top: 12px;
        }
        
        .preset-colors {
            display: grid;
            grid-template-columns: repeat(8, 1fr);
            gap: 10px;
            margin-bottom: 16px;
        }
        
        .preset-color {
            width: 100%;
            aspect-ratio: 1;
            border-radius: 10px;
            border: 3px solid transparent;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            position: relative;
        }
        
        .preset-color::after {
            content: '✓';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-size: 18px;
            font-weight: bold;
            opacity: 0;
            transition: opacity 0.3s;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .preset-color.selected {
            border-color: white;
            transform: scale(1.1);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        }
        
        .preset-color.selected::after {
            opacity: 1;
        }
        
        .preset-color:hover {
            transform: scale(1.15);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
        }
        
        .gradient-color-picker {
            width: 100%;
            height: 50px;
            border-radius: 12px;
            background: linear-gradient(to right, 
                #ef4444, #f59e0b, #eab308, #84cc16, #22c55e, 
                #10b981, #14b8a6, #06b6d4, #0ea5e9, #3b82f6, 
                #6366f1, #8b5cf6, #a855f7, #d946ef, #ec4899, #f43f5e);
            cursor: pointer;
            position: relative;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            border: 2px solid var(--card-border);
            margin-bottom: 16px;
        }
        
        .gradient-color-picker:hover {
            transform: scale(1.01);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
        }
        
        .hex-input-container {
            display: flex;
            gap: 12px;
            align-items: center;
        }
        
        .color-preview {
            width: 50px;
            height: 50px;
            border-radius: 10px;
            border: 2px solid var(--card-border);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        .gradient-picker {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin-top: 12px;
        }
        
        .gradient-option {
            width: 60px;
            height: 60px;
            border-radius: 12px;
            cursor: pointer;
            border: 3px solid transparent;
            transition: all 0.3s;
        }
        
        .gradient-option:hover {
            transform: scale(1.1);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        }
        
        .gradient-option.selected {
            border-color: var(--accent-color);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
        }
        
        .gradient-option.g1 {
            background: #ffffff;
            border: 2px solid #e5e7eb;
        }
        
        .gradient-option.g2 {
            background: #000000;
        }
        
        .gradient-option.g3 {
            background: #6b7280;
        }
        
        .gradient-option.g4 {
            background: linear-gradient(135deg, #fef3f2, #fff7ed);
        }
        
        .gradient-option.g5 {
            background: linear-gradient(135deg, #f0f9ff, #dbeafe);
        }
        
        .gradient-option.g6 {
            background: linear-gradient(135deg, #f0fdf4, #d1fae5);
        }
        
        .gradient-option.g7 {
            background: linear-gradient(135deg, #faf5ff, #e9d5ff);
        }
        
        .gradient-option.g8 {
            background: linear-gradient(135deg, #fef1f7, #fbcfe8);
        }
        
        .monthly-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 12px;
            background: var(--card-bg);
            backdrop-filter: blur(20px) saturate(180%);
            padding: 32px;
            border-radius: 24px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            border: 1px solid var(--card-border);
        }
        
        .weekday-header {
            text-align: center;
            font-size: 13px;
            font-weight: 700;
            color: var(--text-secondary);
            padding: 16px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }
        
        .month-day {
            min-height: 120px;
            padding: 12px;
            border: 1px solid var(--card-border);
            border-radius: 14px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            background: var(--hover-bg);
            backdrop-filter: blur(10px);
        }
        
        .month-day:hover {
            border-color: var(--accent-color);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            transform: translateY(-4px);
            background: var(--card-bg);
        }
        
        .month-day.today {
            border-color: var(--accent-color);
            background: var(--card-bg);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            border-width: 2px;
        }
        
        .month-day-number {
            font-size: 18px;
            font-weight: 700;
            color: var(--text-color);
            margin-bottom: 10px;
        }
        
        .month-day.today .month-day-number {
            color: var(--accent-color);
            font-size: 20px;
        }
        
        .month-event {
            font-size: 11px;
            padding: 6px 8px;
            border-radius: 8px;
            margin-bottom: 6px;
            color: var(--btn-text);
            font-weight: 600;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .fab {
            position: fixed;
            bottom: 100px;
            right: 40px;
            width: 64px;
            height: 64px;
            border-radius: 50%;
            background: var(--accent-color);
            color: var(--btn-text);
            border: none;
            font-size: 28px;
            cursor: pointer;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 100;
            backdrop-filter: blur(10px);
            border: 2px solid var(--accent-color);
        }
        
        .fab::before {
            content: '';
            position: absolute;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: var(--accent-color);
            animation: pulse 2s infinite;
            opacity: 0.3;
        }
        
        @keyframes pulse {
            0%, 100% {
                transform: scale(1);
                opacity: 0.3;
            }
            50% {
                transform: scale(1.2);
                opacity: 0;
            }
        }
        
        .fab:hover {
            transform: scale(1.15) rotate(90deg);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        }
        
        .ai-fab {
            position: fixed;
            bottom: 30px;
            right: 40px;
            width: 64px;
            height: 64px;
            border-radius: 50%;
            background: linear-gradient(135deg, #8b5cf6, #6366f1);
            color: white;
            border: none;
            font-size: 32px;
            cursor: pointer;
            box-shadow: 0 4px 16px rgba(139, 92, 246, 0.3);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 100;
        }
        
        .ai-fab:hover {
            transform: scale(1.15) rotate(10deg);
            box-shadow: 0 8px 24px rgba(139, 92, 246, 0.4);
        }
        
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
            color: var(--text-color);
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
        
        .daily-view {
            background: var(--card-bg);
            backdrop-filter: blur(20px) saturate(180%);
            border-radius: 24px;
            padding: 32px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            border: 1px solid var(--card-border);
        }
        
        .no-events {
            text-align: center;
            padding: 64px;
            color: var(--text-secondary);
            font-size: 16px;
            font-weight: 500;
        }
        
        .menu-btn {
            background: transparent;
            border: none;
            font-size: 28px;
            cursor: pointer;
            padding: 10px;
            color: var(--text-color);
            transition: all 0.3s;
            border-radius: 12px;
        }
        
        .menu-btn:hover {
            background: var(--hover-bg);
            transform: scale(1.1);
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
                padding: 20px;
            }
            
            .modal-content {
                padding: 28px;
            }
            
            .app-bar {
                padding: 16px 20px;
            }
            
            .app-bar h1 {
                font-size: 22px;
            }
        }
        
        ::-webkit-scrollbar {
            width: 12px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--hover-bg);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--accent-color);
            border-radius: 10px;
            border: 2px solid var(--card-bg);
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent-hover);
        }
        
        body::after {
            content: '';
            position: fixed;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(59, 130, 246, 0.03) 0%, transparent 20%),
                radial-gradient(circle at 90% 80%, rgba(59, 130, 246, 0.03) 0%, transparent 20%),
                radial-gradient(circle at 50% 50%, rgba(59, 130, 246, 0.02) 0%, transparent 25%);
            pointer-events: none;
            z-index: 0;
            animation: float 20s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% {
                transform: translateY(0px);
            }
            50% {
                transform: translateY(-20px);
            }
        }
    </style>
</head>
<body class="gradient-1">
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
        <div class="drawer-header">
            <span>Classes & Commitments</span>
            <button class="drawer-close" onclick="toggleDrawer()">&times;</button>
        </div>
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
    <button class="ai-fab" onclick="openAITeacherModal()" title="AI Teacher">🤖</button>
    
    <!-- Name and Accommodations Modal -->
    <div class="modal active" id="nameModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Welcome to Your Planner!</h2>
            </div>
            <form id="nameForm">
                <div class="form-group">
                    <label>What's your name?</label>
                    <input type="text" id="userNameInput" required placeholder="Enter your name">
                </div>
                <div class="form-group">
                    <label>Do you have any of these accommodations? (Select all that apply)</label>
                    <div class="checkbox-group">
                        <label class="checkbox-item">
                            <input type="checkbox" name="accommodation" value="adhd">
                            <div class="checkbox-label">
                                <strong>ADHD</strong>
                                <span>Additional breaks will be scheduled to help maintain focus</span>
                            </div>
                        </label>
                        <label class="checkbox-item">
                            <input type="checkbox" name="accommodation" value="dyslexia">
                            <div class="checkbox-label">
                                <strong>Dyslexia</strong>
                                <span>Difficulty with reading, including decoding, fluency, and comprehension</span>
                            </div>
                        </label>
                        <label class="checkbox-item">
                            <input type="checkbox" name="accommodation" value="dysgraphia">
                            <div class="checkbox-label">
                                <strong>Dysgraphia</strong>
                                <span>Difficulty with writing, including handwriting, spelling, and organization</span>
                            </div>
                        </label>
                        <label class="checkbox-item">
                            <input type="checkbox" name="accommodation" value="dyscalculia">
                            <div class="checkbox-label">
                                <strong>Dyscalculia</strong>
                                <span>Difficulty with math, including number sense, calculation, and problem-solving</span>
                            </div>
                        </label>
                        <label class="checkbox-item">
                            <input type="checkbox" name="accommodation" value="auditory">
                            <div class="checkbox-label">
                                <strong>Auditory Processing Disorder</strong>
                                <span>Difficulty understanding and processing spoken language</span>
                            </div>
                        </label>
                    </div>
                </div>
                <div class="form-actions">
                    <button type="submit" class="btn btn-primary">Next: Configure Settings</button>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Initial Settings Modal -->
    <div class="modal" id="initialSettingsModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Configure Your Schedule</h2>
            </div>
            <form id="initialSettingsForm">
                <div class="form-group">
                    <label>Choose Your Theme</label>
                    <div class="gradient-picker">
                        <div class="gradient-option g1 selected" onclick="selectGradient(1)" title="White"></div>
                        <div class="gradient-option g2" onclick="selectGradient(2)" title="Black"></div>
                        <div class="gradient-option g3" onclick="selectGradient(3)" title="Grey"></div>
                        <div class="gradient-option g4" onclick="selectGradient(4)" title="Warm Pastel"></div>
                        <div class="gradient-option g5" onclick="selectGradient(5)" title="Cool Pastel"></div>
                        <div class="gradient-option g6" onclick="selectGradient(6)" title="Green Pastel"></div>
                        <div class="gradient-option g7" onclick="selectGradient(7)" title="Purple Pastel"></div>
                        <div class="gradient-option g8" onclick="selectGradient(8)" title="Pink Pastel"></div>
                    </div>
                </div>
                <div class="form-group">
                    <label>Break Length (minutes)</label>
                    <input type="number" id="initialBreakLength" value="10" min="1">
                </div>
                <div class="form-group">
                    <label>Shower Length (minutes)</label>
                    <input type="number" id="initialShowerLength" value="15" min="1">
                </div>
                <div class="form-group">
                    <label>Meal Length (minutes)</label>
                    <input type="number" id="initialMealLength" value="30" min="1">
                </div>
                <div class="form-group">
                    <label>Buffer Between Events (minutes)</label>
                    <input type="number" id="initialBuffer" value="5" min="0">
                </div>
                <div class="form-group">
                    <label>Work Chunk Length (minutes)</label>
                    <input type="number" id="initialWorkChunk" value="50" min="1">
                </div>
                <div class="form-group">
                    <label>Work Start Time</label>
                    <input type="time" id="initialWorkStart" value="16:00">
                </div>
                <div class="form-group">
                    <label>Work End Time</label>
                    <input type="time" id="initialWorkEnd" value="22:00">
                </div>
                <div class="form-actions">
                    <button type="submit" class="btn btn-primary">Get Started!</button>
                </div>
            </form>
        </div>
    </div>
    
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
                    <label>Deadline (optional)</label>
                    <input type="datetime-local" id="eventDeadline">
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
                    <label>Deadline (optional)</label>
                    <input type="datetime-local" id="editEventDeadline">
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
                    <label>Background Theme</label>
                    <div class="gradient-picker">
                        <div class="gradient-option g1 selected" onclick="selectGradient(1)" title="White"></div>
                        <div class="gradient-option g2" onclick="selectGradient(2)" title="Black"></div>
                        <div class="gradient-option g3" onclick="selectGradient(3)" title="Grey"></div>
                        <div class="gradient-option g4" onclick="selectGradient(4)" title="Warm Pastel"></div>
                        <div class="gradient-option g5" onclick="selectGradient(5)" title="Cool Pastel"></div>
                        <div class="gradient-option g6" onclick="selectGradient(6)" title="Green Pastel"></div>
                        <div class="gradient-option g7" onclick="selectGradient(7)" title="Purple Pastel"></div>
                        <div class="gradient-option g8" onclick="selectGradient(8)" title="Pink Pastel"></div>
                    </div>
                </div>
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
                    <input type="text" id="classColor" value="#3b82f6" placeholder="#3b82f6">
                </div>
                <div id="accommodationQuestionsContainer"></div>
                <div class="form-actions">
                    <button type="button" class="btn btn-secondary" onclick="closeModal('addClassModal')">Cancel</button>
                    <button type="submit" class="btn btn-primary">Add Class</button>
                </div>
            </form>
        </div>
    </div>

    <!-- AI Teacher Modal -->
    <div class="modal" id="aiTeacherModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>🤖 AI Teacher</h2>
                <button class="close-btn" onclick="closeModal('aiTeacherModal')">&times;</button>
            </div>
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
        </div>
    </div>

    <script>
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
            workEnd: '22:00',
            selectedGradient: 1
        };
        let durationHistory = {};
        let userName = '';
        let accommodations = [];
        let currentEditingEventId = null;
        let setupComplete = false;
        
        const GEMINI_API_KEY = 'AIzaSyA_AjHXMJSj7lm4XmxiITqCIZ9-kP7tsXw';
        
        document.addEventListener('DOMContentLoaded', () => {
            loadData();
            if (setupComplete) {
                document.getElementById('nameModal').classList.remove('active');
                document.getElementById('initialSettingsModal').classList.remove('active');
            }
            applyGradient(settings.selectedGradient);
            setTodayDate();
            updateView();
            updateClassDropdowns();
        });
        
        // Name and accommodations form
        document.getElementById('nameForm').addEventListener('submit', (e) => {
            e.preventDefault();
            userName = document.getElementById('userNameInput').value.trim() || 'My';
            
            const checkboxes = document.querySelectorAll('input[name="accommodation"]:checked');
            accommodations = Array.from(checkboxes).map(cb => cb.value);
            
            document.getElementById('userName').textContent = userName;
            closeModal('nameModal');
            document.getElementById('initialSettingsModal').classList.add('active');
        });
        
        // Initial settings form
        document.getElementById('initialSettingsForm').addEventListener('submit', (e) => {
            e.preventDefault();
            settings = {
                breakLength: parseInt(document.getElementById('initialBreakLength').value),
                showerLength: parseInt(document.getElementById('initialShowerLength').value),
                mealLength: parseInt(document.getElementById('initialMealLength').value),
                bufferBetweenEvents: parseInt(document.getElementById('initialBuffer').value),
                workChunkLength: parseInt(document.getElementById('initialWorkChunk').value),
                workStart: document.getElementById('initialWorkStart').value,
                workEnd: document.getElementById('initialWorkEnd').value,
                selectedGradient: settings.selectedGradient
            };
            setupComplete = true;
            saveData();
            closeModal('initialSettingsModal');
            updateView();
        });
        
        // Add event form
        document.getElementById('addEventForm').addEventListener('submit', (e) => {
            e.preventDefault();
            const classTag = document.getElementById('eventClass').value || null;
            const classInfo = classes.find(c => c.name === classTag);
            const baseDuration = parseInt(document.getElementById('eventDuration').value);
            
            let adjustedDuration = baseDuration;
            if (classInfo) {
                if (classInfo.relatesTo.includes('writing') && accommodations.includes('dysgraphia')) {
                    adjustedDuration = Math.round(baseDuration * 1.5);
                }
                if (classInfo.relatesTo.includes('math') && accommodations.includes('dyscalculia')) {
                    adjustedDuration = Math.round(baseDuration * 1.5);
                }
                if (classInfo.relatesTo.includes('auditory') && accommodations.includes('auditory')) {
                    adjustedDuration = Math.round(baseDuration * 1.5);
                }
            }
            
            const event = {
                id: Date.now(),
                title: document.getElementById('eventTitle').value,
                eventType: document.getElementById('eventType').value,
                duration: adjustedDuration,
                baseDuration: baseDuration,
                priority: parseInt(document.getElementById('eventPriority').value),
                deadline: document.getElementById('eventDeadline').value || null,
                recurrence: document.getElementById('eventRecurrence').value,
                classTag: classTag,
                eventDate: document.getElementById('eventDate').value,
                startTime: document.getElementById('eventType').value === 'fixed' ? document.getElementById('eventStartTime').value : null,
                color: getEventColor(classTag, parseInt(document.getElementById('eventPriority').value)),
                estimatedDuration: null
            };
            events.push(event);
            saveData();
            closeModal('addEventModal');
            updateView();
            document.getElementById('addEventForm').reset();
        });
        
        // Edit event form
        document.getElementById('editEventForm').addEventListener('submit', (e) => {
            e.preventDefault();
            const eventId = parseInt(document.getElementById('editEventId').value);
            const eventIndex = events.findIndex(e => e.id === eventId);
            if (eventIndex !== -1) {
                const classTag = document.getElementById('editEventClass').value || null;
                const classInfo = classes.find(c => c.name === classTag);
                const baseDuration = parseInt(document.getElementById('editEventDuration').value);
                
                let adjustedDuration = baseDuration;
                if (classInfo) {
                    if (classInfo.relatesTo.includes('writing') && accommodations.includes('dysgraphia')) {
                        adjustedDuration = Math.round(baseDuration * 1.5);
                    }
                    if (classInfo.relatesTo.includes('math') && accommodations.includes('dyscalculia')) {
                        adjustedDuration = Math.round(baseDuration * 1.5);
                    }
                    if (classInfo.relatesTo.includes('auditory') && accommodations.includes('auditory')) {
                        adjustedDuration = Math.round(baseDuration * 1.5);
                    }
                }
                
                events[eventIndex] = {
                    ...events[eventIndex],
                    title: document.getElementById('editEventTitle').value,
                    eventType: document.getElementById('editEventType').value,
                    duration: adjustedDuration,
                    baseDuration: baseDuration,
                    priority: parseInt(document.getElementById('editEventPriority').value),
                    deadline: document.getElementById('editEventDeadline').value || null,
                    recurrence: document.getElementById('editEventRecurrence').value,
                    classTag: classTag,
                    eventDate: document.getElementById('editEventDate').value,
                    startTime: document.getElementById('editEventType').value === 'fixed' ? document.getElementById('editEventStartTime').value : null,
                    color: getEventColor(classTag, parseInt(document.getElementById('editEventPriority').value))
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
                workEnd: document.getElementById('settingsWorkEnd').value,
                selectedGradient: settings.selectedGradient
            };
            saveData();
            closeModal('settingsModal');
            updateView();
        });
        
        // Add class form
        document.getElementById('addClassForm').addEventListener('submit', (e) => {
            e.preventDefault();
            
            const relatesTo = [];
            if (accommodations.includes('dysgraphia')) {
                const writingCheckbox = document.getElementById('classRelatesWriting');
                if (writingCheckbox && writingCheckbox.checked) {
                    relatesTo.push('writing');
                }
            }
            if (accommodations.includes('dyscalculia')) {
                const mathCheckbox = document.getElementById('classRelatesMath');
                if (mathCheckbox && mathCheckbox.checked) {
                    relatesTo.push('math');
                }
            }
            if (accommodations.includes('auditory')) {
                const auditoryCheckbox = document.getElementById('classRelatesAuditory');
                if (auditoryCheckbox && auditoryCheckbox.checked) {
                    relatesTo.push('auditory');
                }
            }
            
            const newClass = {
                id: Date.now(),
                name: document.getElementById('className').value,
                color: document.getElementById('classColor').value || '#3b82f6',
                relatesTo: relatesTo
            };
            classes.push(newClass);
            saveData();
            closeModal('addClassModal');
            updateClassList();
            updateClassDropdowns();
            document.getElementById('addClassForm').reset();
        });
        
        function selectGradient(num) {
            settings.selectedGradient = num;
            applyGradient(num);
            document.querySelectorAll('.gradient-option').forEach(opt => opt.classList.remove('selected'));
            document.querySelectorAll('.gradient-option.g' + num).forEach(opt => opt.classList.add('selected'));
        }
        
        function applyGradient(num) {
            document.body.className = 'gradient-' + num;
        }
        
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
            showAccommodationQuestions();
            document.getElementById('addClassModal').classList.add('active');
        }
        
        function showAccommodationQuestions() {
            const container = document.getElementById('accommodationQuestionsContainer');
            let html = '';
            
            if (accommodations.includes('dysgraphia')) {
                html += `
                    <div class="form-group">
                        <label class="checkbox-item">
                            <input type="checkbox" id="classRelatesWriting">
                            <div class="checkbox-label">
                                <strong>This class involves significant writing</strong>
                                <span>Tasks will receive 1.5x time adjustment</span>
                            </div>
                        </label>
                    </div>
                `;
            }
            
            if (accommodations.includes('dyscalculia')) {
                html += `
                    <div class="form-group">
                        <label class="checkbox-item">
                            <input type="checkbox" id="classRelatesMath">
                            <div class="checkbox-label">
                                <strong>This class involves math or number sense</strong>
                                <span>Tasks will receive 1.5x time adjustment</span>
                            </div>
                        </label>
                    </div>
                `;
            }
            
            if (accommodations.includes('auditory')) {
                html += `
                    <div class="form-group">
                        <label class="checkbox-item">
                            <input type="checkbox" id="classRelatesAuditory">
                            <div class="checkbox-label">
                                <strong>This class involves significant listening/lectures</strong>
                                <span>Tasks will receive 1.5x time adjustment</span>
                            </div>
                        </label>
                    </div>
                `;
            }
            
            container.innerHTML = html;
        }
        
        function openSettings() {
            document.getElementById('settingsBreakLength').value = settings.breakLength;
            document.getElementById('settingsShowerLength').value = settings.showerLength;
            document.getElementById('settingsMealLength').value = settings.mealLength;
            document.getElementById('settingsBuffer').value = settings.bufferBetweenEvents;
            document.getElementById('settingsWorkChunk').value = settings.workChunkLength;
            document.getElementById('settingsWorkStart').value = settings.workStart;
            document.getElementById('settingsWorkEnd').value = settings.workEnd;
            
            document.querySelectorAll('.gradient-option').forEach(opt => opt.classList.remove('selected'));
            document.querySelectorAll('.gradient-option.g' + settings.selectedGradient).forEach(opt => opt.classList.add('selected'));
            
            document.getElementById('settingsModal').classList.add('active');
        }
        
        function deleteClass(classId) {
            if (confirm('Are you sure you want to delete this class?')) {
                classes = classes.filter(c => c.id !== classId);
                saveData();
                updateClassList();
                updateClassDropdowns();
            }
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
            const today = new Date();
            const year = today.getFullYear();
            const month = String(today.getMonth() + 1).padStart(2, '0');
            const day = String(today.getDate()).padStart(2, '0');
            const dateStr = `${year}-${month}-${day}`;
            
            if (document.getElementById('eventDate')) {
                document.getElementById('eventDate').value = dateStr;
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
            const diff = d.getDate() - day;
            return new Date(d.setDate(diff));
        }
        
        function formatDate(date) {
            return date.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
        }
        
        function getMonthName(month) {
            const names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
            return names[month];
        }
        
        function getDayLabel(weekday) {
            const labels = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];
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
            const colors = ['#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe', '#dbeafe'];
            return colors[priority - 1] || '#3b82f6';
        }
        
        function updateClassList() {
            const list = document.getElementById('classList');
            list.innerHTML = classes.map(c => `
                <div class="class-item">
                    <div class="class-color" style="background: ${c.color};"></div>
                    <span>${c.name}</span>
                    <button class="class-delete" onclick="deleteClass(${c.id})">&times;</button>
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
            document.getElementById('editEventDuration').value = event.baseDuration || event.duration;
            document.getElementById('editEventPriority').value = event.priority;
            document.getElementById('editEventDeadline').value = event.deadline || '';
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
            if (event.eventType === 'fixed' && event.startTime) {
                const eventDateTime = new Date(event.eventDate + 'T' + event.startTime);
                return isSameDay(eventDateTime, day);
            }
            
            const eventDate = new Date(event.eventDate);
            if (isSameDay(eventDate, day)) return true;
            
            if (event.recurrence === 'none') return false;
            if (day < eventDate) return false;
            
            if (event.recurrence === 'daily') return true;
            if (event.recurrence === 'weekly') return day.getDay() === eventDate.getDay();
            if (event.recurrence === 'monthly') return day.getDate() === eventDate.getDate();
            
            return false;
        }
        
        function autoPrioritize(tasks, day) {
            const now = new Date();
            tasks.forEach(task => {
                if (task.deadline) {
                    const deadline = new Date(task.deadline);
                    const minutesLeft = (deadline - day) / (1000 * 60);
                    const estimate = task.estimatedDuration || task.duration;
                    
                    let suggested = task.priority;
                    
                    if (minutesLeft <= 0) {
                        suggested = Math.max(1, suggested - 2);
                    } else if (minutesLeft <= 24 * 60) {
                        suggested = Math.max(1, suggested - 1);
                    } else if (minutesLeft <= 3 * 24 * 60) {
                        suggested = Math.max(1, suggested - 0);
                    }
                    
                    if (estimate >= 120 && minutesLeft <= 3 * 24 * 60) {
                        suggested = Math.max(1, suggested - 1);
                    }
                    
                    task.priority = suggested;
                }
            });
            return tasks;
        }
        
        function generateScheduleForDay(day) {
            const schedule = [];
            
            const fixedEvents = events.filter(e => e.eventType === 'fixed' && occursOnDay(e, day));
            fixedEvents.sort((a, b) => {
                const aTime = new Date(a.eventDate + 'T' + a.startTime);
                const bTime = new Date(b.eventDate + 'T' + b.startTime);
                return aTime - bTime;
            });
            
            let flexibleEvents = events.filter(e => e.eventType === 'flexible' && occursOnDay(e, day));
            
            if (flexibleEvents.length === 0) {
                fixedEvents.forEach(fe => {
                    const startTime = new Date(fe.eventDate + 'T' + fe.startTime);
                    const endTime = new Date(startTime.getTime() + fe.duration * 60000);
                    schedule.push({...fe, startTime, endTime});
                });
                return schedule;
            }
            
            flexibleEvents = autoPrioritize(flexibleEvents.map(e => ({...e})), day);
            flexibleEvents.sort((a, b) => a.priority - b.priority);
            
            const [workStartHour, workStartMin] = settings.workStart.split(':').map(Number);
            const [workEndHour, workEndMin] = settings.workEnd.split(':').map(Number);
            
            let cursor = new Date(day);
            cursor.setHours(workStartHour, workStartMin, 0, 0);
            
            const endTime = new Date(day);
            endTime.setHours(workEndHour, workEndMin, 0, 0);
            
            fixedEvents.forEach(fe => {
                const startTime = new Date(fe.eventDate + 'T' + fe.startTime);
                const eventEndTime = new Date(startTime.getTime() + fe.duration * 60000);
                schedule.push({...fe, startTime, endTime: eventEndTime});
            });
            
            flexibleEvents.forEach(flex => {
                if (cursor >= endTime) return;
                
                let slotStart = new Date(cursor);
                
                let hasConflict = true;
                while (hasConflict && slotStart < endTime) {
                    hasConflict = false;
                    const slotEnd = new Date(slotStart.getTime() + flex.duration * 60000);
                    
                    for (let fixed of fixedEvents) {
                        const fixedStart = new Date(fixed.eventDate + 'T' + fixed.startTime);
                        const fixedEnd = new Date(fixedStart.getTime() + fixed.duration * 60000);
                        
                        if ((slotStart >= fixedStart && slotStart < fixedEnd) ||
                            (slotEnd > fixedStart && slotEnd <= fixedEnd) ||
                            (slotStart <= fixedStart && slotEnd >= fixedEnd)) {
                            hasConflict = true;
                            slotStart = new Date(fixedEnd.getTime() + settings.bufferBetweenEvents * 60000);
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
        
        // AI TEACHER FUNCTIONS
        function openAITeacherModal() {
            document.getElementById('aiTeacherModal').classList.add('active');
            scrollAIChatToBottom();
        }
        
        async function sendAIMessage() {
            const input = document.getElementById('aiInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            addAIMessage(message, 'user');
            input.value = '';
            
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
        
        function saveData() {
            const data = {
                userName,
                accommodations,
                events,
                classes,
                settings,
                durationHistory,
                setupComplete
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
