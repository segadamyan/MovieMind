import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ChatbotService {

  constructor(private http: HttpClient) {}

  chat(userInput: string): Observable<any> {
    const url = 'http://localhost:5000/chatbot';
    const payload = {
      input: userInput,
    };
    return this.http.post(url, payload);
  }
}
