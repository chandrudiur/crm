# Overview

Myndwell Admin is a production-ready administrative application for managing survey deployments and user data within the Myndwell survey platform. The application provides comprehensive user management, company administration, survey template creation, deployment monitoring, and reporting capabilities. Built with Flask and using an in-memory data store for rapid prototyping, the system is designed with maintainability, security, and clear separation of concerns in mind.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Architecture
- **Framework**: Flask web framework with modular route organization
- **Data Layer**: In-memory data store using Python dictionaries for rapid development and prototyping
- **Models**: Dataclass-based models with enum types for status management and type safety
- **Service Pattern**: Implicit service layer through centralized data store operations
- **Session Management**: Flask sessions with configurable secret keys for security

## Frontend Architecture
- **Template Engine**: Jinja2 templating with a hierarchical base template structure
- **UI Framework**: Bootstrap 5 for responsive design and component library
- **CSS Architecture**: Custom CSS with CSS variables for theme consistency and maintainability
- **JavaScript**: Vanilla JavaScript with modular functions for sidebar management, chart rendering, and form validation
- **Accessibility**: WCAG AA compliance considerations built into the template structure

## Data Models and Relationships
- **Company-Person Relationship**: One-to-many relationship with domain-based email validation
- **Survey Templates**: Versioned survey definitions with question ordering and branching logic
- **Deployments**: Links companies, surveys, and scheduling with progress tracking
- **Audit Trail**: Comprehensive logging of all system actions for compliance and monitoring

## Authentication and Authorization
- **Role-Based Access**: Multi-role support (admin, manager) with granular permissions
- **Status Management**: User status tracking (active, inactive, pending) for lifecycle management
- **Session Security**: Secure session handling with environment-based configuration

## Design Patterns
- **MVC Pattern**: Clear separation between models, views (templates), and controllers (routes)
- **Repository Pattern**: Centralized data access through the data_store module
- **Factory Pattern**: ID generation and object creation utilities
- **Observer Pattern**: Audit logging for tracking system changes

# External Dependencies

## Frontend Dependencies
- **Bootstrap 5**: UI component framework and responsive grid system
- **Bootstrap Icons**: Icon library for consistent visual elements
- **Chart.js**: Data visualization and reporting charts
- **CDN Delivery**: All frontend assets loaded via CDN for performance and reliability

## Backend Dependencies
- **Flask**: Core web framework for routing and request handling
- **Werkzeug**: WSGI utilities including ProxyFix for deployment behind reverse proxies
- **Python Standard Library**: UUID generation, datetime handling, logging, and data structures

## Development and Deployment
- **Environment Variables**: Configuration management for secrets and deployment settings
- **Logging**: Structured logging with configurable levels for monitoring and debugging
- **Static Assets**: Organized static file structure for CSS, JavaScript, and images

## Future Integration Points
- **Database Migration**: Architecture designed to easily migrate from in-memory storage to persistent databases
- **Authentication Providers**: Prepared for integration with external authentication systems
- **Email Services**: Deployment notification and user invitation system hooks
- **Reporting APIs**: Built-in structure for connecting to external analytics and reporting services