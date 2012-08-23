# *****************************************************************************
#
#   BUILDER
#
#   This is my program for organizing all the random related files on my local
#   machine into the form needed to publish to my website. This file contains
#   links to all local projects and the end-destinations they should reside in
#   under the website project.
#
# ******************************************************************************
#
#   Structure:
#       ~\projects
#           \appspot
#               \helloworld
#               \ndonnellan     <- ndonnellan.appspot.com
#                   \img
#                   \scripts
#                   \stylesheets
#                   \templates
#           \ecosystem
#               \img
#               \scripts
#               \stylesheets
#           \titanium
#           \sandbox
#           \balsamiq
#           
# Process Flow
#   - Move HTML files to the templates directory
#   - Move all Javascript files to the scripts dir
#       - Combine and minify all the javascript into one file (making sure
#         to keep the correct calling order of all functions/classes)
#   - Move all CSS files to the stylesheets dir
#       - Update paths to images in the CSS files to reflect
#         the changed paths
#   - Move all Images to the images dir

import os, re
import shutil, fileinput

paths = {} # Dictionary to hold paths
paths['proj'] = '/Users/ndonnellan/projects'
paths['app'] = paths['proj'] + '/appspot/ndonnellan'
paths['tpl'] = paths['app'] + '/templates'
paths['css'] = paths['app'] + '/stylesheets'
paths['scrp'] = paths['app'] + '/scripts'
paths['img'] = paths['app'] + '/img'

def list_files(some_path, regexp):
    files = []
    for dirname, dirnames, filenames in os.walk(some_path):

        for subdirname in dirnames:
            if not re.search(subdirname,r'^\.'):
                files += list_files(os.path.join(dirname, subdirname), regexp)

        for f in filenames:
            if re.search(regexp, f):
                files.append(os.path.join(dirname, f))

    return files

def filename(path_str):
    return re.search(r'[^/]+$',path_str).group(0)

def copy_list(src_path, regexp, dest_path):
    print 'Moving ' + src_path + ' to ' + dest_path
    for f in list_files(src_path, regexp):
        shutil.copyfile(f, dest_path + '/' + filename(f))

def moveProject(project_name, project_path):
    copy_list(project_path, r'\.js', paths['scrp'])
    copy_list(project_path, r'\.html', paths['tpl'])
    copy_list(project_path, r'\.css', paths['css'])
    copy_list(project_path, r'\.png', paths['img'])


moveProject('ecosystem', paths['proj'] + '/ecosystem')

# Replace URLs in the jquery-ui CSS file that refer to images and point
# them to /img
jqueryui_file = list_files(paths['img'], r'/jquery\-ui')

if jqueryui_file:
    for line in fileinput.FileInput(jqueryui_file,inplace=1):
        line = line.replace('url(images','url(/img')


