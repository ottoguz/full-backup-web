from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
# from .models import Customers, Products, Suppliers, Entry_notes
# from .forms import CustomerForm, ProductsForm, SuppliersForm, Entry_notesForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

import subprocess
import time
import platform
import os

# Library for the GUI
from tkinter import *
from tkinter import filedialog


# Create your views here.

# view for the login template
def auth_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Bem vindo ao Full Backup, {username.capitalize()}")
            return redirect("home")
        else:
            messages.error(request, "Nome de usuário ou senha incorretos!")
    return render(request, "auth/login.html")

# View for the home page after login (to be developed)
def home(request):
    if request.user.is_authenticated:
        return render(request, "auth/home.html")
    else:
        messages.error(request, "Você deve estar logado para obter acesso ao Full Backup!")
        return redirect("login")
    
# Logout function
@login_required
def auth_logout(request):
    logout(request)
    messages.info(request, "Logout bem-sucedido")
    return redirect("login")
    
#View for the signup template
def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confpass = request.POST.get("confpass")
        if password != confpass:
            messages.error(request, "Sua senha e confirmação não conferem!")
        else:
            my_user = User.objects.create_user(username, email, password)
            my_user.save()
            my_user.clean_fields()
            messages.success(request, f"Usuário: {my_user.username} criado com êxito!")
            # send_email(username, email)
            return redirect("login")
    return render(request, "auth/signup.html")


# This function acknowledges which OS the program is running on
def select_os():
    os = platform.system()
    return os

source_dir = ''
def source_dir_func(response):
    global source_dir
    source_dir = filedialog.askdirectory()
    return JsonResponse({'source': source_dir})

dest_dir = ''
def dest_dir_func(response):
    global dest_dir
    dest_dir = filedialog.askdirectory()
    return JsonResponse({'destination': dest_dir})

class Backup:
    def __init__(self, time_now=time.strftime('%H:%M:%S'), date_now=time.strftime('%d-%m-%y')):
        self.__backup_destination = ''
        self.__backup_source = ''
        self.__time_now = time_now
        self.__date_now = date_now

    def get_time_now(self):
        return self.__time_now

    def get_date_now(self):
        return self.__date_now

    def open_move_file(self):
        if os == "Windows":
            open_file = "notepad " + file
            subprocess.run(open_file)
            cd = 'cd'
            current_folder = subprocess.getoutput(cd)
            log_to_folder = "move " + current_folder + '\\' + file + ' ' + self.__backup_destination
            subprocess.run(log_to_folder, shell=True)
            return file
        elif os == "Linux":
            open_file = "gedit " + file
            subprocess.run(open_file, shell=True)
            pwd = "pwd"
            current_folder = subprocess.getoutput(pwd)
            log_to_folder = "mv " + current_folder + "/" + file + " " + self.__backup_destination + "/" + file
            subprocess.run(log_to_folder, shell=True)
            return file

    # Header of the Full Backup display
    def header(self):
        time_now = Backup.get_time_now(self)
        header = '''
      ===========================================================================
    ||    ______ _    _ _      _       ____          _____ _  ___    _ _____     ||
    ||   |  ____| |  | | |    | |     |  _ \   /\   / ____| |/ / |  | |  __ \    ||
    ||   | |__  | |  | | |    | |     | |_)   /  \ | |    | ' /| |  | | |__) |   ||
    ||   |  __| | |  | | |    | |     |  _ < / /\ \| |    |  < | |  | |  ___/    ||
    ||   | |    | |__| | |____| |____ | |_) / ____ \ |____| . \| |__| | |        ||
    ||   |_|     \____/|______|______||____/_/    \_\_____|_|\_ \____/|_|        ||
    ||                                                                           ||
    ||                    FULL BACKUP FROM THE FILE SERVER                       ||
    ||                                                                           ||
      ===========================================================================
      ===========================================================================
                     FULL BACKUP FROM THE FILE SERVER BEGAN AT {}
      ===========================================================================
                    >>> CLOSE THE FILE TO SEND IT VIA EMAIL! <<<
        '''.format(time_now)
        return header

    def gen_backup(self):
        date_now = Backup.get_date_now(self)
        os = select_os()
        backup_file_name = 'full_backup_{}.tar.gz'.format(date_now)
        backup_source = source_dir
        self.__backup_source = backup_source
        backup_destination = dest_dir
        self.__backup_destination = backup_destination
        if os == "Linux":
            backup = 'cd ' + str(backup_destination) + ' && tar -cf {} "{}" '.format(backup_file_name, backup_source)
            subprocess.run(backup, shell=True)
            return backup
        elif os == "Windows":
            backup = 'cd /d ' + str(backup_destination) + ' && tar -cf {} "{}" '.format(backup_file_name, backup_source)
            subprocess.run(backup, shell=True)
            return backup

    def gen_list(self):
        os = select_os()
        if os == "Windows":
            files = "cd /d " + self.__backup_source + " && dir /s"
            files_out = subprocess.getoutput(files)
            return files_out
        elif os == "Linux":
            files = "cd " + self.__backup_source + " && ls"
            files_out = subprocess.getoutput(files)
            return files_out

    def generate_log(self):
        date_now = Backup().get_date_now()
        os = select_os()
        file_log = 'full_backup_log_{}.txt'.format(date_now)
        path_log = self.__backup_destination
        if os == "Linux":
            path_log = path_log + "/" + file_log
            return path_log
        elif os == "Windows":
            path_log = path_log + "\\" + file_log
            return path_log

    def footer(self):
        footer = '''
        ===========================================================================
                                     ENDED FULL BACKUP
                ENDING DATE/TIME  : {}  -  {}
                LOG FILE PATH     : {}
                BKP FILE PATH     : {}
        ===========================================================================
        '''.format(time.strftime('%d/%m/%y'), time.strftime('%H:%M:%S'), self.__backup_destination,
                   self.__backup_destination)
        return footer

    def subscribe_log(self, header, file_list, footer):
        file = 'full_backup_log_{}.txt'.format(time.strftime('%d-%m-%y'))
        f = open(file, 'w')
        f.write(header)
        f.write(file_list)
        f.write(footer)
        f.close()

    def send_email(self, from_email, to_email, pass_email):
        os = select_os()
        global file
        try:
            fromaddr = from_email
            toaddr = to_email
            password = pass_email

            msg = MIMEMultipart()

            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = 'Full backup logs to Xterm'

            body = '\n Please find attached the backup logs'

            msg.attach(MIMEText(body, 'plain'))

            file = 'full_backup_log_{}.txt'.format(time.strftime('%d-%m-%y'))
            attachment = open(file, 'rb')

            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment.read()))
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename= {}'.format(file))

            msg.attach(part)

            attachment.close()

            server = smtplib.SMTP('smtp.hostinger.com.br', 587)
            server.starttls()
            server.login(fromaddr, password)
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()

            self.open_move_file()

        except:

            self.open_move_file()


backup = Backup()

def start_backup(request):
    if request.method == "POST":
        backup.gen_backup()
        backup.generate_log()
    return render(request, "auth/home.html")
    