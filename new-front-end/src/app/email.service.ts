import { environment } from '../environments/environment';
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

console.log(environment.apiUrl); // Use the variable


@Injectable({
  providedIn: 'root'
})
export class EmailService {

  private url: string = environment.apiUrl;

  constructor(private http:HttpClient) { }




  get_emails(){
    const endPoint = `${this.url}email?email=bytemetest69@gmail.com&status=pending`


    const httpOptions = {
      headers: new HttpHeaders({
        'Authorization': "nONe",
      })
    }

    return this.http.get(endPoint, httpOptions);
  }

  send_reply(email_object: any, replymsg: string) {
    const endPoint = `${this.url}reply`;



    const formData = {
      "email": email_object,
      "replymsg": replymsg
    };

    const httpOptions = {
      headers: new HttpHeaders({
        'Authorization': "none",
      }),
    }

    return this.http.post(endPoint, formData, httpOptions);

  }

}
