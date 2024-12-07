import { Component } from '@angular/core';
import { ChatbotService } from '../chatbot.service';
import { SocketService } from '../socket.service';

@Component({
  selector: 'app-chatbot',
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.css'],
})
export class ChatbotComponent {
  messages: { sender: string; text: string }[] = [];
  userInput: string = '';
  typing: boolean = false;

  constructor(private chatbotService: ChatbotService, private socketService: SocketService) {
    this.socketService.message$.subscribe((response: any) => {
      this.typing = false;
      if (Array.isArray(response.message)) {
          response.message.forEach((movie: any) => {
            const flattenedMovie = this.flattenMovieDetails(movie);
            this.messages.push({ sender: 'bot', text: flattenedMovie });
          });
      }
      else {
        this.messages.push({ sender: 'bot', text: response.message });
      }
    });
  }
  
  private flattenMovieDetails(movie: any): string {
    return `
      ${movie.title}: \n
      ${movie.overview}: \n
      Release Date: ${new Date(movie.release_date).toLocaleDateString()} \n
      Popularity: ${movie.popularity} \n
      Vote Average: ${movie.vote_average} \n
      Adult Content: ${movie.adult ? 'Yes' : 'No'}, 
      Language: ${movie.language || 'N/A'} \n
    `;
  }


  sendMessage() {
    if (!this.userInput.trim()) return;
  
    this.messages.push({ sender: 'user', text: this.userInput });
  
    const userMessage = this.userInput;
    this.userInput = '';
    this.typing = true;
  
    this.socketService.sendMessage(userMessage);
  }

}
