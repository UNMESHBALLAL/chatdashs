import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  prompt: string = '';
  responses: string[] = [];
  serverStatus: string = 'unknown'; // 'unknown', 'available', 'unavailable'
  isLoading: boolean = false;

  constructor(private http: HttpClient) {
    this.checkServerStatus();
  }

  // Check if server is available on component initialization
  checkServerStatus() {
    this.http.get('http://127.0.0.1:8000/')
      .subscribe({
        next: () => {
          this.serverStatus = 'available';
        },
        error: () => {
          this.serverStatus = 'unavailable';
        }
      });
  }

  sendPrompt() {
    if (!this.prompt.trim()) return;

    this.isLoading = true;
    const body = {
      prompt: this.prompt,
      max_length: 100
    };

    this.http.post('http://127.0.0.1:8000/generate', body)
      .subscribe({
        next: (response: any) => {
          this.responses.push(response.generated_text || 'No response text');
          this.prompt = '';
          this.serverStatus = 'available';
        },
        error: (error) => {
          console.error('Error:', error);
          this.responses.push('Error: Server not available. Please check if the API is running.');
          this.serverStatus = 'unavailable';
        },
        complete: () => {
          this.isLoading = false;
        }
      });
  }
}