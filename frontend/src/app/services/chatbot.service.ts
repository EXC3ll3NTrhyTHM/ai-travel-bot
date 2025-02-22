import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ChatbotService {

  constructor(private http: HttpClient) { }

  chatWithBot(userInput: string): Observable<{ response: any }> {
    const url = 'http://localhost:8000/api/chatbot/?user-input=' + encodeURIComponent(userInput);
    return this.http.post<{ response: any }>(url, {});
  }
}
