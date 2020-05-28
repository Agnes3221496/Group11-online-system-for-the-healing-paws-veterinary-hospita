# -*- coding:utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))
# 发送者邮箱的服务器地址



class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'petvet.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    QUESTION_IMAGE_UPLOAD_DIR = os.path.join(basedir, 'static/uploaded_image/question_image')
    PET_IMAGE_UPLOAD_DIR = os.path.join(basedir, 'static/uploaded_image/pet_image')

    LANGUAGES = {
        'en': 'English',
        'zh': '简体中文'
    }
    # reference: https: // www.thinbug.com / q / 42393831
