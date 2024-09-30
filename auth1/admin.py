from django.contrib import admin
from auth1.models import User, Employer, Owner, Jobseeker

admin.site.register(User)
admin.site.register(Employer)
admin.site.register(Owner)
admin.site.register(Jobseeker)
