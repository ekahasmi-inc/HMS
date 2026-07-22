Purpose:



This document defines the core philosophy and technical design of the Configuration Engine, which is the foundation of Sukhavasam SaaS v2.



The configuration engine allows multiple hospitality businesses to use the same platform while having:



Different websites

Different branding

Different enabled features

Different workflows

Different pricing rules

Different dashboards



without changing application code.



Sukhavasam SaaS Configuration Engine

Database-Driven Customization Framework



Version: 1.0



1\. Configuration Philosophy

Core Principle



"Code defines capability. Configuration defines behaviour."



The platform code should provide capabilities.



The tenant configuration decides how those capabilities are used.



Traditional Software Model



Example:



A resort wants a restaurant page.



Developer creates:



restaurant.html



restaurant\_view.py



restaurant\_model.py



Problem:



Every customer requirement creates new development work.



Sukhavasam SaaS Model



Restaurant capability already exists.



Configuration:



Restaurant Module



Enabled = True



Display Position = Homepage



Menu Visible = Yes



Online Order = No



Result:



Website automatically changes.



2\. Configuration Layers



Configuration exists at multiple levels.



System Configuration



&#x20;       ↓



Subscription Configuration



&#x20;       ↓



Tenant Configuration



&#x20;       ↓



User Configuration



&#x20;       ↓



Runtime Configuration

2.1 System Configuration



Controlled by SaaS owner.



Examples:



Available modules



Payment providers



Email providers



Default themes



Default templates

2.2 Subscription Configuration



Defines what each plan receives.



Example:



Starter Plan:



Website Builder = Yes



Booking Engine = Yes



CRM = No



AI = No



Professional:



Website



Booking



CRM



Marketing



AI

2.3 Tenant Configuration



Controlled by resort owner.



Example:



Resort Name



Logo



Theme



Enabled Sections



Room Types



Policies



Contact Details

2.4 User Configuration



Personal preferences.



Example:



Dashboard layout



Notification settings



Language



Date format

3\. Configuration Data Model Concept



All configuration follows:



Configuration Entity



&#x20;       +



Configuration Value



&#x20;       +



Configuration Rules



Example:



Website Hero Section:



Entity:



Homepage Hero





Values:



Title:

"Luxury Beach Resort"





Image:

hero.jpg





Button:

Book Now

4\. Database Driven Website Builder



The website builder is not page-template based.



It is component based.



Traditional Website

Homepage



Rooms Page



Gallery Page



Contact Page



Hardcoded.



Sukhavasam Website Engine

Page



&#x20;   |

&#x20;   |

&#x20;   ├── Section

&#x20;   |

&#x20;   |

&#x20;   ├── Component

&#x20;   |

&#x20;   |

&#x20;   └── Content



Example:



Homepage:



Homepage



Order 1

&#x20;   Hero Section



Order 2

&#x20;   Room Showcase



Order 3

&#x20;   Gallery



Order 4

&#x20;   Restaurant



Order 5

&#x20;   Reviews



Order 6

&#x20;   Contact

5\. Dynamic Page Structure

Page Entity



Example:



Page



id



tenant\_id



name



slug



status



seo\_title



seo\_description



Example:



Home



/about



/rooms



/gallery

5.1 Page Section



Each page contains sections.



Example:



Homepage



|



├── Hero



├── About



├── Rooms



├── Gallery



├── Testimonials



└── Contact



Section fields:



id



page\_id



section\_type



display\_order



enabled



configuration\_json



Example JSON:



{

&#x20;"background":"sea.jpg",

&#x20;"title":"Experience Coastal Luxury",

&#x20;"button":"Book Now"

}

6\. Component Library



The platform maintains reusable components.



Website Components

Hero



Gallery



Room Card



Booking Widget



Testimonials



FAQ



Restaurant Menu



Map



Blog Listing



Offer Banner



Contact Form



Each component has:



Component Name



Required Data



Configuration Options



Rendering Template



Example:



Room Card:



Component:



RoomCard





Inputs:



Room Name



Image



Price



Amenities





Options:



Show Price



Show Button



Show Size

7\. Theme Engine



Theme should never be hardcoded.



Theme Configuration



Controls:



Colors



Fonts



Spacing



Buttons



Cards



Images



Header



Footer



Example:



{

"primary\_color":"#0A5C6B",



"button\_style":"rounded",



"font":"Poppins",



"header":"transparent"

}

Theme Structure

Theme



|



├── Layout



├── Colors



├── Typography



├── Components



└── Custom CSS

8\. Feature Toggle System



Features should be activated through configuration.



Example:



Database:



Tenant Feature





tenant\_id



feature



enabled



Example:



Sukhavasam





Swimming Pool



TRUE





Restaurant



TRUE





Online Payment



TRUE





Inventory



FALSE



Application check:



if tenant.has\_feature("restaurant"):

&#x20;   show\_restaurant()

Feature Categories

Core Features



Always available:



Website



Booking



Guest Management

Premium Features

CRM



Marketing



AI



Analytics



Inventory

9\. Form Builder



Forms should be dynamic.



Problem:



Different resorts require different information.



Example:



Beach resort:



Guest Name



Phone



Arrival Time



Vehicle Number



Adventure resort:



Guest Name



Age



Activity Preference



Emergency Contact



Solution:



Database driven forms.



Form Structure:



Form



|



Fields



|



Validation Rules



|



Submission Action



Example:



Booking Form:



Field



Name



Type



Required



Validation



JSON:



{

"name":"arrival\_time",



"type":"time",



"required":true

}

10\. Workflow Configuration



Business processes should be configurable.



Example:



Booking Workflow



Default:



Booking Created



↓



Payment Pending



↓



Payment Received



↓



Confirmation Sent



↓



Check-in



↓



Checkout



Another resort may want:



Booking Request



↓



Owner Approval



↓



Payment



↓



Confirmation



Workflow Engine stores:



Trigger



Condition



Action



Next Step



Example:



Trigger:



Booking Created





Condition:



Payment Completed





Action:



Send Email

11\. Pricing Rules Configuration



Pricing engine should not contain fixed logic.



Traditional:



Weekend = +20%



Festival = +30%



Hardcoded.



Configuration:



Rule:



Season



Condition



Adjustment



Example:



Rule Name:



Weekend Pricing





Condition:



Friday-Sunday





Adjustment:



+20%



Advanced:



Occupancy Based Pricing



Date Based Pricing



Event Pricing



Last Minute Pricing



Long Stay Discount

12\. Dashboard Widget Configuration



Dashboard should also be configurable.



Example:



Owner Dashboard:



Revenue



Bookings



Occupancy



Reviews



Manager Dashboard:



Today's Arrival



Today's Departure



Room Status



Configuration:



Widget



Role



Position



Permission



Example:



Widget:



Revenue Chart





Role:



Owner





Position:



Top Left

13\. Notification Configuration



Messages should be configurable.



Channels:



Email



SMS



WhatsApp



Push Notification



Templates:



Booking Confirmation



Payment Receipt



Welcome Message



Review Request



Example:



Trigger:



Checkout Completed





Action:



Send Review Request

14\. Media Configuration



Images and files should be dynamic.



Storage:



Tenant



|



Media Library



|



Images



Videos



Documents



Used by:



Website



Rooms



Blogs



Marketing



Invoices

15\. SEO Configuration



Each tenant controls:



Meta Title



Meta Description



Keywords



Schema Markup



Sitemap



Dynamic:



Beach Resort in Diveagar



Luxury Stay near Beach



Konkan Resort

16\. Configuration Priority



When multiple configurations exist:



System Default



&#x20;       ↓



Subscription



&#x20;       ↓



Tenant Override



&#x20;       ↓



User Preference



Highest priority wins.



17\. Configuration Versioning



Important for SaaS upgrades.



Example:



Version 1:



Homepage Sections:

Hero

Rooms

Gallery



Version 2:



Hero

Rooms

Gallery

Restaurant



Existing customers should not break.



Database:



Configuration Version



Created Date



Applied Date



Rollback Option

18\. Configuration Management Dashboard



Admin can manage:



Modules



Themes



Templates



Components



Feature Flags



Pricing Rules



Workflows

19\. Development Rules



Any new feature must answer:



Question 1



Can this be configuration?



If yes:



Do not hardcode.



Question 2



Can multiple tenants use this?



If yes:



Design generically.



Question 3



Can the business owner change it?



If yes:



Create configuration.



20\. Final Configuration Architecture



The complete flow:



Tenant Request



&#x20;       ↓



Configuration Database



&#x20;       ↓



Configuration Engine



&#x20;       ↓



Business Rules Engine



&#x20;       ↓



Rendering / Processing



&#x20;       ↓



Customer Experience

Final Statement



The Sukhavasam SaaS configuration engine is the foundation that enables:



1000 Resorts



&#x20;       +



One Codebase



&#x20;       +



Different Websites



&#x20;       +



Different Workflows



&#x20;       +



Different Business Rules



&#x20;       =



Scalable Hospitality SaaS



End of ConfigurationEngine.md

