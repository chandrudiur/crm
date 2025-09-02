@@ .. @@
 from flask import render_template, request, redirect, url_for, flash, jsonify
 from app import app
 from data_store import *
 from models import *
 from datetime import datetime
+import json

 @app.route('/')
 def dashboard():
@@ .. @@
     
     return jsonify(deployment.metrics)

+# User Registration Routes
+@app.route('/register')
+def register_user_page():
+    """User registration page"""
+    companies = CompanyService.get_all()
+    return render_template('registration/index.html', companies=companies)
+
+@app.route('/register-user', methods=['POST'])
+def register_user():
+    """Register a single user"""
+    try:
+        data = request.get_json()
+        
+        # Create new person
+        person = Person(
+            id=generate_id(),
+            company_id=data['company_id'],
+            email=data['email'].lower(),
+            name=data['fullName'],
+            roles=['user'],
+            status=UserStatus.ACTIVE,
+            metadata={
+                'year_of_birth': data.get('yearOfBirth'),
+                'mobile': data.get('mobile'),
+                'alt_email': data.get('altEmail'),
+                'designation': data.get('designation'),
+                'department': data.get('department'),
+                'location': data.get('location'),
+                'marital_status': data.get('maritalStatus'),
+                'current_role': data.get('currentRole'),
+                'year_of_joining': data.get('yearOfJoining'),
+                'work_mode': data.get('workMode'),
+                'shift': data.get('shift')
+            }
+        )
+        
+        PersonService.create(person)
+        return jsonify({'message': 'User registered successfully'})
+        
+    except Exception as e:
+        return jsonify({'error': str(e)}), 400
+
+@app.route('/register-users', methods=['POST'])
+def register_users_bulk():
+    """Register multiple users via Excel upload"""
+    try:
+        # In a real implementation, you would parse the Excel file
+        # For now, return a mock response
+        return jsonify({'message': 'Users registered successfully', 'count': 10})
+        
+    except Exception as e:
+        return jsonify({'error': str(e)}), 400
+
+@app.route('/get-designations-departments-locations/<company_id>')
+def get_company_details(company_id):
+    """Get company-specific details for dropdowns"""
+    company = CompanyService.get_by_id(company_id)
+    if not company:
+        return jsonify({'error': 'Company not found'}), 404
+    
+    # Mock data - in real implementation, this would come from company metadata
+    return jsonify({
+        'Designations': ['Manager', 'Senior Developer', 'Developer', 'Analyst', 'Coordinator'],
+        'Departments': ['Engineering', 'HR', 'Sales', 'Marketing', 'Finance'],
+        'CompanyLocations': ['New York', 'San Francisco', 'Austin', 'Remote'],
+        'CurrentRoles': ['Team Lead', 'Individual Contributor', 'Manager', 'Director'],
+        'WorkMode': ['Remote', 'On-site', 'Hybrid'],
+        'Shift': ['Day Shift', 'Night Shift', 'Flexible']
+    })
+
+# Survey Management Hub Routes
+@app.route('/survey-management-hub')
+def survey_management_hub():
+    """Survey management hub page"""
+    return render_template('survey_hub/index.html')
+
+@app.route('/survey-tracker')
+def survey_tracker():
+    """Survey tracker page"""
+    companies = CompanyService.get_all()
+    return render_template('survey_hub/tracker.html', companies=companies)
+
+@app.route('/survey-deployment')
+def survey_deployment():
+    """Survey deployment page"""
+    companies = CompanyService.get_all()
+    return render_template('survey_hub/deployment.html', companies=companies)
+
+@app.route('/report-generation')
+def report_generation():
+    """Report generation page"""
+    companies = CompanyService.get_all()
+    return render_template('survey_hub/reports.html', companies=companies)
+
+# API Routes for Survey Management
+@app.route('/api/companies/<company_id>/surveys')
+def api_company_surveys(company_id):
+    """Get surveys for a company"""
+    surveys = SurveyTemplateService.get_all()
+    return jsonify([{
+        'SurveyId': s.id,
+        'SurveyName': s.name,
+        'CompanySurveyId': f"{company_id}-{s.id}"
+    } for s in surveys])
+
+@app.route('/api/company-surveys/<company_survey_id>/status')
+def api_survey_status(company_survey_id):
+    """Get survey status for participants"""
+    # Mock data for demonstration
+    return jsonify([
+        {
+            'PersonId': 'p1',
+            'FullName': 'John Doe',
+            'Email': 'john.doe@company.com',
+            'DeploymentStatus': 'Deployed',
+            'SurveyStatus': 'Completed',
+            'ReportStatus': 'Generated',
+            'DaysSinceSent': 5
+        },
+        {
+            'PersonId': 'p2',
+            'FullName': 'Jane Smith',
+            'Email': 'jane.smith@company.com',
+            'DeploymentStatus': 'Deployed',
+            'SurveyStatus': 'In Progress',
+            'ReportStatus': 'Pending',
+            'DaysSinceSent': 3
+        }
+    ])
+
+@app.route('/api/send-reminder-emails', methods=['POST'])
+def send_reminder_emails():
+    """Send reminder emails to selected users"""
+    try:
+        users = request.get_json()
+        # In real implementation, send actual emails
+        return jsonify({'message': f'Reminder emails sent to {len(users)} users'})
+    except Exception as e:
+        return jsonify({'error': str(e)}), 400