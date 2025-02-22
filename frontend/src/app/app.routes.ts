import { Routes } from '@angular/router';
import { HomePageComponent } from './home-page/home-page.component';
import { ChatbotComponent } from './chatbot/chatbot.component';

export const routes: Routes = [
    {path:'', component:HomePageComponent},
    {path:'chatbot', component:ChatbotComponent}
];
