# 655-final-project-frontend

-   Download latest NodeJS or Change Node Version w/ NVM
-   Install Angular
    `npm install -g @angular/cli`

-   Create New Angular Proj
    `ng new 655-project-frontend`

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
