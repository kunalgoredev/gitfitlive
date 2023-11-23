# from django.contrib import admin
# from .models import Question, Option

# class OptionInline(admin.TabularInline):
#     model = Option
#     extra = 3
#     fields = ('option_type', 'custom_text', 'status', 'triggers_text_input', 'triggers_file_upload', 'triggers_date_picker', 'triggers_yes_dropdown', 'triggers_no_dropdown')
#     show_change_link = True  # Allows editing in a separate page if needed

# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     inlines = [OptionInline]
#     list_display = ('text', 'is_active', 'order')  # Customize as needed
#     list_filter = ('is_active',)
#     search_fields = ('text',)




from django.contrib import admin
from .models import Question, Option, YesDropdownOption, NoDropdownOption

class YesDropdownOptionInline(admin.TabularInline):
    model = YesDropdownOption
    extra = 1

class NoDropdownOptionInline(admin.TabularInline):
    model = NoDropdownOption
    extra = 1

# admin.py

from django.contrib import admin
from .models import Question, Option, YesDropdownOption, NoDropdownOption

class OptionInline(admin.TabularInline):
    model = Option
    extra = 1
    fields = ('option_type', 'custom_text', 'status', 'mandatory', 'triggers_text_input', 'triggers_file_upload', 'triggers_date_picker', 'triggers_yes_dropdown', 'triggers_no_dropdown')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]

# ... Register YesDropdownOption and NoDropdownOption if needed ...

# Optionally, register Option if you want it to be editable outside of the Question context
@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'option_type', 'status')
    list_filter = ('question', 'option_type', 'status')
    search_fields = ('question__text', 'custom_text')

admin.site.register(YesDropdownOption)
admin.site.register(NoDropdownOption)