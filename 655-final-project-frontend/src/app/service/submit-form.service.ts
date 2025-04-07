import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { catchError, Observable, throwError } from 'rxjs';
import { environment } from '../../../private/environment';

@Injectable({
  providedIn: 'root'
})
export class SubmitFormService {

  constructor(private http: HttpClient) { 
  }

  submitForm(urlString: string): Observable<any>{
    return this.http.post(environment.submitImageForColorEvaluationURLPath, urlString)
      .pipe(
        catchError(this.handleError)
      );
  }

  // Error Handling Source: https://v17.angular.io/guide/http-handle-request-errors
  private handleError(error: HttpErrorResponse) {
    if (error.status === 0) {
      // A client-side or network error occurred. Handle it accordingly.
      console.error('An error occurred:', error.error);
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong.
      console.error(
        `Backend returned code ${error.status}, body was: `, error.error);
    }
    // Return an observable with a user-facing error message.
    return throwError(() => new Error('Something bad happened; please try again later.'));
  }
}
