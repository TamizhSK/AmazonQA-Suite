"""
Enhanced HTML Report Generation
Provides enhanced reporting with screenshots, performance metrics, and structured results
Developer-focused minimal dark theme
"""

import os
import time
import json
from datetime import datetime
from pathlib import Path


class EnhancedReporter:
    """Enhanced test reporter with screenshots and metrics"""
    
    def __init__(self):
        self.test_results = []
        self.performance_metrics = {}
        self.screenshots = []
        self.start_time = None
        self.end_time = None
        
    def start_session(self):
        """Start reporting session"""
        self.start_time = datetime.now()
        
    def end_session(self):
        """End reporting session"""
        self.end_time = datetime.now()
        
    def add_test_result(self, test_name, status, duration=None, error_message=None, screenshot_path=None):
        """Add test result to report"""
        result = {
            "test_name": test_name,
            "status": status,  # passed, failed, skipped
            "duration": duration or 0,
            "timestamp": datetime.now().isoformat(),
            "error_message": error_message,
            "screenshot_path": screenshot_path
        }
        self.test_results.append(result)
        
    def add_performance_metric(self, metric_name, value, unit="seconds"):
        """Add performance metric"""
        self.performance_metrics[metric_name] = {
            "value": value,
            "unit": unit,
            "timestamp": datetime.now().isoformat()
        }
        
    def add_screenshot(self, path, description=""):
        """Add screenshot to report"""
        if os.path.exists(path):
            self.screenshots.append({
                "path": path,
                "description": description,
                "timestamp": datetime.now().isoformat()
            })
            
    def generate_enhanced_html_report(self, output_path="reports/enhanced_report.html"):
        """Generate enhanced HTML report with developer-focused dark theme"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Calculate summary statistics
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r["status"] == "passed")
        failed_tests = sum(1 for r in self.test_results if r["status"] == "failed")
        skipped_tests = sum(1 for r in self.test_results if r["status"] == "skipped")
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        total_duration = sum(r["duration"] for r in self.test_results)
        
        session_duration = 0
        if self.start_time and self.end_time:
            session_duration = (self.end_time - self.start_time).total_seconds()
        
        # Generate HTML content with developer theme
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Suite Report - Enhanced</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Fira Code', 'Droid Sans Mono', 'Source Code Pro', monospace;
            font-size: 13px;
            line-height: 1.4;
            color: #e6e6e6;
            background-color: #0d1117;
            margin: 0;
            padding: 0;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background-color: #0d1117;
        }}
        
        .header {{
            background-color: #161b22;
            border-bottom: 1px solid #30363d;
            padding: 24px;
            text-align: left;
        }}
        
        .header h1 {{
            color: #f0f6fc;
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 8px;
        }}
        
        .header .subtitle {{
            color: #8b949e;
            font-size: 14px;
            margin-bottom: 16px;
        }}
        
        .progress-container {{
            margin-bottom: 12px;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 4px;
            background-color: #21262d;
            border-radius: 2px;
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            background-color: #3fb950;
            width: {success_rate}%;
            transition: width 0.3s ease;
        }}
        
        .success-rate {{
            color: #c9d1d9;
            font-size: 13px;
            font-weight: 500;
            margin-top: 8px;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px;
            padding: 24px;
            background-color: #0d1117;
            border-bottom: 1px solid #21262d;
        }}
        
        .summary-card {{
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 16px;
            text-align: center;
            transition: all 0.2s ease;
        }}
        
        .summary-card:hover {{
            border-color: #58a6ff;
            background-color: #1c2128;
        }}
        
        .summary-card .number {{
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 4px;
            font-family: 'SF Mono', monospace;
        }}
        
        .summary-card .label {{
            color: #8b949e;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 500;
        }}
        
        .passed {{ color: #3fb950; }}
        .failed {{ color: #f85149; }}
        .skipped {{ color: #d29922; }}
        .total {{ color: #58a6ff; }}
        .duration {{ color: #a5a5a5; }}
        
        .section {{
            padding: 24px;
            border-bottom: 1px solid #21262d;
        }}
        
        .section h2 {{
            color: #f0f6fc;
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 1px solid #30363d;
        }}
        
        .test-results {{
            background-color: #0d1117;
        }}
        
        .test-item {{
            display: flex;
            align-items: center;
            padding: 12px 16px;
            margin-bottom: 8px;
            border-radius: 4px;
            border: 1px solid #30363d;
            background-color: #161b22;
            transition: all 0.2s ease;
            cursor: pointer;
        }}
        
        .test-item:hover {{
            border-color: #58a6ff;
            background-color: #1c2128;
        }}
        
        .test-item.passed {{
            border-left: 3px solid #3fb950;
        }}
        
        .test-item.failed {{
            border-left: 3px solid #f85149;
        }}
        
        .test-item.skipped {{
            border-left: 3px solid #d29922;
        }}
        
        .test-name {{
            flex-grow: 1;
            color: #c9d1d9;
            font-size: 13px;
            font-weight: 500;
        }}
        
        .test-duration {{
            color: #8b949e;
            font-size: 11px;
            margin: 0 12px;
            font-family: 'SF Mono', monospace;
        }}
        
        .test-status {{
            padding: 4px 8px;
            border-radius: 3px;
            font-size: 10px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .status-passed {{
            background-color: #238636;
            color: #ffffff;
        }}
        
        .status-failed {{
            background-color: #da3633;
            color: #ffffff;
        }}
        
        .status-skipped {{
            background-color: #bf8700;
            color: #ffffff;
        }}
        
        .error-message {{
            background-color: #0d1117;
            border: 1px solid #f85149;
            border-radius: 4px;
            padding: 12px;
            margin-top: 8px;
            font-family: 'SF Mono', monospace;
            font-size: 11px;
            color: #f85149;
            white-space: pre-wrap;
            display: none;
        }}
        
        .screenshot-link {{
            color: #58a6ff;
            text-decoration: none;
            font-size: 11px;
            margin-left: 8px;
        }}
        
        .screenshot-link:hover {{
            color: #79c0ff;
            text-decoration: underline;
        }}
        
        .performance-metrics {{
            background-color: #0d1117;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
        }}
        
        .metric-card {{
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 16px;
            border-left: 3px solid #58a6ff;
        }}
        
        .metric-name {{
            color: #f0f6fc;
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 4px;
        }}
        
        .metric-value {{
            color: #58a6ff;
            font-size: 18px;
            font-weight: 600;
            font-family: 'SF Mono', monospace;
        }}
        
        .screenshots {{
            background-color: #0d1117;
        }}
        
        .screenshot-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 16px;
        }}
        
        .screenshot-item {{
            border: 1px solid #30363d;
            border-radius: 6px;
            overflow: hidden;
            background-color: #161b22;
            transition: all 0.2s ease;
        }}
        
        .screenshot-item:hover {{
            border-color: #58a6ff;
        }}
        
        .screenshot-item img {{
            width: 100%;
            height: 160px;
            object-fit: cover;
            cursor: pointer;
        }}
        
        .screenshot-description {{
            padding: 12px;
            background-color: #161b22;
        }}
        
        .screenshot-description strong {{
            color: #f0f6fc;
            font-size: 12px;
            display: block;
            margin-bottom: 4px;
        }}
        
        .screenshot-description small {{
            color: #8b949e;
            font-size: 10px;
        }}
        
        .footer {{
            text-align: center;
            padding: 24px;
            background-color: #161b22;
            border-top: 1px solid #30363d;
            color: #8b949e;
            font-size: 11px;
        }}
        
        .footer p {{
            margin: 4px 0;
        }}
        
        .expandable {{
            position: relative;
        }}
        
        .expandable:after {{
            content: "▼";
            position: absolute;
            right: 12px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 10px;
            color: #8b949e;
            transition: transform 0.2s ease;
        }}
        
        .expandable.expanded:after {{
            transform: translateY(-50%) rotate(180deg);
        }}
        
        /* Scrollbar Styling */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: #161b22;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: #30363d;
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: #484f58;
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .summary {{
                grid-template-columns: repeat(2, 1fr);
                gap: 12px;
                padding: 16px;
            }}
            
            .section {{
                padding: 16px;
            }}
            
            .test-item {{
                flex-direction: column;
                align-items: flex-start;
                gap: 8px;
            }}
            
            .test-duration, .test-status {{
                margin: 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>Test Suite Report</h1>
            <div class="subtitle">Generated on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}</div>
            <div class="progress-container">
                <div class="progress-bar">
                    <div class="progress-fill"></div>
                </div>
                <div class="success-rate">Success Rate: {success_rate:.1f}%</div>
            </div>
        </div>
        
        <!-- Summary -->
        <div class="summary">
            <div class="summary-card">
                <div class="number total">{total_tests}</div>
                <div class="label">Total Tests</div>
            </div>
            <div class="summary-card">
                <div class="number passed">{passed_tests}</div>
                <div class="label">Passed</div>
            </div>
            <div class="summary-card">
                <div class="number failed">{failed_tests}</div>
                <div class="label">Failed</div>
            </div>
            <div class="summary-card">
                <div class="number skipped">{skipped_tests}</div>
                <div class="label">Skipped</div>
            </div>
            <div class="summary-card">
                <div class="number duration">{total_duration:.1f}s</div>
                <div class="label">Total Duration</div>
            </div>
            <div class="summary-card">
                <div class="number duration">{session_duration:.1f}s</div>
                <div class="label">Session Duration</div>
            </div>
        </div>
        
        <!-- Test Results -->
        <div class="section test-results">
            <h2>Test Results</h2>
            <div class="test-list">
        """
        
        # Add test results
        for result in self.test_results:
            error_html = ""
            if result["error_message"]:
                error_html = f'<div class="error-message" id="error-{hash(result["test_name"])}">{result["error_message"]}</div>'
            
            screenshot_html = ""
            if result["screenshot_path"] and os.path.exists(result["screenshot_path"]):
                screenshot_html = f'<a href="{result["screenshot_path"]}" target="_blank" class="screenshot-link">📷 Screenshot</a>'
            
            expandable_class = "expandable" if result["error_message"] else ""
            
            html_content += f"""
                <div class="test-item {result['status']} {expandable_class}" onclick="toggleError('{hash(result['test_name'])}')">
                    <div class="test-name">
                        {result['test_name']}
                        {screenshot_html}
                    </div>
                    <div class="test-duration">{result['duration']:.2f}s</div>
                    <div class="test-status status-{result['status']}">{result['status']}</div>
                    {error_html}
                </div>
            """
        
        # Add performance metrics
        if self.performance_metrics:
            html_content += """
            </div>
        </div>
        
        <!-- Performance Metrics -->
        <div class="section performance-metrics">
            <h2>Performance Metrics</h2>
            <div class="metrics-grid">
            """
            
            for metric_name, metric_data in self.performance_metrics.items():
                html_content += f"""
                <div class="metric-card">
                    <div class="metric-name">{metric_name.replace('_', ' ').title()}</div>
                    <div class="metric-value">{metric_data['value']:.2f} {metric_data['unit']}</div>
                </div>
                """
            
            html_content += "</div>"
        
        # Add screenshots
        if self.screenshots:
            html_content += """
        </div>
        
        <!-- Screenshots -->
        <div class="section screenshots">
            <h2>Screenshots</h2>
            <div class="screenshot-grid">
            """
            
            for screenshot in self.screenshots:
                if os.path.exists(screenshot["path"]):
                    html_content += f"""
                    <div class="screenshot-item">
                        <img src="{screenshot['path']}" alt="Screenshot" onclick="window.open('{screenshot['path']}', '_blank')">
                        <div class="screenshot-description">
                            <strong>{screenshot['description'] or 'Test Screenshot'}</strong>
                            <small>{screenshot['timestamp']}</small>
                        </div>
                    </div>
                    """
            
            html_content += "</div>"
        
        html_content += """
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p>Enhanced Test Report Generator</p>
            <p>Python 3.8+ | Selenium 4.x | Developer Edition</p>
        </div>
    </div>
    
    <script>
        function toggleError(testId) {
            const errorElement = document.getElementById('error-' + testId);
            const testItem = errorElement?.parentElement;
            
            if (errorElement) {
                const isVisible = errorElement.style.display === 'block';
                errorElement.style.display = isVisible ? 'none' : 'block';
                
                if (testItem) {
                    testItem.classList.toggle('expanded', !isVisible);
                }
            }
        }
        
        // Initialize all error messages as hidden
        document.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('.error-message').forEach(el => {
                el.style.display = 'none';
            });
        });
        
        // Auto-refresh timestamp
        let refreshInterval = setInterval(() => {
            if (document.hidden) return;
            const now = new Date();
            const timestamp = now.toLocaleString();
            document.querySelector('.subtitle').textContent = `Last updated: ${timestamp}`;
        }, 30000);
        
        // Stop refresh when page is hidden
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                clearInterval(refreshInterval);
            } else {
                refreshInterval = setInterval(() => {
                    if (document.hidden) return;
                    const now = new Date();
                    const timestamp = now.toLocaleString();
                    document.querySelector('.subtitle').textContent = `Last updated: ${timestamp}`;
                }, 30000);
            }
        });
        
        // Keyboard navigation
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                document.querySelectorAll('.error-message').forEach(el => {
                    el.style.display = 'none';
                });
                document.querySelectorAll('.expandable').forEach(el => {
                    el.classList.remove('expanded');
                });
            }
        });
    </script>
</body>
</html>
        """
        
        # Write HTML file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
        
    def generate_json_report(self, output_path="reports/test_results.json"):
        """Generate JSON report for API consumption"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        report_data = {
            "session": {
                "start_time": self.start_time.isoformat() if self.start_time else None,
                "end_time": self.end_time.isoformat() if self.end_time else None,
                "duration": (self.end_time - self.start_time).total_seconds() if self.start_time and self.end_time else 0
            },
            "summary": {
                "total_tests": len(self.test_results),
                "passed": sum(1 for r in self.test_results if r["status"] == "passed"),
                "failed": sum(1 for r in self.test_results if r["status"] == "failed"),
                "skipped": sum(1 for r in self.test_results if r["status"] == "skipped"),
                "success_rate": (sum(1 for r in self.test_results if r["status"] == "passed") / len(self.test_results) * 100) if self.test_results else 0
            },
            "test_results": self.test_results,
            "performance_metrics": self.performance_metrics,
            "screenshots": self.screenshots
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        return output_path


# Global reporter instance
enhanced_reporter = EnhancedReporter()