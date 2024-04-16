from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
import subprocess
import os


def index(request):
    return render(request, 'myapp/index.html')


def presentation_view(request):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to presentation_control.py
    presentation_control_path = os.path.join(current_dir, 'presentation_control.py')

    # Execute presentation_control.py and capture its output
    try:
        output = subprocess.check_output(['python', presentation_control_path], stderr=subprocess.STDOUT)
        message = "Execution successful"
    except subprocess.CalledProcessError as e:
        output = e.output
        message = "Execution failed"

    # Format the output message with HTML
    html_response = f"""
   <!DOCTYPE html>
    <html>
    <head>
        <title>Execution Status</title>
        <link rel="stylesheet" type="text/css" href="{settings.STATIC_URL}style.css">
        <style>
            .button-wrapper {{
                text-align: right;
            }}

            .button {{
                background-color: #b9d5ef;
                color: black;
                padding: 10px 157px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s;
                margin-left: 10px; /* Add margin to the left side */
            }}

            .button:hover {{
                background-color: #a4c0db;
            }}
        </style>
    </head>
    <body>

  <footer class="footer section has-bg-image text-center"
    style="background-image: url({settings.STATIC_URL}4.png")">
    <div class="container">

      <div class="footer-top grid-list">

        <div class="footer-brand has-before has-after">

          <a href="#" class="logo">
             <img src="{settings.STATIC_URL}logo.png" alt="Logo" width="160" height="80" loading="lazy">
          </a>

          <address class="body-4">
            Elevate your presentations with GestureVerse
          </address>
        <br>
         <br>
          <a href="mailto:booking@GestureVerse.com" class="body-4 contact-link">booking@GestureVerse.com</a>
          <div class="wrapper">
            <div class="separator"></div>
            <div class="separator"></div>
            <div class="separator"></div>
          </div>

          <p class="title-1">Your Execution was successful</p>
<br>
          <form action="" class="input-wrapper">
    <div class="button-wrapper">
        <a href="/">
            <button type="button" class="button">
                <span class="text text-1">Go to Home Page</span>
            </button>
        </a>
    </div>
</form>


        </div>

        <ul class="footer-list">

          <li>
            <a href="#" class="label-2 footer-link hover-underline">Home</a>
          </li>

          <li>
            <a href="#" class="label-2 footer-link hover-underline">Menus</a>
          </li>

          <li>
            <a href="#" class="label-2 footer-link hover-underline">About Us</a>
          </li>

          <li>
            <a href="#" class="label-2 footer-link hover-underline">Our Specialities</a>
          </li>

          <li>
            <a href="#" class="label-2 footer-link hover-underline">Contact</a>
          </li>

        </ul>

        <ul class="footer-list">

          <li>
            <a href="#" class="label-2 footer-link hover-underline">Facebook</a>
          </li>

          <li>
            <a href="#" class="label-2 footer-link hover-underline">Instagram</a>
          </li>

          <li>
            <a href="#" class="label-2 footer-link hover-underline">Twitter</a>
          </li>

          <li>
            <a href="#" class="label-2 footer-link hover-underline">Youtube</a>
          </li>

          <li>
            <a href="#" class="label-2 footer-link hover-underline">Google Map</a>
          </li>

        </ul>

      </div>

      <div class="footer-bottom">

        <p class="copyright">
          &copy; 2024 GestureVerse. All Rights Reserved | Crafted by <a href="#"
            target="_blank" class="link">GestureVerse</a>
        </p>

      </div>

    </div>
  </footer>
    </body>
    </html>
    """

    # Return the HTML response
    return HttpResponse(html_response)


def blackboard_view(request):
    # Get the directory containing views.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to virtual_blackboard.py
    virtual_blackboard_path = os.path.join(current_dir, 'virtual_blackboard.py')

    # Execute virtual_blackboard.py and capture its output
    try:
        output = subprocess.check_output(['python', virtual_blackboard_path], stderr=subprocess.STDOUT)
        message = "Execution successful"
    except subprocess.CalledProcessError as e:
        output = e.output
        message = "Execution failed"

    # Format the output message with HTML
    html_response = f"""
   <!DOCTYPE html>
    <html>
    <head>
        <title>Execution Status</title>
        <link rel="stylesheet" type="text/css" href="{settings.STATIC_URL}style.css">
        <style>
            .button-wrapper {{
                text-align: right;
            }}

            .button {{
                background-color: #b9d5ef;
                color: black;
                padding: 10px 157px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s;
                margin-left: 10px; /* Add margin to the left side */
            }}

            .button:hover {{
                background-color: #a4c0db;
            }}
        </style>
    </head>
    <body>

  <footer class="footer section has-bg-image text-center"
    style="background-image: url({settings.STATIC_URL}4.png")">
    <div class="container">

      <div class="footer-top grid-list">

        <div class="footer-brand has-before has-after">

          <a href="#" class="logo">
             <img src="{settings.STATIC_URL}logo.png" alt="Logo" width="160" height="80" loading="lazy">
          </a>

          <address class="body-4">
            Elevate your presentations with GestureVerse
          </address>
        <br>
         <br>
          <a href="mailto:booking@GestureVerse.com" class="body-4 contact-link">booking@GestureVerse.com</a>

          <div class="wrapper">
            <div class="separator"></div>
            <div class="separator"></div>
            <div class="separator"></div>
          </div>

          <p class="title-1">Your Execution was successful</p>
<br>
          <form action="" class="input-wrapper">
    <div class="button-wrapper">
        <a href="/">
            <button type="button" class="button">
                <span class="text text-1">Go to Home Page</span>
            </button>
        </a>
    </div>
</form>


        </div>

        <ul class="footer-list">

          <li>
            <a href="#" class="label-2 footer-link hover-underline">Home</a>
          </li>

          <li>
            <a href="#" class="label-2 footer-link hover-underline">Menus</a>
          </li>

          <li>
            <a href="#" class="label-2 footer-link hover-underline">About Us</a>
          </li>

          <li>
            <a href="#" class="label-2 footer-link hover-underline">Our Specialities</a>
          </li>

          <li>
            <a href="#" class="label-2 footer-link hover-underline">Contact</a>
          </li>

        </ul>

        <ul class="footer-list">

          <li>
            <a href="#" class="label-2 footer-link hover-underline">Facebook</a>
          </li>

          <li>
            <a href="#" class="label-2 footer-link hover-underline">Instagram</a>
          </li>

          <li>
            <a href="#" class="label-2 footer-link hover-underline">Twitter</a>
          </li>

          <li>
            <a href="#" class="label-2 footer-link hover-underline">Youtube</a>
          </li>

          <li>
            <a href="#" class="label-2 footer-link hover-underline">Google Map</a>
          </li>

        </ul>

      </div>

      <div class="footer-bottom">

        <p class="copyright">
          &copy; 2024 GestureVerse. All Rights Reserved | Crafted by <a href="#"
            target="_blank" class="link">GestureVerse</a>
        </p>

      </div>

    </div>
  </footer>
    </body>
    </html>
    """
    # Return the HTML response
    return HttpResponse(html_response)


def zoom_view(request):
    # Get the directory containing views.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to zoom.py
    zoom_path = os.path.join(current_dir, 'zoom.py')

    # Execute virtual_blackboard.py and capture its output
    try:
        output = subprocess.check_output(['python', zoom_path], stderr=subprocess.STDOUT)
        message = "Execution successful"
    except subprocess.CalledProcessError as e:
        output = e.output
        message = "Execution failed"

    # Format the output message with HTML
    html_response = f"""
   <!DOCTYPE html>
    <html>
    <head>
        <title>Execution Status</title>
        <link rel="stylesheet" type="text/css" href="{settings.STATIC_URL}style.css">
        <style>
            .button-wrapper {{
                text-align: right;
            }}

            .button {{
                background-color: #b9d5ef;
                color: black;
                padding: 10px 157px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s;
                margin-left: 10px; /* Add margin to the left side */
            }}

            .button:hover {{
                background-color: #a4c0db;
            }}
        </style>
    </head>
    <body>

  <footer class="footer section has-bg-image text-center"
    style="background-image: url({settings.STATIC_URL}4.png")">
    <div class="container">

      <div class="footer-top grid-list">

        <div class="footer-brand has-before has-after">

          <a href="#" class="logo">
             <img src="{settings.STATIC_URL}logo.png" alt="Logo" width="160" height="80" loading="lazy">
          </a>

          <address class="body-4">
            Elevate your presentations with GestureVerse
          </address>
        <br>
         <br>
          <a href="mailto:booking@GestureVerse.com" class="body-4 contact-link">booking@GestureVerse.com</a>

          <div class="wrapper">
            <div class="separator"></div>
            <div class="separator"></div>
            <div class="separator"></div>
          </div>

          <p class="title-1">Your Execution was successful</p>
<br>
          <form action="" class="input-wrapper">
    <div class="button-wrapper">
        <a href="/">
            <button type="button" class="button">
                <span class="text text-1">Go to Home Page</span>
            </button>
        </a>
    </div>
</form>


        </div>

        <ul class="footer-list">

          <li>
            <a href="#" class="label-2 footer-link hover-underline">Home</a>
          </li>

          <li>
            <a href="#" class="label-2 footer-link hover-underline">Menus</a>
          </li>

          <li>
            <a href="#" class="label-2 footer-link hover-underline">About Us</a>
          </li>

          <li>
            <a href="#" class="label-2 footer-link hover-underline">Our Specialities</a>
          </li>

          <li>
            <a href="#" class="label-2 footer-link hover-underline">Contact</a>
          </li>

        </ul>

        <ul class="footer-list">

          <li>
            <a href="#" class="label-2 footer-link hover-underline">Facebook</a>
          </li>

          <li>
            <a href="#" class="label-2 footer-link hover-underline">Instagram</a>
          </li>

          <li>
            <a href="#" class="label-2 footer-link hover-underline">Twitter</a>
          </li>

          <li>
            <a href="#" class="label-2 footer-link hover-underline">Youtube</a>
          </li>

          <li>
            <a href="#" class="label-2 footer-link hover-underline">Google Map</a>
          </li>

        </ul>

      </div>

      <div class="footer-bottom">

        <p class="copyright">
          &copy; 2024 GestureVerse. All Rights Reserved | Crafted by <a href="#"
            target="_blank" class="link">GestureVerse</a>
        </p>

      </div>

    </div>
  </footer>
    </body>
    </html>
    """
    # Return the HTML response
    return HttpResponse(html_response)

