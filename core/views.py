from django.shortcuts import render, redirect
from admin_volt.forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserPasswordChangeForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,FileResponse
import pandas as pd
import joblib
import random
# pdf imports
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


# Index
def index(request):
  return render(request, 'pages/index.html')
# Index
def flood_result(request):
  return render(request, 'pages/flood/flood_result.html')

# flood
def flood(request):
    if request.method == 'POST':
        print(request.POST.get('MonsoonIntensity'))
        print(request.POST.get('TopographyDrainage'))
        has_user_input = any(request.POST.get(field) for field in ['MonsoonIntensity', 'TopographyDrainage', 'RiverManagement', 'Deforestation', 'Urbanization', 'ClimateChange', 'DamsQuality', 'Siltation', 'AgriculturalPractices', 'Encroachments', 'IneffectiveDisasterPreparedness', 'DrainageSystems', 'CoastalVulnerability', 'Landslides', 'Watersheds', 'DeterioratingInfrastructure', 'PopulationScore', 'WetlandLoss', 'InadequatePlanning', 'PoliticalFactors'])

        if has_user_input:
            # Retrieve user input from the form
            MonsoonIntensity = int(request.POST.get('MonsoonIntensity'))
            TopographyDrainage = int(request.POST.get('TopographyDrainage'))
            RiverManagement = int(request.POST.get('RiverManagement'))
            Deforestation = int(request.POST.get('Deforestation'))
            Urbanization = int(request.POST.get('Urbanization'))
            ClimateChange = int(request.POST.get('ClimateChange'))
            DamsQuality = int(request.POST.get('DamsQuality'))
            Siltation = int(request.POST.get('Siltation'))
            AgriculturalPractices = int(request.POST.get('AgriculturalPractices'))
            Encroachments = int(request.POST.get('Encroachments'))
            IneffectiveDisasterPreparedness = int(request.POST.get('IneffectiveDisasterPreparedness'))
            DrainageSystems = int(request.POST.get('DrainageSystems'))
            CoastalVulnerability = int(request.POST.get('CoastalVulnerability'))
            Landslides = int(request.POST.get('Landslides'))
            Watersheds = int(request.POST.get('Watersheds'))
            DeterioratingInfrastructure = int(request.POST.get('DeterioratingInfrastructure'))
            PopulationScore = int(request.POST.get('PopulationScore'))
            WetlandLoss = int(request.POST.get('WetlandLoss'))
            InadequatePlanning = int(request.POST.get('InadequatePlanning'))
            PoliticalFactors = int(request.POST.get('PoliticalFactors'))

            # Construct input data as a dictionary
            data = {
                'MonsoonIntensity': [MonsoonIntensity],
                'TopographyDrainage': [TopographyDrainage],
                'RiverManagement': [RiverManagement],
                'Deforestation': [Deforestation],
                'Urbanization': [Urbanization],
                'ClimateChange': [ClimateChange],
                'DamsQuality': [DamsQuality],
                'Siltation': [Siltation],
                'AgriculturalPractices': [AgriculturalPractices],
                'Encroachments': [Encroachments],
                'IneffectiveDisasterPreparedness': [IneffectiveDisasterPreparedness],
                'DrainageSystems': [DrainageSystems],
                'CoastalVulnerability': [CoastalVulnerability],
                'Landslides': [Landslides],
                'Watersheds': [Watersheds],
                'DeterioratingInfrastructure': [DeterioratingInfrastructure],
                'PopulationScore': [PopulationScore],
                'WetlandLoss': [WetlandLoss],
                'InadequatePlanning': [InadequatePlanning],
                'PoliticalFactors': [PoliticalFactors]
            }

            # Convert input data to DataFrame
            input_data = pd.DataFrame(data)
        else:
            input_data = pd.read_csv(request.FILES['csv_upload'])

        # Load saved models (when you need to make predictions)
        svr_model = joblib.load('D:/projects/Flood_Earthquake2024/venv/Lib/site-packages/admin_volt/svr_model.pkl')
        dt_model = joblib.load('D:/projects/Flood_Earthquake2024/venv/Lib/site-packages/admin_volt/dt_model.pkl')
        mlp_model = joblib.load('D:/projects/Flood_Earthquake2024/venv/Lib/site-packages/admin_volt/mlp_model.pkl')
        lr_model = joblib.load('D:/projects/Flood_Earthquake2024/venv/Lib/site-packages/admin_volt/lr_model.pkl')

        # Make predictions
        svr_prediction = svr_model.predict(input_data)
        dt_prediction = dt_model.predict(input_data)
        mlp_prediction = mlp_model.predict(input_data)
        lr_prediction = lr_model.predict(input_data)


        # Combine predictions with input data
        input_data['SVR_Prediction'] = svr_prediction
        input_data['DecisionTree_Prediction'] = dt_prediction
        input_data['MLP_Prediction'] = mlp_prediction
        input_data['LinearRegression_Prediction'] = lr_prediction


        # Convert DataFrame to dictionary for rendering in template
        result_data = input_data.to_dict(orient='records')

        # Print predictions
        print(result_data)
        print("SVR Prediction:", svr_prediction)
        print("Decision Tree Prediction:", dt_prediction)
        print("MLP Prediction:", mlp_prediction)
        print("Linear Regression Prediction:", lr_prediction)


        # Update the context to include predictions
        context = {
            'segment': 'flood',
            'svr_prediction': svr_prediction[0],
            'dt_prediction': dt_prediction[0],
            'mlp_prediction': mlp_prediction[0],
            'lr_prediction': lr_prediction[0],
            'result_data': result_data,
        }

        return render(request, 'pages/flood/flood_result.html', context)
    else:
        # Render the initial form if it's a GET request
        return render(request, 'pages/flood/flood.html')

# Pages
@login_required(login_url="/accounts/login/")
def transaction(request):
  context = {
    'segment': 'transactions'
  }
  return render(request, 'pages/transactions.html', context)

@login_required(login_url="/accounts/login/")
def settings(request):
  context = {
    'segment': 'settings'
  }
  return render(request, 'pages/settings.html', context)

# Tables
@login_required(login_url="/accounts/login/")
def bs_tables(request):
  context = {
    'parent': 'tables',
    'segment': 'bs_tables',
  }
  return render(request, 'pages/tables/bootstrap-tables.html', context)

# Components
@login_required(login_url="/accounts/login/")
def buttons(request):
  context = {
    'parent': 'components',
    'segment': 'buttons',
  }
  return render(request, 'pages/components/buttons.html', context)

@login_required(login_url="/accounts/login/")
def notifications(request):
  context = {
    'parent': 'components',
    'segment': 'notifications',
  }
  return render(request, 'pages/components/notifications.html', context)

@login_required(login_url="/accounts/login/")
def forms(request):
  context = {
    'parent': 'components',
    'segment': 'forms',
  }
  return render(request, 'pages/components/forms.html', context)

@login_required(login_url="/accounts/login/")
def modals(request):
  context = {
    'parent': 'components',
    'segment': 'modals',
  }
  return render(request, 'pages/components/modals.html', context)

@login_required(login_url="/accounts/login/")
def typography(request):
  context = {
    'parent': 'components',
    'segment': 'typography',
  }
  return render(request, 'pages/components/typography.html', context)


# Authentication
def register_view(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      print("Account created successfully!")
      form.save()
      return redirect('/accounts/login/')
    else:
      print("Registration failed!")
  else:
    form = RegistrationForm()
  
  context = { 'form': form }
  return render(request, 'accounts/sign-up.html', context)

class UserLoginView(LoginView):
  form_class = LoginForm
  template_name = 'accounts/sign-in.html'

class UserPasswordChangeView(PasswordChangeView):
  template_name = 'accounts/password-change.html'
  form_class = UserPasswordChangeForm

class UserPasswordResetView(PasswordResetView):
  template_name = 'accounts/forgot-password.html'
  form_class = UserPasswordResetForm

class UserPasswrodResetConfirmView(PasswordResetConfirmView):
  template_name = 'accounts/reset-password.html'
  form_class = UserSetPasswordForm

def logout_view(request):
  logout(request)
  return redirect('/accounts/login/')

def lock(request):
  return render(request, 'accounts/lock.html')

# Errors
def error_404(request):
  return render(request, 'pages/examples/404.html')

def error_500(request):
  return render(request, 'pages/examples/500.html')

# Extra
def upgrade_to_pro(request):
  return render(request, 'pages/upgrade-to-pro.html')
