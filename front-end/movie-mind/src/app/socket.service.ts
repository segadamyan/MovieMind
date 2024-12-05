import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';

@Injectable({
  providedIn: 'root'
})
export class SocketService {
  message$ = this.socket.fromEvent<string>('message');

  constructor(private socket: Socket) {}

  sendMessage(input: string) {
    this.socket.emit('user_input', { input });
  }
}
