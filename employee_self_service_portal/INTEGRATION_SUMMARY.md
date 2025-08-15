# Employee Self Service Portal - TechCarrot CRM MLR Integration

## Overview
This document outlines the integration of custom CRM fields from the `techcarrot_crm_mlr` module into the `employee_self_service_portal` module.

## Changes Made

### 1. Module Dependencies
- **File**: `__manifest__.py`
- **Change**: Added dependency on `techcarrot_crm_mlr` module
- **Before**: `"depends": ["portal", "hr", "hr_attendance", "hr_payroll", "hr_holidays"]`
- **After**: `"depends": ["portal", "hr", "hr_attendance", "hr_payroll", "hr_holidays", "techcarrot_crm_mlr"]`

### 2. Security Access Rights
- **File**: `security/ir.model.access.csv`
- **Change**: Added read access for portal users to the new CRM models:
  - `access_crm_practice_portal_user` - Read access to crm.practice
  - `access_crm_industry_portal_user` - Read access to crm.industry
  - `access_crm_lead_type_portal_user` - Read access to crm.lead.type

### 3. Controller Updates
- **File**: `controllers/main.py`
- **Changes**:
  - Updated `portal_employee_crm_create()` method to handle custom fields
  - Updated `portal_employee_crm_edit()` method to handle custom fields
  - Added data fetching for practices, industries, lead types, employees, and contacts
  - Added custom field processing in form submission

#### New Fields Handled:
- `point_of_contact_id` - Many2one to res.partner
- `practice_id` - Many2one to crm.practice
- `deal_manager_id` - Many2one to hr.employee
- `client_proposal_submission_date` - Date field
- `proposal_submitted_date` - Date field
- `engaged_presales` - Boolean field
- `industry_id` - Many2one to crm.industry
- `type_id` - Many2one to crm.lead.type

### 4. Template Updates

#### Create Form (`views/Employee_details/portal_employee_crm_create.xml`)
- Added form fields for all custom CRM fields
- Added Select2 initialization for searchable dropdowns
- Added proper labels and help text for each field

#### Edit Form (`views/Employee_details/portal_employee_crm_edit.xml`)
- Added form fields for all custom CRM fields with current values pre-populated
- Added Select2 initialization for searchable dropdowns
- Added proper labels and help text for each field

#### List View (`views/Employee_details/portal_employee_crm.xml`)
- Added columns for key custom fields:
  - Practice
  - Industry  
  - Deal Manager
  - Engaged Presales (with badge styling)
- Removed redundant columns to accommodate new fields

### 5. Model Extensions
- **File**: `models/crm_lead.py` (New)
- **Purpose**: Added portal-specific onchange methods
- **Methods**:
  - `_onchange_partner_id_point_of_contact_portal()` - Auto-set point of contact
  - `_onchange_deal_manager_id_portal()` - Auto-set user based on deal manager

### 6. Model Import
- **File**: `models/__init__.py`
- **Change**: Added import for the new crm_lead model

## Field Descriptions

### Core Custom Fields from techcarrot_crm_mlr:
1. **Point of Contact** - Main contact person for the opportunity
2. **Practice** - Practice area (e.g., Web Development, Mobile Apps, etc.)
3. **Deal Manager** - Employee responsible for managing the deal
4. **Industry** - Industry sector of the customer
5. **Type** - Business type for the opportunity
6. **Client Proposal Submission Date** - When proposal was submitted to client
7. **Proposal Submitted Date** - Internal record of proposal submission
8. **Engaged Presales** - Whether presales team is involved

## User Experience Improvements

### Enhanced Forms
- Searchable dropdowns using Select2 for better UX
- Proper field grouping and layout
- Helpful tooltips and descriptions
- Pre-populated values in edit forms

### Enhanced List View
- Display of key custom fields in the main CRM list
- Visual indicators (badges) for boolean fields
- Better column organization

### Data Relationships
- Automatic point of contact selection based on customer
- Automatic user assignment based on deal manager
- Proper data validation and error handling

## Technical Notes

### Dependencies
- The module now requires `techcarrot_crm_mlr` to be installed first
- All custom models (crm.practice, crm.industry, crm.lead.type) must be available

### Permissions
- Portal users have read-only access to master data (practices, industries, types)
- Portal users can create and edit CRM leads with all custom fields
- Standard Odoo security rules still apply

### JavaScript Libraries
- Uses Select2 for enhanced dropdown functionality
- CDN-based loading for better performance
- Graceful degradation if JavaScript is disabled

## Installation Notes

1. Install `techcarrot_crm_mlr` module first
2. Upgrade `employee_self_service_portal` module
3. Verify security access rights are properly applied
4. Test CRM functionality in portal environment

## Future Enhancements

Potential areas for future development:
1. Advanced filtering in CRM list view
2. Dashboard widgets for custom fields
3. Reporting integration with custom fields
4. Mobile-responsive improvements
5. Bulk operations on CRM records
