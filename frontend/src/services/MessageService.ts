// src/services/MessageService.ts
interface MessageConstructor {
  role: string;
  content: string;
  timestamp: number;
  user_id?: string;
}

export default class Message {
  role: string;
  content: string;
  timestamp: number;
  user_id: string;

  constructor({ role, content, timestamp, user_id = 'test_user' }: MessageConstructor) {
    this.role = role;
    this.content = content;
    this.timestamp = timestamp;
    this.user_id = user_id;
  }

  model_dump() {
    return {
      role: this.role,
      content: this.content,
      user_id: this.user_id
    };
  }
}