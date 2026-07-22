Purpose:



This document defines the complete technical foundation of Sukhavasam SaaS v2 before any Django code is written.



The architecture is designed around the core principle:



&#x09;	One platform, multiple hospitality businesses, unlimited configurations, single maintainable codebase.





Sukhavasam SaaS v2 Architecture

Configuration-Driven Multi-Tenant Hospitality Platform



Version: 2.0

Architecture Type: Multi-Tenant SaaS

Backend: Django

Database: PostgreSQL

Deployment Model: Cloud Native



1\. Overall System Architecture

1.1 High-Level Architecture



Sukhavasam SaaS follows a layered architecture.



&#x20;                   Customer / Staff / Owner



&#x20;                           |

&#x20;                           |



&#x20;                   Web / Mobile Browser



&#x20;                           |

&#x20;                           |



&#x20;                 Domain Resolution Layer



&#x20;                           |

&#x20;                           |



&#x20;               Tenant Identification Layer



&#x20;                           |

&#x20;                           |



&#x20;             Authentication \& Authorization



&#x20;                           |

&#x20;                           |



&#x20;             Configuration Rendering Engine



&#x20;                           |

&#x20;                           |



&#x20;             Business Application Services



&#x20;                           |

&#x20;                           |



&#x20;                   Data Access Layer



&#x20;                           |

&#x20;                           |



&#x20;                   PostgreSQL Database



&#x20;                           |

&#x20;                           |



&#x20;       External Services (Payment, Email, AI, Storage)

1.2 Core Architectural Principles

Principle 1: Multi-Tenant First



The platform is designed for multiple resorts from day one.



Not:



One Resort

=

One Application



Instead:



One Application



&#x20;       +



Multiple Resorts



&#x20;       +



Independent Configuration

Principle 2: Configuration Over Customization



Avoid:



Customer Request



↓



Developer Changes Code



↓



Deploy Again



Preferred:



Customer Request



↓



Configuration Change



↓



Feature Available

Principle 3: Modular Architecture



Each business capability exists as an independent module.



Example:



Booking Module



Inventory Module



CRM Module



Restaurant Module



Marketing Module



Modules communicate through defined services.



2\. Multi-Tenant Architecture

2.1 Tenant Concept



A tenant represents one hospitality business.



Example:



Tenant



&#x20;   |

&#x20;   |

&#x20;   ├── Resort Information

&#x20;   ├── Users

&#x20;   ├── Rooms

&#x20;   ├── Bookings

&#x20;   ├── Website Configuration

&#x20;   ├── Theme

&#x20;   └── Subscription

2.2 Tenant Isolation Model



Recommended architecture:



Shared Database + Tenant ID



Example:



Database:



PostgreSQL





Tenant Table



id | name



1  | Sukhavasam



2  | Beach Resort Goa



3  | Mountain Stay



Every business table contains:



tenant\_id



Example:



Booking Table:



id



tenant\_id



guest\_name



room



date



Advantages:



Easy scaling

Easy maintenance

Single deployment

Lower cost

Easier analytics

2.3 Future Enterprise Option



For large customers:



Shared Database



&#x20;      OR



Dedicated Database



Architecture should support both.



3\. Domain / Subdomain Architecture



Primary domain:



sukhavasam.in

Platform Website

www.sukhavasam.in



Contains:



Marketing website

Pricing

Registration

Documentation

Subscriber Websites



Example:



tajresort.sukhavasam.in



beachvilla.sukhavasam.in



mountainstay.sukhavasam.in



Request Flow:



Visitor



&#x20;  |



tajresort.sukhavasam.in



&#x20;  |



DNS



&#x20;  |



Django Middleware



&#x20;  |



Extract Subdomain



&#x20;  |



Find Tenant



&#x20;  |



Load Configuration



&#x20;  |



Render Website

3.1 Domain Mapping Future Support



Architecture should support:



Custom domain:



www.myresort.com



mapping to:



myresort.sukhavasam.in



Flow:



Incoming Domain



&#x20;      |



Domain Mapping Table



&#x20;      |



Tenant Resolver



&#x20;      |



Website Renderer

4\. Backend Architecture

Technology

Python



Django



Django REST Framework



PostgreSQL



Redis



Celery

4.1 Django Application Structure



Recommended:



backend/





config/



&#x20;   settings/



&#x20;   urls.py



&#x20;   celery.py







apps/





core/



accounts/



tenant/



subscription/



website/



configuration/



booking/



inventory/



restaurant/



crm/



marketing/



analytics/



reports/



payments/



notifications/



ai/



common/





api/

4.2 Application Responsibilities

Core



Foundation:



Base models

Utilities

Middleware

Constants

Accounts



Responsible:



Users

Authentication

Profiles

Login

Tenant



Responsible:



Resorts

Subdomains

Tenant switching

Subscription



Responsible:



Plans

Billing

Feature activation

Website



Responsible:



Dynamic pages

Sections

Themes

Configuration



Responsible:



System configuration engine

Booking



Responsible:



Availability

Reservations

Payments

PMS



Responsible:



Operations

Check-in

Check-out

Housekeeping

5\. Frontend Architecture



The frontend follows component-based design.



5.1 Website Layer



Dynamic subscriber website:



templates/





website/



&#x20;   home



&#x20;   rooms



&#x20;   gallery



&#x20;   restaurant



&#x20;   contact





Rendered using:



Tenant Configuration



&#x20;       +



Theme



&#x20;       +



Content



&#x20;       +



Components

5.2 Dashboard Layer



Admin interface:



dashboard/





overview



bookings



rooms



customers



inventory



restaurant



marketing



reports



settings

5.3 UI Components



Reusable components:



Navbar



Footer



Hero



RoomCard



BookingForm



Calendar



Gallery



ReviewCard



Charts



Tables

6\. Database Architecture



Database:



PostgreSQL



High-level entities:



Tenant



&#x20;|



User



&#x20;|



Subscription



&#x20;|



Configuration



&#x20;|



Website



&#x20;|



Room



&#x20;|



Booking



&#x20;|



Payment



&#x20;|



Guest



&#x20;|



Inventory



&#x20;|



CRM



&#x20;|



Marketing

6.1 Database Rules



Every business table must include:



id



tenant\_id



created\_at



updated\_at



created\_by



Example:



Room:



id



tenant\_id



name



capacity



price



status



created\_at

7\. Configuration Architecture



This is the heart of the platform.



Everything configurable:



Website Configuration



Example:



Homepage





Hero Section



Enabled: Yes



Order: 1





Gallery



Enabled: Yes



Order: 2





Restaurant



Enabled: No

Feature Configuration



Example:



Swimming Pool Module



Enabled



True

Permission Configuration



Example:



Manager



Can view bookings



Cannot change pricing

Business Configuration



Example:



GST Percentage



Cancellation Policy



Check-in Time



Checkout Time

8\. Security Architecture

Authentication



Support:



Email login

Password

OTP future

Social login future

Authorization



Role-based access:



Owner



Manager



Receptionist



Restaurant Staff



Housekeeping



Accountant

Data Security



Rules:



Tenant data isolation

Permission checks

Audit logs

Encryption for sensitive information

Secure API access

9\. Deployment Architecture



Initial deployment:



User



&#x20;|



Cloudflare



&#x20;|



Application Server



&#x20;|



Django



&#x20;|



PostgreSQL



&#x20;|



Redis

Components:

Application Server



Runs:



Django

API

Background workers

Database



PostgreSQL:



Stores:



Users

Bookings

Configuration

Transactions

Storage



For:



Images

Documents

Media



Future:



AWS S3



or



Cloudinary

10\. Scaling Strategy



Architecture should support:



Stage 1



0-100 resorts



Single Application Server



Single Database

Stage 2



100-1000 resorts



Multiple Application Servers



Database Optimization



Redis Cache



Background Workers

Stage 3



1000+ resorts



Load Balancer



Multiple Services



Database Replication



Microservice Extraction

Future Microservice Possibility



Current:



Modular Monolith



Future:



Booking Service



Payment Service



AI Service



Notification Service

11\. Development Rules



Every new module must follow:



Requirement



↓



Architecture Review



↓



Database Design



↓



Configuration Design



↓



Development



↓



Testing



↓



Deployment

12\. Architecture Decision Summary

Decision	Choice

Application Style	Modular Monolith

Tenant Model	Shared Database + tenant\_id

Backend	Django

Database	PostgreSQL

Frontend	Component Driven

Website	Configuration Driven

Hosting	Cloud Native

Storage	Object Storage

Authentication	Role Based

Scaling	Horizontal Scaling Ready

Final Architecture Statement



Sukhavasam SaaS will be built as a configuration-driven, multi-tenant hospitality operating system where:



One Codebase



&#x20;       +



Multiple Resorts



&#x20;       +



Independent Branding



&#x20;       +



Configurable Features



&#x20;       +



Scalable Infrastructure



&#x20;       =



Hospitality SaaS Platform



End of Architecture.md

