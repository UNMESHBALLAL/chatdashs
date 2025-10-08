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
  serverStatus: string = 'available'; // 'unknown', 'available', 'unavailable'
  isLoading: boolean = false;

  constructor(private http: HttpClient) {
   // this.checkServerStatus();
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
dashboard: any = null;

sendPrompt() {
  this.isLoading = true;
  this.http.post<{generated_text: string}>('http://127.0.0.1:8000/generate', { prompt: this.prompt })
    .subscribe({
      next: (res) => {
        this.responses.push(res.generated_text);
        this.isLoading = false;
      },
      error: () => this.isLoading = false
    });
}

generateDashboard() {
  this.isLoading = true;
  this.http.post<{dashboard: any}>('http://127.0.0.1:8000/generate_dashboard', { instruction: this.prompt })
    .subscribe({
      next: (res) => {
        this.dashboard = res.dashboard;
        this.isLoading = false;
      },
      error: () => this.isLoading = false
    });
}

}