import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ChatbotService {
  private apiUrl = 'http://localhost:8000/api/chatbot/';

  constructor() {}

  async chatWithBotStreaming(userInput: string, callback: (token: string) => void) {
    const response = await fetch(this.apiUrl, {
      method: 'POST',
      body: JSON.stringify({ 'user-input': userInput }),
      headers: { 'Content-Type': 'application/json' }
    });

    const reader = response.body?.getReader();
    if (!reader) return;

    const decoder = new TextDecoder();
    let result = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const newToken = decoder.decode(value, { stream: true });
      callback(newToken);
  }
  }
}
