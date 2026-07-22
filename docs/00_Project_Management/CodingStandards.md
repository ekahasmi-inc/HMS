Sukhavasam SaaS Engineering Standards



Version: 1.0



Purpose



This document defines the mandatory engineering standards for the Sukhavasam SaaS platform.



Every Django application, model, API, service, template, and utility must follow these standards.



The goal is to ensure:



Consistency

Scalability

Maintainability

Testability

Security

Performance

1\. Engineering Philosophy



Every line of code should satisfy these principles:



Configuration over Hardcoding

Composition over Duplication

Convention over Configuration

Services over Fat Views

Reusable Components

Single Responsibility

Tenant Isolation

Security by Default

Database First

Backward Compatibility

2\. Project Structure

backend/



apps/



config/



templates/



static/



media/



requirements/



scripts/



docs/



tests/



No application code outside apps/.



3\. Django App Structure



Every app follows the same structure.



booking/



admin.py



apps.py



models/



services/



selectors/



serializers/



views/



urls.py



permissions/



validators/



tasks/



signals/



events/



repositories/



forms/



templates/



tests/



migrations/



Never place everything inside one models.py or views.py.



4\. Naming Conventions

Apps

booking



configuration



marketing



crm



Lowercase.



Singular names should be avoided.



Models

RoomType



Reservation



Guest



Invoice



PascalCase.



Singular.



Database Tables

booking\_room



booking\_reservation



crm\_guest



Use Django defaults with db\_table only when needed.



Fields

first\_name



booking\_date



created\_at



Snake\_case.



Functions

calculate\_price()



create\_booking()



send\_invoice()



Use verb-based names.



Constants

MAX\_GUESTS



DEFAULT\_TIMEZONE



Uppercase.



5\. UUID Policy



Every business entity uses UUID as the primary key.



Benefits:



Secure public identifiers

Easier integrations

No sequential ID exposure



Recommended:



id = models.UUIDField(

&#x20;   primary\_key=True,

&#x20;   default=uuid.uuid4,

&#x20;   editable=False,

)



Avoid integer IDs for business entities.



6\. BaseModel Standards



Every business model inherits from BaseModel.



BaseModel should include:



UUID primary key

created\_at

updated\_at

created\_by

updated\_by

is\_active



Tenant-specific models additionally inherit TenantModel.



Never duplicate audit fields.



7\. Tenant Isolation



Every tenant-owned table includes:



tenant = ForeignKey(...)



No query should access tenant data without tenant context.



Always filter by tenant in selectors and services.



8\. Service Layer Pattern



Views should never contain business logic.



Example:



❌



def create\_booking(request):

&#x20;   ...



✔



BookingService.create(...)



Responsibilities:



Views



HTTP



Services



Business logic



Selectors



Read queries



Repositories (optional)



Complex persistence

9\. Selector Pattern



Selectors handle all read operations.



Example:



ReservationSelector.get\_active\_reservations(...)



Never place complex queries inside views.



10\. Repository Pattern



Use repositories only for complex write operations.



Simple CRUD does not require repositories.



11\. Serializer Standards



One serializer per responsibility.



Example:



ReservationCreateSerializer



ReservationListSerializer



ReservationDetailSerializer



ReservationUpdateSerializer



Avoid one serializer for everything.



12\. View Standards



Prefer:



APIView



ViewSets



Generic Views



Business logic belongs in services.



Views should:



Validate request

Call service

Return response



Nothing more.



13\. URL Standards

/api/v1/bookings/



/api/v1/rooms/



/api/v1/payments/



Plural nouns.



Version every API.



14\. API Response Standard



Success:



{

&#x20; "success": true,

&#x20; "message": "Reservation created",

&#x20; "data": {}

}



Failure:



{

&#x20; "success": false,

&#x20; "message": "Room unavailable",

&#x20; "errors": {}

}



Consistent response format across modules.



15\. Exception Handling



Never expose raw exceptions.



Create custom exceptions.



Examples:



BookingException



PaymentException



InventoryException



Centralize exception handling using DRF exception handlers or middleware.



16\. Logging



Never use:



print(...)



Use structured logging.



Levels:



DEBUG

INFO

WARNING

ERROR

CRITICAL



Include:



Tenant

User

Module

Request ID

17\. Signals vs Domain Events



Use Django signals only for framework-level concerns.



Use explicit domain events for business workflows.



Preferred:



ReservationCreated



↓



PaymentPending



↓



Notification Service



This is easier to test and reason about.



18\. Background Tasks



Long-running operations must use Celery.



Examples:



Invoice generation

Email

WhatsApp

Reports

AI content

Image optimization



Views should return immediately.



19\. Testing Standards



Every app includes:



tests/



models/



services/



selectors/



api/



permissions/



Minimum coverage targets:



Services

Selectors

API endpoints

Permission checks

20\. Migration Policy



Never edit old migrations after they are shared.



Rules:



One logical change per migration

Review generated migrations

Data migrations separate from schema migrations when practical

Test migrations against production-like data

21\. File Upload Strategy



Never store uploads directly under module folders.



Recommended structure:



media/



tenant/



rooms/



blogs/



invoices/



profiles/



gallery/



Support pluggable storage (local, S3, Cloudinary) via Django's storage backend.



22\. Security Standards



Mandatory:



CSRF protection

XSS protection

ORM parameterization

Secure cookies

HTTPS

Password hashing

Role checks

Tenant validation

Rate limiting for sensitive endpoints

23\. Performance Standards



Use:



select\_related

prefetch\_related

Pagination

Caching where appropriate

Background jobs for heavy processing



Avoid N+1 query problems.



24\. Configuration Rules



Never hardcode:



GST

Currency

Booking rules

Cancellation policy

Theme values

Email templates

Feature availability



Read from the configuration engine.



25\. Documentation Rules



Every app must include:



README.md

architecture.md

api.md



Every service should have a clear docstring explaining its purpose and inputs.



26\. Git Standards



Branch naming:



feature/booking-engine



bugfix/payment



hotfix/security



refactor/configuration



Commit format:



feat: Add booking workflow



fix: Resolve payment callback issue



refactor: Move pricing logic to service



docs: Update architecture

27\. Code Review Checklist



Before merging:



Tenant-safe?

Tested?

Documented?

Configuration-driven?

No duplicated logic?

No hardcoded values?

Logging added?

Permissions checked?

Performance reviewed?

28\. Architecture Rules



Modules communicate through services and events.



Never import internal models from unrelated apps when a service interface exists.



Keep coupling low.



29\. Future-Proofing



Design every module assuming:



Multiple properties

Multiple currencies

Multiple languages

Multiple payment gateways

Mobile apps

Public APIs

White-label deployments



Even if version 1 does not expose these capabilities.



30\. Engineering Manifesto



Every feature must answer YES to these questions before implementation:



Is it configuration-driven?

Is it tenant-aware?

Is it reusable?

Is it independently testable?

Can it scale without redesign?

Does it avoid duplication?

Is it secure by default?

Is it documented?

Can another module reuse it?

Would this design still make sense with 10,000 tenants?



If the answer to any of these is No, redesign before writing code.

