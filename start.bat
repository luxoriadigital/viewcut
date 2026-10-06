@echo off
title Viewcut - local server
cd /d "%~dp0"
start "" http://localhost:5174
node serve.js
