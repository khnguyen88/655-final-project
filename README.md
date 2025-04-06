# 655 Final Project

## Personal Setup Process - FRONTEND

-   Download latest NodeJS or Change Node Version w/ NVM

-   Install Angular
    `npm install -g @angular/cli`

-   Create New Angular Proj
    `ng new 655-final-project-frontend --no-standalone`

    -   Stylesheet Format: Sass (SCSS)
    -   Enable Server-Side Rnedering SSR and Static Site Gneration: No

-   Move Into Angular Project Folder: `cd 655-final-project-frontend`

-   Install other dependencies
    `npm install rxjs`
    `npm install primeng @primeng/themes`
    `npm i primeflex`
    `npm install @angular/animations`

-   Create Images Service
    `ng generate service service/images`

-   Create Components
    `ng generate component component/results-history-gallery`
    `ng generate component component/file-upload-form`

-   Create Folder called "envrionment" in the src/app/ folder path
-   Create a file called "envrionment.ts" in the src/app/envrionment folder

    -   This will hold the baseUrl and basePaths for the various endpoints

-   Created a subfolder in the angular poject folder called "private" It will contain eventually contain two files:

    -   "environment.ts": contains base url and paths to the cloud application endpoints
    -   "security.ts": contains secuirty information to access the cloud application endpoints

-   Add the "/private" path in the .gitignore file.

-   Find templates of the files required for the "private" folder in the "template" folder. Copy those files in your local "private" folder and fill-in the appropiate details.

-   Need to configure angular project to use prime-ng theme properly to show proper color theme. It's a whole process. Follow the instructions from this guide:

    -   https://primeng.org/theming

-   We will also need to install Tailwind for angular to apply the theme properly to show proper fonts. Follow the instructions from this guide:
    -   https://tailwindcss.com/docs/installation/framework-guides/angular
    -   https://primeng.org/tailwind

## Backend Setup
