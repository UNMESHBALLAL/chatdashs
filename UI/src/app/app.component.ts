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

  constructor(private http: HttpClient) {}

  sendPrompt() {
    const body = {
      prompt: this.prompt,
      max_length: 100 // You can adjust this value as needed
    };

    this.http.post('http://127.0.0.1:8000/generate', body)
      .subscribe((response: any) => {
        this.responses.push(response.generated_text); // Adjust according to the actual response structure
        this.prompt = ''; // Clear the input after sending
      }, error => {
        console.error('Error:', error);
      });
  }
}