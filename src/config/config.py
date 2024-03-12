# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
file help to setup settings.yaml file
@author <anujy@simplifyvms.com>
"""
import os
from dynaconf import Dynaconf
import src.config.settings as aws_settings
settings = Dynaconf(
    settings_files=['settings.yaml'],
)
if settings.env == "PRODUCTION":
    if settings.enable == True:
        # env = os.getenv("BUILD_ENV")
        env = 'dev'
        secret_aws: str = settings[settings.get('env')].get(
            'aws').get('aws_secret_name')
        aws_secret = aws_settings.get_secret(env, secret_aws)
        prod = settings.production
        prod['DATABASES']['DB_ENGINE'] = aws_secret.get("docdbEngine")
        prod['DATABASES']['DB_HOST'] = aws_secret.get("docdbHost")
        prod['DATABASES']['DB_PORT'] = aws_secret.get("docdbPort")
        prod['DATABASES']['DB_USERNAME'] = aws_secret.get("docdbUserName")
        prod['DATABASES']['DB_PASSWORD'] = aws_secret.get("docdbPassword")
        prod['DATABASES']['DB_NAME'] = aws_secret.get("docdbName")
        prod['DATABASES']['DB_CLUSTERIDENTIFIER'] = aws_secret.get(
            "docdbClusterIdentifier")
        prod['AWS']['REDIS_HOST'] = aws_secret.get("redisHost")
        prod['AWS']['REDIS_PORT'] = aws_secret.get("redisPort")
        prod['AWS']['REDIS_PASSWORD'] = aws_secret.get("redisPassword")
        prod['API_KEY']['GOOGLE_API_KEY'] = aws_secret.get("google_geo_location")
        host = aws_secret.get("sesHost")
        port = aws_secret.get("sesPort")
        user = aws_secret.get("sesUsername")
        password = aws_secret.get("sesPassword")
