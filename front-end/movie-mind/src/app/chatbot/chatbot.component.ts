import { Component } from '@angular/core';
import { ChatbotService } from '../chatbot.service';

@Component({
  selector: 'app-chatbot',
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.css'],
})
export class ChatbotComponent {
  messages: { sender: string; text: string }[] = [];
  userInput: string = '';
  typing: boolean = false;

  constructor(private chatbotService: ChatbotService) {}

  sendMessage() {
    if (!this.userInput.trim()) return;

    this.messages.push({ sender: 'user', text: this.userInput });
    const userMessage = this.userInput;
    this.userInput = '';
    this.typing = true;

    this.chatbotService.chat(userMessage).subscribe((response) => {
      this.typing = false;
      this.messages.push({ sender: 'bot', text: response.message });
    });
  }

}
