from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app
from data_store import *
from models import *
from datetime import datetime

@app.route('/')
def dashboard():
    """Dashboard with KPIs and overview"""
    companies = CompanyService.get_all()
    persons = PersonService.get_all()
    surveys = SurveyTemplateService.get_all()
    deployments = DeploymentService.get_all()
    
    # Calculate KPIs
    total_companies = len(companies)
    total_users = len(persons)
    active_surveys = len([s for s in surveys if s.status == SurveyStatus.READY])
    active_deployments = len([d for d in deployments if d.status == DeploymentStatus.ACTIVE])
    
    # Recent activity
    recent_deployments = sorted(deployments, key=lambda x: x.created_at, reverse=True)[:5]
    
    return render_template('dashboard.html', 
                         total_companies=total_companies,
                         total_users=total_users,
                         active_surveys=active_surveys,
                         active_deployments=active_deployments,
                         recent_deployments=recent_deployments)

# User Management Routes
@app.route('/users')
def users_index():
    """List all users"""
    persons = PersonService.get_all()
    companies = CompanyService.get_all()
    company_map = {c.id: c.name for c in companies}
    return render_template('users/index.html', persons=persons, company_map=company_map)

@app.route('/users/create', methods=['GET', 'POST'])
def users_create():
    """Create new user"""
    if request.method == 'POST':
        person = Person(
            id=generate_id(),
            company_id=request.form['company_id'],
            email=request.form['email'],
            name=request.form['name'],
            roles=request.form.getlist('roles'),
            status=UserStatus(request.form['status']),
            metadata={
                'department': request.form.get('department', ''),
                'location': request.form.get('location', '')
            }
        )
        PersonService.create(person)
        flash('User created successfully!', 'success')
        return redirect(url_for('users_index'))
    
    companies = CompanyService.get_all()
    return render_template('users/create.html', companies=companies)

@app.route('/users/<user_id>/edit', methods=['GET', 'POST'])
def users_edit(user_id):
    """Edit existing user"""
    person = PersonService.get_by_id(user_id)
    if not person:
        flash('User not found!', 'error')
        return redirect(url_for('users_index'))
    
    if request.method == 'POST':
        updates = {
            'company_id': request.form['company_id'],
            'email': request.form['email'],
            'name': request.form['name'],
            'roles': request.form.getlist('roles'),
            'status': UserStatus(request.form['status']),
            'metadata': {
                'department': request.form.get('department', ''),
                'location': request.form.get('location', '')
            }
        }
        PersonService.update(user_id, updates)
        flash('User updated successfully!', 'success')
        return redirect(url_for('users_index'))
    
    companies = CompanyService.get_all()
    return render_template('users/edit.html', person=person, companies=companies)

@app.route('/users/<user_id>/delete', methods=['POST'])
def users_delete(user_id):
    """Delete user"""
    if PersonService.delete(user_id):
        flash('User deleted successfully!', 'success')
    else:
        flash('User not found!', 'error')
    return redirect(url_for('users_index'))

# Survey Template Routes
@app.route('/surveys')
def surveys_index():
    """List all survey templates"""
    surveys = SurveyTemplateService.get_all()
    return render_template('surveys/index.html', surveys=surveys)

@app.route('/surveys/create', methods=['GET', 'POST'])
def surveys_create():
    """Create new survey template"""
    if request.method == 'POST':
        template = SurveyTemplate(
            id=generate_id(),
            name=request.form['name'],
            version=request.form['version'],
            program=request.form['program'],
            status=SurveyStatus(request.form['status']),
            description=request.form['description']
        )
        SurveyTemplateService.create(template)
        flash('Survey template created successfully!', 'success')
        return redirect(url_for('surveys_index'))
    
    return render_template('surveys/create.html')

@app.route('/surveys/<survey_id>/edit', methods=['GET', 'POST'])
def surveys_edit(survey_id):
    """Edit survey template"""
    survey = SurveyTemplateService.get_by_id(survey_id)
    if not survey:
        flash('Survey template not found!', 'error')
        return redirect(url_for('surveys_index'))
    
    if request.method == 'POST':
        updates = {
            'name': request.form['name'],
            'version': request.form['version'],
            'program': request.form['program'],
            'status': SurveyStatus(request.form['status']),
            'description': request.form['description']
        }
        SurveyTemplateService.update(survey_id, updates)
        flash('Survey template updated successfully!', 'success')
        return redirect(url_for('surveys_index'))
    
    questions = QuestionService.get_all()
    return render_template('surveys/edit.html', survey=survey, questions=questions)

# Deployment Routes
@app.route('/deployments')
def deployments_index():
    """List all deployments"""
    deployments = DeploymentService.get_all()
    companies = CompanyService.get_all()
    surveys = SurveyTemplateService.get_all()
    
    company_map = {c.id: c.name for c in companies}
    survey_map = {s.id: s.name for s in surveys}
    
    return render_template('deployments/index.html', 
                         deployments=deployments, 
                         company_map=company_map,
                         survey_map=survey_map)

@app.route('/deployments/create', methods=['GET', 'POST'])
def deployments_create():
    """Create new deployment"""
    if request.method == 'POST':
        email_template = EmailTemplate(
            subject=request.form['email_subject'],
            body=request.form['email_body'],
            preview_text=request.form.get('email_preview', '')
        )
        
        deployment = Deployment(
            id=generate_id(),
            company_id=request.form['company_id'],
            survey_template_id=request.form['survey_template_id'],
            name=request.form['name'],
            status=DeploymentStatus.DRAFT,
            audience_type=request.form['audience_type'],
            channel=request.form['channel'],
            start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d') if request.form['start_date'] else None,
            end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d') if request.form['end_date'] else None,
            email_template=email_template,
            max_attempts=int(request.form.get('max_attempts', 1))
        )
        
        DeploymentService.create(deployment)
        flash('Deployment created successfully!', 'success')
        return redirect(url_for('deployments_index'))
    
    companies = CompanyService.get_all()
    surveys = SurveyTemplateService.get_all()
    return render_template('deployments/create.html', companies=companies, surveys=surveys)

@app.route('/deployments/<deployment_id>/monitor')
def deployments_monitor(deployment_id):
    """Monitor deployment status and metrics"""
    deployment = DeploymentService.get_by_id(deployment_id)
    if not deployment:
        flash('Deployment not found!', 'error')
        return redirect(url_for('deployments_index'))
    
    company = CompanyService.get_by_id(deployment.company_id)
    survey = SurveyTemplateService.get_by_id(deployment.survey_template_id)
    
    return render_template('deployments/monitor.html', 
                         deployment=deployment, 
                         company=company, 
                         survey=survey)

# Company Routes
@app.route('/companies')
def companies_index():
    """List all companies"""
    companies = CompanyService.get_all()
    return render_template('companies/index.html', companies=companies, data_store=data_store)

@app.route('/companies/create', methods=['GET', 'POST'])
def companies_create():
    """Create new company"""
    if request.method == 'POST':
        domains = [d.strip() for d in request.form['domains'].split(',') if d.strip()]
        company = Company(
            id=generate_id(),
            name=request.form['name'],
            domains=domains,
            status=request.form['status']
        )
        CompanyService.create(company)
        flash('Company created successfully!', 'success')
        return redirect(url_for('companies_index'))
    
    return render_template('companies/create.html')

# Question Bank Routes
@app.route('/questions')
def questions_index():
    """List all questions"""
    search_query = request.args.get('search', '')
    if search_query:
        questions = QuestionService.search(search_query)
    else:
        questions = QuestionService.get_all()
    
    return render_template('questions/index.html', questions=questions, search_query=search_query)

# Reports Routes
@app.route('/reports')
def reports_index():
    """Reports dashboard"""
    deployments = DeploymentService.get_all()
    companies = CompanyService.get_all()
    
    return render_template('reports/index.html', deployments=deployments, companies=companies)

# Audit Trail Routes
@app.route('/audit')
def audit_index():
    """Audit trail"""
    audit_logs = list(data_store['audit_logs'].values())
    return render_template('audit/index.html', audit_logs=audit_logs)

# API Endpoints for AJAX
@app.route('/api/questions/search')
def api_questions_search():
    """Search questions for survey builder"""
    query = request.args.get('q', '')
    questions = QuestionService.search(query) if query else QuestionService.get_all()
    
    return jsonify([{
        'id': q.id,
        'code': q.code,
        'text': q.text,
        'type': q.type.value,
        'choices': [{'code': c.code, 'label': c.label} for c in q.choices]
    } for q in questions])

@app.route('/api/deployments/<deployment_id>/metrics')
def api_deployment_metrics(deployment_id):
    """Get deployment metrics"""
    deployment = DeploymentService.get_by_id(deployment_id)
    if not deployment:
        return jsonify({'error': 'Deployment not found'}), 404
    
    return jsonify(deployment.metrics)
