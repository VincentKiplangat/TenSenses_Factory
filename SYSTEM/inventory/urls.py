from django.urls import path
from . import views

urlpatterns = [
    # Batches
    path('', views.batch_list, name='inventory_home'),
    path('batches/', views.batch_list, name='batch_list'),
    path('batches/create/', views.create_batch, name='create_batch'),
    path('batches/<int:pk>/', views.batch_detail, name='batch_detail'),
    path('batches/<int:pk>/update/', views.update_batch, name='update_batch'),
    path('batches/<int:pk>/delete/', views.delete_batch, name='delete_batch'),

    # Normal SKR
    path('<int:pk>/add-normal-skr/', views.add_normal_skr, name='add_normal_skr'),
    path('edit-sample/<int:pk>/', views.edit_sample, name='edit_sample'),
    path('sample/<int:pk>/delete/', views.delete_sample, name='delete_sample'),

    # Moisture SKR
    path('inventory/<int:pk>/add-moisture-skr/', views.add_moisture_skr, name='add_moisture_skr'),
    path('sample/moisture/edit/<int:pk>/', views.edit_moisture_skr, name='edit_moisture_skr'),
    path('sample/moisture/delete/<int:pk>/', views.delete_moisture_skr, name='delete_moisture_skr'),

    # AJAX endpoints
    path('ajax/get-store-region/<int:fo_id>/', views.get_store_and_region, name='get_store_and_region'),
    path('ajax/get-stores/<int:region_id>/', views.get_stores_by_region, name='ajax_get_stores'),
    path('ajax/get-field-officers/<int:store_id>/', views.get_field_officers_by_store, name='ajax_get_fos'),

    # Downloads
    path('batches/<int:batch_id>/download_normal_skr/', views.download_normal_skr, name='download_normal_skr'),
    path('batches/<int:batch_id>/download_skr_moisture/', views.download_skr_moisture, name='download_skr_moisture'),
    path('download_fo_average/<int:batch_id>/', views.download_fo_average, name='download_fo_average'),
    # path('batch/<int:batch_id>/download-combined/', views.download_combined_excel, name='download_combined_excel'),
    # path('batches/<int:batch_id>/download-combined/', views.download_combined_skr_excel, name='download_combined_excel'),
path('batches/<int:batch_id>/download-combined/', views.download_combined_skr_excel, name='download_combined_skr_excel'),
path('batch/<int:batch_id>/download-combined/', views.download_combined_excel, name='download_combined_excel'),



    # Region CRUD
    path('regions/', views.create_region, name='create_region'),
    path('regions/delete/<int:pk>/', views.delete_region, name='delete_region'),

    # Store CRUD
    path('store/add/', views.create_store, name='create_store'),
    path('store/delete/<int:pk>/', views.delete_store, name='delete_store'),

    # Field Officer CRUD
    path('field-officers/', views.create_field_officer, name='create_field_officer'),
    path('field-officer/delete/<int:pk>/', views.delete_field_officer, name='delete_field_officer'),


    # path('batch/<int:batch_id>/sizing-report/', views.sizing_report_view, name='sizing_report'),
    path('batch/<int:batch_id>/download-sizing-excel/', views.download_sizing_data_excel, name='download_sizing_data_excel'),

path('batches/<int:pk>/', views.batch_detail, name='batch_detail'),
path('batches/<int:pk>/receiving/', views.receiving_detail, name='receiving_detail'),

# Processing Stages
path('batches/<int:pk>/nut-washing/', views.nut_washing_view, name='nut_washing'),
path('batches/<int:pk>/drying/', views.drying_view, name='drying'),
path('batches/<int:pk>/drier-offloading/', views.drier_offloading_view, name='drier_offloading'),
path('batches/<int:pk>/cracking/', views.cracking_view, name='cracking'),
path('batches/<int:pk>/inshell-sorting/', views.inshell_sorting_view, name='inshell_sorting'),
path('batches/<int:pk>/kernel-sorting/', views.kernel_sorting_view, name='kernel_sorting'),
path('batches/<int:pk>/grading/', views.grading_view, name='grading'),
path('batches/<int:pk>/packaging/', views.packaging_view, name='packaging'),


]


