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
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            color: #ffffff;
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
        }
        
        body.gradient-1 {
            --gradient-bg: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
        }
        
        body.gradient-2 {
            --gradient-bg: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 25%, #c44569 50%, #556270 75%, #4ecdc4 100%);
        }
        
        body.gradient-3 {
            --gradient-bg: linear-gradient(135deg, #11998e 0%, #38ef7d 25%, #fee140 50%, #fa709a 75%, #fbc2eb 100%);
        }
        
        body.gradient-4 {
            --gradient-bg: linear-gradient(135deg, #6a11cb 0%, #2575fc 25%, #00d2ff 50%, #3a7bd5 75%, #00d2ff 100%);
        }
        
        body.gradient-5 {
            --gradient-bg: linear-gradient(135deg, #f093fb 0%, #f5576c 25%, #4facfe 50%, #00f2fe 75%, #43e97b 100%);
        }
        
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.3), transparent 50%),
                        radial-gradient(circle at 80% 80%, rgba(252, 70, 107, 0.3), transparent 50%),
                        radial-gradient(circle at 40% 20%, rgba(99, 179, 237, 0.3), transparent 50%);
            pointer-events: none;
            z-index: 0;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .app-bar {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            border-bottom: 1px solid rgba(255, 255, 255, 0.18);
            padding: 20px 40px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
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
            color: #ffffff;
            letter-spacing: -0.5px;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
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
            background: linear-gradient(135deg, rgba(138, 43, 226, 0.8), rgba(199, 21, 133, 0.8));
            color: white;
            box-shadow: 0 8px 24px rgba(138, 43, 226, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 32px rgba(138, 43, 226, 0.6);
        }
        
        .btn-secondary {
            background: rgba(255, 255, 255, 0.12);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.18);
            backdrop-filter: blur(10px);
        }
        
        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(255, 255, 255, 0.2);
        }
        
        .btn-icon {
            background: rgba(255, 255, 255, 0.1);
            padding: 10px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            min-width: 44px;
            height: 44px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .btn-icon:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: scale(1.05);
            box-shadow: 0 8px 24px rgba(255, 255, 255, 0.2);
        }
        
        .btn-icon.active {
            background: linear-gradient(135deg, rgba(138, 43, 226, 0.9), rgba(199, 21, 133, 0.9));
            color: white;
            box-shadow: 0 8px 24px rgba(138, 43, 226, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.3);
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
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            border-radius: 24px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.18);
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
            color: #ffffff;
            min-width: 280px;
            text-align: center;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
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
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            border-radius: 20px;
            padding: 20px;
            min-height: 500px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.18);
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
            background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
            opacity: 0;
            transition: opacity 0.4s;
        }
        
        .day-column:hover::before {
            opacity: 1;
        }
        
        .day-column:hover {
            transform: translateY(-8px);
            box-shadow: 0 16px 48px 0 rgba(31, 38, 135, 0.25);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        
        .day-column.today {
            background: rgba(138, 43, 226, 0.15);
            border: 2px solid rgba(138, 43, 226, 0.6);
            box-shadow: 0 8px 32px 0 rgba(138, 43, 226, 0.4);
        }
        
        .day-header {
            text-align: center;
            padding-bottom: 16px;
            border-bottom: 2px solid rgba(255, 255, 255, 0.2);
            margin-bottom: 20px;
        }
        
        .day-label {
            font-size: 12px;
            font-weight: 700;
            color: rgba(255, 255, 255, 0.8);
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }
        
        .day-number {
            font-size: 32px;
            font-weight: 800;
            color: #ffffff;
            margin-top: 8px;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        }
        
        .day-column.today .day-number {
            background: linear-gradient(135deg, #a78bfa, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .event-card {
            background: linear-gradient(135deg, rgba(138, 43, 226, 0.9), rgba(199, 21, 133, 0.9));
            border-radius: 16px;
            padding: 16px;
            margin-bottom: 12px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }
        
        .event-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transition: left 0.5s;
        }
        
        .event-card:hover::before {
            left: 100%;
        }
        
        .event-card:hover {
            transform: translateX(4px) scale(1.02);
            box-shadow: 0 12px 40px rgba(138, 43, 226, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.4);
        }
        
        .event-title {
            font-size: 15px;
            font-weight: 700;
            color: white;
            margin-bottom: 8px;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }
        
        .event-time {
            font-size: 13px;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 6px;
            font-weight: 500;
        }
        
        .event-duration {
            font-size: 12px;
            color: rgba(255, 255, 255, 0.75);
            font-weight: 500;
        }
        
        .event-class {
            font-size: 11px;
            color: rgba(255, 255, 255, 0.95);
            margin-top: 6px;
            font-weight: 600;
            background: rgba(255, 255, 255, 0.15);
            display: inline-block;
            padding: 4px 10px;
            border-radius: 8px;
        }
        
        .event-card.break {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.9), rgba(5, 150, 105, 0.9));
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
            background: rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(40px) saturate(180%);
            -webkit-backdrop-filter: blur(40px) saturate(180%);
            border-radius: 28px;
            padding: 40px;
            max-width: 600px;
            width: 90%;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 24px 60px rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.2);
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
            color: #ffffff;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }
        
        .close-btn {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            font-size: 24px;
            color: #ffffff;
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
            background: rgba(255, 255, 255, 0.2);
            transform: rotate(90deg);
            box-shadow: 0 8px 24px rgba(255, 255, 255, 0.2);
        }
        
        .form-group {
            margin-bottom: 24px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 10px;
            font-size: 14px;
            font-weight: 600;
            color: #ffffff;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }
        
        .form-group input,
        .form-group select,
        .form-group textarea {
            width: 100%;
            padding: 14px 18px;
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 14px;
            font-size: 14px;
            font-family: 'Poppins', sans-serif;
            transition: all 0.3s;
            background: rgba(255, 255, 255, 0.08);
            color: #ffffff;
            backdrop-filter: blur(10px);
            font-weight: 500;
        }
        
        .form-group input::placeholder,
        .form-group textarea::placeholder {
            color: rgba(255, 255, 255, 0.5);
        }
        
        .form-group input:focus,
        .form-group select:focus,
        .form-group textarea:focus {
            outline: none;
            border-color: rgba(138, 43, 226, 0.8);
            background: rgba(255, 255, 255, 0.12);
            box-shadow: 0 8px 24px rgba(138, 43, 226, 0.3);
            transform: translateY(-2px);
        }
        
        .form-group select {
            cursor: pointer;
        }
        
        .form-group select option {
            background: rgba(30, 30, 60, 0.95);
            color: #ffffff;
        }
        
        .form-actions {
            display: flex;
            gap: 12px;
            justify-content: flex-end;
            margin-top: 24px;
        }
        
        .drawer {
            position: fixed;
            left: -350px;
            top: 0;
            width: 350px;
            height: 100%;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(40px) saturate(180%);
            -webkit-backdrop-filter: blur(40px) saturate(180%);
            box-shadow: 4px 0 24px rgba(0, 0, 0, 0.3);
            transition: left 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            z-index: 999;
            overflow-y: auto;
            border-right: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .drawer.open {
            left: 0;
        }
        
        .drawer-header {
            background: linear-gradient(135deg, rgba(138, 43, 226, 0.9), rgba(199, 21, 133, 0.9));
            color: white;
            padding: 32px 24px;
            font-size: 22px;
            font-weight: 800;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .drawer-close {
            background: rgba(255, 255, 255, 0.2);
            border: none;
            color: white;
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
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            transition: all 0.3s;
            backdrop-filter: blur(10px);
        }
        
        .class-item:hover {
            background: rgba(255, 255, 255, 0.15);
            transform: translateX(8px);
            box-shadow: 0 8px 24px rgba(255, 255, 255, 0.15);
        }
        
        .class-item:hover .class-delete {
            opacity: 1;
        }
        
        .class-color {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            border: 2px solid rgba(255, 255, 255, 0.3);
        }
        
        .class-item span {
            color: #ffffff;
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
            border-color: rgba(255, 255, 255, 0.8);
            box-shadow: 0 8px 24px rgba(255, 255, 255, 0.4);
        }
        
        .gradient-option.g1 {
            background: linear-gradient(135deg, #667eea, #764ba2);
        }
        
        .gradient-option.g2 {
            background: linear-gradient(135deg, #ff6b6b, #c44569);
        }
        
        .gradient-option.g3 {
            background: linear-gradient(135deg, #11998e, #38ef7d);
        }
        
        .gradient-option.g4 {
            background: linear-gradient(135deg, #6a11cb, #2575fc);
        }
        
        .gradient-option.g5 {
            background: linear-gradient(135deg, #f093fb, #f5576c);
        }
        
        .monthly-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 12px;
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(20px) saturate(180%);
            padding: 32px;
            border-radius: 24px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }
        
        .weekday-header {
            text-align: center;
            font-size: 13px;
            font-weight: 700;
            color: rgba(255, 255, 255, 0.8);
            padding: 16px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }
        
        .month-day {
            min-height: 120px;
            padding: 12px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 14px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
        }
        
        .month-day:hover {
            border-color: rgba(138, 43, 226, 0.6);
            box-shadow: 0 8px 24px rgba(138, 43, 226, 0.3);
            transform: translateY(-4px);
            background: rgba(255, 255, 255, 0.1);
        }
        
        .month-day.today {
            border-color: rgba(138, 43, 226, 0.8);
            background: rgba(138, 43, 226, 0.15);
            box-shadow: 0 8px 24px rgba(138, 43, 226, 0.4);
        }
        
        .month-day-number {
            font-size: 18px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 10px;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }
        
        .month-day.today .month-day-number {
            background: linear-gradient(135deg, #a78bfa, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 20px;
        }
        
        .month-event {
            font-size: 11px;
            padding: 6px 8px;
            border-radius: 8px;
            margin-bottom: 6px;
            color: white;
            font-weight: 600;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }
        
        .fab {
            position: fixed;
            bottom: 40px;
            right: 40px;
            width: 64px;
            height: 64px;
            border-radius: 50%;
            background: linear-gradient(135deg, rgba(138, 43, 226, 0.95), rgba(199, 21, 133, 0.95));
            color: white;
            border: none;
            font-size: 28px;
            cursor: pointer;
            box-shadow: 0 8px 32px rgba(138, 43, 226, 0.5);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 100;
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255, 255, 255, 0.3);
        }
        
        .fab::before {
            content: '';
            position: absolute;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: linear-gradient(135deg, rgba(138, 43, 226, 0.5), rgba(199, 21, 133, 0.5));
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% {
                transform: scale(1);
                opacity: 1;
            }
            50% {
                transform: scale(1.2);
                opacity: 0;
            }
        }
        
        .fab:hover {
            transform: scale(1.15) rotate(90deg);
            box-shadow: 0 12px 48px rgba(138, 43, 226, 0.7);
        }
        
        .daily-view {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(20px) saturate(180%);
            border-radius: 24px;
            padding: 32px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }
        
        .no-events {
            text-align: center;
            padding: 64px;
            color: rgba(255, 255, 255, 0.7);
            font-size: 16px;
            font-weight: 500;
        }
        
        .menu-btn {
            background: transparent;
            border: none;
            font-size: 28px;
            cursor: pointer;
            padding: 10px;
            color: #ffffff;
            transition: all 0.3s;
            border-radius: 12px;
        }
        
        .menu-btn:hover {
            background: rgba(255, 255, 255, 0.1);
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
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, rgba(138, 43, 226, 0.6), rgba(199, 21, 133, 0.6));
            border-radius: 10px;
            border: 2px solid rgba(255, 255, 255, 0.1);
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, rgba(138, 43, 226, 0.8), rgba(199, 21, 133, 0.8));
        }
        
        body::after {
            content: '';
            position: fixed;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(255, 255, 255, 0.05) 0%, transparent 20%),
                radial-gradient(circle at 90% 80%, rgba(255, 255, 255, 0.05) 0%, transparent 20%),
                radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.03) 0%, transparent 25%);
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
    
    <div class="modal" id="settingsModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Settings</h2>
                <button class="close-btn" onclick="closeModal('settingsModal')">&times;</button>
            </div>
            <form id="settingsForm">
                <div class="form-group">
                    <label>Background Gradient</label>
                    <div class="gradient-picker">
                        <div class="gradient-option g1 selected" onclick="selectGradient(1)"></div>
                        <div class="gradient-option g2" onclick="selectGradient(2)"></div>
                        <div class="gradient-option g3" onclick="selectGradient(3)"></div>
                        <div class="gradient-option g4" onclick="selectGradient(4)"></div>
                        <div class="gradient-option g5" onclick="selectGradient(5)"></div>
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
                    <input type="text" id="classColor" value="#8a2be2" placeholder="#8a2be2">
                </div>
                <div class="form-actions">
                    <button type="button" class="btn btn-secondary" onclick="closeModal('addClassModal')">Cancel</button>
                    <button type="submit" class="btn btn-primary">Add Class</button>
                </div>
            </form>
        </div>
    </div>
    
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
                <div class="form-group">
                    <label>Do you have any accommodations? (e.g., extra time, note-taking)</label>
                    <textarea id="accommodationsInput" rows="3" placeholder="Optional: Enter any accommodations you need..."></textarea>
                </div>
                <div class="form-actions">
                    <button type="submit" class="btn btn-primary">Get Started</button>
                </div>
            </form>
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
        let accommodations = '';
        let currentEditingEventId = null;
        
        document.addEventListener('DOMContentLoaded', () => {
            loadData();
            if (userName) {
                document.getElementById('nameModal').classList.remove('active');
            }
            applyGradient(settings.selectedGradient);
            setTodayDate();
            updateView();
            updateClassDropdowns();
        });
        
        document.getElementById('nameForm').addEventListener('submit', (e) => {
            e.preventDefault();
            userName = document.getElementById('userNameInput').value.trim() || 'My';
            accommodations = document.getElementById('accommodationsInput').value.trim();
            document.getElementById('userName').textContent = userName;
            closeModal('nameModal');
            saveData();
        });
        
        document.getElementById('addEventForm').addEventListener('submit', (e) => {
            e.preventDefault();
            const event = {
                id: Date.now(),
                title: document.getElementById('eventTitle').value,
                eventType: document.getElementById('eventType').value,
                duration: parseInt(document.getElementById('eventDuration').value),
                priority: parseInt(document.getElementById('eventPriority').value),
                deadline: document.getElementById('eventDeadline').value || null,
                recurrence: document.getElementById('eventRecurrence').value,
                classTag: document.getElementById('eventClass').value || null,
                eventDate: document.getElementById('eventDate').value,
                startTime: document.getElementById('eventType').value === 'fixed' ? document.getElementById('eventStartTime').value : null,
                color: getEventColor(document.getElementById('eventClass').value, parseInt(document.getElementById('eventPriority').value)),
                estimatedDuration: null
            };
            events.push(event);
            saveData();
            closeModal('addEventModal');
            updateView();
            document.getElementById('addEventForm').reset();
        });
        
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
                    deadline: document.getElementById('editEventDeadline').value || null,
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
        
        document.getElementById('addClassForm').addEventListener('submit', (e) => {
            e.preventDefault();
            const newClass = {
                id: Date.now(),
                name: document.getElementById('className').value,
                color: document.getElementById('classColor').value || '#8a2be2'
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
            document.querySelector('.gradient-option.g' + num).classList.add('selected');
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
            
            document.querySelectorAll('.gradient-option').forEach(opt => opt.classList.remove('selected'));
            document.querySelector('.gradient-option.g' + settings.selectedGradient).classList.add('selected');
            
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
            const colors = ['#8b5cf6', '#a78bfa', '#c4b5fd', '#ddd6fe', '#ede9fe'];
            return colors[priority - 1] || '#8a2be2';
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
            document.getElementById('editEventDuration').value = event.duration;
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
                                color: 'linear-gradient(135deg, rgba(16, 185, 129, 0.9), rgba(5, 150, 105, 0.9))'
                            });
                        }
                        
                        cursor = new Date(breakEnd.getTime() + settings.bufferBetweenEvents * 60000);
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
                        ${extraEvents > 0 ? `<div style="font-size: 10px; color: rgba(255,255,255,0.7);">+${extraEvents} more</div>` : ''}
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
                accommodations,
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
                accommodations = parsed.accommodations || '';
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
</html>'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)
