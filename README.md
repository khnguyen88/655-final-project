# 655 Final Project

## Cloned Project Setup Process - FRONTEND

-   Copy project folder from git repository
-   Change directory to the 655-final-project-frontend subfolder
-   Run `npm install`
-   Rename the subfolder, **private_template** to **private**, this should make your folder ignored by git
-   In the **private** folder, in the **environment.ts** file update the URL paths to the correct cloud services endpoints that you created using the **Backend Tutorial**
-   Run `ng serve` (to test application)
-   Run `ng build` (to build your production files for deployment). The files will be stored in the `dist` folder
-   Open up your project on your Google Cloud Console
-

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
    `npm install primeflex --save`
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

-   Need to import specific primeng and primeflex related styles into the angular project's styles.scss file:
    `@import "tailwindcss";`
    `@import 'primeflex/primeflex.scss';`

-   WRITE AND ITERATE THROUGH CODE

-   Update Environment file with the correct url paths to the cloud application or services endpoints

-   Run `ng build`

-   If you get a build error, Adjust Angular JSON to Increase Budget for Production (Situational. Set to Whats Needed)

    -   https://stackoverflow.com/questions/78093540/angular-build-warning-bundle-initial-exceeded-maximum-budget-i-know-how-to-re

        ```
        "configurations": {
                    "production": {
                    "budgets": [
                        {
                        "type": "initial",
                        "maximumWarning": "2000kb",
                        "maximumError": "5600kb"
                        },
        ```

## Backend Setup
