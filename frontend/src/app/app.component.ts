import { Component, ElementRef, ViewChild, AfterViewInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  imports: [CommonModule, RouterModule]
})
export class AppComponent {
  title = 'SkillsShowcaseWebsite';
  isSidebarRetracted = false;
  isLoggedIn = false;
  showModal: boolean = false;
  @ViewChild('sidebar') sidebar!: ElementRef<HTMLDivElement>;

  constructor(private router: RouterModule) {}

  ngOnInit(): void {
    // Subscribe to authentication state changes
    console.log(this.isLoggedIn);
    // this.authService.currentUser.subscribe((user: any) => {
    //   if (user !== 'null') {
    //     this.isLoggedIn = true; // Update the login state
    //   }
    // });
  }

  toggleSidebar() {
    this.isSidebarRetracted = !this.isSidebarRetracted;
    this.closeAllSubMenus();
  }

  toggleDropDown(event: any) {

    const button = event.currentTarget as HTMLElement;
    const subMenu = button.nextElementSibling as HTMLElement;

    if (!subMenu.classList.contains('show')) {
      this.closeAllSubMenus();
    }

    if (subMenu) {
      subMenu.classList.toggle('show');
      button.classList.toggle('rotate');
    }
    if (this.isSidebarRetracted){
      this.isSidebarRetracted = !this.isSidebarRetracted;
    }
  }

  closeAllSubMenus() {
    const showElements = this.sidebar.nativeElement.getElementsByClassName('show');

    Array.from(showElements).forEach((element) => {
      console.log('Removing show class from:', element);
      element.classList.remove('show');
      if (element.previousElementSibling) {
        element.previousElementSibling.classList.remove('rotate');
      }
    });
  }

  scrollToTop() {
    console.log('Scrolling to top');
    window.scrollTo({
      top: 0,
      behavior: 'smooth' // Smooth scrolling
    });
  }

  scrollingUp() {
    console.log('Scrolling up');
  }

  logout() {
    // this.authService.logout(); // Call the logout method
    // this.isLoggedIn = false; // Update the login state
    // window.location.reload(); // Reload the page
  }

  login() {
    // if (!this.authService.isLoggedIn()) {
    //   this.showModal = true; // Show the modal if the user is not signed in
    //   return;
    // }
  }
}
