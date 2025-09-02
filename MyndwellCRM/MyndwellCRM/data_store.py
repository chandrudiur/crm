import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from models import *

# In-memory data store
data_store = {
    'companies': {},
    'persons': {},
    'questions': {},
    'survey_templates': {},
    'deployments': {},
    'audit_logs': {}
}

def generate_id():
    return str(uuid.uuid4())

def init_data_store():
    """Initialize the data store with sample data"""
    
    # Create sample companies
    company1 = Company(
        id=generate_id(),
        name="Acme Corporation",
        domains=["acme.com", "acmecorp.com"],
        status="active"
    )
    
    company2 = Company(
        id=generate_id(),
        name="TechStart Inc",
        domains=["techstart.io"],
        status="active"
    )
    
    data_store['companies'][company1.id] = company1
    data_store['companies'][company2.id] = company2
    
    # Create sample persons
    person1 = Person(
        id=generate_id(),
        company_id=company1.id,
        email="john.doe@acme.com",
        name="John Doe",
        roles=["admin", "manager"],
        status=UserStatus.ACTIVE,
        metadata={"department": "HR", "location": "New York"}
    )
    
    person2 = Person(
        id=generate_id(),
        company_id=company1.id,
        email="jane.smith@acme.com",
        name="Jane Smith",
        roles=["user"],
        status=UserStatus.ACTIVE,
        metadata={"department": "Engineering", "location": "San Francisco"}
    )
    
    person3 = Person(
        id=generate_id(),
        company_id=company2.id,
        email="bob.wilson@techstart.io",
        name="Bob Wilson",
        roles=["admin"],
        status=UserStatus.ACTIVE,
        metadata={"department": "Product", "location": "Austin"}
    )
    
    data_store['persons'][person1.id] = person1
    data_store['persons'][person2.id] = person2
    data_store['persons'][person3.id] = person3
    
    # Create sample questions
    question1 = Question(
        id=generate_id(),
        code="Q001",
        text="How satisfied are you with your current work environment?",
        type=QuestionType.SCALE,
        choices=[
            QuestionChoice("1", "Very Dissatisfied", 1),
            QuestionChoice("2", "Dissatisfied", 2),
            QuestionChoice("3", "Neutral", 3),
            QuestionChoice("4", "Satisfied", 4),
            QuestionChoice("5", "Very Satisfied", 5)
        ],
        validation=QuestionValidation(required=True, min_value=1, max_value=5)
    )
    
    question2 = Question(
        id=generate_id(),
        code="Q002",
        text="Which benefits are most important to you? (Select all that apply)",
        type=QuestionType.MULTI,
        choices=[
            QuestionChoice("health", "Health Insurance"),
            QuestionChoice("dental", "Dental Insurance"),
            QuestionChoice("vision", "Vision Insurance"),
            QuestionChoice("retirement", "Retirement Plan"),
            QuestionChoice("pto", "Paid Time Off"),
            QuestionChoice("remote", "Remote Work Options")
        ],
        validation=QuestionValidation(required=True)
    )
    
    question3 = Question(
        id=generate_id(),
        code="Q003",
        text="What suggestions do you have for improving our workplace?",
        type=QuestionType.FREE,
        validation=QuestionValidation(required=False)
    )
    
    data_store['questions'][question1.id] = question1
    data_store['questions'][question2.id] = question2
    data_store['questions'][question3.id] = question3
    
    # Create sample survey template
    survey_template1 = SurveyTemplate(
        id=generate_id(),
        name="Employee Satisfaction Survey",
        version="1.0",
        program="Wellness",
        status=SurveyStatus.READY,
        description="Annual employee satisfaction and engagement survey",
        questions=[
            SurveyQuestion(
                id=generate_id(),
                survey_template_id="",  # Will be set after creation
                question_id=question1.id,
                order=1,
                section="Work Environment"
            ),
            SurveyQuestion(
                id=generate_id(),
                survey_template_id="",
                question_id=question2.id,
                order=2,
                section="Benefits"
            ),
            SurveyQuestion(
                id=generate_id(),
                survey_template_id="",
                question_id=question3.id,
                order=3,
                section="Feedback"
            )
        ]
    )
    
    # Update survey question references
    for sq in survey_template1.questions:
        sq.survey_template_id = survey_template1.id
    
    data_store['survey_templates'][survey_template1.id] = survey_template1
    
    # Create sample deployment
    deployment1 = Deployment(
        id=generate_id(),
        company_id=company1.id,
        survey_template_id=survey_template1.id,
        name="Q4 2024 Employee Survey",
        status=DeploymentStatus.ACTIVE,
        audience_type="all",
        channel="email",
        start_date=datetime.now() - timedelta(days=5),
        end_date=datetime.now() + timedelta(days=25),
        email_template=EmailTemplate(
            subject="Your Voice Matters - Complete Our Employee Survey",
            body="""Dear {{name}},
            
We value your feedback and would like to invite you to participate in our employee satisfaction survey.

Your responses are completely confidential and will help us improve our workplace.

Please click the link below to begin:
{{survey_link}}

Thank you for your time!

Best regards,
HR Team""",
            preview_text="Help us improve our workplace with your feedback"
        ),
        metrics={
            'invites_sent': 45,
            'responses_received': 32,
            'completion_rate': 71
        }
    )
    
    data_store['deployments'][deployment1.id] = deployment1

# CRUD Operations
class CompanyService:
    @staticmethod
    def get_all() -> List[Company]:
        return list(data_store['companies'].values())
    
    @staticmethod
    def get_by_id(company_id: str) -> Optional[Company]:
        return data_store['companies'].get(company_id)
    
    @staticmethod
    def create(company: Company) -> Company:
        if not company.id:
            company.id = generate_id()
        company.created_at = datetime.now()
        company.updated_at = datetime.now()
        data_store['companies'][company.id] = company
        return company
    
    @staticmethod
    def update(company_id: str, updates: Dict) -> Optional[Company]:
        company = data_store['companies'].get(company_id)
        if company:
            for key, value in updates.items():
                if hasattr(company, key):
                    setattr(company, key, value)
            company.updated_at = datetime.now()
        return company
    
    @staticmethod
    def delete(company_id: str) -> bool:
        return data_store['companies'].pop(company_id, None) is not None

class PersonService:
    @staticmethod
    def get_all() -> List[Person]:
        return list(data_store['persons'].values())
    
    @staticmethod
    def get_by_company(company_id: str) -> List[Person]:
        return [p for p in data_store['persons'].values() if p.company_id == company_id]
    
    @staticmethod
    def get_by_id(person_id: str) -> Optional[Person]:
        return data_store['persons'].get(person_id)
    
    @staticmethod
    def create(person: Person) -> Person:
        if not person.id:
            person.id = generate_id()
        person.created_at = datetime.now()
        person.updated_at = datetime.now()
        data_store['persons'][person.id] = person
        return person
    
    @staticmethod
    def update(person_id: str, updates: Dict) -> Optional[Person]:
        person = data_store['persons'].get(person_id)
        if person:
            for key, value in updates.items():
                if hasattr(person, key):
                    setattr(person, key, value)
            person.updated_at = datetime.now()
        return person
    
    @staticmethod
    def delete(person_id: str) -> bool:
        return data_store['persons'].pop(person_id, None) is not None

class QuestionService:
    @staticmethod
    def get_all() -> List[Question]:
        return list(data_store['questions'].values())
    
    @staticmethod
    def get_by_id(question_id: str) -> Optional[Question]:
        return data_store['questions'].get(question_id)
    
    @staticmethod
    def create(question: Question) -> Question:
        if not question.id:
            question.id = generate_id()
        question.created_at = datetime.now()
        question.updated_at = datetime.now()
        data_store['questions'][question.id] = question
        return question
    
    @staticmethod
    def search(query: str) -> List[Question]:
        results = []
        query_lower = query.lower()
        for question in data_store['questions'].values():
            if (query_lower in question.text.lower() or 
                query_lower in question.code.lower()):
                results.append(question)
        return results

class SurveyTemplateService:
    @staticmethod
    def get_all() -> List[SurveyTemplate]:
        return list(data_store['survey_templates'].values())
    
    @staticmethod
    def get_by_id(template_id: str) -> Optional[SurveyTemplate]:
        return data_store['survey_templates'].get(template_id)
    
    @staticmethod
    def create(template: SurveyTemplate) -> SurveyTemplate:
        if not template.id:
            template.id = generate_id()
        template.created_at = datetime.now()
        template.updated_at = datetime.now()
        data_store['survey_templates'][template.id] = template
        return template
    
    @staticmethod
    def update(template_id: str, updates: Dict) -> Optional[SurveyTemplate]:
        template = data_store['survey_templates'].get(template_id)
        if template:
            for key, value in updates.items():
                if hasattr(template, key):
                    setattr(template, key, value)
            template.updated_at = datetime.now()
        return template

class DeploymentService:
    @staticmethod
    def get_all() -> List[Deployment]:
        return list(data_store['deployments'].values())
    
    @staticmethod
    def get_by_id(deployment_id: str) -> Optional[Deployment]:
        return data_store['deployments'].get(deployment_id)
    
    @staticmethod
    def create(deployment: Deployment) -> Deployment:
        if not deployment.id:
            deployment.id = generate_id()
        deployment.created_at = datetime.now()
        deployment.updated_at = datetime.now()
        data_store['deployments'][deployment.id] = deployment
        return deployment
    
    @staticmethod
    def update(deployment_id: str, updates: Dict) -> Optional[Deployment]:
        deployment = data_store['deployments'].get(deployment_id)
        if deployment:
            for key, value in updates.items():
                if hasattr(deployment, key):
                    setattr(deployment, key, value)
            deployment.updated_at = datetime.now()
        return deployment
