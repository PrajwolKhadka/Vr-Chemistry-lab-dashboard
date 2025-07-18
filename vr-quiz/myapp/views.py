# # import io
# # import json
# # from collections import Counter
# # from django.shortcuts import get_object_or_404, render
# # from .models import KeyValueData, SurveyResponse
# # import requests
# # from django.db import models
# # import matplotlib.pyplot as plt
# # from django.shortcuts import render
# # from io import BytesIO
# # import base64

# # import requests


# # def index(request):
# #     # API endpoints
# #     urls = [
# #         "https://services.api.unity.com/cloud-save/v1/data/projects/77f104be-1501-4cb5-b939-e690de43ec34/environments/002f4514-3bea-412a-a9dc-37e1ba68de0f/players/eYYj2HZdoxaLbigIRCburFmCM6va/items",
# #         # "https://services.api.unity.com/cloud-save/v1/data/projects/77f104be-1501-4cb5-b939-e690de43ec34/environments/002f4514-3bea-412a-a9dc-37e1ba68de0f/players/OJI57uih2bCucpRRAhrUodk9SpJE/items",
# #         # "https://services.api.unity.com/cloud-save/v1/data/projects/77f104be-1501-4cb5-b939-e690de43ec34/environments/002f4514-3bea-412a-a9dc-37e1ba68de0f/players/aLA5MGKRijI9tKUzdGohwmPrADDd/items",
# #         # "https://services.api.unity.com/cloud-save/v1/data/projects/77f104be-1501-4cb5-b939-e690de43ec34/environments/002f4514-3bea-412a-a9dc-37e1ba68de0f/players/oIfm4SJ3YxXiAXXLs0aqcQ6uC2ta/items",
# #     ]
    
# #     auth_header = "Basic MDgwMTMzNzktMzdlMy00YzE1LTk4ZjQtYjVjZWE2MmU4NmVhOlJBVUxUWFhwdHM2V3ZTR3ZCVVhVVW1zMXNkb2h2b3VP"

# #     headers = {
# #         "Authorization": auth_header,
# #         "Content-Type": "application/json"
# #     }

# #     # Correct answers for rest questions
# #     correct_answers = [[3], [0], [2], [3], [2], [2], [1], [2]]

# #     key_value_pairs = {}  # For passing to the template

# #     def compare_answers(user_answer, correct_answer):
# #         if len(user_answer) == 1 and len(correct_answer) == 1:
# #             return user_answer == correct_answer
# #         else:
# #             user_set = set(user_answer)
# #             correct_set = set(correct_answer)
# #             valid_numbers = {0, 1, 2}
# #             return user_set == correct_set and all(x in valid_numbers for x in user_set)

# #     try:
# #         for url in urls:
# #             response = requests.get(url, headers=headers)
# #             response.raise_for_status()
# #             data = response.json()

# #             for item in data.get('results', []):
# #                 key = item.get('key')
# #                 answers = item.get('value', {}).get('answers', [])
# #                 score = item.get('value', {}).get('score', 0)

# #                 first_five = answers[:5] if len(answers) >= 5 else answers
# #                 rest_questions = answers[5:] if len(answers) > 5 else []

# #                 correctness = []
# #                 for user_answer, correct_answer in zip(rest_questions, correct_answers):
# #                     if compare_answers(user_answer, correct_answer):
# #                         correctness.append(1)
# #                     else:
# #                         correctness.append(0)

# #                 correct_sum = sum(correctness)
# #                 skipped = correct_sum != score

# #                 first_five_str = json.dumps(first_five)
# #                 rest_questions_str = json.dumps(rest_questions)
# #                 correctness_str = ','.join(map(str, correctness))

# #                 # Update or create the model instance, preserving existing name and gender
# #                 SurveyResponse.objects.update_or_create(
# #                     id=key,
# #                     defaults={
# #                         'selected_options_from_one_to_five': first_five_str,
# #                         'selected_options_rest_questions': rest_questions_str,
# #                         'score': score,
# #                         'correctly_answered': correctness_str,
# #                         'skipped': skipped,
# #                     }
# #                 )

# #         # Fetch all survey responses from the model
# #         responses = SurveyResponse.objects.all()
# #         for response in responses:
# #             gender_display = response.get_gender_display() if response.gender else ''
# #             key_value_pairs[response.id] = {
# #                 'name': response.name or '',
# #                 'gender': gender_display,
# #                 'score': response.score,
# #                 'skipped': 'Yes' if response.skipped else 'No',
# #                 'correctly_answered': response.correctly_answered or ''
# #             }

# #     except requests.exceptions.RequestException as e:
# #         print("Error:", e)

# #     return render(request, 'index.html', {'key_value_pairs': key_value_pairs})

# # def analytics(request):
# #     # Initialize data structures
# #     survey_data = {
# #         'q1': Counter(), 'q2': Counter(), 'q3': Counter(), 'q4': Counter(), 'q5': Counter()
# #     }
# #     quiz_data = {f'q{i}': Counter() for i in range(6, 33)}
# #     correctness_data = {f'q{i}': {'correct': 0, 'total': 0} for i in range(6, 33)}
# #     skipped_correctness = {f'q{i}': {'skipped': {'correct': 0, 'total': 0}, 'not_skipped': {'correct': 0, 'total': 0}} for i in range(6, 33)}
# #     skipped_distribution = {'skipped': 0, 'not_skipped': 0}

# #     # Option mappings for survey questions
# #     survey_options = {
# #         'q1': {0: 'Very light', 1: 'Manageable', 2: 'Heavy', 3: 'Very heavy'},
# #         'q2': {0: 'Strongly agree', 1: 'Agree', 2: 'Neutral', 3: 'Disagree', 4: 'Strongly disagree'},
# #         'q3': {0: 'Excellent', 1: 'Good', 2: 'Average', 3: 'Poor', 4: 'Very poor'},
# #         'q4': {0: 'Always', 1: 'Often', 2: 'Sometimes', 3: 'Rarely', 4: 'Never'},
# #         'q5': {0: 'Inspiring students', 1: 'Professional recognition', 2: 'Opportunities for growth', 3: 'Salary and benefits', 4: 'Academic freedom'}
# #     }

# #     # Option mappings for quiz questions (simplified, using indices for brevity)
# #     quiz_options = {f'q{i}': {j: chr(65 + j) for j in range(5)} for i in range(6, 33)}  # A, B, C, D, E
# #     quiz_options['q29'] = {0: 'Mosaic plagiarism', 1: 'Code plagiarism', 2: 'Self-plagiarism', 3: 'Fabricated plagiarism'}

# #     responses = SurveyResponse.objects.all()
# #     total_responses = responses.count()

# #     for response in responses:
# #         try:
# #             # Parse survey answers
# #             survey_answers = json.loads(response.selected_options_from_one_to_five or '[]')
# #             for i, answer in enumerate(survey_answers[:5], 1):
# #                 if answer:
# #                     if i == 5:  # Multi-select for Q5
# #                         for opt in answer:
# #                             survey_data[f'q{i}'][opt] += 1
# #                     else:
# #                         survey_data[f'q{i}'][answer[0]] += 1

# #             # Parse quiz answers and correctness
# #             quiz_answers = json.loads(response.selected_options_rest_questions or '[]')
# #             correctness = [int(x) for x in (response.correctly_answered or '').split(',') if x]
# #             for i, (answer, correct) in enumerate(zip(quiz_answers, correctness), 6):
# #                 if answer:
# #                     if i == 29:  # Multi-select for Q29
# #                         for opt in answer:
# #                             quiz_data[f'q{i}'][opt] += 1
# #                     else:
# #                         quiz_data[f'q{i}'][answer[0]] += 1
# #                     correctness_data[f'q{i}']['total'] += 1
# #                     correctness_data[f'q{i}']['correct'] += correct
# #                     # Track skipped vs. non-skipped correctness
# #                     skip_key = 'skipped' if response.skipped else 'not_skipped'
# #                     skipped_correctness[f'q{i}'][skip_key]['total'] += 1
# #                     skipped_correctness[f'q{i}'][skip_key]['correct'] += correct

# #             # Track skipped distribution
# #             skipped_distribution['skipped' if response.skipped else 'not_skipped'] += 1

# #         except json.JSONDecodeError:
# #             continue

# #     # Prepare chart data
# #     survey_chart_data = {}
# #     for q, counter in survey_data.items():
# #         labels = [survey_options[q].get(k, str(k)) for k in sorted(counter.keys())]
# #         values = [counter.get(k, 0) / max(total_responses, 1) * 100 for k in sorted(counter.keys())]
# #         chart_type = 'pie' if q == 'q5' else 'bar'
# #         scales = {} if chart_type == 'pie' else {'y': {'beginAtZero': True, 'title': {'display': True, 'text': 'Percentage (%)'}}}
# #         legend_display = chart_type == 'pie'
# #         survey_chart_data[q] = {
# #             'labels': labels,
# #             'values': values,
# #             'type': chart_type,
# #             'scales': json.dumps(scales),  # Convert to JSON string for safe template rendering
# #             'legend_display': legend_display
# #         }

# #     quiz_chart_data = {}
# #     for q, counter in quiz_data.items():
# #         labels = [quiz_options[q].get(k, str(k)) for k in sorted(counter.keys())]
# #         values = [counter.get(k, 0) / max(total_responses, 1) * 100 for k in sorted(counter.keys())]
# #         quiz_chart_data[q] = {'labels': labels, 'values': values}

# #     correctness_chart_data = {
# #         'labels': [f'Q{i}' for i in range(6, 33)],
# #         'values': [
# #             (data['correct'] / max(data['total'], 1) * 100) if data['total'] > 0 else 0
# #             for data in correctness_data.values()
# #         ]
# #     }

# #     skipped_correctness_chart_data = {
# #         'labels': [f'Q{i}' for i in range(6, 33)],
# #         'skipped': [
# #             (data['skipped']['correct'] / max(data['skipped']['total'], 1) * 100) if data['skipped']['total'] > 0 else 0
# #             for data in skipped_correctness.values()
# #         ],
# #         'not_skipped': [
# #             (data['not_skipped']['correct'] / max(data['not_skipped']['total'], 1) * 100) if data['not_skipped']['total'] > 0 else 0
# #             for data in skipped_correctness.values()
# #         ]
# #     }

# #     skipped_pie_data = {
# #         'labels': ['Skipped', 'Not Skipped'],
# #         'values': [
# #             skipped_distribution['skipped'] / max(total_responses, 1) * 100,
# #             skipped_distribution['not_skipped'] / max(total_responses, 1) * 100
# #         ]
# #     }

# #     context = {
# #         'survey_chart_data': survey_chart_data,
# #         'quiz_chart_data': quiz_chart_data,
# #         'correctness_chart_data': correctness_chart_data,
# #         'skipped_correctness_chart_data': skipped_correctness_chart_data,
# #         'skipped_pie_data': skipped_pie_data,
# #         'total_responses': total_responses
# #     }

# #     return render(request, 'analytics.html', context)


# # def generate_chart(data):
# #     correct = data.count(1)
# #     incorrect = data.count(0)
# #     indices = list(range(1, len(data) + 1))
    
# #     # Create figure
# #     fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
# #     # Bar Chart
# #     axes[0].bar(['Correct', 'Incorrect'], [correct, incorrect], color=['green', 'red'])
# #     axes[0].set_title("Correct vs Incorrect")
    
# #     # Line Chart
# #     axes[1].plot(indices, data, marker='o', linestyle='-', color='blue')
# #     axes[1].set_title("Progression of Answers")
# #     axes[1].set_xlabel("Question Number")
# #     axes[1].set_ylabel("Correct (1) / Incorrect (0)")
    
# #     # Pie Chart
# #     axes[2].pie([correct, incorrect], labels=['Correct', 'Incorrect'], autopct='%1.1f%%', colors=['green', 'red'])
# #     axes[2].set_title("Percentage of Correct Answers")
    
# #     plt.tight_layout()
    
# #     # Save to a BytesIO buffer
# #     buffer = io.BytesIO()
# #     plt.savefig(buffer, format='png')
# #     buffer.seek(0)
# #     img_str = base64.b64encode(buffer.getvalue()).decode()
# #     plt.close()
    
# #     return img_str
# # def vul(request):
# #     record = None
# #     error = None
# #     chart_data = {}
# #     quiz_responses = []

# #     # Search functionality
# #     key = request.GET.get('key')
# #     if key:
# #         try:
# #             record = SurveyResponse.objects.get(id=key)
# #         except SurveyResponse.DoesNotExist:
# #             error = "No employee found with this ID."

# #     if record:
# #         # Quiz options mapping
# #         quiz_options = {f'q{i}': {j: chr(65 + j) for j in range(5)} for i in range(6, 33)}  # A, B, C, D, E
# #         quiz_options['q29'] = {0: 'Mosaic plagiarism', 1: 'Code plagiarism', 2: 'Self-plagiarism', 3: 'Fabricated plagiarism'}

# #         # Parse quiz answers and correctness
# #         quiz_answers = json.loads(record.selected_options_rest_questions or '[]')
# #         correctness = [int(x) for x in (record.correctly_answered or '').split(',') if x]

# #         # Line chart data for correctness
# #         chart_data = {
# #             'labels': [f'Q{i}' for i in range(6, 33)],
# #             'values': [100 if correct else 0 for correct in correctness]
# #         }

# #         # Quiz responses for table
# #         for i, (answer, correct) in enumerate(zip(quiz_answers, correctness), 6):
# #             q = f'q{i}'
# #             if answer:
# #                 if i == 29:  # Multi-select for Q29
# #                     response_text = ', '.join(quiz_options[q].get(opt, str(opt)) for opt in answer)
# #                 else:
# #                     response_text = quiz_options[q].get(answer[0], str(answer[0]))
# #                 quiz_responses.append({
# #                     'question': f'Question {i}',
# #                     'response': response_text,
# #                     'correct': 'Correct' if correct else 'Incorrect'
# #                 })

# #     context = {
# #         'record': record,
# #         'error': error,
# #         'chart_data': chart_data,
# #         'quiz_responses': quiz_responses
# #     }
# #     return render(request, 'vulnerable.html', context)


# # import csv
# # import json
# # from django.http import HttpResponse
# # from .models import SurveyResponse

# # def download(request):
# #     # Define response with CSV content type and filename
# #     response = HttpResponse(content_type='text/csv')
# #     response['Content-Disposition'] = 'attachment; filename="survey_responses.csv"'

# #     # Option mappings for survey questions
# #     survey_options = {
# #         'q1': {0: 'Very light', 1: 'Manageable', 2: 'Heavy', 3: 'Very heavy'},
# #         'q2': {0: 'Strongly agree', 1: 'Agree', 2: 'Neutral', 3: 'Disagree', 4: 'Strongly disagree'},
# #         'q3': {0: 'Excellent', 1: 'Good', 2: 'Average', 3: 'Poor', 4: 'Very poor'},
# #         'q4': {0: 'Always', 1: 'Often', 2: 'Sometimes', 3: 'Rarely', 4: 'Never'},
# #         'q5': {0: 'Inspiring students', 1: 'Professional recognition', 2: 'Opportunities for growth', 3: 'Salary and benefits', 4: 'Academic freedom'}
# #     }

# #     # Option mappings for quiz questions
# #     quiz_options = {f'q{i}': {j: chr(65 + j) for j in range(5)} for i in range(6, 33)}  # A, B, C, D, E
# #     quiz_options['q29'] = {0: 'Mosaic plagiarism', 1: 'Code plagiarism', 2: 'Self-plagiarism', 3: 'Fabricated plagiarism'}

# #     # Create CSV writer
# #     writer = csv.writer(response)
    
# #     # Write header
# #     headers = ['id', 'name', 'gender', 'score', 'skipped']
# #     headers.extend([f'Q{i}' for i in range(1, 33)])  # Q1 to Q32
# #     headers.extend([f'Q{i}_correct' for i in range(6, 33)])  # Correctness for Q6 to Q32
# #     writer.writerow(headers)

# #     # Fetch all responses
# #     responses = SurveyResponse.objects.all()

# #     for record in responses:
# #         row = [
# #             record.id,
# #             record.name or '',
# #             record.get_gender_display() if record.gender else '',
# #             record.score,
# #             'Yes' if record.skipped else 'No'
# #         ]

# #         # Parse survey answers (Q1–Q5)
# #         survey_answers = json.loads(record.selected_options_from_one_to_five or '[]')
# #         for i in range(1, 6):
# #             q = f'q{i}'
# #             if i-1 < len(survey_answers) and survey_answers[i-1]:
# #                 if i == 5:  # Multi-select for Q5
# #                     answer = ', '.join(survey_options[q].get(opt, str(opt)) for opt in survey_answers[i-1])
# #                 else:
# #                     answer = survey_options[q].get(survey_answers[i-1][0], str(survey_answers[i-1][0]))
# #             else:
# #                 answer = ''
# #             row.append(answer)

# #         # Parse quiz answers (Q6–Q32)
# #         quiz_answers = json.loads(record.selected_options_rest_questions or '[]')
# #         for i in range(6, 33):
# #             q = f'q{i}'
# #             if i-6 < len(quiz_answers) and quiz_answers[i-6]:
# #                 if i == 29:  # Multi-select for Q29
# #                     answer = ', '.join(quiz_options[q].get(opt, str(opt)) for opt in quiz_answers[i-6])
# #                 else:
# #                     answer = quiz_options[q].get(quiz_answers[i-6][0], str(quiz_answers[i-6][0]))
# #             else:
# #                 answer = ''
# #             row.append(answer)

# #         # Parse correctness (Q6–Q32)
# #         correctness = [int(x) for x in (record.correctly_answered or '').split(',') if x]
# #         for i in range(6, 33):
# #             if i-6 < len(correctness):
# #                 correct = 'Correct' if correctness[i-6] else 'Incorrect'
# #             else:
# #                 correct = ''
# #             row.append(correct)

# #         writer.writerow(row)

# #     return response



# import io
# import json
# from collections import Counter
# from django.shortcuts import get_object_or_404, render
# from .models import KeyValueData, SurveyResponse
# import requests
# from django.db import models
# import matplotlib.pyplot as plt
# from django.shortcuts import render
# from io import BytesIO
# import base64
# import requests
# import csv
# from django.http import HttpResponse

# def index(request):
#     # API endpoints
#     urls = [
#         "https://services.api.unity.com/cloud-save/v1/data/projects/77f104be-1501-4cb5-b939-e690de43ec34/environments/002f4514-3bea-412a-a9dc-37e1ba68de0f/players/eYYj2HZdoxaLbigIRCburFmCM6va/items",
#     ]
    
#     auth_header = "Basic MDgwMTMzNzktMzdlMy00YzE1LTk4ZjQtYjVjZWE2MmU4NmVhOlJBVUxUWFhwdHM2V3ZTR3ZCVVhVVW1zMXNkb2h2b3VP"

#     headers = {
#         "Authorization": auth_header,
#         "Content-Type": "application/json"
#     }

#     # Correct answers for all 8 questions
#     correct_answers = [[3], [0], [2], [3], [2], [2], [1], [2]]

#     key_value_pairs = {}  # For passing to the template

#     def compare_answers(user_answer, correct_answer):
#         return user_answer == correct_answer

#     try:
#         for url in urls:
#             response = requests.get(url, headers=headers)
#             response.raise_for_status()
#             data = response.json()

#             for item in data.get('results', []):
#                 key = item.get('key')
#                 answers = item.get('value', {}).get('answers', [])
#                 score = item.get('value', {}).get('score', 0)

#                 correctness = []
#                 for user_answer, correct_answer in zip(answers, correct_answers):
#                     if compare_answers(user_answer, correct_answer):
#                         correctness.append(1)
#                     else:
#                         correctness.append(0)

#                 correct_sum = sum(correctness)
#                 passed = correct_sum >= 5  # Assuming pass mark is 5/8

#                 answers_str = json.dumps(answers)
#                 correctness_str = ','.join(map(str, correctness))

#                 # Update or create the model instance
#                 SurveyResponse.objects.update_or_create(
#                     id=key,
#                     defaults={
#                         'answers': answers_str,
#                         'score': score,
#                         'correctly_answered': correctness_str,
#                         'passed': passed,
#                     }
#                 )

#         # Fetch all survey responses from the model
#         responses = SurveyResponse.objects.all()
#         for response in responses:
#             gender_display = response.get_gender_display() if response.gender else ''
#             key_value_pairs[response.id] = {
#                 'name': response.name or '',
#                 'gender': gender_display,
#                 'score': response.score,
#                 'passed': 'Pass' if response.passed else 'Fail',
#                 'correctly_answered': response.correctly_answered or ''
#             }

#     except requests.exceptions.RequestException as e:
#         print("Error:", e)

#     return render(request, 'index.html', {'key_value_pairs': key_value_pairs})

# def analytics(request):
#     # Initialize data structures
#     question_data = {f'q{i}': Counter() for i in range(1, 9)}
#     correctness_data = {f'q{i}': {'correct': 0, 'total': 0} for i in range(1, 9)}
#     pass_fail_data = {'Pass': 0, 'Fail': 0}

#     # Option mappings for questions
#     question_options = {
#         'q1': {0: 'Option A', 1: 'Option B', 2: 'Option C', 3: 'Option D'},
#         'q2': {0: 'Option A', 1: 'Option B', 2: 'Option C', 3: 'Option D'},
#         'q3': {0: 'Option A', 1: 'Option B', 2: 'Option C', 3: 'Option D'},
#         'q4': {0: 'Option A', 1: 'Option B', 2: 'Option C', 3: 'Option D'},
#         'q5': {0: 'Option A', 1: 'Option B', 2: 'Option C', 3: 'Option D'},
#         'q6': {0: 'Option A', 1: 'Option B', 2: 'Option C', 3: 'Option D'},
#         'q7': {0: 'Option A', 1: 'Option B', 2: 'Option C', 3: 'Option D'},
#         'q8': {0: 'Option A', 1: 'Option B', 2: 'Option C', 3: 'Option D'},
#     }

#     responses = SurveyResponse.objects.all()
#     total_responses = responses.count()

#     for response in responses:
#         try:
#             # Parse answers
#             answers = json.loads(response.answers or '[]')
#             correctness = [int(x) for x in (response.correctly_answered or '').split(',') if x]
            
#             # Track pass/fail
#             pass_fail_data['Pass' if response.passed else 'Fail'] += 1

#             # Track question responses and correctness
#             for i, (answer, correct) in enumerate(zip(answers, correctness), 1):
#                 q = f'q{i}'
#                 if answer:
#                     question_data[q][answer[0]] += 1
#                     correctness_data[q]['total'] += 1
#                     correctness_data[q]['correct'] += correct

#         except json.JSONDecodeError:
#             continue

#     # Prepare chart data
#     question_chart_data = {}
#     for q, counter in question_data.items():
#         labels = [question_options[q].get(k, str(k)) for k in sorted(counter.keys())]
#         values = [counter.get(k, 0) for k in sorted(counter.keys())]
#         question_chart_data[q] = {
#         'labels': labels,
#         'values': values,
#         'most_picked': question_options[q].get(counter.most_common(1)[0][0], str(counter.most_common(1)[0][0])),
#         'most_picked_count': counter.most_common(1)[0][1]
# }

#     correctness_chart_data = {
#         'labels': [f'Q{i}' for i in range(1, 9)],
#         'values': [
#             (data['correct'] / max(data['total'], 1) * 100) if data['total'] > 0 else 0
#             for data in correctness_data.values()
#         ]
#     }


#     pass_fail_pie_data = {
#         'labels': list(pass_fail_data.keys()),
#         'values': list(pass_fail_data.values())
#     }

#     context = {
#         'question_chart_data': question_chart_data,
#         'correctness_chart_data': correctness_chart_data,
#         'pass_fail_pie_data': pass_fail_pie_data,
#         'total_responses': total_responses,
#         'responses': responses  # For the user list table
#     }

#     return render(request, 'analytics.html', context)

# def download(request):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="survey_responses.csv"'

#     writer = csv.writer(response)
    
#     # Write header
#     headers = ['id', 'name', 'gender', 'score', 'passed']
#     headers.extend([f'Q{i}' for i in range(1, 9)])  # Q1 to Q8
#     headers.extend([f'Q{i}_correct' for i in range(1, 9)])  # Correctness for Q1 to Q8
#     writer.writerow(headers)

#     responses = SurveyResponse.objects.all()

#     for record in responses:
#         row = [
#             record.id,
#             record.name or '',
#             record.get_gender_display() if record.gender else '',
#             record.score,
#             'Pass' if record.passed else 'Fail'
#         ]

#         # Parse answers
#         answers = json.loads(record.answers or '[]')
#         for i in range(1, 9):
#             if i-1 < len(answers) and answers[i-1]:
#                 row.append(str(answers[i-1][0]))
#             else:
#                 row.append('')

#         # Parse correctness
#         correctness = [int(x) for x in (record.correctly_answered or '').split(',') if x]
#         for i in range(1, 9):
#             if i-1 < len(correctness):
#                 row.append('Correct' if correctness[i-1] else 'Incorrect')
#             else:
#                 row.append('')

#         writer.writerow(row)

#     return response


import json
import requests
from django.shortcuts import render
from .models import SurveyResponse

def index(request):
    CORRECT_ANSWERS = [3,0,2,3,2,2,1,2] 
    urls = [
        "https://services.api.unity.com/cloud-save/v1/data/projects/77f104be-1501-4cb5-b939-e690de43ec34/environments/002f4514-3bea-412a-a9dc-37e1ba68de0f/players/eYYj2HZdoxaLbigIRCburFmCM6va/items",
        "https://services.api.unity.com/cloud-save/v1/data/projects/77f104be-1501-4cb5-b939-e690de43ec34/environments/002f4514-3bea-412a-a9dc-37e1ba68de0f/players/eVp37K8ZPwKkYJF6fgE9dfWkke6o/items",
    ]
    
    headers = {
        "Authorization": "Basic MDgwMTMzNzktMzdlMy00YzE1LTk4ZjQtYjVjZWE2MmU4NmVhOlJBVUxUWFhwdHM2V3ZTR3ZCVVhVVW1zMXNkb2h2b3VP",
        "Content-Type": "application/json"
    }

    try:
        for url in urls:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            for item in data.get('results', []):
                key = item.get('key')
                value = item.get('value', {})
                answers = value.get('answers', [])
                player_answers = value.get('playerAnswers', [])
                gender = value.get('gender')
                player_name = value.get('playerName')
                score = value.get('score', 0)

                # Calculate correctness
                correctness = [1 if a == pa else 0 for a, pa in zip(player_answers,CORRECT_ANSWERS)]
                passed = score >= 5  # Passing threshold

                # SurveyResponse.objects.update_or_create(
                #     id=key,
                defaults={
                        'answers': json.dumps(answers),
                        'player_answers': json.dumps(player_answers),
                        'score': score,
                        'correctly_answered': ','.join(map(str, correctness)),
                        'passed': passed,
                        # 'gender': gender,
                        # 'player_name': player_name,
                    }
                if player_name is not None:
                    defaults['player_name'] = player_name
                if gender is not None:
                    defaults['gender'] = gender

                SurveyResponse.objects.update_or_create(
                        id=key,
                        defaults=defaults
                )
                

    except requests.exceptions.RequestException as e:
        print("API Error:", e)

    # responses = SurveyResponse.objects.all()
    # return render(request, 'index.html', {'responses': responses})
    # responses = SurveyResponse.objects.all()
    return analytics(request)

def analytics(request):
    responses = SurveyResponse.objects.all().order_by('-created_at')
    total = responses.count()
    
    # Pass/Fail stats
    pass_count = responses.filter(passed=True).count()
    fail_count = total - pass_count
    
    # Question analysis
    question_stats = []
    for q_num in range(8):
        correct = sum(1 for r in responses if len(r.get_correctness()) > q_num and r.get_correctness()[q_num] == 1)
        question_stats.append({
            'number': q_num + 1,
            'correct': correct,
            'percentage': round((correct / total) * 100, 2) if total > 0 else 0
        })
    
    # Most problematic questions (lowest correctness)
    problematic_questions = sorted(question_stats, key=lambda x: x['percentage'])[:8]
    
    gender_stats = [
        {
            'gender': 'Male',
            'pass_count': responses.filter(gender='M', passed=True).count(),
            'total': responses.filter(gender='M').count()
        },
        {
            'gender': 'Female',
            'pass_count': responses.filter(gender='F', passed=True).count(),
            'total': responses.filter(gender='F').count()
        }
    ]

    context = {
        'total_responses': total,
        'pass_count': pass_count,
        'fail_count': fail_count,
        'question_stats': question_stats,
        'problematic_questions': problematic_questions,
        'gender_stats': gender_stats,
        'responses': responses
    }
    return render(request, 'analytics.html', context)