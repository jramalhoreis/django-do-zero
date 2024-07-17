

from django.urls import path

from polls.views import (
                        index,ola,
                        QuestionCreateView, question_create, 
                        QuestionUpdateView, question_update,
                        QuestionDeleteView, question_delete)

from polls import views

urlpatterns = [

    path('', index, name='index'),
    path('index/<str:categoria>', index, name='index'),

    path('ola/', ola, name='ola'),
    path('polls/create', QuestionCreateView.as_view(), name="question_create_view"),
    path('polls/add', question_create, name='question_create'),

    path('polls/update/<int:pk>', QuestionUpdateView.as_view(), name="question_update_view"),
    path('polls/edit/<int:question_id>', question_update, name='question_update'),

    path('polls/delete/<int:pk>', QuestionDeleteView.as_view(), name="question_delete_view"),
    path('polls/remove/<int:question_id>', question_delete, name='question_remove'),


    path('polls/enquete/<int:pk>/show', views.QuestionDetailView.as_view(), name='question_detail'),

    path('polls/list', views.QuestionListView.as_view(), name='polls_list'),

    path('about-us', views.SobreTemplateView.as_view(), name='about_page'),

    path('enquete/<int:question_id>/vote', views.vote, name="poll_vote"),

    path('enquete/<int:question_id>/result', views.results, name='polls_results'),

    path('enquete/<int:pk>/alternativa/add', views.ChoiceCreateView.as_view(), name='choice_add'),

    path('enquete/<int:pk>/alternativa/edit', views.ChoiceUpdateView.as_view(), name='choice_edit'),

    path('enquete/<int:pk>/alternativa/delete', views.ChoiceDeleteView.as_view(), name='choice_delete'),

    path('enquete/import', views.QuestionImportView.as_view(), name='question_import'),

    path('question_send/<int:question_id>', views.poll_send, name='question_send'),

    path('questions/export/csv', views.questions_export_csv, name='questions_export_csv'),

    path('api/questions', views.get_all_questions, name='questions_data'),

]





