import { Component } from '@angular/core';
import { ChatbotService } from '../services/chatbot.service';
import { Observable } from 'rxjs';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http'; 

@Component({
  selector: 'app-chatbot',
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.css'],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    HttpClientModule
  ]
})
export class ChatbotComponent {
  messages: { text: string, sender: string }[] = [];
  userInput: string = '';
  isExpanded: boolean = false;
  chatbotForm!: FormGroup;

  constructor(
    private chatbotService: ChatbotService,
    private fb: FormBuilder,
  ) {
    this.initializeForm();
  }

  initializeForm(): void {
    this.chatbotForm = this.fb.group({
      content: ['', [Validators.required]],
    });
    // if (this.currentUser.user_id) {
    //   const userId = this.currentUser.user_id;
    //   console.log('User ID:', userId);
    //   this.authService.getUserProfile(userId).subscribe(
    //     (profile: UserProfile) => {
    //       this.userProfile = profile;
    //       this.author = this.userProfile.username;
    //       this.commentForm.patchValue({ author: this.author });
    //       console.log('User profile loaded:', this.userProfile);
    //     },
    //     error => {
    //       console.error('Error loading user profile:', error);
    //     }
    //   );
    // } else {
    //   console.error('No current user found');
    // }
  }

  sendMessage() {
    this.userInput = this.chatbotForm.get('content')?.value;
    console.log('User input:', this.userInput);
    if (this.userInput.trim()) {
      this.messages.push({ text: this.userInput, sender: 'User' });

      this.chatbotService.chatWithBot(this.userInput).subscribe((response: { response: any; }) => {
        this.messages.push({ text: response.response, sender: 'Bot' });
      });

      this.userInput = '';
    }
  }

  checkCollapse() {
    if (!this.chatbotForm.get('content')?.value.trim()) {
      this.isExpanded = false;
    }
  }

  adjustHeight(event: Event) {
    const textarea = event.target as HTMLTextAreaElement;
    textarea.style.height = 'auto'; // Reset height to recalculate
    textarea.style.height = textarea.scrollHeight + 'px'; // Adjust height dynamically
  }
}