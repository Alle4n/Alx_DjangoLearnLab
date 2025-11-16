# LibraryProject

This is a basic Django project setup as part of the `Introduction_to_Django` exercise.  
It serves as the foundation for building Django apps like the `bookshelf` app.

This project uses Django Groups and Permissions to control access to Report objects.

Custom permissions added to the Report model:
- can_view  : User can view report list and details
- can_create: User can create reports
- can_edit  : User can edit existing reports
- can_delete: User can delete reports

Groups configured in Django Admin:
1. Viewers
   - Permissions: can_view

2. Editors
   - Permissions: can_view, can_create, can_edit

3. Admins
   - Permissions: can_view, can_create, can_edit, can_delete

Views use `@permission_required` to enforce access:
- report_list()  → requires accounts.can_view
- create_report() → requires accounts.can_create
- edit_report()   → requires accounts.can_edit
- delete_report() → requires accounts.can_delete
