-- Active: 1778121948956@@127.0.0.1@3306@mysql
# root계정으로 실행

# 모든 host에서 접근가능한 django계정 생성(비밀번호 django)
-- create user 'django'@'%' identified by 'django';

# qnadb 생성
create database qnadb character set utf8mb4 collate utf8mb4_unicode_ci;

# django사용자에게 qnadb 권한 부여
grant all privileges on qnadb.* to 'django'@'%';
flush privileges;