# 655-final-project-frontend

# Personal Setup Process

-   Download latest NodeJS or Change Node Version w/ NVM

-   Install Angular
    `npm install -g @angular/cli`

-   Create New Angular Proj
    `ng new 655-final-project-frontend`

    -   Stylesheet Format: Sass (SCSS)
    -   Enable Server-Side Rnedering SSR and Static Site Gneration: No

-   Move Into Angular Project Folder: `cd 655-final-project-frontend`

-   Install other dependencies
    `npm install rxjs`
    `npm install primeng @primeng/themes`

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
