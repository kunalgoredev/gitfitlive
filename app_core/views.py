# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Question, Option, Response

from django.shortcuts import render, redirect
from .models import Question
from django.core.paginator import Paginator

def display_questions_view(request):
    # Initialize or get the current state of responses from the session
    if 'quiz_responses' not in request.session:
        request.session['quiz_responses'] = {}

    responses = request.session['quiz_responses']

    # Save responses when navigating between pages
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = key.split('_')[1]
                responses[question_id] = value
        request.session.modified = True

    # Query and paginate questions
    questions_list = Question.objects.filter(is_active=True).order_by('order')
    paginator = Paginator(questions_list, 5)  # Adjust the number per page as needed
    page = request.GET.get('page')
    questions = paginator.get_page(page)

    context = {
        'questions': questions,
        'responses': responses
    }

    if request.htmx:
        return render(request, 'app_core/question_list.html', context)
    return render(request, 'app_core/quiz.html', context)


# Load additional inputs based on option selected
# views.py

def load_additional_inputs(request, question_id, option_id):
    option = get_object_or_404(Option, id=option_id)
    return render(request, 'app_core/additional_inputs.html', {'option': option})


from django.core.paginator import Paginator
from .models import Question

def load_questions_page(request):
    page = request.GET.get('page', 1)
    questions_list = Question.objects.filter(is_active=True).order_by('order')
    paginator = Paginator(questions_list, 5)

    questions = paginator.get_page(page)

    # Prepare selected options from session data
    selected_responses = request.session.get('responses', {})
    question_selected_options = {}
    for question in questions:
        selected_option_id = selected_responses.get(str(question.id), {}).get('selected_option_id')
        question_selected_options[question.id] = selected_option_id

    context = {
        'questions': questions,
        'question_selected_options': question_selected_options,
    }
    return render(request, 'app_core/questions_page.html', context)



# def load_questions_page(request):
#     page = request.GET.get('page', 1)
#     questions_list = Question.objects.filter(is_active=True).order_by('order')
#     paginator = Paginator(questions_list, 5)  # Adjust the number per page as needed

#     questions = paginator.get_page(page)
#     return render(request, 'app_core/questions_page.html', {'questions': questions})


# Validate inputs (optional, based on your validation needs)
def validate_input(request, option_id):
    option = get_object_or_404(Option, id=option_id)
    value = request.GET.get('value', '')
    if option.mandatory and not value.strip():
        return JsonResponse({'error': 'This field is required.'}, status=400)
    return JsonResponse({'message': 'Valid input.'})

def submit_quiz(request):
    if request.method == 'POST':
        responses = request.session.get('quiz_responses', {})

        # Process the responses here...
        # For example, save them to the database

        # Clear the responses from the session
        del request.session['quiz_responses']
        request.session.modified = True

        return redirect('thank_you')

    return redirect('display_questions')


# Thank you page view
def thankyou(request):
    return render(request, 'app_core/thankyou.html')


# from django.http import HttpResponse
# from django.shortcuts import render, get_object_or_404
# from .models import Option

# def update_response(request, question_id):
#     if request.method == 'POST':
#         # Fetch or initialize the responses for the current question
#         question_responses = request.session.get('responses', {}).get(str(question_id), {})

#         # Extract the selected_option_id from the POST request
#         selected_option_id = request.POST.get(f'question_{question_id}')
#         if not selected_option_id:
#             # If no option ID is present, return an error response
#             return JsonResponse({'status': 'error'}, status=400)

#         selected_option = get_object_or_404(Option, id=selected_option_id)
#         question_responses['selected_option_id'] = selected_option_id

#         # Update for additional triggered fields
#         # ... (existing logic for handling additional fields) ...

#         # Update the session
#         if 'responses' not in request.session:
#             request.session['responses'] = {}
#         request.session['responses'][str(question_id)] = question_responses
#         request.session.modified = True

#         # Check if additional inputs need to be loaded
#         if any([selected_option.triggers_text_input, selected_option.triggers_file_upload,
#                 selected_option.triggers_date_picker, selected_option.triggers_yes_dropdown,
#                 selected_option.triggers_no_dropdown]):
#             # Render and return the additional inputs HTML
#             return render(request, 'app_core/additional_inputs.html', {'option': selected_option})
#         else:
#             # No additional inputs required, return an empty div with the same ID
#             return HttpResponse(f'<div id="additional-inputs-{question_id}"></div>')

#     return JsonResponse({'status': 'error'}, status=400)


# from django.shortcuts import render, get_object_or_404
# from django.http import JsonResponse
# from .models import Option

# def update_response(request, question_id):
#     if request.method == 'POST':
#         # Fetch or initialize the responses for the current question
#         question_responses = request.session.get('responses', {}).get(str(question_id), {})

#         selected_option_id = request.POST.get(f'question_{question_id}')
#         if selected_option_id:
#             selected_option = get_object_or_404(Option, id=selected_option_id)
#             question_responses['selected_option_id'] = selected_option_id

#             # Check and update for additional triggered fields
#             if selected_option.triggers_text_input:
#                 question_responses['text_input'] = request.POST.get(f'text_input_{question_id}', '')

#             if selected_option.triggers_file_upload:
#                 file = request.FILES.get(f'file_upload_{question_id}')
#                 if file:
#                     # Implement file handling logic here
#                     pass

#             if selected_option.triggers_date_picker:
#                 question_responses['date_picker'] = request.POST.get(f'date_picker_{question_id}', '')

#             if selected_option.triggers_yes_dropdown:
#                 question_responses['yes_dropdown'] = request.POST.get(f'yes_dropdown_{question_id}', '')

#             if selected_option.triggers_no_dropdown:
#                 question_responses['no_dropdown'] = request.POST.get(f'no_dropdown_{question_id}', '')

#             # Update the session with the new responses
#             if 'responses' not in request.session:
#                 request.session['responses'] = {}
#             request.session['responses'][str(question_id)] = question_responses
#             request.session.modified = True
#             print(request.session['responses'])  # For debugging purposes


#             # Return the additional inputs HTML
#             return render(request, 'app_core/additional_inputs.html', {'option': selected_option})

#         return JsonResponse({'status': 'error'}, status=400)

#     return JsonResponse({'status': 'error'}, status=400)
