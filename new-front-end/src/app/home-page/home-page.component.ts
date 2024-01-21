import { Component, importProvidersFrom } from '@angular/core';
import { GridComponent } from '../grid/grid.component';
import { SidePanelComponent } from '../side-panel/side-panel.component';
import { DialogOverviewExample } from '../example/dialog-overview-example';
import { provideHttpClient } from '@angular/common/http';
import { MatNativeDateModule } from '@angular/material/core';
import { bootstrapApplication } from '@angular/platform-browser';
import { provideAnimations } from '@angular/platform-browser/animations';
import { EmailService } from '../email.service';
@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [GridComponent, SidePanelComponent, DialogOverviewExample],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.css'
})
export class HomePageComponent {

  constructor(private emailService:EmailService) {

  }

  isloading:boolean = true;

  allEmails:any;

  ngOnInit(){

    this.isloading = true
    this.emailService.get_emails().subscribe(response => {
      this.isloading = false;
      this.allEmails = response;
    })
  }

  
}

