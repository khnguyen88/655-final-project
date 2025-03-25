import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../private/environment';

@Injectable({
  providedIn: 'root'
})
export class ImagesService {

  constructor(private http: HttpClient) { 
  }

  getSearchResultsHistory(): Observable<any>{
    return this.http.get(environment.getSearchResultsHistoryPathName);
  }
}
